# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""ams-life: the brain map (pages/brain) in the plugin, read only.

- page/brain, page/brain/node, page/brain/search: what she keeps, as the page's
  stars and lines (brain_graph.py), behind the dashboard login like the rest of
  the panel. Nothing here changes her: files are read as they are (no phone
  window is pruned on the way), the body is read without moving it on, and the
  forget registry is asked about everything; when it cannot be read nothing is
  returned.
- Every reply's recall is noted, ids only, the last brain_graph.TURNS_MAX
  turns, after the same checks as any other write (the forget registry, the
  forget count). The owner's deletes take it out of there too (_forget), and a
  restore deletes again from it what the owner deleted (_forget_registered).
"""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from . import brain_graph
except ImportError:
    import brain_graph

BRAIN_TURNS_PATH = DATA_DIR / "brain_turns.json"
BRAIN_CACHE_SECONDS = 30   # one build serves the parts, the stars opened and the searches meanwhile


def _arg(args, name) -> str:
    try:
        return str(args.get(name) or "").strip()
    except Exception:
        return ""


class BrainMixin:
    # ------------------------------------------------------------------
    # What each reply recalled (ids only)
    # ------------------------------------------------------------------
    def _turn_log(self):
        return brain_graph.TurnLog(BRAIN_TURNS_PATH)

    @staticmethod
    def _brain_body(core) -> dict:
        """Her body's seven numbers as they are now (no decay applied: reading moves nothing)."""
        if core is None:
            return {}
        return brain_graph.body_of({
            "social": getattr(core, "social", 0.0), "boredom": getattr(core, "boredom", 0.0),
            "seen_need": getattr(core, "seen_need", 0.0), "talked": getattr(core, "talked", 0.0),
            "stress": getattr(core, "stress", 0.0), "v": getattr(core, "v", 0.0),
            "novelty_need": getattr(core, "novelty_need", 0.5),
            "homeostasis": getattr(core, "homeostasis", None) or {}})

    def _note_turn(self, event, turn, core=None) -> dict:
        """Note what this reply recalled (turn["recall_order"], in order, and the lines it went
        along) and what the discretion table held back here (turn["recall_held"]). Not when
        something was forgotten since this message came in, nor when the message is from
        someone (or is one) she may not keep, nor when the registry cannot be read."""
        rec = [str(x) for x in turn.get("recall_order") or []]
        held = [str(x) for x in turn.get("recall_held") or []]
        if not rec and not held:
            return {}
        if self._job_stale():
            return {}
        here = self._here(event)
        try:
            sid, _name = self._speaker(event)
        except Exception:
            sid = ""
        try:
            if not self._may_keep([sid] if sid else [], here, time.time()):
                return {}
        except forget_registry.Unreadable as exc:
            logger.warning("[ams-life] forget registry unreadable, turn not noted: %s", exc)
            return {}
        known = self._library_ids()
        try:
            return self._turn_log().add({
                "ts": time.time(), "where": here,
                "recalled": [x for x in rec if x in known], "held": [x for x in held if x in known],
                "path": turn.get("recall_path") or [], "body": self._brain_body(core)})
        except Exception as exc:
            logger.warning("[ams-life] turn note failed: %s", exc)
            return {}

    def _forget_turns(self, gone_ids=(), person="") -> int:
        """The owner deleted memories (gone_ids) or a person: out of the turns too (his private
        chat's turns whole)."""
        places = ["private:" + str(person)] if person else []
        if not gone_ids and not places:
            return 0
        return self._turn_log().prune(gone_ids=gone_ids, gone_places=places)

    def _turns_to_library(self) -> int:
        """After a restore: no turn names a memory that is not in the library."""
        return self._turn_log().prune(keep_ids=self._library_ids())

    # ------------------------------------------------------------------
    # The page's data
    # ------------------------------------------------------------------
    def _brain_key(self) -> bytes:
        """The key the page's ids are made with: new each time the plugin starts, never stored
        or sent, so an id cannot be turned back into a QQ number or a group number."""
        key = getattr(self, "_brain_page_key", None)
        if key is None:
            key = self._brain_page_key = os.urandom(16)
        return key

    def _brain_sources(self) -> dict:
        """Read what she keeps, as it is on disk (no writes; may run in a worker thread)."""
        now = time.time()
        out = {"memories": self._read_library(vectors=False)["entries"], "events": [], "records": {},
               "impressions": {}, "windows": {}, "turns": self._turn_log().read()}
        if EVENT_ARCHIVE_PATH.exists():
            for line in EVENT_ARCHIVE_PATH.read_text(encoding="utf-8").splitlines():
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if isinstance(rec, dict):
                    out["events"].append(rec)
        if USER_DIR.exists():
            for path in sorted(USER_DIR.glob("*.json")):
                try:
                    rec = json.loads(path.read_text(encoding="utf-8"))
                except Exception:
                    continue
                if not isinstance(rec, dict):
                    continue
                qq = str(rec.get("sender_id") or path.stem)
                out["records"][qq] = {"names": [rec.get("sender_name")] + list(rec.get("names") or []),
                                      "ts": rec.get("last_seen") or rec.get("ts") or 0}
        if hasattr(self, "_impression_store"):
            store = self._impression_store()
            for place in store.places():
                out["impressions"][place] = dict(store.load(place).get("people") or {})
        if PHONE_DIR.exists():
            for path in sorted(PHONE_DIR.glob("*.json")):
                try:
                    win = json.loads(path.read_text(encoding="utf-8"))
                except Exception:
                    continue
                place = str((win or {}).get("place") or "") if isinstance(win, dict) else ""
                if not place or self._window_file(place) != path:
                    continue
                lines = [x for x in win.get("recent") or [] if isinstance(x, dict)]
                ts = [float(x.get("ts") or 0) for x in lines if x.get("ts")]
                out["windows"][place] = {
                    "lines24": sum(1 for t in ts if t >= now - 86400), "first": min(ts) if ts else 0,
                    "last": max(ts) if ts else 0,
                    "names": {str(x.get("sender_id")): str(x.get("sender_name") or "") for x in lines
                              if x.get("sender_id") and x.get("sender_name") and x.get("role") != "assistant"}}
        return out

    def _brain_mark(self) -> tuple:
        """What a build depends on beyond the files: the forget count and the registry's last row."""
        try:
            return (self._forget_count(), self._registry().last_seq())
        except Exception as exc:
            raise forget_registry.Unreadable(str(exc)) from exc

    def _brain_person_kept(self, qq, at=None) -> bool:
        return self._may_keep([qq], "", at)

    async def _brain_snapshot(self):
        """The page's data, built at most every BRAIN_CACHE_SECONDS, and again at once when
        anything was deleted or registered meanwhile."""
        mark = self._brain_mark()
        cache = getattr(self, "_brain_cache", None)
        if cache is not None and cache[0] == mark and time.time() - cache[1].made < BRAIN_CACHE_SECONDS:
            return cache[1]
        reg = self._registry()

        def impression_kept(qq, place):
            try:
                return reg.impression_allowed(qq, place)
            except Exception as exc:
                raise forget_registry.Unreadable(str(exc)) from exc
        for _attempt in range(3):
            src = await asyncio.to_thread(self._brain_sources)
            src["notes"] = [x for x in (self.self_model or {}).get("notebook") or [] if isinstance(x, dict)]
            src["body"] = self._brain_body(self._core(None))
            src["now"] = time.time()
            src["impressions"] = {place: {qq: rec for qq, rec in people.items() if impression_kept(qq, place)}
                                  for place, people in src["impressions"].items()}
            snap = brain_graph.build(src, brain_graph.PageIds(self._brain_key()), self._origin_kept,
                                     self._brain_person_kept)
            snap.impressions = src["impressions"]
            again = self._brain_mark()
            if again == mark:
                self._brain_cache = (mark, snap)
                return snap
            mark = again   # something was deleted while reading: read again
        raise RuntimeError("她的记忆正在变，请稍后再打开")

    @staticmethod
    def _page_args(args):
        if args is not None:
            return args
        try:
            from quart import request
            return request.args
        except Exception:
            return {}

    async def page_brain(self, args=None):
        """The stars and lines (no words, names or numbers). Part 0 has everything but the rest
        of the stars and lines; ?part=k&snap=<token> fetches the others of the same build. When
        that build is gone (something was deleted meanwhile) the answer is {"stale": true}, not
        an error: AstrBot's page bridge passes an error on as its message alone."""
        args = self._page_args(args)
        try:
            part = max(0, int(_arg(args, "part") or 0))
        except ValueError:
            part = 0
        try:
            if part:
                cache = getattr(self, "_brain_cache", None)
                if not cache or cache[1].token != _arg(args, "snap") or cache[0] != self._brain_mark() \
                        or part >= cache[1].parts:
                    return {"status": "ok", "data": {"stale": True}}
                return {"status": "ok", "data": cache[1].part(part)}
            snap = await self._brain_snapshot()
            return {"status": "ok", "data": snap.part(0)}
        except forget_registry.Unreadable:
            return {"status": "error", "message": "遗忘登记读不出来，先不给数据。", "data": {}}
        except Exception as exc:
            return {"status": "error", "message": str(exc)[:180], "data": {}}

    async def page_brain_node(self, args=None):
        """One star, when the owner opens it: ?id=<id>; a person's QQ number with &reveal=qq."""
        args = self._page_args(args)
        try:
            snap = await self._brain_snapshot()
            d = brain_graph.detail(snap, _arg(args, "id"), getattr(snap, "impressions", None),
                                   reveal_qq=_arg(args, "reveal") == "qq")
        except forget_registry.Unreadable:
            return {"status": "error", "message": "遗忘登记读不出来，先不给内容。", "data": {}}
        except Exception as exc:
            return {"status": "error", "message": str(exc)[:180], "data": {}}
        if d is None:
            return {"status": "error", "message": "没有这颗星了（也许刚被删掉）", "data": {}}
        return {"status": "ok", "data": d}

    async def page_brain_search(self, args=None):
        """?q=<words>: the ids of the stars whose words match, never the words."""
        args = self._page_args(args)
        try:
            snap = await self._brain_snapshot()
            return {"status": "ok", "data": {"ids": brain_graph.search(snap, _arg(args, "q"))}}
        except forget_registry.Unreadable:
            return {"status": "error", "message": "遗忘登记读不出来，先不搜。", "data": {"ids": []}}
        except Exception as exc:
            return {"status": "error", "message": str(exc)[:180], "data": {"ids": []}}
