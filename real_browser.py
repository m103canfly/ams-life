# -*- coding: utf-8 -*-
"""A temporary, read-only browser for pages that need scripts."""
import asyncio
import ipaddress
import logging
import socket
from urllib.parse import urljoin, urlsplit

logger = logging.getLogger(__name__)
OPEN_SECONDS = 20
# Script-driven pages may fetch their visible content after DOMContentLoaded.
SETTLE_SECONDS = 8
TEXT_SECONDS = 10
SHOT_SECONDS = 10
CHALLENGE_MAX_CHARS = 600
SHOT_VIEWPORT = {"width": 390, "height": 844}
SHOT_QUALITY = 70
CHALLENGE_MARKERS = ("verify you are human", "checking your browser", "just a moment...",
                     "captcha", "cloudflare", "请验证您是人类")
_lock = asyncio.Lock()


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


async def read_page(url, check, on_block=None):
    return await _visit(url, check, None, on_block)


async def screenshot(url, check, path, on_block=None):
    return await _visit(url, check, path, on_block)


async def _visit(url, check, shot_path, on_block):
    # Safety 8: one browser page at a time, including other callers of this module.
    async with _lock:
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

        async def route_request(route):
            # Safety 3: every request must be public and read-only.
            nonlocal blocked
            request = route.request
            if request.method.upper() not in ("GET", "HEAD"):
                blocked += 1
                logger.info("[ams-life] browser: blocked request (method)")
                await route.abort()
                return
            ok, reason = await checked(request.url)
            if not ok:
                blocked += 1
                logger.info("[ams-life] browser: blocked request (%s)", reason)
                await route.abort()
                return
            await route.continue_()

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
            ok, reason = await checked(url)
            if not ok:
                blocked += 1
                logger.info("[ams-life] browser: page refused (%s)", reason)
                return None
            await context.route("**/*", route_request)
            # Safety 3: close long-lived WebSockets before they can communicate.
            await context.route_web_socket("**/*", lambda ws: track(ws.close()))
            page = await context.new_page()
            # Safety 5: dismiss dialogs and close any page opened by the site.
            page.on("dialog", lambda dialog: track(dialog.dismiss()))
            context.on("page", lambda new_page: track(new_page.close()))
            context.on("response", lambda response: track(check_response(response)))
            response = await asyncio.wait_for(page.goto(url, wait_until="domcontentloaded", timeout=OPEN_SECONDS * 1000),
                                              timeout=OPEN_SECONDS)
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
            # Safety 6: only read title and visible body text; no interaction or injected script.
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
                await asyncio.wait_for(page.screenshot(path=str(shot_path), type="jpeg", quality=SHOT_QUALITY,
                                                       full_page=False, timeout=SHOT_SECONDS * 1000),
                                       timeout=SHOT_SECONDS)
                final_url = page.url
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
                    browser = await playwright.chromium.launch(channel="msedge", headless=True,
                                                               chromium_sandbox=True,
                                                               args=["--disable-features=DnsOverHttps"])
                    # Safety 2: deny downloads, permissions and service workers; keep TLS and CSP checks.
                    options = dict(accept_downloads=False, permissions=[], service_workers="block",
                                   ignore_https_errors=False, bypass_csp=False)
                    if shot_path is not None:
                        options["viewport"] = dict(SHOT_VIEWPORT)
                    context = await browser.new_context(**options)
                    # Safety 7: the caller passes the result to browse.wrap as untrusted material.
                    result = await asyncio.wait_for(read(context), timeout=OPEN_SECONDS + SETTLE_SECONDS + 2 * TEXT_SECONDS + SHOT_SECONDS)
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
