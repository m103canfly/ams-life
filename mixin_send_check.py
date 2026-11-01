# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The last look at a reply before it is sent (send_check.py).

Private sources and names are checked for every reply. The reply is
looked at in on_llm_response (_look_at_reply): it leaks -> the model is asked once more
(_redo_reply, with the same request and one line more); it still leaks -> nothing is sent
and nothing of it is kept. on_agent_done (_settle_history) then makes the conversation
AstrBot saves hold what was sent: the last assistant message becomes exactly that, without
the model's thinking, and the event's copy of the thinking is cleared.

Only reason codes, exception types and counts are logged; the counts per day
(states/send_check.json) are for the panel.
"""
from __future__ import annotations

try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403

try:
    from . import adapter_astrbot_turn, send_check, mixin_discretion
except ImportError:
    import adapter_astrbot_turn
    import send_check
    import mixin_discretion

import ipaddress
from urllib.parse import urlparse


def _sessions(event, person):
    cache = getattr(event, "_ams_member_of", None)
    if not isinstance(cache, dict):
        cache = event._ams_member_of = {}
    person = str(person or "")
    if person not in cache:
        cache[person] = set()
        if person.isascii() and person.isdigit():
            try:
                data = json.loads((mixin_discretion.USER_DIR / (person + ".json")).read_text(encoding="utf-8"))
                rows = data.get("sessions") or []
                cache[person] = {discretion.place_of(s) for s in rows if isinstance(s, str)}
            except (OSError, ValueError, AttributeError, TypeError):
                pass
    return cache[person]


def _name_walls(plugin, event):
    cached = getattr(event, "_ams_name_walls", None)
    if cached is not None:
        return cached
    store = plugin._impression_store()
    names = {}
    for person, values in store._read(store.root / "names.json").items():
        if isinstance(values, list):
            for name in values:
                names.setdefault(str(name), set()).add(str(person))
    for place in store.places():
        for person, rec in store.load(place)["people"].items():
            if isinstance(rec, dict):
                for name in [rec.get("name")] + list(rec.get("aliases") or []):
                    if name:
                        names.setdefault(str(name), set()).add(str(person))
    here = plugin._here(event)
    speaker = str(plugin._speaker(event)[0] or "")
    present = set(plugin._present_people(event)) | {speaker}
    acceptable = {here}
    if here.startswith("group:"):
        group = here.split(":", 1)[1]
        for row in (plugin.config or {}).get("shared_groups", []):
            if isinstance(row, (list, tuple)) and group in row:
                acceptable.update("group:" + str(x) for x in row)
    elif here.startswith("private:"):
        acceptable = {x for x in _sessions(event, speaker) if x.startswith("group:")}
    blocked, unknown = [], 0
    for name, owners in names.items():
        name = name.strip()
        if len(name) < 2 or discretion.plain_word(name) or name in send_check.everyday_words.WORDS:
            continue
        if owners & present:
            continue
        sessions = [_sessions(event, person) for person in owners]
        if any(not places for places in sessions):
            unknown += 1
        elif not any(places & acceptable for places in sessions):
            blocked.append(name)
    if unknown:
        logger.info("[ams-life] send check: %d names have unknown places", unknown)
    event._ams_name_walls = blocked
    return blocked


def _local_embedding(plugin):
    conf = plugin._embedding_runtime_config() or {}
    try:
        host = urlparse(str(conf.get("base_url") or "")).hostname or ""
        return host.lower() == "localhost" or ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False

SEND_CHECK_PATH = STATE_DIR / "send_check.json"
_SEGMENT = re.compile(r"\n|；(?=（)")


class SendCheckMixin:
    # ------------------------------------------------------------------
    # what this reply may not bring up, noted while its prompt is built
    # ------------------------------------------------------------------
    @staticmethod
    def _check_note(event) -> dict:
        note = getattr(event, "_ams_check", None)
        if not isinstance(note, dict):
            note = {"forbidden": [], "allowed": "", "req": None, "sent": None}
            try:
                setattr(event, "_ams_check", note)
            except Exception:
                pass
        return note

    def _forbid(self, event, iid, text="", people=(), vec=None, private=True) -> None:
        """Something labelled "这里不能讲" in this reply's prompt: its words, and the names of
        who said it / was in it (not of whoever is talking to her or here)."""
        if event is None:
            return
        speaker = str(self._speaker(event)[0] or "")
        keep_out = {speaker} | set(self._present_people(event))
        names = [n for n in self._known_names([p for p in people if str(p) not in keep_out])
                 if n and not n.isdigit()]
        self._check_note(event)["forbidden"].append(
            {"id": str(iid), "text": str(text or ""), "private": private, "names": names, "vec": vec or None})

    def _forbid_names(self, event, iid, people=()) -> None:
        """Something labelled "不点名": only the names of the people in it."""
        self._forbid(event, iid, "", people, private=False)

    def _note_allowed(self, event, req, compact) -> None:
        """What this reply's prompt holds that may be said here: the block without the items
        labelled "这里不能讲", AstrBot's message, system prompt and history; and the request,
        for asking once more."""
        note = self._check_note(event)
        system = str(getattr(req, "system_prompt", "") or "")
        if compact:   # with no user parts the block is in the system prompt: only its "keep" counts
            system = system.replace(str(compact), "")
        parts = [system]
        for msg in getattr(req, "contexts", None) or []:
            if not isinstance(msg, dict) or msg.get("role") != "assistant":
                continue
            content = msg.get("content") if isinstance(msg, dict) else None
            if isinstance(content, str):
                parts.append(content)
            elif isinstance(content, list):
                parts.extend(str(p.get("text") or "") for p in content if isinstance(p, dict))
        note["allowed"] = "\n".join(parts)
        note["user_text"] = adapter_astrbot_turn.incoming_of(event).text
        note["req"] = req
        note["compact"] = str(compact or "")

    def _common_pieces(self) -> set:
        """send_check.common_pieces of all she keeps, worked out again when the library changes."""
        lib = self._read_library()
        entries = [e for e in lib.get("entries") or [] if isinstance(e, dict) and not e.get("deleted")]
        sig = (len(entries), max((float(e.get("ts", 0) or 0) for e in entries), default=0.0))
        cached = getattr(self, "_common_cache", None)
        if cached and cached[0] == sig:
            return cached[1]
        items = [(e.get("text"), e.get("sender_id") or e.get("role"), discretion.origin_of(e)["where"])
                 for e in entries]
        common = send_check.common_pieces(items)
        self._common_cache = (sig, common)
        return common

    # ------------------------------------------------------------------
    # the look, the second try, nothing sent
    # ------------------------------------------------------------------
    async def _check_reply(self, event, reply) -> dict:
        note = self._check_note(event)
        forbidden = list(note.get("forbidden") or [])
        names = _name_walls(self, event)
        if names:
            forbidden.append({"id": "names", "text": "", "private": False,
                              "names": names, "strict_names": True, "vec": None})
        if not forbidden or not str(reply or "").strip():
            return {"leak": False, "ids": [], "why": {}, "close": [], "top": 0.0}
        vec = None
        try:
            if not _local_embedding(self) or not any(item.get("text") or item.get("vec") for item in forbidden):
                return send_check.check(reply, forbidden, note.get("allowed", ""), user_text=note.get("user_text", ""))
            vec = await self._embed_text(str(reply))
            for item in forbidden:
                if item.get("vec") is None and item.get("text"):
                    cache = getattr(self, "_check_vecs", None)
                    if not isinstance(cache, dict):
                        cache = self._check_vecs = {}
                    if item["id"] not in cache:
                        cache[item["id"]] = await self._embed_text(item["text"]) or []
                    item["vec"] = cache[item["id"]] or None
        except Exception as exc:
            logger.warning("[ams-life] send check: no vectors (%s); local checks only", type(exc).__name__)
        return send_check.check(reply, forbidden, note.get("allowed", ""), reply_vec=vec, user_text=note.get("user_text", ""))

    async def _redo_reply(self, event):
        """Ask the chat model once more with the same request and one line more. Returns the
        new words, or None."""
        note = self._check_note(event)
        req = note.get("req")
        if req is None:
            return None
        provider = getattr(self, "_neutral_model", None)
        if provider is None:
            try:
                provider = self.context.get_using_provider(str(getattr(event, "unified_msg_origin", "") or ""))
            except Exception:
                provider = None
        if provider is None:
            return None
        system = getattr(req, "system_prompt", None)
        compact = note.get("compact", "")
        if compact and compact in str(system or ""):
            compact = ""   # the block went into the system prompt (no user parts): not twice
        prompt = "\n\n".join(x for x in (compact, str(getattr(req, "prompt", "") or ""), send_check.REDO_NOTE) if x)
        self._count_check("redo_calls")
        try:
            reply = await self._model(self._spending("redo", provider)).chat(
                prompt=prompt, messages=list(getattr(req, "contexts", None) or []), system=system,
                images=list(getattr(req, "image_urls", None) or []))
        except Exception as exc:
            logger.warning("[ams-life] send check: asking once more failed: %s", type(exc).__name__)
            return None
        tokens = sum(int(v or 0) for v in reply.usage.values())
        if tokens:
            self._count_check("redo_tokens", tokens)
        text = interpretation.strip_state_tags(reply.text).strip()
        return text or None

    async def _look_at_reply(self, event, response, reply) -> str:
        """The reply as it may be sent: as it is, said once more, or "" (nothing is sent: the
        event is stopped, so AstrBot neither sends nor saves it). Logs only reason codes."""
        result = await self._check_reply(event, reply)
        self._check_note(event)["top"] = result["top"]   # the highest cosine (for the replay)
        if result["close"]:
            self._count_check("close")
            logger.info("[ams-life] send check: close (%d)", len(result["close"]))
        if not result["leak"]:
            self._check_note(event).update(sent=reply, outcome="sent")
            return reply
        reasons = ",".join(sorted({why for reasons in result["why"].values() for why in reasons}))
        again = await self._redo_reply(event)
        if again:
            second = await self._check_reply(event, again)
            if not second["leak"]:
                self._count_check("redone")
                logger.info("[ams-life] send check: redone (%s)", reasons)
                self._set_reply(response, again)
                self._check_note(event).update(sent=again, outcome="redone")
                return again
        self._count_check("held")
        logger.info("[ams-life] send check: held back (%s)", reasons)
        self._check_note(event).update(sent="", outcome="held")
        try:
            event.stop_event()
        except Exception:
            pass
        self._set_reply(response, "")
        return ""

    def _check_failed(self, event, exc, response) -> str:
        """The look itself failed: held back as if it leaked (not sent, nothing kept)."""
        self._count_check("failed")
        logger.warning("[ams-life] send check: failed (%s), held back", type(exc).__name__)
        self._check_note(event).update(sent="", outcome="failed")
        try:
            event.stop_event()
        except Exception:
            pass
        self._set_reply(response, "")
        return ""

    @staticmethod
    def _set_reply(response, text) -> None:
        """Her words replaced, through the reply handle (AstrBotReply.set_text keeps the old body)."""
        adapter_astrbot_turn.reply_handle(response).set_text(text)

    def _settle_history(self, event, run_context) -> None:
        """on_agent_done: what AstrBot saves of this turn is what was sent. The last assistant
        message becomes exactly the words sent, without the model's thinking; the event's copy
        of the thinking is cleared (so it is never put into what is sent either)."""
        try:
            if hasattr(event, "set_extra"):
                event.set_extra("_llm_reasoning_content", None)
        except Exception:
            pass
        sent = self._check_note(event).get("sent")
        messages = getattr(run_context, "messages", None)
        if not isinstance(messages, list):
            return
        last = next((m for m in reversed(messages) if getattr(m, "role", None) == "assistant"), None)
        if last is None:
            return
        content = getattr(last, "content", None)
        try:
            if isinstance(content, list):
                parts = [p for p in content if getattr(p, "type", "") != "think"]
                texts = [p for p in parts if getattr(p, "type", "") == "text"]
                if sent is not None and texts:
                    texts[0].text = sent
                    parts = [p for p in parts if p is texts[0] or getattr(p, "type", "") != "text"]
                elif sent is not None:
                    last.content = sent
                    return
                last.content = parts
            elif sent is not None and isinstance(content, str):
                last.content = sent
        except Exception as exc:
            logger.warning("[ams-life] send check: history not settled: %s", type(exc).__name__)

    # ------------------------------------------------------------------
    # counts per day, for the panel (numbers only)
    # ------------------------------------------------------------------
    def _count_check(self, what, n=1) -> None:
        try:
            day = time.strftime("%Y-%m-%d")
            data = json.loads(SEND_CHECK_PATH.read_text(encoding="utf-8")) if SEND_CHECK_PATH.exists() else {}
            if not isinstance(data, dict):
                data = {}
            today = data.setdefault(day, {})
            today[what] = int(today.get(what, 0) or 0) + int(n)
            for old in sorted(data)[:-30]:   # a month is enough
                data.pop(old, None)
            STATE_DIR.mkdir(parents=True, exist_ok=True)
            tmp = SEND_CHECK_PATH.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            atomic_file.replace(tmp, SEND_CHECK_PATH)
        except Exception as exc:
            logger.warning("[ams-life] send check count failed: %s", type(exc).__name__)

    def _check_counts_today(self) -> dict:
        try:
            data = json.loads(SEND_CHECK_PATH.read_text(encoding="utf-8")) if SEND_CHECK_PATH.exists() else {}
            today = (data or {}).get(time.strftime("%Y-%m-%d")) or {}
        except Exception:
            today = {}
        return {k: int(today.get(k, 0) or 0) for k in ("redone", "held", "close", "failed", "redo_calls")}
