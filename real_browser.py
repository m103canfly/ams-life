# -*- coding: utf-8 -*-
"""A temporary, read-only browser for pages that need scripts."""
import asyncio
import ipaddress
import logging
import socket
import ssl
from contextlib import asynccontextmanager
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import getproxies

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
_lock = asyncio.Lock()


def _system_resolve(host) -> list:
    """The addresses this computer's resolver gives for a name ([] when it gives none)."""
    try:
        return sorted({info[4][0] for info in socket.getaddrinfo(host, None)})
    except Exception:
        return []


def _public_address(text) -> bool:
    """True for an address out on the internet (not this computer, the home network, ...)."""
    try:
        ip = ipaddress.ip_address(str(text).strip("[]").split("%", 1)[0])
    except ValueError:
        return False
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    return bool(ip.is_global and not ip.is_multicast)


def _ascii_host(host) -> str:
    try:
        return str(host or "").encode("idna").decode("ascii")
    except Exception:
        return str(host or "")


def _pin_address(url, check, resolve) -> tuple:
    """(address, reason): the one address to connect to for `url`, resolved here exactly once.
    `check` is the caller's rule on the address (scheme, port, no user, no local name); every
    address the name resolves to must be public, and the first one is the one we connect to."""
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
        return (host, "") if _public_address(host) else (None, "local address")
    try:
        addresses = list(resolve(host) or [])
    except Exception:
        addresses = []
    if not addresses:
        return None, "unresolved"
    for address in addresses:
        if not _public_address(address):
            return None, "local address"
    return str(addresses[0]), ""


def _connect(ip, port, hostname, tls, timeout):
    """A socket to the address checked; the hostname is only TLS's SNI and certificate check."""
    sock = socket.create_connection((ip, int(port)), timeout=timeout)
    if not tls:
        return sock
    try:
        context = ssl.create_default_context()
        return context.wrap_socket(sock, server_hostname=_ascii_host(hostname))
    except BaseException:
        try:
            sock.close()
        except Exception:
            pass
        raise


def _read_all(sock, limit) -> bytes:
    out, total = [], 0
    while total < limit:
        try:
            piece = sock.recv(min(65536, limit - total))
        except socket.timeout:
            break
        if not piece:
            break
        out.append(piece)
        total += len(piece)
    return b"".join(out)


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
    headers["content-length"] = str(len(body))
    return status, headers, body


def _fetch_once(url, ip, timeout=OPEN_SECONDS, connect=None) -> tuple:
    """One GET to the address checked: (status, headers, body). The hostname stays in Host and
    in TLS; only `ip` is connected to. Redirects are not followed here."""
    connect = connect or _connect
    parts = urlsplit(str(url))
    scheme = parts.scheme.lower()
    host = parts.hostname or ""
    port = parts.port or (443 if scheme == "https" else 80)
    header_host = _ascii_host(host)
    if parts.port and parts.port != (443 if scheme == "https" else 80):
        header_host += ":" + str(parts.port)
    target = quote(parts.path or "/", safe="/%:@!$&'()*+,;=-._~")
    if parts.query:
        target += "?" + quote(parts.query, safe="=&%:@!$'()*+,;/-._~")
    request = ("GET %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nAccept-Encoding: identity\r\n"
               "Connection: close\r\n\r\n" % (target, header_host)).encode("ascii", "replace")
    sock = connect(ip, port, host, scheme == "https", timeout)
    try:
        sock.sendall(request)
        raw = _read_all(sock, MAX_RESPONSE_BYTES + 65536)
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
    """The system proxy, as Playwright's context takes it ({} when there is none)."""
    try:
        proxies = getproxies()
    except Exception:
        return {}
    server = proxies.get("https") or proxies.get("http")
    if not server:
        return {}
    proxy = {"server": server}
    bypass = proxies.get("no", "")
    if bypass:
        proxy["bypass"] = ",".join(part.strip() for part in bypass.replace(";", ",").split(",") if part.strip())
    return proxy


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
            ip = ipaddress.ip_address(address.split("%", 1)[0])
            if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
                ip = ip.ipv4_mapped
            if not ip.is_global or ip.is_multicast:
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
        self.proxy = None
        self.context = None

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


async def _proxy_get(context, url):
    """One request through the system proxy (the proxy resolves; this computer connects to it)."""
    response = await context.request.get(url, max_redirects=0, timeout=OPEN_SECONDS * 1000)
    try:
        status = int(getattr(response, "status", 0) or 0)
        headers = getattr(response, "headers", None)
        if not isinstance(headers, dict):
            try:
                headers = dict(await response.all_headers())
            except Exception:
                headers = {}
        headers = {str(k).lower(): str(v) for k, v in (headers or {}).items() if str(k)}
        body = b""
        read = getattr(response, "body", None)
        if read is not None:
            try:
                body = bytes(await read() or b"")
            except Exception:
                body = b""
        return status, headers, body
    finally:
        try:
            await response.dispose()
        except Exception:
            pass


async def _get(route, gate, url, address):
    if gate.proxy:
        return await _proxy_get(gate.context, url)
    return await asyncio.to_thread(_fetch_once, url, address, OPEN_SECONDS)


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
        address, reason = await asyncio.to_thread(_pin_address, url, gate.check, gate.resolve)
        if address is None:
            on_block(reason)
            await route.abort()
            return
        status, headers, body = await _get(route, gate, url, address)
        location = headers.get("location") if isinstance(headers, dict) else None
        if status in REDIRECT_STATUS and location:
            # followed here, never by the browser: every hop resolved, checked, and connected again
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
        proxy = _proxy_config().get("server")
        gate.proxy = proxy

        def track(coro):
            task = asyncio.create_task(coro)
            pending.add(task)
            task.add_done_callback(pending.discard)

        async def route_request(route):
            await _route_pinned(route, gate)

        async def read(context):
            gate.context = context
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
            address, reason = await asyncio.to_thread(_pin_address, final_url, gate.check, gate.resolve)
            if address is None:
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
                address, reason = await asyncio.to_thread(_pin_address, address_to_check, gate.check, gate.resolve)
                if address is None:
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
