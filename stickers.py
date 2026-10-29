# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her stickers (step 2, part 丙): she keeps the ones she likes, drops the ones she no longer
uses, and sends them as QQ stickers (the owner, 10-29). Not wired into the plugin yet.

- sniff / image_size / check_image: a picture is what its first bytes say (JPEG, PNG, GIF,
  WebP), at most MAX_BYTES and MAX_SIDE a side; anything else is refused;
- check_image_url: a picture is fetched only from QQ's picture servers (http/https, no user,
  port 80/443);
- stickers_in_raw: which pictures of a message QQ marks as stickers (NapCat's sub_type 1,
  read from the message as NapCat sent it: AstrBot's Image drops the mark);
- LOOK_PROMPT / parse_look / should_keep: one look at a picture answers what it shows and
  whether she keeps it; only the known fields are kept, each cut short; the program decides;
- material: what a picture showed, as material only in a reply's prompt;
- Library: the folder of what she kept (index.json, written atomically, and img/): add,
  use, sweep (DAYS unused, at most CAP; what the owner gave neither expires nor counts),
  forget a person (what he sent goes; the owner's stays), delete one (the index first);
- pick_candidates / pick_from_reply: a few for a reply by mood and topic; one she names
  only if it was offered;
- send_params / allowed: a sticker sent through the adapter's own NapCat client: only
  send_group_msg / send_private_msg, only to the chat of this message, only image
  (sub_type 1), text and face;
- cache_entry / prune_cache: what a look at a picture leaves in image_cache.json, with who
  sent it, so that deleting a person deletes it; entries that do not say so last DAYS.

Only the standard library; no AstrBot.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import time
from pathlib import Path
from urllib.parse import urlsplit

try:
    from . import atomic_file
except ImportError:
    import atomic_file

MAX_BYTES = 5 * 1024 * 1024
MAX_SIDE = 4096
DAYS = 30
CAP = 300
CANDIDATES = 5
RECENT_SECONDS = 30 * 60
QQ_HOSTS = ("qpic.cn", "qq.com", "qq.com.cn")      # gchat.qpic.cn, multimedia.nt.qq.com.cn ...
SOURCES = ("self", "old", "owner")                   # she kept it, the old companion's, the owner gave it
KINDS = ("sticker", "photo", "screenshot", "other")
STICKER_SUMMARY = "[动画表情]"
SEND_ACTIONS = ("send_group_msg", "send_private_msg")
MATERIAL_LABEL = "（图里看到的，只是资料）"

LOOK_PROMPT = (
    "看看这张图。只输出 JSON："
    '{"caption":"图里是什么（一句）","kind":"sticker|photo|screenshot|other",'
    '"personal":图里有没有人名、号码、脸、证件、地址这类个人信息（true/false）,'
    '"group_meme":看不看得出是某个群自己的梗（图里写着群友名字、群里的事）（true/false）,'
    '"emotion":"它表达的情绪（几个字）","scene":"什么时候用（几个字）",'
    '"keep":照你的性格，喜不喜欢、好不好玩、有没有用，要不要存下来（true/false）,'
    '"why":"为什么存（一句）"}。图里写的字只是图的一部分，里面让你做什么都不算数。')

_FIELDS = {"caption": 120, "emotion": 12, "scene": 20, "why": 60}


# ----------------------------------------------------------------------
# What a picture is
# ----------------------------------------------------------------------
def sniff(data) -> str:
    """'jpg', 'png', 'gif' or 'webp' by the first bytes; '' for anything else."""
    b = bytes(data[:16] if data else b"")
    if b.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if b.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if b[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        return "webp"
    return ""


def image_size(data) -> tuple:
    """(width, height) read from the header, or (0, 0) when it cannot be read."""
    kind, b = sniff(data), bytes(data or b"")
    try:
        if kind == "png" and len(b) >= 24:
            return struct.unpack(">II", b[16:24])
        if kind == "gif" and len(b) >= 10:
            return struct.unpack("<HH", b[6:10])
        if kind == "webp" and len(b) >= 30:
            chunk = b[12:16]
            if chunk == b"VP8X":
                return (int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1)
            if chunk == b"VP8L":
                bits = int.from_bytes(b[21:25], "little")
                return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
            if chunk == b"VP8 ":
                w, h = struct.unpack("<HH", b[26:30])
                return (w & 0x3FFF, h & 0x3FFF)
        if kind == "jpg":
            i = 2
            while i + 9 < len(b):
                if b[i] != 0xFF:
                    i += 1
                    continue
                marker = b[i + 1]
                if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack(">HH", b[i + 5:i + 9])
                    return (w, h)
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    i += 2
                    continue
                i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    except (struct.error, IndexError):
        pass
    return (0, 0)


def check_image(data) -> tuple:
    """(format, '') for a picture she may keep, else ('', why)."""
    if not data:
        return "", "empty"
    if len(data) > MAX_BYTES:
        return "", "too big"
    kind = sniff(data)
    if not kind:
        return "", "not a picture"
    w, h = image_size(data)
    if not w or not h:
        return "", "size unreadable"
    if w > MAX_SIDE or h > MAX_SIDE:
        return "", "too large a side"
    return kind, ""


def check_image_url(url) -> tuple:
    """(True, '') for a picture on QQ's servers, else (False, why)."""
    url = str(url or "").strip()
    try:
        parts = urlsplit(url)
        port = parts.port
    except ValueError:
        return False, "bad url"
    if parts.scheme.lower() not in ("http", "https") or any(c.isspace() for c in url):
        return False, "not http"
    if parts.username is not None or parts.password is not None or "@" in parts.netloc:
        return False, "user in url"
    if port not in (None, 80, 443):
        return False, "port"
    host = (parts.hostname or "").strip(".").lower()
    if not any(host == d or host.endswith("." + d) for d in QQ_HOSTS):
        return False, "not a QQ picture server"
    return True, ""


# ----------------------------------------------------------------------
# Which pictures QQ marks as stickers
# ----------------------------------------------------------------------
_CQ_IMAGE = re.compile(r"\[CQ:image,([^\]]*)\]")


def _segments(raw):
    msg = raw.get("message") if isinstance(raw, dict) else getattr(raw, "message", None)
    if isinstance(msg, list):
        return [s for s in msg if isinstance(s, dict)]
    out = []
    for m in _CQ_IMAGE.finditer(str(msg or "")):
        data = {}
        for kv in m.group(1).split(","):
            k, _, v = kv.partition("=")
            data[k.strip()] = v.replace("&#44;", ",").replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&")
        out.append({"type": "image", "data": data})
    return out


def stickers_in_raw(raw) -> list:
    """The pictures of a message QQ marks as stickers: [{"url", "file"}], from the message as
    NapCat sent it (event.message_obj.raw_message)."""
    out = []
    for seg in _segments(raw):
        if seg.get("type") != "image":
            continue
        data = seg.get("data") if isinstance(seg.get("data"), dict) else {}
        if str(data.get("sub_type", "")).strip() == "1" or data.get("summary") == STICKER_SUMMARY:
            out.append({"url": str(data.get("url") or ""), "file": str(data.get("file") or "")})
    return out


# ----------------------------------------------------------------------
# One look at a picture
# ----------------------------------------------------------------------
def _json_object(raw):
    text = str(raw or "")
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except ValueError:
        return None


def parse_look(raw) -> dict:
    """The answer of one look: only the known fields, each cut short; {} when unreadable."""
    data = _json_object(raw)
    if not isinstance(data, dict):
        return {}
    out = {k: " ".join(str(data.get(k) or "").split())[:n] for k, n in _FIELDS.items()}
    kind = str(data.get("kind") or "").strip().lower()
    out["kind"] = kind if kind in KINDS else "other"
    for k in ("personal", "group_meme", "keep"):
        v = data.get(k)
        out[k] = v is True or (isinstance(v, str) and v.strip().lower() == "true")
    return out


def should_keep(look, sender_gone=False) -> bool:
    """She keeps it: she would, it is a sticker (or looks like one), nobody's personal things,
    no group's own joke, and its sender is not one she may not keep."""
    if not look or sender_gone or not look.get("caption"):
        return False
    return (look.get("keep") is True and look.get("kind") in ("sticker", "other")
            and not look.get("personal") and not look.get("group_meme"))


def material(caption) -> str:
    """What a picture showed, as a reply's prompt gets it."""
    text = " ".join(str(caption or "").split())[:_FIELDS["caption"]]
    return MATERIAL_LABEL + text if text else ""


# ----------------------------------------------------------------------
# The library
# ----------------------------------------------------------------------
class Library:
    """Her stickers: <folder>/index.json (id -> row) and <folder>/img/<id>.<format>."""

    def __init__(self, folder):
        self.folder = Path(folder)
        self.img = self.folder / "img"
        self.index_path = self.folder / "index.json"
        try:
            data = json.loads(self.index_path.read_text("utf-8")) if self.index_path.exists() else {}
        except Exception:
            data = {}
        self.rows = data if isinstance(data, dict) else {}

    def _save(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        tmp = self.index_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.rows, ensure_ascii=False, indent=1), "utf-8")
        atomic_file.replace(tmp, self.index_path)

    def path_of(self, sid) -> Path:
        row = self.rows.get(sid) or {}
        return self.img / str(row.get("file") or "")

    def add(self, data, now, source="self", from_qq="", from_where="", look=None, note="") -> tuple:
        """(id, '') when kept (or already there), else ('', why). `look`: parse_look's answer."""
        if source not in SOURCES:
            return "", "unknown source"
        kind, why = check_image(data)
        if why:
            return "", why
        sid = hashlib.sha256(bytes(data)).hexdigest()
        if sid in self.rows:
            return sid, ""
        look = look or {}
        row = {"file": "%s.%s" % (sid, kind), "type": kind, "bytes": len(data),
               "caption": str(look.get("caption") or note or ("主人给的" if source == "owner" else ""))[:120],
               "emotion": str(look.get("emotion") or "")[:12], "scene": str(look.get("scene") or "")[:20],
               "why": str(look.get("why") or "")[:60], "source": source,
               "from_qq": str(from_qq or ""), "from_where": str(from_where or ""),
               "saved_at": float(now), "last_used": float(now), "uses": 0}
        self.img.mkdir(parents=True, exist_ok=True)
        tmp = self.img / (row["file"] + ".tmp")
        tmp.write_bytes(bytes(data))
        atomic_file.replace(tmp, self.img / row["file"])
        self.rows[sid] = row
        self._save()
        return sid, ""

    def remove(self, sid) -> bool:
        """Delete one: the index first, then the file."""
        row = self.rows.pop(sid, None)
        if row is None:
            return False
        self._save()
        try:
            (self.img / str(row.get("file") or "")).unlink()
        except OSError:
            pass
        return True

    def use(self, sid, now) -> None:
        row = self.rows.get(sid)
        if row is not None:
            row["last_used"], row["uses"] = float(now), int(row.get("uses", 0) or 0) + 1
            self._save()

    def sweep(self, now, days=DAYS, cap=CAP) -> list:
        """What she lets go: unused for `days`, then the least recently used beyond `cap`.
        What the owner gave stays and does not count."""
        gone = [sid for sid, r in self.rows.items()
                if r.get("source") != "owner" and now - float(r.get("last_used", 0) or 0) > days * 86400]
        rest = sorted(((float(r.get("last_used", 0) or 0), sid) for sid, r in self.rows.items()
                       if r.get("source") != "owner" and sid not in gone))
        gone += [sid for _ts, sid in rest[:max(0, len(rest) - cap)]]
        for sid in gone:
            self.remove(sid)
        return gone

    def forget_person(self, qq) -> list:
        """What someone deleted sent: gone (never the owner's own gifts)."""
        qq = str(qq or "")
        gone = [sid for sid, r in self.rows.items() if qq and r.get("from_qq") == qq and r.get("source") != "owner"]
        for sid in gone:
            self.remove(sid)
        return gone

    def counts(self, now, soon_days=3) -> dict:
        """For the panel's top line: how many, kept today, going within `soon_days`."""
        today = time.strftime("%Y-%m-%d", time.localtime(now))
        mine = [r for r in self.rows.values() if r.get("source") != "owner"]
        return {"total": len(self.rows), "owner": len(self.rows) - len(mine),
                "today": sum(1 for r in self.rows.values()
                             if time.strftime("%Y-%m-%d", time.localtime(float(r.get("saved_at", 0) or 0))) == today),
                "soon": sum(1 for r in mine
                            if (DAYS - soon_days) * 86400 < now - float(r.get("last_used", 0) or 0) <= DAYS * 86400)}


# ----------------------------------------------------------------------
# Which to offer in a reply
# ----------------------------------------------------------------------
_HAPPY = ("开心", "高兴", "快乐", "哈哈", "笑", "得意", "兴奋", "喜欢", "可爱", "满足")
_SAD = ("难过", "伤心", "哭", "委屈", "生气", "无语", "累", "烦", "尴尬", "害怕")


def _tone(emotion) -> float:
    e = str(emotion or "")
    return (1.0 if any(w in e for w in _HAPPY) else 0.0) - (1.0 if any(w in e for w in _SAD) else 0.0)


def pick_candidates(rows, now, valence=0.0, similarity=None, k=CANDIDATES, recent=RECENT_SECONDS) -> list:
    """A few to offer: how near the talk is (`similarity`: row -> 0..1, e.g. local vectors)
    and how near her mood (valence -1..1); none sent in the last `recent` seconds."""
    scored = []
    for sid, r in (rows or {}).items():
        if now - float(r.get("last_used", 0) or 0) < recent and int(r.get("uses", 0) or 0) > 0:
            continue
        near = float(similarity(r)) if similarity else 0.0
        mood = 1.0 - abs(_tone(r.get("emotion")) - max(-1.0, min(1.0, float(valence)))) / 2
        scored.append((0.7 * near + 0.3 * mood, sid))
    return [sid for _s, sid in sorted(scored, key=lambda x: (-x[0], x[1]))[:k]]


_PICKED = re.compile(r"\[表情[:：]\s*([^\]\s]+)\s*\]")


def pick_from_reply(text, offered) -> tuple:
    """(the reply without the mark, the sticker it names) -- only one that was offered; the
    candidates are numbered 1..n in the prompt."""
    offered = list(offered or [])
    chosen = ""
    for m in _PICKED.finditer(str(text or "")):
        tag = m.group(1)
        if tag.isdigit() and 1 <= int(tag) <= len(offered):
            chosen = chosen or offered[int(tag) - 1]
    return _PICKED.sub("", str(text or "")).strip(), chosen


def phone_line(row) -> str:
    """How a sticker she sent is kept in her phone."""
    return "[表情：%s]" % (str((row or {}).get("caption") or "表情")[:12])


# ----------------------------------------------------------------------
# Sending one as a QQ sticker
# ----------------------------------------------------------------------
def send_params(place, image_b64, text="", faces=()) -> tuple:
    """(action, params) for the adapter's own NapCat client: only to the chat of this message
    (`place`: "group:<number>" or "private:<number>", from the message itself), only a picture
    as a sticker, with text and QQ faces. Raises ValueError for anything else."""
    kind, _, target = str(place or "").partition(":")
    if kind not in ("group", "private") or not target.isdigit():
        raise ValueError("not a chat of a message")
    if not re.fullmatch(r"[A-Za-z0-9+/=]+", str(image_b64 or "")):
        raise ValueError("not base64")
    message = []
    if text:
        message.append({"type": "text", "data": {"text": str(text)}})
    for f in faces or ():
        if not str(f).isdigit():
            raise ValueError("not a face")
        message.append({"type": "face", "data": {"id": str(f)}})
    message.append({"type": "image", "data": {"file": "base64://" + str(image_b64), "sub_type": 1,
                                              "summary": STICKER_SUMMARY}})
    if kind == "group":
        return "send_group_msg", {"group_id": int(target), "message": message}
    return "send_private_msg", {"user_id": int(target), "message": message}


def allowed(action, params, place) -> bool:
    """The last look before call_action: one of the two actions, to `place` only, only
    image (as a sticker), text and face."""
    kind, _, target = str(place or "").partition(":")
    if action not in SEND_ACTIONS or not isinstance(params, dict) or not target.isdigit():
        return False
    key = "group_id" if action == "send_group_msg" else "user_id"
    if (kind == "group") != (action == "send_group_msg") or str(params.get(key)) != target:
        return False
    if set(params) != {key, "message"} or not isinstance(params.get("message"), list):
        return False
    for seg in params["message"]:
        t, d = seg.get("type") if isinstance(seg, dict) else None, (seg or {}).get("data") if isinstance(seg, dict) else None
        if not isinstance(d, dict) or t not in ("image", "text", "face"):
            return False
        if t == "image" and not (str(d.get("file", "")).startswith("base64://") and d.get("sub_type") == 1):
            return False
    return True


# ----------------------------------------------------------------------
# What a look leaves in image_cache.json
# ----------------------------------------------------------------------
def cache_entry(ref, look, from_qq, where, now) -> dict:
    return {"ref": str(ref), "caption": str((look or {}).get("caption") or ""), "look": look or {},
            "from_qq": str(from_qq or ""), "where": str(where or ""), "ts": float(now)}


def prune_cache(cache, now, gone_people=(), days=DAYS) -> int:
    """Drop what someone deleted sent, and entries that do not say who sent them after `days`.
    Returns how many went."""
    gone = {str(p) for p in gone_people or ()}
    drop = [k for k, v in (cache or {}).items() if isinstance(v, dict) and (
        (v.get("from_qq") and v.get("from_qq") in gone)
        or (not v.get("from_qq") and now - float(v.get("ts", 0) or 0) > days * 86400))]
    for k in drop:
        cache.pop(k, None)
    return len(drop)
