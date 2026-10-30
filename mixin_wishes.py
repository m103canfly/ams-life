# -*- coding: utf-8 -*-
"""Her proposals, checked as words to the owner before they are kept."""
import re

try:
    from .common import DATA_DIR, discretion, logger
    from . import wishes, send_check
except ImportError:
    from common import DATA_DIR, discretion, logger
    import wishes
    import send_check

WISHES_PATH = DATA_DIR / "wishes.json"


class WishesMixin:
    async def _tool_wish(self, event, what="", why=""):
        return await self._record_wish(event, what, why, "reply")

    async def _record_wish(self, event, what="", why="", where="reply"):
        if not self.enabled or not getattr(self, "wishes_enabled", False):
            return "没开"
        # A reply initializes the registry before tool execution. Never create its
        # database from this tool; without it the forget checks cannot run safely.
        if hasattr(self, "_registry") and getattr(self, "_forget_reg", None) is None:
            return "不能记下"
        try:
            def clean(value):
                text = self._without_gone(str(value or ""), event)
                text = discretion.hide_numbers(text, self._known_numbers())
                return re.sub(r"(?<!\d)\d{5,}(?!\d)", "号码", text).strip()
            what, why = clean(what), clean(why)
            if not wishes.WHAT_MIN <= len(what) <= wishes.WHAT_MAX or len(why) > wishes.WHY_MAX:
                return "字数不合适"
            if (await self._check_for_owner(what + "\n" + why)).get("leak", True):
                return "这条里有别人的私事，换个说法"
            if getattr(self, "_job_stale", lambda: False)():
                return "不能记下"
            people = [p for p, names in self._names_index().items()
                      if any(n and not n.isdigit() and send_check.mentions(what + "\n" + why, n)
                             for n in names)]
            speaker = str(self._speaker(event)[0] or "") if event is not None and where == "reply" else ""
            ids = self._source_ids(event) if event is not None and where == "reply" else []
            place = self._here(event) if event is not None else ""
            if not self._may_keep(people + ([speaker] if speaker else []), place, source_ids=ids):
                return "不能记下"
            return wishes.add(WISHES_PATH, what, why, where, people, ids, speaker)
        except Exception as exc:
            logger.warning("[ams-life] wish not kept (%s)", type(exc).__name__)
            return "不能记下"

    def _forget_wishes(self, person="", source_ids=()):
        return wishes.forget(WISHES_PATH, person, source_ids)

    def _new_wishes_count(self):
        if not getattr(self, "wishes_enabled", False):
            return 0
        return sum(x.get("status") == "新" for x in wishes.read(WISHES_PATH)["items"])

    def _wish_block(self, category):
        if not getattr(self, "wishes_enabled", False):
            return
        try:
            wishes.count_block(WISHES_PATH, category)
        except Exception as exc:
            logger.warning("[ams-life] wish count unavailable (%s)", type(exc).__name__)

    def _wish_materials(self, now=None):
        if not getattr(self, "wishes_enabled", False):
            return []
        from datetime import datetime
        return wishes.materials(WISHES_PATH, datetime.fromtimestamp(now) if now is not None else None)

    @staticmethod
    def _wish_local():
        try:
            import ipaddress
            from quart import request
            from urllib.parse import urlsplit
            if any(request.headers.get(key) for key in ("Forwarded", "X-Forwarded-For", "X-Real-IP")):
                return False
            host = urlsplit("//" + request.host).hostname or ""
            host_is_local = host.lower() == "localhost" or ipaddress.ip_address(host).is_loopback
            return host_is_local and ipaddress.ip_address(request.remote_addr).is_loopback
        except Exception:
            return False

    async def page_wishes(self):
        if not self._wish_local():
            return {"status": "error", "message": "仅限本机", "data": {}}
        if not getattr(self, "enabled", False) or not getattr(self, "wishes_enabled", False):
            return {"status": "ok", "data": {"on": False, "items": []}}
        try:
            items = [{key: item.get(key, "") for key in ("id", "what", "why", "time", "status", "marked_at")}
                     for item in wishes.read(WISHES_PATH)["items"]]
            for item in items:
                for key in ("what", "why"):
                    item[key] = re.sub(r"(?<!\d)\d{5,}(?!\d)", "号码", str(item[key]))
            return {"status": "ok", "data": {"on": True, "items": items}}
        except Exception:
            return {"status": "error", "message": "愿望单暂时读不了", "data": {}}

    async def page_wishes_status(self, body=None):
        if not self._wish_local():
            return {"status": "error", "message": "仅限本机", "data": {}}
        if not getattr(self, "enabled", False) or not getattr(self, "wishes_enabled", False):
            return {"status": "error", "message": "没开", "data": {}}
        body = await self._page_body(body)
        if body.get("status") not in ("好", "先放着", "不要"):
            return {"status": "error", "message": "状态不合适", "data": {}}
        try:
            if wishes.set_status(WISHES_PATH, body.get("id"), body["status"]):
                return {"status": "ok", "data": {"updated": True}}
        except Exception:
            pass
        return {"status": "error", "message": "没有这条愿望", "data": {}}
