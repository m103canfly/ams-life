# -*- coding: utf-8 -*-
"""A temporary, read-only browser for pages that need scripts."""
import asyncio
import concurrent.futures
import functools
import ipaddress
import logging
import socket
import ssl
import threading
import time
from contextlib import asynccontextmanager
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import getproxies

try:
    from . import browse
except ImportError:
    import browse

logger = logging.getLogger(__name__)
OPEN_SECONDS = 20
LOCK_WAIT_SECONDS = 3
# Limit redirect chains to bound work and reject loops.
MAX_HOPS = 5
# Script-driven pages may fetch their visible content after DOMContentLoaded.
SETTLE_SECONDS = 8
TEXT_SECONDS = 10
EXTRACT_SECONDS = 5
# Bound parser input and work by UTF-8 bytes, including for multibyte pages.
HTML_MAX_BYTES = 2 * 1024 * 1024
BROWSER_MIN_CHARS = 200
EXTRACT_MIN_RATIO = 0.25
SHOT_SECONDS = 10
CHALLENGE_MAX_CHARS = 600
SHOT_VIEWPORT = {"width": 390, "height": 844}
SHOT_QUALITY = 70
CHALLENGE_MARKERS = ("verify you are human", "checking your browser", "just a moment...",
                     "captcha", "cloudflare", "请验证您是人类")
WEBRTC_INIT = """for (const name of ['RTCPeerConnection', 'webkitRTCPeerConnection']) {
    try { Object.defineProperty(globalThis, name, {value: undefined, writable: false, configurable: false}); }
    catch (_) { try { delete globalThis[name]; } catch (_) {} }
}"""
# R7 (DNS rebinding): the browser resolves no name itself. Every request is taken by us,
# resolved once, checked, and connected by the address checked. The hostname stays only in
# the Host header and in TLS (SNI and certificate check).
HOST_RESOLVER_RULE = "--host-resolver-rules=MAP * ~NOTFOUND"
MAX_SUBREQUESTS = 60
MAX_RESPONSE_BYTES = HTML_MAX_BYTES
REDIRECT_STATUS = (301, 302, 303, 307, 308)
HOP_HEADERS = ("connection", "keep-alive", "proxy-connection", "transfer-encoding", "upgrade", "trailer")
# Fetching a page is done on our own small pool, never the default one: a slow page
# (or a slow name) may not take the threads embeddings, pictures and voice use.
FETCH_WORKERS = 4
HOP_SECONDS = OPEN_SECONDS          # one hop's whole budget: name, connect, send, read
MAX_ADDRESSES = 4                   # a name may give many addresses: a hop tries these at most
READ_CHUNK = 65536
PROXY_SCHEMES = ("http",)           # the only proxy kind we speak ourselves
_lock = asyncio.Lock()
_fetch_lock = threading.Lock()
_fetch_pool = concurrent.futures.ThreadPoolExecutor(max_workers=FETCH_WORKERS,
                                                    thread_name_prefix="ams-fetch")
_active_fetches = 0


class FetchBusy(RuntimeError):
    """Every fetch thread is taken: the page is not fetched, and the request is aborted."""


def _take_fetch_slot() -> bool:
    global _active_fetches
    with _fetch_lock:
        if _active_fetches >= FETCH_WORKERS:
            return False
        _active_fetches += 1
        return True


def _release_fetch_slot() -> None:
    global _active_fetches
    with _fetch_lock:
        _active_fetches = max(0, _active_fetches - 1)


async def _pool_call(fn, *args, **kwargs):
    """`fn` on the fetch pool, or FetchBusy when every thread is taken. The slot is held until
    the thread really ends, even when the waiting coroutine is cancelled or times out."""
    if not _take_fetch_slot():
        raise FetchBusy("all fetch threads are busy")
    try:
        future = _fetch_pool.submit(functools.partial(fn, *args, **kwargs))
    except BaseException:
        _release_fetch_slot()
        raise
    future.add_done_callback(lambda _done: _release_fetch_slot())
    return await asyncio.wrap_future(future)


def _set_timeout(sock, seconds) -> None:
    """The socket's next recv/send may wait at most `seconds` (fake sockets may not take it)."""
    setter = getattr(sock, "settimeout", None)
    if not callable(setter):
        return
    try:
        setter(max(0.001, float(seconds)))
    except Exception:
        pass


def _remaining(deadline) -> float:
    return max(0.0, float(deadline) - time.monotonic())


def _ipv4_first(addresses) -> list:
    """The addresses once each, IPv4 before IPv6: a home without IPv6 must not lose a
    dual-stack site to an address it cannot reach. The resolver's own order is kept inside
    each family."""
    seen, v4, v6 = set(), [], []
    for address in addresses or ():
        text = str(address or "")
        if not text or text in seen:
            continue
        seen.add(text)
        try:
            is_v6 = isinstance(ipaddress.ip_address(text.split("%", 1)[0]),
                               ipaddress.IPv6Address)
        except ValueError:
            is_v6 = False
        (v6 if is_v6 else v4).append(text)
    return v4 + v6


def _system_resolve(host) -> list:
    """The addresses this computer's resolver gives for a name ([] when it gives none)."""
    try:
        addresses = [info[4][0] for info in socket.getaddrinfo(host, None)]
    except Exception:
        return []
    return _ipv4_first(addresses)


def _public_address(text) -> bool:
    """True for an address out on the internet (not this computer, the home network, an
    address IPv6 carries inside, ...)."""
    try:
        ipaddress.ip_address(str(text).strip("[]").split("%", 1)[0])
    except ValueError:
        return False
    return not browse._bad_address(text)


def _ascii_host(host) -> str:
    try:
        return str(host or "").encode("idna").decode("ascii")
    except Exception:
        return str(host or "")


def _pin_addresses(url, check, resolve) -> tuple:
    """(addresses, reason): the addresses to try for `url`, resolved here exactly once.
    `check` is the caller's rule on the address (scheme, port, no user, no local name); every
    address the name resolves to must be public, and IPv4 comes first. None with a reason
    when the page may not be read."""
    try:
        ok, reason = check(url)
    except Exception:
        return None, "unchecked"
    if not ok:
        return None, reason or "refused"
    try:
        host = urlsplit(str(url)).hostname or ""
    except ValueError:
        return None, "bad url"
    if not host:
        return None, "no host"
    try:
        ipaddress.ip_address(host.strip("[]").split("%", 1)[0])
        literal = True
    except ValueError:
        literal = False
    if literal:
        return ([host], "") if _public_address(host) else (None, "local address")
    try:
        addresses = list(resolve(host) or [])
    except Exception:
        addresses = []
    if not addresses:
        return None, "unresolved"
    for address in addresses:
        if not _public_address(address):
            return None, "local address"
    return _ipv4_first(addresses), ""


def _pin_address(url, check, resolve) -> tuple:
    """(the first address to try, reason), as _pin_addresses but only the best one."""
    addresses, reason = _pin_addresses(url, check, resolve)
    return (str(addresses[0]) if addresses else None), reason


def _connect(ip, port, hostname, tls, timeout):
    """A socket to the address checked; the hostname is only TLS's SNI and certificate check.
    `timeout` covers the connect and the TLS handshake together, not each of them."""
    budget = max(0.001, float(timeout or OPEN_SECONDS))
    deadline = time.monotonic() + budget
    sock = socket.create_connection((ip, int(port)), timeout=budget)
    if not tls:
        return sock
    try:
        context = ssl.create_default_context()
        _set_timeout(sock, _remaining(deadline))    # the handshake gets what the connect left
        return context.wrap_socket(sock, server_hostname=_ascii_host(hostname))
    except BaseException:
        try:
            sock.close()
        except Exception:
            pass
        raise


def _read_all(sock, limit, deadline=None) -> bytes:
    """Up to `limit` bytes, a chunk at a time, until the hop's `deadline`; the socket is left
    for the caller to close, so a slow server cannot keep it (or a thread) alive."""
    out, total = [], 0
    while total < limit:
        left = _remaining(deadline) if deadline is not None else None
        if left is not None:
            if left <= 0:
                break
            _set_timeout(sock, left)
        try:
            piece = sock.recv(min(READ_CHUNK, limit - total))
        except (socket.timeout, TimeoutError):
            break
        except OSError:
            break
        if not piece:
            break
        out.append(piece)
        total += len(piece)
    return b"".join(out)


def _read_head(sock, deadline=None, limit=65536) -> bytes:
    """One response's head (up to the empty line), within the hop's deadline."""
    out = b""
    while b"\r\n\r\n" not in out and len(out) < limit:
        left = _remaining(deadline) if deadline is not None else None
        if left is not None:
            if left <= 0:
                break
            _set_timeout(sock, left)
        try:
            piece = sock.recv(min(4096, limit - len(out)))
        except (socket.timeout, TimeoutError):
            break
        except OSError:
            break
        if not piece:
            break
        out += piece
    return out


def _content_length(head):
    """The Content-Length a response head gives, or None when it gives none (or is chunked):
    with it, the body is read up to that many bytes instead of waiting for the server to close."""
    try:
        text = bytes(head).partition(b"\r\n\r\n")[0]
        found = {}
        for line in text.split(b"\r\n")[1:]:
            if b":" not in line:
                continue
            name, value = line.split(b":", 1)
            found[name.strip().lower()] = value.strip()
        if b"chunked" in found.get(b"transfer-encoding", b"").lower():
            return None
        value = found.get(b"content-length", b"")
        return int(value) if value.isdigit() else None
    except Exception:
        return None


def _read_response(sock, deadline, limit) -> bytes:
    """One response's head and body: the body only up to its Content-Length (and `limit`), so a
    server that keeps the connection open after its answer is not waited for."""
    head = _read_head(sock, deadline)
    if b"\r\n\r\n" not in head:
        return head
    length = _content_length(head)
    if length is None:
        want = max(0, limit - len(head))
    else:
        want = max(0, min(length, limit) - len(head.partition(b"\r\n\r\n")[2]))
    if want <= 0:
        return head
    return head + _read_all(sock, want, deadline)


def _status_of(raw) -> int:
    try:
        return int(bytes(raw).split(b"\r\n", 1)[0].split()[1])
    except (IndexError, ValueError):
        return 0


def _dechunk(body) -> bytes:
    out, index = [], 0
    while index < len(body):
        end = body.find(b"\r\n", index)
        if end < 0:
            break
        try:
            size = int(body[index:end].split(b";")[0].strip(), 16)
        except ValueError:
            break
        if size <= 0:
            break
        start = end + 2
        out.append(body[start:start + size])
        index = start + size + 2
    return b"".join(out)


def _parse_response(raw) -> tuple:
    """(status, headers, body) of one HTTP/1.1 response; chunked bodies are joined, and the
    body is cut at MAX_RESPONSE_BYTES."""
    head, sep, body = bytes(raw).partition(b"\r\n\r\n")
    if not sep:
        return 0, {}, b""
    lines = head.split(b"\r\n")
    try:
        status = int(lines[0].split()[1])
    except (IndexError, ValueError):
        return 0, {}, b""
    headers = {}
    for line in lines[1:]:
        if b":" not in line:
            continue
        name, value = line.split(b":", 1)
        key = name.decode("latin-1").strip().lower()
        if key:
            headers[key] = value.decode("latin-1").strip()
    if "chunked" in headers.get("transfer-encoding", "").lower():
        body = _dechunk(body)
    length = headers.get("content-length")
    if length and length.isdigit():
        body = body[:int(length)]
    body = body[:MAX_RESPONSE_BYTES]
    for key in HOP_HEADERS:
        headers.pop(key, None)
    # we asked for identity: whatever the server still sent compressed is not for the browser
    headers.pop("content-encoding", None)
    headers["content-length"] = str(len(body))
    return status, headers, body


def _host_in_url_form(host) -> str:
    """A host as it goes in a Host header, a CONNECT line or a proxy's absolute form: an IPv6
    address keeps its brackets (the URL parser drops them from the name)."""
    name = _ascii_host(host)
    if ":" in name and not name.startswith("["):
        return "[" + name + "]"
    return name


def _host_header(host, port, scheme) -> str:
    name = _host_in_url_form(host)
    if int(port) != (443 if str(scheme).lower() == "https" else 80):
        name += ":" + str(port)
    return name


def _request_target(parts) -> str:
    target = quote(parts.path or "/", safe="/%:@!$&'()*+,;=-._~")
    if parts.query:
        target += "?" + quote(parts.query, safe="=&%:@!$'()*+,;/-._~")
    return target


def _get_request(url, via_proxy=False) -> bytes:
    """The one GET we send: origin form straight to the page, absolute form to an HTTP proxy.
    Identity: no compressed body to unpack without a limit."""
    parts = urlsplit(str(url))
    scheme = parts.scheme.lower()
    host = parts.hostname or ""
    port = parts.port or (443 if scheme == "https" else 80)
    header_host = _host_header(host, port, scheme)
    target = _request_target(parts)
    if via_proxy and scheme != "https":
        target = "%s://%s%s" % (scheme, header_host, target)
    extra = "Proxy-Connection: close\r\n" if via_proxy else ""
    return ("GET %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nAccept-Encoding: identity\r\n"
            "%sConnection: close\r\n\r\n" % (target, header_host, extra)).encode("ascii", "replace")


def _fetch_once(url, ip, timeout=OPEN_SECONDS, connect=None) -> tuple:
    """One GET to the address checked: (status, headers, body). The hostname stays in Host and
    in TLS; only `ip` is connected to. Redirects are not followed here. The whole hop (connect,
    send, read) is bound by `timeout`; the socket is closed either way."""
    connect = connect or _connect
    deadline = time.monotonic() + max(0.001, float(timeout or OPEN_SECONDS))
    parts = urlsplit(str(url))
    scheme = parts.scheme.lower()
    host = parts.hostname or ""
    port = parts.port or (443 if scheme == "https" else 80)
    request = _get_request(url)
    sock = connect(ip, port, host, scheme == "https", max(0.001, _remaining(deadline)))
    try:
        _set_timeout(sock, _remaining(deadline))
        sock.sendall(request)
        raw = _read_response(sock, deadline, MAX_RESPONSE_BYTES)
    finally:
        try:
            sock.close()
        except Exception:
            pass
    return _parse_response(raw)


@asynccontextmanager
async def _timed_lock():
    await asyncio.wait_for(_lock.acquire(), timeout=LOCK_WAIT_SECONDS)
    try:
        yield
    finally:
        _lock.release()


def _proxy_config() -> dict:
    """The system proxy, as Playwright's context takes it ({} when there is none). No bypass
    list: a host in NO_PROXY is fetched by us on the checked-address path, never resolved and
    connected by the browser itself."""
    try:
        proxies = getproxies()
    except Exception:
        return {}
    server = proxies.get("https") or proxies.get("http")
    if not server:
        return {}
    return {"server": server}


def _no_proxy_host(host, listed) -> bool:
    """Whether `host` is in the system's NO_PROXY list (a name or a domain, or *)."""
    if isinstance(listed, str):
        entries = [part.strip() for part in listed.replace(";", ",").split(",") if part.strip()]
    elif isinstance(listed, (list, tuple)):
        entries = [str(part).strip() for part in listed if str(part).strip()]
    else:
        entries = []
    host = str(host or "").strip(".").lower()
    for entry in entries:
        entry = entry.split("://")[-1].split("/")[0].lstrip(".").lower()
        if ":" in entry and not entry.startswith("["):
            entry = entry.split(":", 1)[0]      # host:port
        if not entry:
            continue
        if entry == "*" or host == entry or host.endswith("." + entry):
            return True
    return False


def _parse_proxy(server) -> tuple:
    """((host, port), reason) of an HTTP proxy; (None, reason) for anything else. Only an HTTP
    proxy is spoken here: another kind is refused, never taken for no proxy and dialled."""
    text = str(server or "").strip()
    if not text:
        return None, "no proxy"
    if "://" not in text:
        text = "http://" + text
    try:
        parts = urlsplit(text)
        port = parts.port
    except ValueError:
        return None, "proxy"
    if parts.scheme.lower() not in PROXY_SCHEMES:
        return None, "proxy scheme"
    if not parts.hostname:
        return None, "proxy"
    return (parts.hostname, int(port or 80)), ""


def _proxy_for(url) -> tuple:
    """(server, reason) for one address: (None, "") = straight to the checked address,
    (server, "") = through that HTTP proxy, (None, reason) = refused, never a direct
    connection. A SOCKS or ALL_PROXY setting is refused, not ignored."""
    try:
        proxies = getproxies() or {}
    except Exception:
        return None, ""
    try:
        parts = urlsplit(str(url))
        scheme = parts.scheme.lower()
        host = (parts.hostname or "").strip(".")
    except ValueError:
        return None, ""
    if _no_proxy_host(host, proxies.get("no")):
        # NO_PROXY: our own path, resolved and connected by the address checked
        return None, ""
    server = proxies.get(scheme) or proxies.get("http")
    if not server:
        if proxies.get("all") or proxies.get("socks") or proxies.get("socks5"):
            return None, "proxy scheme"
        return None, ""
    _, reason = _parse_proxy(server)
    if reason:
        return None, reason
    return str(server), ""


def _pin_proxied(url, check, resolve) -> tuple:
    """(addresses, reason) for a page a proxy fetches. The name itself is checked, and a name
    that resolves here to this computer or the home network is refused; a name that does not
    resolve here is left to the proxy (taken as the card's remaining risk: the proxy resolves
    the name again)."""
    try:
        ok, reason = check(url)
    except Exception:
        return None, "unchecked"
    if not ok:
        return None, reason or "refused"
    try:
        host = urlsplit(str(url)).hostname or ""
    except ValueError:
        return None, "bad url"
    if not host:
        return None, "no host"
    try:
        ipaddress.ip_address(host.strip("[]").split("%", 1)[0])
        literal = True
    except ValueError:
        literal = False
    if literal:
        return ([], "") if _public_address(host) else (None, "local address")
    try:
        addresses = list(resolve(host) or [])
    except Exception:
        addresses = []
    for address in addresses:
        if not _public_address(address):
            return None, "local address"
    return [], ""


def _fetch_once_proxy(url, proxy, timeout=OPEN_SECONDS, connect=None) -> tuple:
    """One GET through an HTTP proxy, sent by us: the same identity request, the same 2MB cut
    and the same stripped headers as a direct GET. https goes by CONNECT, so the proxy never
    sees the page's plain text. The whole hop is bound by `timeout` and the socket is closed."""
    connect = connect or _connect
    found, reason = _parse_proxy(proxy)
    if found is None:
        raise OSError(reason or "proxy")
    proxy_host, proxy_port = found
    deadline = time.monotonic() + max(0.001, float(timeout or OPEN_SECONDS))
    parts = urlsplit(str(url))
    scheme = parts.scheme.lower()
    host = parts.hostname or ""
    port = parts.port or (443 if scheme == "https" else 80)
    authority = "%s:%d" % (_host_in_url_form(host), int(port))
    sock = connect(proxy_host, proxy_port, "", False, max(0.001, _remaining(deadline)))
    try:
        if scheme == "https":
            tunnel = ("CONNECT %s HTTP/1.1\r\nHost: %s\r\nProxy-Connection: close\r\n\r\n"
                      % (authority, authority)).encode("ascii", "replace")
            _set_timeout(sock, _remaining(deadline))
            sock.sendall(tunnel)
            status = _status_of(_read_head(sock, deadline))
            if status != 200:
                raise OSError("proxy refused")
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=_ascii_host(host))
        request = _get_request(url, via_proxy=(scheme != "https"))
        _set_timeout(sock, _remaining(deadline))
        sock.sendall(request)
        raw = _read_response(sock, deadline, MAX_RESPONSE_BYTES)
    finally:
        try:
            sock.close()
        except Exception:
            pass
    return _parse_response(raw)


async def _launch_browser(playwright, shot_path=None, pin_dns=False):
    # R7: with `pin_dns`, Chromium resolves no name itself; every request is served by us.
    args = ["--disable-features=DnsOverHttps",
            "--force-webrtc-ip-handling-policy=disable_non_proxied_udp"]
    if pin_dns:
        args.append(HOST_RESOLVER_RULE)
    browser = await playwright.chromium.launch(channel="msedge", headless=True,
                                               chromium_sandbox=True, args=args)
    try:
        options = dict(accept_downloads=False, permissions=[], service_workers="block",
                       ignore_https_errors=False, bypass_csp=False)
        if not pin_dns:
            # the shared launch (the interactive browser) keeps the system proxy; the pinned
            # browser (pin_dns) fetches every request itself, so Chromium gets no proxy at all
            proxy = _proxy_config()
            if proxy:
                options["proxy"] = proxy
        if shot_path is not None:
            options["viewport"] = dict(SHOT_VIEWPORT)
        context = await browser.new_context(**options)
        try:
            await context.add_init_script(WEBRTC_INIT)
        except BaseException:
            await context.close()
            raise
    except BaseException:
        await browser.close()
        raise
    return browser, context


async def _article_text(page, body):
    async def extract():
        html = await page.content()
        html = html.encode("utf-8")[:HTML_MAX_BYTES].decode("utf-8", errors="ignore")

        def parse():
            import trafilatura
            return trafilatura.extract(html, include_comments=False, include_tables=True, favor_precision=True)

        return await asyncio.to_thread(parse)

    try:
        text = await asyncio.wait_for(extract(), timeout=EXTRACT_SECONDS)
        if isinstance(text, str) and len(text.strip()) >= max(BROWSER_MIN_CHARS, len(body.strip()) * EXTRACT_MIN_RATIO):
            return text
    except Exception:
        pass
    return body


def _strict_url(url, check):
    # Safety 3: reject unresolved names and every non-public resolved address.
    try:
        ok, reason = check(url)
        if not ok:
            return False, reason
        host = urlsplit(url).hostname
        addresses = {info[4][0] for info in socket.getaddrinfo(host, None)}
        if not addresses:
            return False, "unresolved"
        for address in addresses:
            if not _public_address(address):
                return False, "local address"
        return True, ""
    except Exception:
        return False, "unresolved or invalid"


def _target_closed(exc):
    return (type(exc).__name__ == "TargetClosedError" or
            (type(exc).__name__ == "Error" and "Target page, context or browser has been closed" in str(exc)))


async def _route_request(route, checked, on_block, on_redirect=None, on_method_block=None):
    counted = False

    def record(reason):
        nonlocal counted
        counted = True
        on_block(reason)

    try:
        await _route_request_active(route, checked, record, on_redirect, on_method_block)
    except Exception as exc:
        await _route_failed(route, exc, record, counted)


async def _route_failed(route, exc, on_block, counted=False):
    if _target_closed(exc):
        return
    logger.info("[ams-life] browser: request failed (%s)", type(exc).__name__)
    if not counted:
        try:
            on_block("request failed")
        except Exception:
            pass
    try:
        await route.abort()
    except Exception:
        pass


async def _route_request_active(route, checked, on_block, on_redirect=None, on_method_block=None):
    request = route.request
    if request.method.upper() not in ("GET", "HEAD"):
        if on_method_block:
            on_method_block(request)
        on_block("method")
        await route.abort()
        return
    ok, reason = await checked(request.url)
    if not ok:
        on_block(reason)
        await route.abort()
        return
    response = None
    try:
        response = await route.fetch(max_redirects=0, timeout=OPEN_SECONDS * 1000)
        if 300 <= response.status < 400:
            if on_redirect:
                on_redirect(request, response)
            on_block("redirect")
            await route.abort()
        else:
            await route.fulfill(response=response)
    finally:
        if response is not None:
            try:
                await response.dispose()
            except Exception as exc:
                if not _target_closed(exc):
                    raise


async def _navigate(context, page, address, checked, on_block):
    for hop in range(MAX_HOPS + 1):
        ok, reason = await checked(address)
        if not ok:
            on_block(reason)
            return None
        probe = await context.request.get(address, max_redirects=0, timeout=OPEN_SECONDS * 1000)
        try:
            status, location = probe.status, probe.headers.get("location")
        finally:
            await probe.dispose()
        if 300 <= status < 400:
            if not location or hop == MAX_HOPS:
                return None
            address = urljoin(address, location)
            continue
        if not 200 <= status < 300:
            return None
        return await page.goto(address, wait_until="domcontentloaded", timeout=OPEN_SECONDS * 1000)
    return None


async def _take_screenshot(page, path):
    await asyncio.wait_for(page.screenshot(path=str(path), type="jpeg", quality=SHOT_QUALITY,
                                           full_page=False, timeout=SHOT_SECONDS * 1000),
                           timeout=SHOT_SECONDS)


class _RequestGate:
    """One page's requests: resolved once each, names walled, at most MAX_SUBREQUESTS of them."""

    def __init__(self, check, resolve, on_block):
        self.check, self.resolve, self.on_block = check, resolve, on_block
        self.requests = 0
        self.blocked = 0
        self.document_url = ""
        self.main_frame = None
        self.checked = {}   # url -> (addresses, reason), so the last look need not resolve again

    def block(self, reason) -> None:
        self.blocked += 1
        try:
            self.on_block(reason)
        except Exception:
            pass

    def take(self) -> bool:
        if self.requests >= MAX_SUBREQUESTS:
            return False
        self.requests += 1
        return True

    def is_document(self, request) -> bool:
        try:
            if not request.is_navigation_request():
                return False
        except Exception:
            return False
        frame = getattr(request, "frame", None)
        return self.main_frame is None or frame is self.main_frame


async def _get_direct(url, addresses):
    """One hop to the addresses checked, trying them in order (an IPv6 address a home cannot
    reach does not lose the site). Every attempt is on the fetch pool; the hop has one deadline
    shared by its addresses, and only the first few are tried, so a name that gives many
    addresses cannot multiply the hop's time."""
    last = None
    deadline = time.monotonic() + HOP_SECONDS
    for address in list(addresses or ())[:MAX_ADDRESSES]:
        left = _remaining(deadline)
        if left <= 0:
            break
        try:
            return await _pool_call(_fetch_once, url, address, left)
        except FetchBusy:
            raise
        except Exception as exc:
            last = exc
    if last is not None:
        raise last
    raise OSError("no address")


async def _get_proxied(url, proxy):
    """One hop through the HTTP proxy, by us: the same limits as a direct hop."""
    return await _pool_call(_fetch_once_proxy, url, proxy, HOP_SECONDS)


def _check_url(url, gate) -> tuple:
    """(addresses, reason) for one address: through the proxy when the system sets one, else
    the addresses checked here; (None, why) when the page may not be read."""
    proxy, why = _proxy_for(url)
    if why:
        return None, why
    if proxy:
        return _pin_proxied(url, gate.check, gate.resolve)
    return _pin_addresses(url, gate.check, gate.resolve)


async def _checked(url, gate) -> tuple:
    """The rules on one address, on the fetch pool (a name lookup may block). FetchBusy is
    raised for the caller to abort with its own reason."""
    found = await _pool_call(_check_url, url, gate)
    gate.checked[str(url)] = found
    return found


async def _checked_free(url, gate) -> tuple:
    """The final look at a page's address after it was read: the same rules, but it takes no
    fetch slot (a page that timed out may still hold every thread), so a name lookup is put on
    the default thread instead. Without this the last look could fail a page that was read.
    An address already checked in this visit is not resolved again."""
    found = gate.checked.get(str(url))
    if found is None:
        found = await asyncio.to_thread(_check_url, url, gate)
    return found


async def _route_pinned(route, gate):
    counted = False

    def record(reason):
        nonlocal counted
        counted = True
        gate.block(reason)

    try:
        await _route_pinned_active(route, gate, record)
    except Exception as exc:
        await _route_failed(route, exc, record, counted)


async def _route_pinned_active(route, gate, on_block):
    request = route.request
    if str(request.method or "").upper() != "GET":
        on_block("method")
        await route.abort()
        return
    url = str(request.url or "")
    scheme = urlsplit(url).scheme.lower()
    if scheme in ("data", "blob"):
        # not a network request: the browser has it already
        await route.fallback()
        return
    if scheme not in ("http", "https"):
        on_block("scheme")
        await route.abort()
        return
    document = gate.is_document(request)
    if not document and not gate.take():
        on_block("too many requests")
        await route.abort()
        return
    hops = 0
    while True:
        proxy = _proxy_for(url)[0]
        try:
            addresses, reason = await _checked(url, gate)
        except FetchBusy:
            on_block("busy")
            await route.abort()
            return
        except Exception:
            addresses, reason = None, "unchecked"
        if addresses is None:
            on_block(reason)
            await route.abort()
            return
        try:
            if proxy:
                status, headers, body = await _get_proxied(url, proxy)
            else:
                status, headers, body = await _get_direct(url, addresses)
        except FetchBusy:
            on_block("busy")
            await route.abort()
            return
        location = headers.get("location") if isinstance(headers, dict) else None
        if status in REDIRECT_STATUS and location:
            # followed here, never by the browser: every hop resolved, checked and fetched again
            if hops >= MAX_HOPS:
                on_block("redirect limit")
                await route.abort()
                return
            following = urljoin(url, location)
            if urlsplit(following).scheme.lower() not in ("http", "https"):
                on_block("scheme")
                await route.abort()
                return
            url, hops = following, hops + 1
            continue
        if document:
            gate.document_url = url
        await route.fulfill(status=status, headers=headers, body=body)
        return


async def read_page(url, check, on_block=None, resolve=None):
    return await _safe_visit(url, check, None, on_block, resolve)


async def screenshot(url, check, path, on_block=None, resolve=None):
    return await _safe_visit(url, check, path, on_block, resolve)


async def _safe_visit(url, check, path, on_block, resolve=None):
    try:
        return await _visit(url, check, path, on_block, resolve)
    except asyncio.TimeoutError:
        logger.info("[ams-life] 浏览器正忙")
        return None


async def _visit(url, check, shot_path, on_block, resolve=None):
    # Safety 8: one browser page at a time, including other callers of this module.
    async with _timed_lock():
        try:
            from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
        except ImportError:
            logger.info("[ams-life] browser: playwright unavailable")
            return None
        browser = context = None
        pending = set()

        def note_block(reason):
            if reason != "request failed":
                logger.info("[ams-life] browser: blocked request (%s)", reason)

        gate = _RequestGate(check, resolve or _system_resolve, note_block)

        def track(coro):
            task = asyncio.create_task(coro)
            pending.add(task)
            task.add_done_callback(pending.discard)

        async def route_request(route):
            await _route_pinned(route, gate)

        async def read(context):
            await context.route("**/*", route_request)
            # Safety 3: close long-lived WebSockets before they can communicate.
            await context.route_web_socket("**/*", lambda ws: track(ws.close()))
            page = await context.new_page()
            gate.main_frame = getattr(page, "main_frame", None)
            # Safety 5: dismiss dialogs and close any page opened by the site.
            page.on("dialog", lambda dialog: track(dialog.dismiss()))
            context.on("page", lambda new_page: track(new_page.close()))

            response = await asyncio.wait_for(
                page.goto(url, wait_until="domcontentloaded", timeout=OPEN_SECONDS * 1000), timeout=OPEN_SECONDS)
            while pending:
                await asyncio.gather(*list(pending), return_exceptions=True)
            status = int(getattr(response, "status", 0) or 0)
            browser_url = str(getattr(page, "url", "") or "")
            final_url = gate.document_url or browser_url
            if (response is None or not 200 <= status < 300
                    or urlsplit(browser_url).scheme.lower() not in ("http", "https")
                    or urlsplit(final_url).scheme.lower() not in ("http", "https")):
                logger.info("[ams-life] browser: navigation failed")
                return None
            try:
                await asyncio.wait_for(page.wait_for_load_state("networkidle", timeout=SETTLE_SECONDS * 1000),
                                       timeout=SETTLE_SECONDS)
            except (asyncio.TimeoutError, PlaywrightTimeoutError):
                pass
            # Safety 6: read the title and visible text; no interaction or injected script.
            title = await asyncio.wait_for(page.title(), timeout=TEXT_SECONDS)
            body = await asyncio.wait_for(page.locator("body").inner_text(timeout=TEXT_SECONDS * 1000),
                                          timeout=TEXT_SECONDS)
            if not body.strip():
                logger.info("[ams-life] browser: empty page")
                return None
            while pending:
                await asyncio.gather(*list(pending), return_exceptions=True)
            try:
                addresses, reason = await _checked_free(final_url, gate)
            except Exception:
                addresses, reason = None, "unchecked"
            if addresses is None:
                logger.info("[ams-life] browser: redirect refused (%s)", reason)
                return None
            # Safety 9: short challenge pages are not read or photographed.
            if len(body.strip()) < CHALLENGE_MAX_CHARS and any(
                    marker in (title + "\n" + body).lower() for marker in CHALLENGE_MARKERS):
                logger.info("[ams-life] browser: verification page")
                return None
            if shot_path is not None:
                await _take_screenshot(page, shot_path)
            else:
                body = await _article_text(page, body)
            # Stop further requests before deciding whether every request was safe.
            end_url = str(getattr(page, "url", "") or "")
            await context.close()
            while pending:
                await asyncio.gather(*list(pending), return_exceptions=True)
            for address_to_check in list(dict.fromkeys([final_url, end_url])):
                try:
                    addresses, reason = await _checked_free(address_to_check, gate)
                except Exception:
                    addresses, reason = None, "unchecked"
                if addresses is None:
                    logger.info("[ams-life] browser: redirect refused (%s)", reason)
                    return None
            return shot_path if shot_path is not None else {"url": final_url, "title": title, "text": body}

        result = None
        try:
            async with async_playwright() as playwright:
                try:
                    # Safety 1: use Edge with its sandbox and a fresh, temporary context.
                    # Safety 3: disable the browser's encrypted DNS.
                    # Safety 2 and 3: shared context settings and WebRTC prevention.
                    browser, context = await _launch_browser(playwright, shot_path, pin_dns=True)
                    # Safety 7: the caller passes the result to browse.wrap as untrusted material.
                    result = await asyncio.wait_for(read(context), timeout=OPEN_SECONDS + SETTLE_SECONDS + 2 * TEXT_SECONDS + SHOT_SECONDS + EXTRACT_SECONDS)
                finally:
                    for task in list(pending):
                        task.cancel()
                    if pending:
                        await asyncio.gather(*list(pending), return_exceptions=True)
                    try:
                        if context is not None:
                            await context.close()
                    finally:
                        if browser is not None:
                            await browser.close()
        except Exception as exc:
            # Safety 10: log only a reason, never page contents or addresses.
            logger.info("[ams-life] browser: read failed (%s)", type(exc).__name__)
            result = None
        finally:
            if on_block is not None and gate.blocked:
                try:
                    on_block(gate.blocked)
                except Exception:
                    logger.info("[ams-life] browser: blocked request count could not be saved")
            if shot_path is not None and result is None:
                try:
                    from pathlib import Path
                    Path(shot_path).unlink(missing_ok=True)
                except Exception:
                    logger.info("[ams-life] browser: incomplete screenshot could not be removed")
        return result
