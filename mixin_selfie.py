# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her phone: tools enqueue work; only a cleared reply can send it."""
from __future__ import annotations

import asyncio
import base64
import json
import re
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

try:
    from .common import *  # noqa: F401,F403
    from . import tts, browse
except ImportError:
    from common import *  # noqa: F401,F403
    import tts
    import browse

SELFIE_DIR = DATA_DIR / "selfie"
REF_DIR = SELFIE_DIR / "refs"
SPEND_PATH = STATE_DIR / "spend.json"
SEND_DELAY = 1.5
PHOTO_RETRIES = 3
PHOTO_WAITING = 3
SELFIE_PROMPT = ("真人质感的手机照片，真实皮肤和光影，有实感、有生活气息，不要动漫画风，不要塑料感，不要摆拍感。\n"
                 "参考图1是她本人：不管什么角度，脸、发型、头饰都照参考图1，同一个人，不要增减头饰，不要加光环。\n"
                 "粉色长发，后脑勺高处扎一束很长的高马尾（只有一束，不是双马尾），头顶一小撮呆毛；琥珀色眼睛。\n"
                 "角度和姿势照下面写的来，不用正对镜头，像生活里随手拍的、朋友抓拍的。\n"
                 "衣服按场景来，身上没有发光的花纹。竖构图 4:3。\n这张照片：")
SNAP_PROMPT = ("普通人用手机随手拍的照片，真实，有生活气息，不是摄影作品，不要精修，不要广告感。\n"
               "画面里没有人脸，也没有人物正面；最多露出拍照人的一只手或袖口（浅色宽松毛衣袖子，手指纤细）。\n"
               "构图随意，可能有点歪、有点糊，光线就是当时的自然光，有手机照片的噪点。\n"
               "不要出现文字水印、门牌号、车牌、能认出具体地点的招牌。竖构图 3:4。\n拍的是：")
PHOTO_GUIDE = ("拍照由你自己决定。自拍：新衣发型、节日、出门、心情好、被夸或熟人问近况时可以拍；"
               "深夜、刚醒没收拾、心情很差或不熟的人索要时不拍，刚醒和极熟的人撒娇可例外。"
               "自拍的 what 须写清在哪、穿什么、角度姿势、在干什么；变换角度：四分之三侧、低头、回头、对镜、俯拍、朋友抓拍没看镜头。"
               "随手拍吃的、天空风景、猫、招牌、买的东西、游戏、节日装饰；避开别人脸和能认出住处的门牌车牌。")
SCREEN_GUIDE = ("分享你看过的网页：有趣帖子新闻、讨论中查到的资料、与熟人有关的内容。"
                "不分享含别人聊天记录、名字或号码的内容，不把私聊的东西发到群里。")
VOICE_GUIDE = ("挑一句话用语音说：情绪满、忙着懒得打字、对方先发语音、困了晚安、唱生日歌、"
               "安慰人、刚醒或模仿声音逗人时可以；多给私聊熟人，群里少，陌生人不发。"
               "对方上班开会或不方便听、群里人多话题正经、内容太长时不发。")
COMMON_GUIDE = "群里刷屏、话题无关、正事或对方难过时别发搞笑内容；刚发过也要考虑是否合适。每种工具每轮最多一次。"
GENERATED = re.compile(r"^ams-phone-(photo|voice)-\d{14}-[0-9a-f]{32}\.(png|wav|mp3)$")


def _read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    atomic_file.replace(tmp, path)


class SelfieMixin:
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

    def _give_phone_tools(self, req, event):
        cfg = self.config or {}
        if not self.enabled or not any(cfg.get(k, False) for k in ("photo_enabled", "screenshot_enabled", "say_aloud_enabled")):
            return
        try:
            from astrbot.core.agent.tool import FunctionTool, ToolSet
        except ImportError:
            logger.warning("[ams-life] phone tools unavailable")
            return
        context = self._phone_context(event) + COMMON_GUIDE
        tools = []
        if cfg.get("photo_enabled", False):
            tools.append(FunctionTool(name="take_photo", description=PHOTO_GUIDE + context,
                parameters={"type": "object", "properties": {"kind": {"type": "string", "enum": ["selfie", "snap"]},
                "what": {"type": "string", "description": "拍什么、在哪、光线，60字以内"}}, "required": ["kind", "what"]}, handler=self._tool_take_photo))
        if cfg.get("screenshot_enabled", False) and self._browse_on():
            tools.append(FunctionTool(name="share_screenshot", description=SCREEN_GUIDE + context,
                parameters={"type": "object", "properties": {"url": {"type": "string"}, "caption": {"type": "string"}},
                "required": ["url", "caption"]}, handler=self._tool_share_screenshot))
        if cfg.get("say_aloud_enabled", False):
            tools.append(FunctionTool(name="say_aloud", description=VOICE_GUIDE + context,
                parameters={"type": "object", "properties": {"text": {"type": "string", "description": "要说的一句话，100字以内"}},
                "required": ["text"]}, handler=self._tool_say_aloud))
        if not tools:
            return
        existing = getattr(req, "func_tool", None)
        if existing is None:
            req.func_tool = ToolSet(tools)
        else:
            for tool in tools:
                existing.add_tool(tool)

    @staticmethod
    def _phone_queue(event):
        queue = getattr(event, "_ams_phone_queue", None)
        if queue is None:
            queue = event._ams_phone_queue = {}
        return queue

    async def _tool_take_photo(self, event, kind="", what=""):
        queue = self._phone_queue(event)
        if "photo" in queue:
            return "这次已经有了"
        what = str(what or "").strip()
        if not self.enabled or not self.config.get("photo_enabled") or kind not in ("selfie", "snap") or not what or len(what) > 60:
            return "不能拍这张"
        queue["photo"] = (kind, what)
        logger.info("[ams-life] phone photo queued")
        return "排上了"

    def _phone_seen_pages(self, event):
        """Only successful searches and reads in this reply, not merely allowed URLs."""
        return self._browse_seen_pages(event) if self._browse_on() else {}

    async def _tool_share_screenshot(self, event, url="", caption=""):
        queue = self._phone_queue(event)
        if "screenshot" in queue:
            return "这次已经有了"
        url, caption = str(url or "").strip(), str(caption or "").strip()
        pages = self._phone_seen_pages(event)
        if not self.enabled or not self.config.get("screenshot_enabled") or not caption or url not in pages:
            return "只能分享看过的网页"
        queue["screenshot"] = (url, str(pages[url]), caption)
        logger.info("[ams-life] phone screenshot queued")
        return "排上了"

    async def _tool_say_aloud(self, event, text=""):
        queue = self._phone_queue(event)
        if "voice" in queue:
            return "这次已经有了"
        text = str(text or "").strip()
        if not self.enabled or not self.config.get("say_aloud_enabled") or not text or len(text) > 100:
            return "这句话不能说"
        text = tts.speakable(text, 100)
        if not text:
            return "这句话不能说"
        queue["voice"] = text
        logger.info("[ams-life] phone voice queued")
        return "排上了"

    def _phone_counts(self):
        data = _read_json(SPEND_PATH, {})
        if not isinstance(data, dict):
            return {}
        return data.get(time.strftime("%Y-%m-%d") + "-phone", {}) or {}

    def _phone_account(self, kind, price=None, sent=False):
        try:
            data = _read_json(SPEND_PATH, {})
            if not isinstance(data, dict):
                data = {}
            date = time.strftime("%Y-%m-%d")
            if price is not None:
                day = data.setdefault(date, {})
                day["phone_" + kind] = round(float(day.get("phone_" + kind, 0)) + max(0, float(price)), 6)
            if sent:
                counts = data.setdefault(date + "-phone", {})
                counts[kind] = int(counts.get(kind, 0)) + 1
                counts["last"] = time.time()
            _write_json(SPEND_PATH, data)
        except Exception as exc:
            logger.warning("[ams-life] phone accounting failed: %s", type(exc).__name__)

    def _phone_price(self, kind):
        try:
            return max(0.0, float((self.config or {}).get("phone_" + kind + "_price", 0) or 0))
        except (TypeError, ValueError):
            return 0.0

    async def _post_json(self, url, payload, key, timeout=120):
        def run():
            req = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), method="POST",
                headers={"Authorization": "Bearer " + str(key or ""), "Content-Type": "application/json", "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), resp.headers.get("content-type", "")
        return await asyncio.to_thread(run)

    async def _post_selfie(self, url, prompt, key, size, ref):
        def run():
            boundary = "----amslife" + uuid.uuid4().hex
            def field(name, value):
                return ("--" + boundary + "\r\nContent-Disposition: form-data; name=\"" + name + "\"\r\n\r\n" + value + "\r\n").encode("utf-8")
            parts = [field("model", "codex-image"), field("prompt", prompt), field("size", size), field("n", "1")]
            parts.append(("--" + boundary + "\r\nContent-Disposition: form-data; name=\"image\"; filename=\"reference.png\"\r\nContent-Type: image/png\r\n\r\n").encode("utf-8") + ref.read_bytes() + b"\r\n")
            parts.append(("--" + boundary + "--\r\n").encode("utf-8"))
            req = urllib.request.Request(url, data=b"".join(parts), method="POST", headers={"Authorization": "Bearer " + str(key or ""),
                "Content-Type": "multipart/form-data; boundary=" + boundary})
            with urllib.request.urlopen(req, timeout=300) as resp:
                return resp.read()
        return await asyncio.to_thread(run)

    def _phone_path(self, kind, ext):
        SELFIE_DIR.mkdir(parents=True, exist_ok=True)
        return SELFIE_DIR / ("ams-phone-" + kind + "-" + time.strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex + ext)

    async def _make_photo(self, kind, what):
        names = self._browse_names()
        what = browse.clean_query(what, names=names)
        for name in names:
            name = str(name or "").strip()
            if len(name) == 1:
                what = what.replace(name, " ")
        what = re.sub(r"\s+", " ", what).strip()
        if not what:
            logger.info("[ams-life] phone photo cancelled: empty description")
            return None
        pending = getattr(self, "_phone_photo_pending", 0)
        if pending >= PHOTO_WAITING + 1:
            logger.info("[ams-life] phone photo queue full")
            return None
        self._phone_photo_pending = pending + 1
        try:
            lock = getattr(self, "_phone_photo_lock", None)
            if lock is None:
                lock = self._phone_photo_lock = asyncio.Lock()
            async with lock:
                api = dict(self.api_config.get("image") or {})
                base = str(api.get("base_url") or "").rstrip("/")
                if not base:
                    return None
                refname = str((self.config or {}).get("selfie_reference", "her_base.png") or "her_base.png")
                if Path(refname).name != refname or refname in (".", ".."):
                    return None
                ref = REF_DIR / refname
                if kind == "selfie" and not ref.is_file():
                    logger.info("[ams-life] phone reference missing")
                    return None
                prompt = (SELFIE_PROMPT if kind == "selfie" else SNAP_PROMPT) + what
                for attempt in range(PHOTO_RETRIES):
                    try:
                        if kind == "selfie":
                            raw = await self._post_selfie(base + "/images/edits", prompt, api.get("api_key"), "1080x1440", ref)
                        else:
                            raw, _ = await self._post_json(base + "/images/generations", {"model": "codex-image", "prompt": prompt,
                                "size": "1080x1440", "n": 1}, api.get("api_key"), timeout=300)
                        self._phone_account(kind, self._phone_price("photo"))
                        value = json.loads(raw.decode("utf-8"))
                        blob = base64.b64decode(value["data"][0]["b64_json"], validate=True)
                        if not blob:
                            return None
                        path = self._phone_path("photo", ".png")
                        path.write_bytes(blob)
                        return path
                    except urllib.error.HTTPError as exc:
                        if exc.code != 429 or attempt + 1 == PHOTO_RETRIES:
                            logger.info("[ams-life] phone photo cancelled: service")
                            return None
                        await asyncio.sleep(2 ** attempt)
                    except Exception as exc:
                        logger.warning("[ams-life] phone photo failed: %s", type(exc).__name__)
                        return None
        finally:
            self._phone_photo_pending -= 1

    async def _make_voice(self, text):
        try:
            lock = getattr(self, "_phone_voice_lock", None)
            if lock is None:
                lock = self._phone_voice_lock = asyncio.Lock()
            async with lock:
                api = dict(self.api_config.get("tts") or {})
                base = str(api.get("base_url") or "").rstrip("/")
                if not base:
                    return None
                raw, ctype = await self._post_json(base + "/audio/speech", {"model": api.get("model") or "", "input": text,
                    "voice": api.get("voice") or "", "response_format": api.get("format") or "wav"}, api.get("api_key"), timeout=90)
                self._phone_account("voice", self._phone_price("voice"))
                if not raw:
                    return None
                path = self._phone_path("voice", ".wav" if "wav" in ctype else ".mp3")
                path.write_bytes(raw)
                return path
        except Exception as exc:
            logger.warning("[ams-life] phone voice failed: %s", type(exc).__name__)
            return None

    def _phone_prune(self, kind):
        try:
            limit = max(1, int((self.config or {}).get("phone_" + kind + "_retention", 50)))
            files = [p for p in SELFIE_DIR.iterdir() if p.is_file() and GENERATED.fullmatch(p.name)
                     and GENERATED.fullmatch(p.name).group(1) == kind]
            files.sort(key=lambda p: (p.stat().st_mtime_ns, p.name), reverse=True)
            for path in files[limit:]:
                path.unlink()
        except FileNotFoundError:
            pass
        except Exception as exc:
            logger.warning("[ams-life] phone retention failed: %s", type(exc).__name__)

    async def _phone_clear(self, event, text):
        try:
            if (await self._check_reply(event, text)).get("leak"):
                logger.info("[ams-life] phone held back")
                return False
            return True
        except Exception:
            logger.info("[ams-life] phone held back")
            return False

    async def _media_after_reply(self, event, queue):
        rest = getattr(event, "_ams_rest_task", None)
        if rest is not None:
            try:
                await rest
            except asyncio.CancelledError:
                if not rest.cancelled():
                    raise
            except Exception as exc:
                logger.warning("[ams-life] phone: reply wait failed (%s)", type(exc).__name__)
        await asyncio.sleep(SEND_DELAY)
        try:
            if hasattr(event, "is_stopped") and event.is_stopped():
                return
            if "photo" in queue:
                kind, what = queue["photo"]
                if await self._phone_clear(event, what):
                    path = await self._make_photo(kind, what)
                    if path and not (hasattr(event, "is_stopped") and event.is_stopped()):
                        await event.send(MessageChain([Image.fromFileSystem(str(path))]))
                        self._phone_account(kind, sent=True)
                        self._note_she_sent(event, kind)
                        self._phone_prune("photo")
            if "screenshot" in queue:
                url, title, caption = queue["screenshot"]
                if (await self._phone_clear(event, caption) and await self._phone_clear(event, title + "\n" + url)
                        and not (hasattr(event, "is_stopped") and event.is_stopped())):
                    await event.send(MessageChain([Plain(title + "\n" + url + "\n" + caption)]))
                    self._phone_account("screenshot", sent=True)
                    self._note_she_sent(event, "screenshot")
            if "voice" in queue and await self._phone_clear(event, queue["voice"]):
                path = await self._make_voice(queue["voice"])
                if path and not (hasattr(event, "is_stopped") and event.is_stopped()):
                    await event.send(MessageChain([Record.fromFileSystem(str(path))]))
                    self._phone_account("voice", sent=True)
                    self._note_she_sent(event, "voice")
                    self._phone_prune("voice")
        except Exception as exc:
            logger.warning("[ams-life] phone send failed: %s", type(exc).__name__)
