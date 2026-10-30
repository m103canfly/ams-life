# -*- coding: utf-8 -*-
"""A temporary, read-only browser for pages that need scripts."""
import asyncio
import ipaddress
import logging
import socket
from contextlib import asynccontextmanager
from urllib.parse import urljoin, urlsplit
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
_lock = asyncio.Lock()


@asynccontextmanager
async def _timed_lock():
    await asyncio.wait_for(_lock.acquire(), timeout=LOCK_WAIT_SECONDS)
    try:
        yield
    finally:
        _lock.release()


async def _launch_browser(playwright, shot_path=None):
    browser = await playwright.chromium.launch(channel="msedge", headless=True,
                                               chromium_sandbox=True,
                                               args=["--disable-features=DnsOverHttps",
                                                     "--force-webrtc-ip-handling-policy=disable_non_proxied_udp"])
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


async def _route_request(route, checked, on_block, on_redirect=None, on_method_block=None):
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
    except Exception:
        logger.info("[ams-life] browser: request failed")
        await route.abort()
    finally:
        if response is not None:
            await response.dispose()


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
        rejected = []
        blocked = 0

        async def checked(address):
            return await asyncio.to_thread(_strict_url, address, check)

        def track(coro):
            task = asyncio.create_task(coro)
            pending.add(task)
            task.add_done_callback(pending.discard)

        def note_block(reason):
            nonlocal blocked
            blocked += 1
            logger.info("[ams-life] browser: blocked request (%s)", reason)

        async def route_request(route):
            await _route_request(route, checked, note_block)

        async def check_response(response):
            # Safety 4: redirects and all other responses are checked too.
            ok, reason = await checked(response.url)
            if not ok:
                rejected.append(reason)
            if 300 <= response.status < 400:
                location = response.headers.get("location")
                if location:
                    ok, reason = await checked(urljoin(response.url, location))
                    if not ok:
                        rejected.append(reason)

        async def read(context):
            nonlocal blocked
            await context.route("**/*", route_request)
            # Safety 3: close long-lived WebSockets before they can communicate.
            await context.route_web_socket("**/*", lambda ws: track(ws.close()))
            page = await context.new_page()
            # Safety 5: dismiss dialogs and close any page opened by the site.
            page.on("dialog", lambda dialog: track(dialog.dismiss()))
            context.on("page", lambda new_page: track(new_page.close()))
            context.on("response", lambda response: track(check_response(response)))

            response = await asyncio.wait_for(_navigate(context, page, url, checked, note_block), timeout=OPEN_SECONDS)
            while pending:
                await asyncio.gather(*list(pending), return_exceptions=True)
            if rejected:
                logger.info("[ams-life] browser: redirect refused (%s)", rejected[0])
                return None
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
            ok, reason = await checked(final_url)
            if not ok or rejected:
                logger.info("[ams-life] browser: redirect refused (%s)", reason if not ok else rejected[0])
                return None
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
            ok, reason = await checked(final_url)
            if not ok or rejected:
                logger.info("[ams-life] browser: redirect refused (%s)", reason if not ok else rejected[0])
                return None
            return shot_path if shot_path is not None else {"url": final_url, "title": title, "text": body}

        result = None
        try:
            async with async_playwright() as playwright:
                try:
                    # Safety 1: use Edge with its sandbox and a fresh, temporary context.
                    # Safety 3: disable the browser's encrypted DNS.
                    # Safety 2 and 3: shared context settings and WebRTC prevention.
                    browser, context = await _launch_browser(playwright, shot_path)
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
