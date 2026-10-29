# -*- coding: utf-8 -*-
# ams-life — derived from BioCore v1.2.99 (https://github.com/Johnhmzm/astrbot_plugin_biocore),
# Copyright (C) 2026 Johnhmzm, AGPL-3.0. Modified by m103canfly since 2026-10-27; see NOTICE.md.
"""BioCorePlugin methods moved out of main.py unchanged: images and voice: refs, local VLM service, caption and transcription context."""
from __future__ import annotations
try:
    from .common import *  # noqa: F401,F403
except ImportError:
    from common import *  # noqa: F401,F403
try:
    from .body import *  # noqa: F401,F403
except ImportError:
    from body import *  # noqa: F401,F403
try:
    from . import stickers
except ImportError:
    import stickers


class MediaMixin:
    @staticmethod
    def _image_ref(img) -> str:
        if not isinstance(img, Image):
            return ""
        return str(getattr(img, "url", "") or getattr(img, "file", "") or getattr(img, "path", "") or "").strip()

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
            messages = event.get_messages() or []
        except Exception:
            return []
        refs = []
        private = bool(getattr(event, "is_private_chat", lambda: False)())
        raw_text = str(getattr(event, "message_str", "") or "") + " " + self._text_from_components(event)
        if private:
            for msg in messages:
                if isinstance(msg, Image):
                    ref = self._image_ref(msg)
                    if ref:
                        refs.append(ref)
                if isinstance(msg, Reply):
                    for child in (getattr(msg, "chain", None) or []):
                        ref = self._image_ref(child)
                        if ref:
                            refs.append(ref)
        else:
            if not any(w and w in raw_text for w in (getattr(self, "image_trigger_words", None) or [])):
                return []
            for msg in messages:
                if isinstance(msg, Reply):
                    for child in (getattr(msg, "chain", None) or []):
                        ref = self._image_ref(child)
                        if ref:
                            refs.append(ref)
        seen = set()
        out = []
        for ref in refs:
            if ref not in seen:
                seen.add(ref)
                out.append(ref)
        return out

    def _load_image_cache(self) -> dict:
        try:
            if IMAGE_CACHE_PATH.exists():
                d = json.loads(IMAGE_CACHE_PATH.read_text(encoding="utf-8"))
                if isinstance(d, dict):
                    return d
        except Exception:
            pass
        return {}

    def _save_image_cache(self, cache: dict) -> None:
        if self._job_stale():
            return  # someone (or a message) she may not keep, or something forgotten meanwhile
        try:
            if len(cache) > self.image_cache_max_entries:
                items = sorted(cache.items(), key=lambda kv: float(kv[1].get("ts", 0) or 0), reverse=True)
                cache = dict(items[:self.image_cache_max_entries])
            IMAGE_CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
        except Exception as exc:
            logger.warning("[biocore] image cache save failed: %s", exc)

    async def _image_health_ok(self) -> bool:
        if int(self.image_service_port or 0) <= 0:
            return False
        def _check() -> bool:
            try:
                req = urllib.request.Request(
                    f"http://127.0.0.1:{self.image_service_port}/v1/models",
                    headers={"Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=2) as resp:
                    return 200 <= int(resp.status) < 300
            except Exception:
                return False
        try:
            return await asyncio.to_thread(_check)
        except Exception:
            return False

    def _image_idle_watch(self):
        if self._image_proc is None:
            return
        if self._image_idle_task is not None and not self._image_idle_task.done():
            return
        self._image_idle_task = asyncio.create_task(self._image_idle_loop())

    async def _image_idle_loop(self):
        try:
            while True:
                await asyncio.sleep(5)
                if self._image_proc is None:
                    return
                if time.time() - float(self._image_last_used or 0.0) >= self.image_service_idle_seconds:
                    await self._stop_image_service()
                    return
        finally:
            self._image_idle_task = None

    async def _stop_image_service(self):
        proc = self._image_proc
        self._image_proc = None
        if proc is None:
            return
        try:
            if proc.poll() is None:
                subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               timeout=10, check=False)
        except Exception as exc:
            logger.warning("[biocore] image service stop failed: %s", exc)
        try:
            proc.wait(timeout=5)
        except Exception:
            pass
        logger.info("[biocore] image service stopped after idle")

    async def _ensure_image_service(self) -> bool:
        if int(self.image_service_port or 0) <= 0:
            return False
        self._image_last_used = time.time()
        if await self._image_health_ok():
            return True
        if self._image_service_lock is None:
            self._image_service_lock = asyncio.Lock()
        async with self._image_service_lock:
            if await self._image_health_ok():
                self._image_last_used = time.time()
                return True
            try:
                if (not self.image_llama_server or not self.image_llama_model
                        or not self.image_llama_server.is_file()
                        or not self.image_llama_model.is_file()):
                    logger.warning("[biocore] image service paths missing; configure image_llama_server / image_llama_model")
                    return False
                args = [str(self.image_llama_server), "-m", str(self.image_llama_model)]
                if self.image_llama_mmproj and self.image_llama_mmproj.is_file():
                    args += ["--mmproj", str(self.image_llama_mmproj)]
                args += ["--host", "127.0.0.1", "--port", str(self.image_service_port),
                         "-ngl", "99", "-c", "8192", "-np", "1", "-lm", "none",
                         "-cram", "0", "-ctxcp", "0", "--no-warmup"]
                flags = 0x08000000 if os.name == "nt" else 0
                self._image_proc = subprocess.Popen(args, stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL,
                                                    creationflags=flags)
                logger.info("[biocore] image service starting pid=%s", self._image_proc.pid)
                for _ in range(60):
                    if await self._image_health_ok():
                        self._image_last_used = time.time()
                        self._image_idle_watch()
                        return True
                    await asyncio.sleep(1)
                logger.warning("[biocore] image service did not become ready")
                await self._stop_image_service()
                return False
            except Exception as exc:
                logger.warning("[biocore] image service start failed: %s", exc)
                self._image_proc = None
                return False

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

    async def _image_context(self, event) -> str:
        refs = self._image_refs(event)
        stickers_on = bool(getattr(self, "_stickers_on", None) and self._stickers_on())
        if stickers_on:
            # step 2 (丙): QQ stickers of this message are looked at wherever it was sent
            refs = list(dict.fromkeys(refs + self._sticker_refs(event)))
        if not refs:
            return ""
        if not self._llm_allowed("image_caption"):
            return ""
        # Local llama-server is optional. A general AstrBot vision provider
        # must work without image_llama_* / image_service_port.
        _local_vlm = bool(self.image_llama_server and self.image_llama_model
                          and int(self.image_service_port or 0) > 0)
        if _local_vlm:
            if not await self._ensure_image_service():
                logger.warning("[biocore] local VLM unavailable; falling back to configured vision provider")
        self._image_last_used = time.time()
        cache = self._load_image_cache()
        missing = [r for r in refs if _sha256(r) not in cache]
        if missing:
            try:
                cfg = self.context.get_config()
                provider_settings = cfg.get("provider_settings", {}) if isinstance(cfg, dict) else {}
                prompt = interpretation.image_caption_prompt(
                    provider_settings.get("image_caption_prompt"))
                # Image caption always uses the vision provider, never a text LLM.
                provider = self._vision_provider_for(event)
                if provider is not None:
                    for ref in missing[:3]:
                        look = None
                        try:
                            if stickers_on:
                                # one call: what it shows, and whether she keeps it (step 2, 丙)
                                caption, look = await self._look_once(provider, ref, event)
                            else:
                                resp = await provider.text_chat(prompt=prompt, image_urls=[ref])
                                caption = interpretation.parse_image_caption(
                                    str(getattr(resp, "completion_text", "") or ""))
                        except Exception as exc:
                            logger.warning("[biocore] image caption failed: %s", exc)
                            caption = ""
                        if caption and look is not None:
                            cache[_sha256(ref)] = stickers.cache_entry(
                                ref, look, self._speaker(event)[0], self._here(event), time.time())
                            await self._maybe_keep(event, ref, look)
                        elif caption:
                            cache[_sha256(ref)] = {"ref": ref, "caption": caption, "ts": time.time()}
                    self._save_image_cache(cache)
            except Exception as exc:
                logger.warning("[biocore] image provider failed: %s", exc)
        lines = []
        for ref in refs[:3]:
            item = cache.get(_sha256(ref))
            if item and item.get("caption"):
                lines.append(str(item["caption"]))
        self._image_last_used = time.time()
        if not lines:
            return ""
        return "\n".join(lines)
