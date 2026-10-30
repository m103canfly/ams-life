# -*- coding: utf-8 -*-
"""A bounded interactive session using the same browser safety layer as page reads."""
import asyncio
import inspect
import os
import re
import time
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import url2pathname

try:
    from . import browse, real_browser
except ImportError:
    import browse
    import real_browser

MAX_STEPS = 30
MAX_SECONDS = 600
MAX_ELEMENTS = 60
VISIBLE_CHARS = 3000
SNAPSHOT_CHARS = 10000
SNAPSHOT_DEPTH = 20
ACTION_SECONDS = 20
ROLES = {"link": "链接", "button": "按钮", "textbox": "文本框", "searchbox": "搜索框",
         "combobox": "下拉框", "checkbox": "复选框", "tab": "标签"}
TYPE_ROLES = frozenset(("textbox", "searchbox", "combobox"))
ACTIONS = frozenset(("open", "click", "type", "press", "scroll_down", "scroll_up",
                     "back", "read", "screenshot", "finish"))
KEYS = frozenset(("Enter", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "PageUp",
                  "PageDown", "Space", "Escape", "Tab"))
LOGIN_MARKERS = ("密码", "口令", "账号", "账户", "登录", "用户名", "password", "passwd",
                 "username", "user name", "login", "log in", "sign in", "account")
UNAVAILABLE = "不能用"
BLOCKED = "这个这里点不了"
LIMIT = "已到步数或时间上限，请结束"
_LINE = re.compile(r'^\s*-\s*(link|button|textbox|searchbox|combobox|checkbox|tab)\b(.*)$', re.I)
_REF = re.compile(r'\[ref=(e\d+)\]')
_NAME = re.compile(r'^\s*"([^"\n]*)"')


def _file_in_games(url, games_dir):
    try:
        parts = urlsplit(url)
        if parts.scheme.lower() != "file" or parts.netloc or parts.query:
            return False
        path = Path(url2pathname(unquote(parts.path))).resolve()
        root = Path(games_dir).resolve()
        # On Windows, comparisons must ignore drive and path case.
        relative = os.path.relpath(os.path.normcase(str(path)), os.path.normcase(str(root)))
        return relative != "." and relative != ".." and not relative.startswith(".." + os.sep)
    except (ValueError, OSError):
        return False


class BrowsingSession:
    def __init__(self, check, *, browser_enabled=False, browser_interactive_enabled=False,
                 allowed_urls=(), typing_check=None, games_dir=None, on_block=None):
        self.enabled = bool(browser_enabled and browser_interactive_enabled)
        self.check, self.allowed_urls = check, set(allowed_urls)
        self.typing_check, self.games_dir, self.on_block = typing_check, games_dir, on_block
        self.browser = self.context = self.page = self.playwright = self.manager = None
        self.pending, self.refs = set(), {}
        self.ref_url = None
        self.redirect, self.popups = None, []
        self.rejected = False
        self.blocked_methods = 0
        self.steps, self.started = 0, None
        self.game = False
        self.finished = False
        self.locked = False

    async def __aenter__(self):
        if not self.enabled:
            return self
        await real_browser._lock.acquire()
        self.locked = True
        try:
            from playwright.async_api import async_playwright
            self.manager = async_playwright()
            self.playwright = await self.manager.__aenter__()
            self.browser, self.context = await real_browser._launch_browser(self.playwright, True)
            await self.context.route("**/*", self._route)
            await self.context.route_web_socket("**/*", lambda ws: self._track(ws.close()))
            self.page = await self.context.new_page()
            # Safety 3 and 5: a file chooser is cancelled without selecting a file; dismiss dialogs.
            self.page.on("filechooser", lambda chooser: None)
            self.page.on("dialog", lambda dialog: self._track(dialog.dismiss()))
            # Safety 4: close new pages; their navigation is handled on the current page.
            self.context.on("page", lambda page: self._track(self._popup(page)))
            self.context.on("response", lambda response: self._track(self._check_response(response)))
            self.started = time.monotonic()
            return self
        except ImportError:
            await self.close()
            self.enabled = False
            return self
        except BaseException:
            await self.close()
            raise

    async def __aexit__(self, *args):
        await self.close()

    def _track(self, coro):
        task = asyncio.create_task(coro)
        self.pending.add(task)
        task.add_done_callback(self.pending.discard)

    async def _drain(self):
        while self.pending:
            await asyncio.gather(*list(self.pending), return_exceptions=True)

    async def _popup(self, page):
        try:
            if page.url and page.url != "about:blank":
                self.popups.append(page.url)
            await page.close()
        except Exception:
            self.rejected = True

    async def _checked(self, address):
        return await asyncio.to_thread(real_browser._strict_url, address, self.check)

    async def _check_response(self, response):
        try:
            if self.game:
                if not self.games_dir or not _file_in_games(response.url, self.games_dir):
                    self.rejected = True
                return
            ok, _ = await self._checked(response.url)
            if not ok:
                self.rejected = True
            if 300 <= response.status < 400:
                location = response.headers.get("location")
                if location and not (await self._checked(urljoin(response.url, location)))[0]:
                    self.rejected = True
        except Exception:
            self.rejected = True

    def _blocked(self, reason):
        if reason == "method":
            self.blocked_methods += 1
        if self.on_block:
            try:
                self.on_block(1)
            except Exception:
                pass

    def _redirected(self, request, response):
        # Safety 1: only the main frame's navigation may be followed after an abort.
        try:
            location = response.headers.get("location")
            if location and request.is_navigation_request() and request.frame == self.page.main_frame:
                self.redirect = urljoin(request.url, location)
        except Exception:
            pass

    async def _route(self, route):
        request = route.request
        # Safety 4: a popup's first navigation must not reach the network before it is checked.
        try:
            if request.is_navigation_request() and request.frame.page != self.page:
                self.popups.append(request.url)
                await route.abort()
                return
        except Exception:
            pass
        if self.game:
            if request.method.upper() in ("GET", "HEAD") and _file_in_games(request.url, self.games_dir):
                await route.continue_()
            else:
                self._blocked("method" if request.method.upper() not in ("GET", "HEAD") else "game")
                await route.abort()
            return
        # Safety 2: the shared route rejects non-GET/HEAD methods and never follows redirects.
        await real_browser._route_request(route, self._checked, self._blocked, self._redirected)

    def _remaining(self):
        return MAX_SECONDS - (time.monotonic() - self.started) if self.started is not None else 0

    def _can_act(self):
        return self.enabled and self.page is not None and not self.finished

    async def _run(self, coro):
        return await asyncio.wait_for(coro, timeout=min(ACTION_SECONDS, max(0.001, self._remaining())))

    async def _goto(self, url):
        response = await real_browser._navigate(self.context, self.page, url, self._checked, self._blocked)
        if response is None or not 200 <= response.status < 300:
            return False
        return (await self._checked(self.page.url))[0]

    async def _valid_page(self):
        if self.rejected:
            return False
        if self.game:
            return bool(self.games_dir and _file_in_games(self.page.url, self.games_dir))
        return (await self._checked(self.page.url))[0]

    async def open(self, url):
        return await self.act({"action": "open", "url": url})

    async def open_game(self, name):
        if not self._can_act():
            return UNAVAILABLE
        # Safety 7: game entry is a step too, and cannot bypass the session limits.
        if self.steps >= MAX_STEPS or self._remaining() <= 0:
            return LIMIT
        self.steps += 1
        self.refs.clear()
        try:
            if not self.games_dir or not isinstance(name, str) or Path(name).is_absolute():
                return BLOCKED
            root = Path(self.games_dir).resolve()
            target = (root / name).resolve()
            if target.suffix.lower() != ".html" or not target.is_file() or not _file_in_games(target.as_uri(), root):
                return BLOCKED
            self.game = True
            await self._run(self.page.goto(target.as_uri(), wait_until="domcontentloaded",
                                           timeout=real_browser.OPEN_SECONDS * 1000))
            return await self.snapshot()
        except Exception:
            return BLOCKED

    async def snapshot(self):
        if not self._can_act():
            return UNAVAILABLE
        if self._remaining() <= 0 or self.steps >= MAX_STEPS:
            self.refs.clear()
            return LIMIT
        self.refs.clear()
        try:
            await self._run(self._drain())
            if not await self._run(self._valid_page()):
                return BLOCKED
            address = self.page.url
            title = await self._run(self.page.title())
            body = await self._run(self.page.locator("body").inner_text(timeout=real_browser.TEXT_SECONDS * 1000))
            if len(body.strip()) < real_browser.CHALLENGE_MAX_CHARS and any(
                    marker in (title + "\n" + body).lower() for marker in real_browser.CHALLENGE_MARKERS):
                return BLOCKED
            raw = await self._run(self.page.aria_snapshot(mode="ai", depth=SNAPSHOT_DEPTH,
                                                          timeout=real_browser.TEXT_SECONDS * 1000))
            if self.page.url != address or not await self._run(self._valid_page()):
                return BLOCKED
            self.ref_url = self.page.url
            prefix = "网址: %s\n标题: %s\n可见文字: %s\n元素:\n" % (
                self.page.url[:400], title[:200], body[:VISIBLE_CHARS])
            lines = []
            for line in raw.splitlines():
                match, ref = _LINE.match(line), _REF.search(line)
                if not match or not ref:
                    continue
                role, tail = match.group(1).lower(), match.group(2)
                name_match = _NAME.match(tail)
                name = (name_match.group(1) if name_match else "")[:120]
                number = len(self.refs) + 1
                label = '[%d] %s “%s”' % (number, ROLES[role], name)
                if len(prefix) + sum(len(item) + 1 for item in lines) + len(label) > SNAPSHOT_CHARS:
                    break
                self.refs[number] = (ref.group(1), role, line.lower())
                lines.append(label)
                if number >= MAX_ELEMENTS:
                    break
            text = prefix + "\n".join(lines)
            return browse.wrap(self.page.url, text[:SNAPSHOT_CHARS], limit=SNAPSHOT_CHARS)
        except Exception:
            self.refs.clear()
            return BLOCKED

    async def _follow(self):
        await self._drain()
        if self.rejected:
            return False
        # Safety 1 and 4: follow the captured destination through the same per-hop checks.
        destination = self.redirect
        self.redirect = None
        if self.popups:
            destination = self.popups[-1]
            self.popups.clear()
        if destination:
            if self.game:
                if not _file_in_games(destination, self.games_dir):
                    return False
                await self.page.goto(destination, wait_until="domcontentloaded", timeout=real_browser.OPEN_SECONDS * 1000)
            elif not await self._goto(destination):
                return False
        return True

    async def _action(self, action):
        name = action["action"]
        if name == "open":
            url = action.get("url")
            if self.game or url not in self.allowed_urls:
                return BLOCKED
            self.game = False
            if not await self._goto(url):
                return BLOCKED
        elif name in ("click", "type"):
            item = self.refs.get(action.get("n"))
            if item is None or self.page.url != self.ref_url or not await self._valid_page():
                return BLOCKED
            title = await self.page.title()
            body = await self.page.locator("body").inner_text(timeout=real_browser.TEXT_SECONDS * 1000)
            if len(body.strip()) < real_browser.CHALLENGE_MAX_CHARS and any(
                    marker in (title + "\n" + body).lower() for marker in real_browser.CHALLENGE_MARKERS):
                return BLOCKED
            ref, role, line = item
            locator = self.page.get_by_ref(ref)
            if name == "click":
                before = self.blocked_methods
                try:
                    await locator.click(timeout=ACTION_SECONDS * 1000)
                except Exception:
                    if not self.redirect and not self.popups and self.blocked_methods == before:
                        raise
            else:
                # Safety 6: fail closed if the caller has not supplied a typing check.
                if role not in TYPE_ROLES or not callable(self.typing_check):
                    return BLOCKED
                if any(marker in line for marker in LOGIN_MARKERS):
                    return BLOCKED
                kind = (await locator.get_attribute("type") or "").lower()
                if kind == "password":
                    return BLOCKED
                cleaned = self.typing_check(action.get("text", ""))
                if inspect.isawaitable(cleaned):
                    cleaned = await cleaned
                if not isinstance(cleaned, str):
                    return BLOCKED
                await locator.fill(cleaned, timeout=ACTION_SECONDS * 1000)
        elif name == "press":
            key = action.get("key")
            if not isinstance(key, str) or key not in KEYS:
                return BLOCKED
            await self.page.keyboard.press(key)
        elif name in ("scroll_down", "scroll_up"):
            await self.page.mouse.wheel(0, 600 if name == "scroll_down" else -600)
        elif name == "back":
            await self.page.go_back(wait_until="domcontentloaded", timeout=ACTION_SECONDS * 1000)
        elif name == "read":
            if not await self._valid_page():
                return BLOCKED
            body = await self.page.locator("body").inner_text(timeout=real_browser.TEXT_SECONDS * 1000)
            title = await self.page.title()
            if not body.strip() or (len(body.strip()) < real_browser.CHALLENGE_MAX_CHARS and any(
                    marker in (title + "\n" + body).lower() for marker in real_browser.CHALLENGE_MARKERS)):
                return BLOCKED
            body = await real_browser._article_text(self.page, body)
            return browse.wrap(self.page.url, "Title: %s\nContent: %s" % (title, body))
        elif name == "screenshot":
            path = action.get("path")
            if not path or not await self._valid_page():
                return BLOCKED
            title = await self.page.title()
            body = await self.page.locator("body").inner_text(timeout=real_browser.TEXT_SECONDS * 1000)
            if not body.strip() or (len(body.strip()) < real_browser.CHALLENGE_MAX_CHARS and any(
                    marker in (title + "\n" + body).lower() for marker in real_browser.CHALLENGE_MARKERS)):
                return BLOCKED
            await real_browser._take_screenshot(self.page, path)
            return path
        return None

    async def act(self, action):
        if not self._can_act():
            return UNAVAILABLE
        if (not isinstance(action, dict) or not isinstance(action.get("action"), str)
                or action.get("action") not in ACTIONS):
            return BLOCKED
        name = action["action"]
        if name == "finish":
            self.finished = True
            self.refs.clear()
            return "已结束"
        # Safety 7: once either limit is reached, only finish remains available.
        if self.steps >= MAX_STEPS or self._remaining() <= 0:
            self.refs.clear()
            return LIMIT
        self.steps += 1
        before = self.blocked_methods
        self.redirect, self.popups = None, []
        try:
            result = await self._run(self._action(action))
            self.refs.clear()
            if not await self._run(self._follow()):
                if name == "screenshot" and result and result != BLOCKED:
                    Path(result).unlink(missing_ok=True)
                return BLOCKED
            if self.blocked_methods != before:
                if name == "screenshot" and result and result != BLOCKED:
                    Path(result).unlink(missing_ok=True)
                return BLOCKED
            if result == BLOCKED:
                return result
            snapshot = await self.snapshot()
            if snapshot == BLOCKED:
                if name == "screenshot" and result:
                    Path(result).unlink(missing_ok=True)
                return BLOCKED
            if name == "read" and result is not None:
                return result + "\n" + snapshot
            if name == "screenshot" and result is not None:
                return {"path": result, "snapshot": snapshot}
            return snapshot
        except Exception:
            self.refs.clear()
            if name == "screenshot" and action.get("path"):
                try:
                    Path(action["path"]).unlink(missing_ok=True)
                except OSError:
                    pass
            return BLOCKED

    async def close(self):
        self.finished = True
        try:
            for task in list(self.pending):
                task.cancel()
            await self._drain()
            try:
                if self.context:
                    context, self.context = self.context, None
                    await context.close()
            finally:
                if self.browser:
                    browser, self.browser = self.browser, None
                    await browser.close()
        finally:
            try:
                if self.manager:
                    manager, self.manager = self.manager, None
                    await manager.__aexit__(None, None, None)
            finally:
                if self.locked:
                    self.locked = False
                    real_browser._lock.release()
