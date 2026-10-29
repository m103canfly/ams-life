# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""ams-life: her camera and her voice (added 2026-10-30).

Two things she can do besides writing: take a photo of herself and say something
out loud.  Both are off unless the switches in <data>/media_settings.json say on,
both are capped per day, and anything that fails sends nothing at all - it only
leaves a line in the log.

The picture follows the standard the owner settled on 2026-10-30 (written down on
his machine, not in this repository): two references (her face + the hair ornament from the
official art, in <data>/selfie/refs/, never in this repository), 4:3 portrait
1080x1440, plain home clothes, no glowing mark on her chest.  The voice goes through
the local GPT-SoVITS bridge (tools/gsv_openai_tts.py).  Where both services are and
their keys are the panel's API settings (image, tts), never written here.
"""
from __future__ import annotations

import asyncio
import base64
import json
import time
import urllib.request
import uuid
from pathlib import Path

try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403


SELFIE_DIR = DATA_DIR / "selfie"
REF_DIR = SELFIE_DIR / "refs"
SETTINGS_PATH = DATA_DIR / "media_settings.json"
COUNTER_PATH = SELFIE_DIR / "counters.json"

DEFAULTS = {
    "selfie_enabled": False,   # on only where media_settings.json says so
    "selfie_daily_limit": 0,
    "selfie_keywords": ["在干嘛", "在干什么", "在做什么", "干嘛呢", "在忙什么", "忙什么呢",
                        "看看你", "发张照片", "发张照", "发自拍", "拍张照", "自拍", "你在哪"],
    "selfie_scene_fallback": "她刚发完消息，正对着镜头，家里的日常",
    "voice_enabled": False,
    "voice_daily_limit": 0,
    "voice_keywords": ["发语音", "语音", "说句话", "说一句", "念一下", "读一下", "听听你的声音"],
}

LOOK = ("2.5次元写真，动漫五官 + 真实皮肤质感和光影，像真人用手机拍的自拍。"
        "脸完全照参考图1（同一个人，琥珀色眼睛）。"
        "头饰照参考图2还原：刘海一侧一枚白色羽翼发饰；两束高马尾的根部各有一片淡蓝色半透明的冰晶羽翼，"
        "发亮、有棱角；马尾发根系浅蓝色丝带。粉色长发扎成高双马尾。"
        "衣服：宽松的家居便服（露肩短袖T恤或宽松毛衣），不是战衣，没有护甲。"
        "胸口干净，没有任何发光纹路。"
        "手机竖屏自拍，4:3 照片，构图随意、背景有点乱，像随手拍的。两只眼睛都睁开。"
        "她在做什么：")


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path, value):
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception:
        pass


class SelfieMixin:
    # ---------- settings and the daily caps ----------
    def _media_settings(self):
        raw = _read_json(SETTINGS_PATH, {})
        if not isinstance(raw, dict):
            raw = {}
        out = dict(DEFAULTS)
        out.update({k: v for k, v in raw.items() if k in DEFAULTS})
        return out

    def _media_count(self, kind):
        today = time.strftime("%Y-%m-%d")
        data = _read_json(COUNTER_PATH, {})
        if not isinstance(data, dict) or data.get("date") != today:
            return 0
        try:
            return int(data.get(kind) or 0)
        except Exception:
            return 0

    def _media_bump(self, kind):
        today = time.strftime("%Y-%m-%d")
        data = _read_json(COUNTER_PATH, {})
        if not isinstance(data, dict) or data.get("date") != today:
            data = {"date": today}
        try:
            data[kind] = int(data.get(kind) or 0) + 1
        except Exception:
            data[kind] = 1
        _write_json(COUNTER_PATH, data)

    def _media_wanted(self, event, cfg, enabled_key, keywords_key):
        if not cfg.get(enabled_key):
            return False
        try:
            text = str(getattr(event, "message_str", "") or "")
        except Exception:
            text = ""
        if not text:
            return False
        return any(k in text for k in (cfg.get(keywords_key) or []))

    # ---------- the two services ----------
    async def _post_json(self, url, payload, key, timeout=120):
        def run():
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(url, data=data, method="POST", headers={
                "Authorization": "Bearer " + str(key or ""),
                "Content-Type": "application/json",
                "Accept": "*/*",
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), resp.headers.get("content-type", "")
        return await asyncio.to_thread(run)

    async def _post_selfie(self, url, prompt, key, size, timeout=300):
        def run():
            boundary = "----amslife" + uuid.uuid4().hex[:12]
            def field(name, value):
                return ("--" + boundary + "\r\nContent-Disposition: form-data; name=\"" + name +
                        "\"\r\n\r\n" + value + "\r\n").encode("utf-8")
            parts = [field("model", "codex-image"), field("prompt", prompt), field("size", size), field("n", "1")]
            for idx, name in enumerate(("face.png", "ornament.png"), start=1):
                path = REF_DIR / name
                if not path.exists():
                    raise FileNotFoundError(str(path))
                blob = path.read_bytes()
                parts.append(("--" + boundary + "\r\nContent-Disposition: form-data; name=\"image\"; filename=\"" +
                              name + "\"\r\nContent-Type: image/png\r\n\r\n").encode("utf-8") + blob + b"\r\n")
            parts.append(("--" + boundary + "--\r\n").encode("utf-8"))
            req = urllib.request.Request(url, data=b"".join(parts), method="POST", headers={
                "Authorization": "Bearer " + str(key or ""),
                "Content-Type": "multipart/form-data; boundary=" + boundary,
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        return await asyncio.to_thread(run)

    async def _make_selfie(self, scene):
        """Returns the path of a picture, or None. Never raises."""
        try:
            cfg_api = dict(self.api_config.get("image") or {})
            base = str(cfg_api.get("base_url") or "").rstrip("/")
            if not base:
                logger.warning("[ams-life] selfie: no image API configured")
                return None
            prompt = LOOK + str(scene or "")[:80]
            raw = await self._post_selfie(base + "/images/edits", prompt, cfg_api.get("api_key"), "1080x1440")
            payload = json.loads(raw.decode("utf-8", "replace"))
            b64 = ((payload.get("data") or [{}])[0] or {}).get("b64_json")
            if not b64:
                logger.warning("[ams-life] selfie: no image in the answer")
                return None
            SELFIE_DIR.mkdir(parents=True, exist_ok=True)
            path = SELFIE_DIR / (time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6] + ".png")
            path.write_bytes(base64.b64decode(b64))
            return path
        except Exception as exc:
            logger.warning("[ams-life] selfie failed: %s", exc)
            return None

    async def _make_voice(self, text):
        """Returns the path of a sound file, or None. Never raises."""
        try:
            cfg_api = dict(self.api_config.get("tts") or {})
            base = str(cfg_api.get("base_url") or "").rstrip("/")
            if not base:
                logger.warning("[ams-life] voice: no TTS API configured")
                return None
            payload = {
                "model": cfg_api.get("model") or "",
                "input": str(text or "")[:300],
                "voice": cfg_api.get("voice") or "",
                "response_format": cfg_api.get("format") or "wav",
            }
            raw, ctype = await self._post_json(base + "/audio/speech", payload, cfg_api.get("api_key"), timeout=90)
            if not raw:
                return None
            ext = ".wav" if "wav" in (ctype or "") else ".mp3"
            SELFIE_DIR.mkdir(parents=True, exist_ok=True)
            path = SELFIE_DIR / (time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6] + ext)
            path.write_bytes(raw)
            return path
        except Exception as exc:
            logger.warning("[ams-life] voice failed: %s", exc)
            return None

    # ---------- what happens after she answers ----------
    async def _media_after_reply(self, event, reply):
        """Called once per answer. Sends a photo, a voice note, or nothing."""
        try:
            cfg = self._media_settings()
            want_selfie = self._media_wanted(event, cfg, "selfie_enabled", "selfie_keywords")
            want_voice = self._media_wanted(event, cfg, "voice_enabled", "voice_keywords")
            if not (want_selfie or want_voice):
                return
            logger.info("[ams-life] media wanted: selfie=%s voice=%s", want_selfie, want_voice)

            # 主人 10-30 定：不设上限。极限 <= 0 就是不限；以后想限就把数字填回正数。
            if want_selfie:
                _limit = int(cfg.get("selfie_daily_limit") or 0)
                if _limit > 0 and self._media_count("selfie") >= _limit:
                    logger.info("[ams-life] selfie: today's limit is reached")
                    want_selfie = False
            if want_voice:
                if not str(reply or "").strip():
                    want_voice = False
                else:
                    _limit = int(cfg.get("voice_daily_limit") or 0)
                    if _limit > 0 and self._media_count("voice") >= _limit:
                        logger.info("[ams-life] voice: today's limit is reached")
                        want_voice = False

            if want_voice:
                path = await self._make_voice(reply)
                if path is not None:
                    self._media_bump("voice")
                    await asyncio.sleep(1.5)   # her written answer goes out first
                    await event.send(MessageChain([Record.fromFileSystem(str(path))]))
                    self._note_she_sent(event, "voice")
                    logger.info("[ams-life] voice sent: %s", path.name)

            if want_selfie:
                scene = str(reply or "").strip() or cfg.get("selfie_scene_fallback")
                scene = scene.replace("\n", " ")[:60]
                path = await self._make_selfie(scene)
                if path is not None:
                    self._media_bump("selfie")
                    await event.send(MessageChain([Image.fromFileSystem(str(path))]))
                    self._note_she_sent(event, "selfie")
                    logger.info("[ams-life] selfie sent: %s", path.name)
        except Exception as exc:
            logger.warning("[ams-life] camera or voice failed: %s", exc)
