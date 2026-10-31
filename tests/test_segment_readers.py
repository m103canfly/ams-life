# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Compare segment readers with their frozen component readers."""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401
import adapter_astrbot
import harness
import main
import turn
import mixin_browse, mixin_discretion, mixin_events, mixin_media, mixin_phone, mixin_selfie
from astrbot.api.message_components import At, Face, Image, Plain, Record, Reply

# mixin_browse.py at 82b5412: lines 331, 345.
OldBrowse_source = r'''
class OldBrowse:
    @staticmethod
    def _message_words(event) -> str:
        """The words of this message and of the one it quotes."""
        parts = [adapter_astrbot_turn.incoming_of(event).text]
        try:
            for comp in event.get_messages() or []:
                for x in [comp] + list(getattr(comp, "chain", None) or []):
                    for attr in ("text", "message_str"):
                        v = getattr(x, attr, None)
                        if isinstance(v, str):
                            parts.append(v)
        except Exception:
            pass
        return "\n".join(parts)

'''
exec(OldBrowse_source, vars(mixin_browse))
OldBrowse = mixin_browse.OldBrowse

# mixin_discretion.py at 82b5412: lines 383, 424.
OldDiscretion_source = r'''
class OldDiscretion:
    def _gone_remover(self, event=None):
        """_without_gone with what it needs looked up once (for many texts at a time)."""
        ats = []
        if event is not None:
            self._note_her(event)
            try:  # the message's own @ parts: their numbers are known, their "@名字(号码)" exact
                for comp in event.get_messages() or []:
                    if type(comp).__name__ == "At":
                        qq = str(getattr(comp, "qq", "") or "")
                        if qq.isdigit():
                            ats.append((str(getattr(comp, "name", "") or "").strip(), qq))
            except Exception:
                pass
        gone = self._gone_people()
        try:   # a deleted person's number, and the ids of messages the registry rules out
            numbers = gone | set(self._registry_sets()[1])
        except Exception:
            numbers = set(gone)
        her = set(getattr(self, "_her_ids", None) or ())
        seen = getattr(self, "_gone_names", None)
        if not isinstance(seen, dict):
            seen = self._gone_names = {}
        gone_names = {p: set(self._known_names([p])) for p in gone}

        def scrub(text):
            text = str(text or "")
            if not text:
                return text
            for name, qq in discretion.at_names(text):
                if qq in gone and name:
                    seen.setdefault(qq, set()).add(name)
            out = discretion.drop_gone(text, gone, her, HER_NAME, numbers, ats)
            hits = self._gone_names_in(text)   # names of people the owner deleted
            for name, qq in hits.items():
                seen.setdefault(qq, set()).add(name)
            names = set(hits)
            if gone:
                names |= {n for p in gone for n in gone_names[p] | seen.get(p, set()) if not str(n).isdigit()}
            if names:
                out = discretion.anonymize(out, names, to=discretion.SOMEBODY)
            return out
        return scrub
'''
exec(OldDiscretion_source, vars(mixin_discretion))
OldDiscretion = mixin_discretion.OldDiscretion

# mixin_events.py at 82b5412: lines 1695, 1711.
OldEvents_source = r'''
class OldEvents:
    def _attachments_from_messages(self, event) -> list:
        out = []
        try:
            for m in event.get_messages() or []:
                if isinstance(m, Image):
                    ref = str(getattr(m, "url", "") or getattr(m, "file", "") or getattr(m, "path", "") or "").strip()
                    if ref:
                        out.append({"type": "image", "ref": ref[:500]})
                elif isinstance(m, Record):
                    ref = str(getattr(m, "url", "") or getattr(m, "file", "") or "").strip()
                    if ref:
                        out.append({"type": "voice", "ref": ref[:500]})
        except Exception:
            pass
        return out

'''
exec(OldEvents_source, vars(mixin_events))
OldEvents = mixin_events.OldEvents

# mixin_media.py at 82b5412: lines 35, 68, 70, 107, 112, 138, 264, 290.
OldMedia_source = r'''
class OldMedia:
    def _text_from_components(self, event) -> str:
        parts = []
        try:
            for msg in event.get_messages() or []:
                text = getattr(msg, "text", None)
                if isinstance(text, str):
                    parts.append(text)
        except Exception:
            pass
        return " ".join(parts)

    def _image_refs(self, event) -> list:
        if not getattr(self, "image_recognition_enabled", True):
            return []
        try:
            if not event.is_private_chat() and not self._addresses_her(event):
                return []
            refs = []
            for msg in event.get_messages() or []:
                if isinstance(msg, Image):
                    refs.append(self._image_ref(msg))
                elif isinstance(msg, Reply):
                    sender = str(getattr(msg, 'sender_id', '') or '').strip()
                    mid = str(getattr(msg, 'id', '') or '').strip()
                    try:
                        allowed = self._may_keep([sender] if sender else [], self._here(event), None,
                                                 [mid] if mid else [])
                    except Exception:
                        allowed = False
                    if allowed:
                        refs.extend(self._image_ref(child) for child in (getattr(msg, "chain", None) or []))
            return list(dict.fromkeys(ref for ref in refs if ref))
        except Exception:
            return []
    def _remember_images(self, event):
        now = time.time()
        state = getattr(self, '_recent_images', None)
        if state is None:
            state = self._recent_images = {}
        for place in list(state):
            state[place] = [row for row in state[place] if 0 <= now - row['ts'] <= RECENT_IMAGE_SECONDS]
            if not state[place]:
                del state[place]
        here = self._here(event)
        sender = str(self._speaker(event)[0] or '')
        self_id = str(getattr(getattr(event, 'message_obj', None), 'self_id', '') or '')
        if not here or not sender or sender == self_id or self._job_stale():
            return
        ids = self._source_ids(event)
        try:
            if not self._may_keep([sender], here, now, ids):
                return
        except Exception:
            return
        try:
            messages = event.get_messages() or []
        except Exception:
            return
        rows = state.setdefault(here, [])
        for msg in messages:
            ref = self._image_ref(msg)
            if ref and not any(row['ref'] == ref and row['id'] == (ids[0] if ids else '') for row in rows):
                rows.append({'ref': ref, 'sender': sender, 'id': ids[0] if ids else '', 'ts': now, 'seen': False})
        del rows[:-RECENT_IMAGE_LIMIT]
        if not rows:
            state.pop(here, None)

    async def _quoted_image_refs(self, event):
        refs = []
        for msg in getattr(event, 'get_messages', lambda: [])() or []:
            if not isinstance(msg, Reply) or any(self._image_ref(c) for c in (getattr(msg, 'chain', None) or [])):
                continue
            mid = getattr(msg, 'id', None) or getattr(msg, 'message_id', None)
            if not mid:
                continue
            try:
                result = await self._messenger(event).call('get_msg', message_id=str(mid))
                data = result.get('data', result) if isinstance(result, dict) else {}
                parts = data.get('message', []) if isinstance(data, dict) else []
                sender_data = data.get('sender') if isinstance(data, dict) else None
                sender = str(sender_data.get('user_id') or '').strip() if isinstance(sender_data, dict) else ''
                if not self._may_keep([sender] if sender else [], self._here(event), None, [str(mid)]):
                    continue
                for part in parts if isinstance(parts, list) else []:
                    if isinstance(part, dict) and part.get('type') == 'image' and isinstance(part.get('data'), dict):
                        image = part['data']
                        ref = str(image.get('url') or image.get('file') or image.get('path') or '').strip()
                        if ref:
                            refs.append(ref)
            except Exception:
                continue
        return refs

    async def _voice_context(self, event) -> str:
        if not getattr(self, "voice_transcription_enabled", True):
            return ""
        try:
            provider = await self.context.get_using_stt_provider_async(
                getattr(event, "unified_msg_origin", "") or "")
            if provider is None:
                return ""
            texts = []
            for m in event.get_messages() or []:
                if not isinstance(m, Record):
                    continue
                ref = str(getattr(m, "url", "") or getattr(m, "file", "") or getattr(m, "path", "") or "").strip()
                if not ref:
                    continue
                try:
                    txt = await provider.get_text(ref)
                    if str(txt or "").strip():
                        texts.append(str(txt).strip()[:300])
                except Exception as exc:
                    logger.warning("[biocore] voice transcribe failed: %s", exc)
            return "；".join(texts)[:600]
        except Exception as exc:
            logger.warning("[biocore] voice context failed: %s", exc)
            return ""

'''
exec(OldMedia_source, vars(mixin_media))
OldMedia = mixin_media.OldMedia

# mixin_phone.py at 82b5412: lines 276, 285, 287, 318.
OldPhone_source = r'''
class OldPhone:
    @staticmethod
    def _reply_to(event) -> str:
        """The id of the message this one quotes, if any. Kept apart: forgetting never reads it."""
        try:
            for comp in event.get_messages() or []:
                if type(comp).__name__ == "Reply":
                    return str(getattr(comp, "id", "") or "")[:80]
        except Exception:
            pass
        return ""
    def _message_text(self, event) -> str:
        """The message as text; pictures, stickers and the like become a short placeholder.
        As AstrBot writes it (_without_gone): an @ is "@名字(号码)" ("@(号码)" with no name),
        her own name for an @ of her, "@某人" for someone deleted."""
        parts = []
        self._note_her(event)
        her, gone = getattr(self, "_her_ids", None) or set(), self._gone_people()
        try:
            for comp in event.get_messages() or []:
                kind = type(comp).__name__
                if kind == "Plain":
                    parts.append(str(getattr(comp, "text", "") or ""))
                elif kind == "At":
                    qq, name = str(getattr(comp, "qq", "") or ""), str(getattr(comp, "name", "") or "").strip()
                    if qq in gone and name:
                        self.__dict__.setdefault("_gone_names", {}).setdefault(qq, set()).add(name)
                    elif qq and qq not in her:
                        self._note_at(qq, name)   # someone @'d who may never write: his number is known
                    parts.append("@" + (HER_NAME if qq in her else discretion.SOMEBODY if qq in gone
                                        else "%s(%s)" % (name, qq) if qq else name or discretion.SOMEBODY))
                elif kind == "AtAll":
                    parts.append("@全体成员")
                elif kind == "Reply":
                    continue
                else:
                    parts.append(_PART_NAMES.get(kind, "[消息]"))
        except Exception:
            parts = []
        text = "".join(parts).strip()
        if not text:
            text = adapter_astrbot_turn.incoming_of(event).text.strip()
        return self._without_gone(text, event)
'''
exec(OldPhone_source, vars(mixin_phone))
OldPhone = mixin_phone.OldPhone

# mixin_selfie.py at 82b5412: lines 168, 196.
OldSelfie_source = r'''
class OldSelfie:
    def _phone_context(self, event):
        try:
            familiar = self._familiarity(self._speaker(event)[0])
            relation = "很熟" if familiar >= 0.7 else "认识" if familiar >= 0.3 else "不熟"
        except Exception:
            relation = "不明"
        try:
            state = self._core(event).snapshot()
            mood = float(state.get("v", 0))
            energy = float(state.get("energy", 0.5))
            mood_text = "心情好" if mood > 0.15 else "心情低落" if mood < -0.15 else "心情平静"
            energy_text = "困倦" if energy <= 0.35 else "精神尚可"
        except Exception:
            mood_text, energy_text = "心情未知", "困倦程度未知"
        try:
            parts = event.get_messages() or []
            voice = any(isinstance(x, Record) for x in parts)
            photo = any(isinstance(x, Image) for x in parts)
            private = event.is_private_chat()
        except Exception:
            voice, photo, private = False, False, False
        counts = self._phone_counts()
        last = counts.get("last", 0)
        elapsed = "没有记录" if not last else "%d 分钟前" % max(0, int((time.time() - last) / 60))
        return ("现在%s，%s，%s；%s，跟对方%s。今天自拍%d张、随手拍%d张、截图%d张、语音%d条，最近一次%s。"
                "对方本轮%s语音、%s照片。" % (time.strftime("%H:%M"), mood_text, energy_text,
                "私聊" if private else "群聊", relation, counts.get("selfie", 0), counts.get("snap", 0),
                counts.get("screenshot", 0), counts.get("voice", 0), elapsed,
                "发了" if voice else "没发", "发了" if photo else "没发"))
'''
exec(OldSelfie_source, vars(mixin_selfie))
OldSelfie = mixin_selfie.OldSelfie

# mixin_phone.py 87-138 at 82b5412.
old_forward_source = r'''
async def old_expand_forward(plugin, event):
    """Fetch only on a reply; retain the enclosing message's origin in its window."""
    rendered = []
    try:
        for comp in event.get_messages() or []:
            if type(comp).__name__ not in ("Forward", "Nodes", "Node"):
                continue
            fid = getattr(comp, "id", None) or getattr(comp, "res_id", None)
            if not fid:
                continue
            result = await plugin._messenger(event).call("get_forward_msg", id=str(fid))
            if not isinstance(result, dict):
                continue
            data = result.get("data", result)
            messages = data.get("messages", []) if isinstance(data, dict) else []
            for node in messages[:FORWARD_MAX] if isinstance(messages, list) else []:
                if not isinstance(node, dict):
                    continue
                content = node.get("message", node.get("content", []))
                if isinstance(content, str):
                    body = re.sub(r"\[CQ:[^\]]*\]", "", content)
                elif isinstance(content, list):
                    body = "".join(str((part.get("data") or {}).get("text") or "")
                                   for part in content if isinstance(part, dict)
                                   and part.get("type") == "text" and isinstance(part.get("data"), dict))
                else:
                    body = ""
                sender = node.get("sender") or {}
                name = str(sender.get("nickname") or sender.get("card") or "某人") if isinstance(sender, dict) else "某人"
                name = re.sub(r"[\r\n：:]|\d{5,}", " ", name).strip()[:40] or "某人"
                body = re.sub(r"\d{5,}", "某人", plugin._for_model(body, event))
                if body.strip():
                    rendered.append(name + "：" + body[:FORWARD_LINE_CHARS])
            if rendered:
                break
    except Exception:
        return ""
    if not rendered:
        return ""
    expanded = "（转发来的聊天记录，出处与本消息相同）\n" + "\n".join(_original(x) for x in rendered)
    here, mid = plugin._here(event), plugin._message_id(event)
    try:
        if here and mid and not plugin._job_stale():
            win = plugin._read_window(here)
            for line in reversed(win["recent"]):
                if line.get("role") == "user" and str(line.get("msg_id") or "") == mid:
                    line["forward_text"] = expanded
                    plugin._write_window(here, win)
                    break
    except Exception:
        pass
    return expanded
'''
exec(old_forward_source, vars(mixin_phone))
old_expand_forward = mixin_phone.old_expand_forward


class AtAll: pass
class Forward:
    def __init__(self, id): self.id = id
class Node:
    id = 0
class Nodes: pass
class Video: pass
class File: pass
class Sticker: pass


def reply(id='', sender_id='', chain=None, text='', message_str=''):
    return Reply(id=id, sender_id=sender_id, chain=chain or [], text=text, message_str=message_str)


def image(url='', file='', path=''):
    return Image(url=url, file=file, path=path)


def record(url='', file='', path=''):
    return Record(url=url, file=file, path=path)


def make_event():
    ev = harness.FakeEvent('platform', sender='10001', group='900001', self_id='20002')
    parts = [Plain('words'), At(qq='10003', name='A'), At(qq='abc', name='B'),
             At(qq='20002', name='Me'), At(qq='10005', name='Gone'),
             At(qq='all', name='全体成员'), AtAll(),
             reply('quote', '10003', [Plain('inside'), image(path='quoted'),
                   reply('nested', '10001', [Plain('deep')], 'nested text', 'nested message')],
                   'reply text', 'reply message'), reply('missing', '10003'),
             image(url='url'), image(file='file'), image(path='path'), record(path='voice'),
             Face(id='1'), Forward('forward'), Node(), Nodes(), Video(), File(), Sticker()]
    ev.get_messages = lambda: parts
    return ev


def fake():
    p = MagicMock()
    p._her_ids = {'20002'}
    p._gone_names = {}
    p._gone_people.return_value = {'10005'}
    p._known_names.return_value = []
    p._gone_names_in.return_value = {}
    p._registry_sets.return_value = (set(), set())
    p._here.return_value = 'group:900001'
    p._speaker.return_value = ('10001', 'A')
    p._source_ids.return_value = ['message']
    p._job_stale.return_value = False
    p._may_keep.return_value = True
    p._addresses_her.return_value = True
    p._without_gone.side_effect = lambda text, event: text
    p._image_ref.side_effect = mixin_media.MediaMixin._image_ref
    p.image_recognition_enabled = True
    p.voice_transcription_enabled = True
    p._recent_images = {}
    p._familiarity.return_value = 0.5
    p._core.return_value.snapshot.return_value = {'v': 0, 'energy': 0.5}
    p._phone_counts.return_value = {}
    p.context.get_using_stt_provider_async = AsyncMock()
    p.context.get_using_stt_provider_async.return_value.get_text = AsyncMock(return_value='heard')
    p._messenger.return_value.call = AsyncMock(return_value={'data': {'sender': {'user_id': '10003'}, 'message': []}})
    return p


class SegmentReaders(unittest.IsolatedAsyncioTestCase):
    async def test_old_readers_match_segments_and_effects(self):
        ev = make_event()
        old, new = fake(), fake()
        self.assertEqual(OldBrowse._message_words(ev), mixin_browse.BrowseMixin._message_words(ev))
        for text in ['@A(10003) @Gone(10005)', '@B(abc)']:
            self.assertEqual(OldDiscretion._gone_remover(old, ev)(text),
                             mixin_discretion.DiscretionMixin._gone_remover(new, ev)(text))
        self.assertEqual(OldEvents._attachments_from_messages(old, ev), mixin_events.EventsMixin._attachments_from_messages(new, ev))
        self.assertEqual(OldMedia._text_from_components(old, ev), mixin_media.MediaMixin._text_from_components(new, ev))
        for allowed in (True, False):
            old._may_keep.return_value = new._may_keep.return_value = allowed
            self.assertEqual(OldMedia._image_refs(old, ev), mixin_media.MediaMixin._image_refs(new, ev))
            self.assertEqual(old._may_keep.call_args_list, new._may_keep.call_args_list)
            old._may_keep.reset_mock(); new._may_keep.reset_mock()
        old._may_keep.return_value = new._may_keep.return_value = True
        OldMedia._remember_images(old, ev); mixin_media.MediaMixin._remember_images(new, ev)
        self.assertEqual(old._recent_images, new._recent_images)
        self.assertEqual(await OldMedia._quoted_image_refs(old, ev), await mixin_media.MediaMixin._quoted_image_refs(new, ev))
        self.assertEqual(old._messenger.return_value.call.call_args_list, new._messenger.return_value.call.call_args_list)
        self.assertEqual(await OldMedia._voice_context(old, ev), await mixin_media.MediaMixin._voice_context(new, ev))
        self.assertEqual(old.context.get_using_stt_provider_async.return_value.get_text.call_args_list,
                         new.context.get_using_stt_provider_async.return_value.get_text.call_args_list)
        old._messenger.return_value.call.reset_mock(); new._messenger.return_value.call.reset_mock()
        self.assertEqual(await old_expand_forward(old, ev), await mixin_phone._expand_forward(new, ev))
        self.assertEqual(old._messenger.return_value.call.call_args_list, new._messenger.return_value.call.call_args_list)
        self.assertEqual(OldPhone._reply_to(ev), mixin_phone.PhoneMixin._reply_to(ev))
        self.assertEqual(OldPhone._message_text(old, ev), mixin_phone.PhoneMixin._message_text(new, ev))
        self.assertEqual(old._note_at.call_args_list, new._note_at.call_args_list)
        self.assertEqual(old._gone_names, new._gone_names)
        self.assertEqual(OldSelfie._phone_context(old, ev), mixin_selfie.SelfieMixin._phone_context(new, ev))

    async def test_turn_event_readers(self):
        ev = make_event()
        wrapped = turn.TurnEvent(adapter_astrbot.from_astrbot(ev))
        old, new = fake(), fake()
        self.assertEqual(OldBrowse._message_words(ev), mixin_browse.BrowseMixin._message_words(wrapped))
        self.assertEqual(OldDiscretion._gone_remover(old, ev)('@Gone(10005)'), mixin_discretion.DiscretionMixin._gone_remover(new, wrapped)('@Gone(10005)'))
        self.assertEqual(OldEvents._attachments_from_messages(old, ev), mixin_events.EventsMixin._attachments_from_messages(new, wrapped))
        self.assertEqual(OldMedia._text_from_components(old, ev), mixin_media.MediaMixin._text_from_components(new, wrapped))
        self.assertEqual(OldPhone._reply_to(ev), mixin_phone.PhoneMixin._reply_to(wrapped))
        self.assertEqual(OldPhone._message_text(old, ev), mixin_phone.PhoneMixin._message_text(new, wrapped))
        self.assertEqual(old._note_at.call_args_list, new._note_at.call_args_list)

    def test_mixin_sources_do_not_read_components(self):
        root = Path(__file__).resolve().parent.parent
        for name in ('browse', 'discretion', 'events', 'media', 'phone', 'selfie'):
            self.assertNotIn('get_messages(', (root / ('mixin_' + name + '.py')).read_text(encoding='utf-8'))
