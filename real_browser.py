# -*- coding: utf-8 -*-
"""A temporary, read-only browser for pages that need scripts."""
import asyncio
import base64
import http.client
import ipaddress
import logging
import socket
import ssl
from contextlib import asynccontextmanager
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import getproxies, proxy_bypass

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
_lock = asyncio.Lock()


@asynccontextmanager
async def _timed_lock():
    await asyncio.wait_for(_lock.acquire(), timeout=LOCK_WAIT_SECONDS)
    try:
        yield
    finally:
        _lock.release()


async def _launch_browser(playwright, shot_path=None, pinned=False):
    browser = await playwright.chromium.launch(channel="msedge", headless=True,
                                               chromium_sandbox=True,
                                               args=["--disable-features=DnsOverHttps",
                                                     "--force-webrtc-ip-handling-policy=disable_non_proxied_udp"]
                                               + (["--host-resolver-rules=MAP * ~NOTFOUND"] if pinned else []))
    try:
        options = dict(accept_downloads=False, permissions=[], service_workers="block",
                       ignore_https_errors=False, bypass_csp=False)
        try:
            proxies = getproxies()
        except Exception:
            proxies = {}
        server = proxies.get("https") or proxies.get("http")
        if server:
            proxy = {"server": server}
            bypass = proxies.get("no", "")
            if bypass:
                proxy["bypass"] = ",".join(part.strip() for part in bypass.replace(";", ",").split(",") if part.strip())
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


def _pinned_get(url, address, headers, proxy=None):
    """Fetch one hop; the checked address is the only direct destination."""
    parts = urlsplit(url)
    host = parts.hostname
    port = parts.port or (443 if parts.scheme == "https" else 80)
    target = (parts.path or "/") + (("?" + parts.query) if parts.query else "")
    outgoing = {k: v for k, v in headers.items()
                if k.lower() not in ("host", "connection", "proxy-authorization", "content-length")}
    outgoing["Host"] = parts.netloc
    if proxy:
        p = urlsplit(proxy if "://" in proxy else "http://" + proxy)
        if p.scheme != "http" or not p.hostname:
            raise ValueError("unsupported proxy")
        conn = http.client.HTTPConnection(p.hostname, p.port or 80, timeout=OPEN_SECONDS)
        proxy_headers = {}
        if p.username is not None:
            credentials = (unquote(p.username) + ":" + unquote(p.password or "")).encode("utf-8")
            proxy_headers["Proxy-Authorization"] = "Basic " + base64.b64encode(credentials).decode("ascii")
        if parts.scheme == "https":
            conn.set_tunnel(host, port, headers=proxy_headers)
            conn.connect()
            conn.sock = ssl.create_default_context().wrap_socket(conn.sock, server_hostname=host)
        else:
            target = parts._replace(fragment="").geturl()
            outgoing.update(proxy_headers)
    else:
        conn = http.client.HTTPConnection(address, port, timeout=OPEN_SECONDS)
        family = socket.AF_INET6 if ipaddress.ip_address(address).version == 6 else socket.AF_INET
        sock = socket.socket(family, socket.SOCK_STREAM)
        sock.settimeout(OPEN_SECONDS)
        try:
            sock.connect((address, port))
        except BaseException:
            sock.close()
            raise
        conn.sock = sock
        if parts.scheme == "https":
            try:
                conn.sock = ssl.create_default_context().wrap_socket(conn.sock, server_hostname=host)
            except BaseException:
                conn.close()
                raise
    try:
        conn.request("GET", target, headers=outgoing)
        response = conn.getresponse()
        body = response.read(HTML_MAX_BYTES + 1)
        if len(body) > HTML_MAX_BYTES:
            raise ValueError("response too large")
        return response.status, dict(response.getheaders()), body
    finally:
        conn.close()


def _fetch_checked(url, headers, check=browse.check_url):
    """Check and fetch each redirect hop without a second hostname lookup."""
    for hop in range(MAX_HOPS + 1):
        ok, reason = check(url)
        if ok:
            ok, reason = browse.check_url(url)
        if not ok:
            raise ValueError(reason)
        parts = urlsplit(url)
        addresses = list(dict.fromkeys(info[4][0] for info in socket.getaddrinfo(parts.hostname, None)))
        for address in addresses:
            ipaddress.ip_address(address.split("%", 1)[0])
        if not addresses or any(browse._bad_address(address) for address in addresses):
            raise ValueError("local or unresolved address")
        try:
            proxies = getproxies()
            proxy = None if not proxies or proxy_bypass(parts.hostname) else (proxies.get("https") or proxies.get("http"))
        except Exception:
            proxy = None
        status, response_headers, body = _pinned_get(url, addresses[0], headers, proxy)
        location = next((value for key, value in response_headers.items() if key.lower() == "location"), None)
        if 300 <= status < 400:
            if not location or hop == MAX_HOPS:
                raise ValueError("redirect limit")
            next_url = urljoin(url, location)
            if urlsplit(next_url).netloc != parts.netloc:
                headers = {k: v for k, v in headers.items() if k.lower() not in ("cookie", "authorization")}
            url = next_url
            continue
        return status, response_headers, body
    raise ValueError("redirect limit")


async def _pinned_route(route, on_block, count, check=browse.check_url):
    request = route.request
    scheme = urlsplit(request.url).scheme.lower()
    if scheme in ("data", "blob"):
        await route.continue_()
        return
    count[0] += 1
    if count[0] > 61 or request.method.upper() != "GET" or scheme not in ("http", "https"):
        on_block("request refused")
        await route.abort()
        return
    try:
        status, headers, body = await asyncio.wait_for(
            asyncio.to_thread(_fetch_checked, request.url, dict(getattr(request, "headers", {}) or {}), check),
            timeout=OPEN_SECONDS)
        headers = {k: v for k, v in headers.items()
                   if k.lower() not in ("connection", "transfer-encoding", "content-length")}
        await route.fulfill(status=status, headers=headers, body=body)
    except Exception:
        on_block("request failed")
        await route.abort()


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


async def read_page(url, check, on_block=None):
    return await _safe_visit(url, check, None, on_block)


async def screenshot(url, check, path, on_block=None):
    return await _safe_visit(url, check, path, on_block)


async def _safe_visit(url, check, path, on_block):
    try:
        return await _visit(url, check, path, on_block)
    except asyncio.TimeoutError:
        logger.info("[ams-life] 浏览器正忙")
        return None


async def _visit(url, check, shot_path, on_block):
    # Safety 8: one browser page at a time, including other callers of this module.
    async with _timed_lock():
        try:
            from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
        except ImportError:
            logger.info("[ams-life] browser: playwright unavailable")
            return None
        browser = context = None
        pending = set()
        blocked = 0
        count = [0]

        def track(coro):
            task = asyncio.create_task(coro)
            pending.add(task)
            task.add_done_callback(pending.discard)

        def note_block(reason):
            nonlocal blocked
            blocked += 1
            if reason != "request failed":
                logger.info("[ams-life] browser: blocked request (%s)", reason)

        async def route_request(route):
            await _pinned_route(route, note_block, count, check)

        async def read(context):
            nonlocal blocked
            await context.route("**/*", route_request)
            # Safety 3: close long-lived WebSockets before they can communicate.
            await context.route_web_socket("**/*", lambda ws: track(ws.close()))
            page = await context.new_page()
            # Safety 5: dismiss dialogs and close any page opened by the site.
            page.on("dialog", lambda dialog: track(dialog.dismiss()))
            context.on("page", lambda new_page: track(new_page.close()))
            response = await asyncio.wait_for(page.goto(url, wait_until="domcontentloaded",
                                                        timeout=OPEN_SECONDS * 1000), timeout=OPEN_SECONDS)
            while pending:
                await asyncio.gather(*list(pending), return_exceptions=True)
            if response is None or not 200 <= response.status < 300 or urlsplit(page.url).scheme.lower() not in ("http", "https"):
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
            final_url = page.url
            # Safety 9: short challenge pages are not read or photographed.
            if len(body.strip()) < CHALLENGE_MAX_CHARS and any(
                    marker in (title + "\n" + body).lower() for marker in CHALLENGE_MARKERS):
                logger.info("[ams-life] browser: verification page")
                return None
            if shot_path is not None:
                await _take_screenshot(page, shot_path)
                final_url = page.url
            else:
                body = await _article_text(page, body)
            # Stop further responses before deciding whether every response was safe.
            await context.close()
            while pending:
                await asyncio.gather(*list(pending), return_exceptions=True)
            return shot_path if shot_path is not None else {"url": final_url, "title": title, "text": body}

        result = None
        try:
            async with async_playwright() as playwright:
                try:
                    # Safety 1: use Edge with its sandbox and a fresh, temporary context.
                    # Safety 3: disable the browser's encrypted DNS.
                    # Safety 2 and 3: shared context settings and WebRTC prevention.
                    browser, context = await _launch_browser(playwright, shot_path, pinned=True)
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
            if on_block is not None and blocked:
                try:
                    on_block(blocked)
                except Exception:
                    logger.info("[ams-life] browser: blocked request count could not be saved")
            if shot_path is not None and result is None:
                try:
                    from pathlib import Path
                    Path(shot_path).unlink(missing_ok=True)
                except Exception:
                    logger.info("[ams-life] browser: incomplete screenshot could not be removed")
        return result
