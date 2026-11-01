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
    from . import adapter_astrbot_turn, events, stickers
except ImportError:
    import adapter_astrbot_turn
    import events
    import stickers
try:
    from .mixin_ports import PortsMixin
except ImportError:
    from mixin_ports import PortsMixin

# Short enough to describe a just-sent picture, bounded per conversation to limit memory.
RECENT_IMAGE_SECONDS = 120
RECENT_IMAGE_LIMIT = 10
RECENT_IMAGE_LOOK_LIMIT = 2

class MediaMixin(PortsMixin):
    @staticmethod
    def _image_ref(img) -> str:
        if not isinstance(img, Image):
            return ""
        return str(getattr(img, "url", "") or getattr(img, "file", "") or getattr(img, "path", "") or "").strip()

    def _text_from_components(self, event) -> str:
        parts = []
        try:
            for msg in adapter_astrbot_turn.incoming_of(event).segments:
                text = msg.data.get("text") if msg.type in ("text", "reply") else None
                if isinstance(text, str):
                    parts.append(text)
        except Exception:
            pass
        return " ".join(parts)

    def _image_refs(self, event) -> list:
        if not getattr(self, "image_recognition_enabled", True):
            return []
        try:
            if not adapter_astrbot_turn.incoming_of(event).is_private and not self._addresses_her(event):
                return []
            refs = []
            for msg in adapter_astrbot_turn.incoming_of(event).segments:
                if msg.type == "image":
                    refs.append(events.image_ref(msg))
                elif msg.type == "reply":
                    sender = str(msg.data.get('sender_id', '') or '').strip()
                    mid = str(msg.data.get('id', '') or '').strip()
                    try:
                        allowed = self._may_keep([sender] if sender else [], self._here(event), None,
                                                 [mid] if mid else [])
                    except Exception:
                        allowed = False
                    if allowed:
                        refs.extend(events.image_ref(child) for child in (msg.data.get("chain") or []))
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
        speaker = self._speaker(event)
        sender, name = str(speaker[0] or ''), str(speaker[1] or '')
        self_id = adapter_astrbot_turn.incoming_of(event).self_id
        if not here or not sender or sender == self_id or self._job_stale():
            return
        ids = self._source_ids(event)
        try:
            if not self._may_keep([sender], here, now, ids):
                return
        except Exception:
            return
        try:
            messages = adapter_astrbot_turn.incoming_of(event).segments
        except Exception:
            return
        sticker_refs = set(self._sticker_refs(event))
        for item in stickers.stickers_in_segments(messages):
            sticker_refs.update(ref for ref in (item.get('url'), item.get('file')) if ref)
        rows = state.setdefault(here, [])
        for msg in messages:
            ref = events.image_ref(msg)
            if ref and ref not in sticker_refs and not any(row['ref'] == ref and row['id'] == (ids[0] if ids else '') for row in rows):
                rows.append({'ref': ref, 'sender': sender, 'name': name, 'id': ids[0] if ids else '', 'ts': now, 'seen': False})
        del rows[:-RECENT_IMAGE_LIMIT]
        if not rows:
            state.pop(here, None)

    def _forget_recent_images(self, person='', source_ids=()):
        ids = set(str(x) for x in source_ids or ())
        state = getattr(self, '_recent_images', {})
        for here in list(state):
            state[here] = [row for row in state[here]
                           if not (person and row['sender'] == person) and row['id'] not in ids]
            if not state[here]:
                del state[here]

    async def _quoted_image_refs(self, event):
        refs = []
        for msg in adapter_astrbot_turn.incoming_of(event).segments:
            if msg.type != 'reply' or any(events.image_ref(c) for c in (msg.data.get('chain') or [])):
                continue
            mid = msg.data.get('id')
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

    def _load_image_cache(self) -> dict:
        try:
            if IMAGE_CACHE_PATH.exists():
                d = json.loads(IMAGE_CACHE_PATH.read_text(encoding="utf-8"))
                if isinstance(d, dict):
                    now = time.time()
                    active = {k: v for k, v in d.items() if not k.startswith("content:") or
                              (isinstance(v, dict) and 0 <= now - float(v.get("ts", 0) or 0) < 86400)}
                    if len(active) != len(d):
                        IMAGE_CACHE_PATH.write_text(json.dumps(active, ensure_ascii=False), encoding="utf-8")
                    return active
        except Exception:
            pass
        return {}

    def _save_image_cache(self, cache: dict) -> None:
        if self._job_stale():
            return  # someone (or a message) she may not keep, or something forgotten meanwhile
        try:
            # Calls may have added content entries while this address cache was in use.
            current = self._load_image_cache()
            cache.update({k: v for k, v in current.items() if k.startswith("content:") and k not in cache})
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
        if getattr(self, "_neutral_model", None) is not None:
            provider = None
        else:
            try:
                provider = await self.context.get_using_stt_provider_async(
                    getattr(event, "unified_msg_origin", "") or "")
            except Exception as exc:
                # No such method without AstrBot (or asking failed): QQ's own words below.
                logger.warning("[biocore] voice context failed: %s", exc)
                provider = None
        if provider is not None:
            try:
                texts = []
                for m in adapter_astrbot_turn.incoming_of(event).segments:
                    if m.type != "record":
                        continue
                    ref = str(m.data.get("url") or m.data.get("file") or m.data.get("path") or "").strip()
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
        # No speech-to-text provider from AstrBot: ask QQ itself about this voice.
        try:
            incoming = adapter_astrbot_turn.incoming_of(event)
            if not any(m.type == "record" for m in incoming.segments):
                return ""
            mid = str(incoming.message_id or "").strip()
            if not mid:
                return ""
            try:
                answer = await self._messenger(event).call("fetch_ptt_text", message_id=mid)
            except Exception as exc:
                logger.warning("[biocore] voice text from QQ failed: %s", type(exc).__name__)
                return ""
            words = ""
            if isinstance(answer, str):
                words = answer
            elif isinstance(answer, dict):
                for key in ("text", "content", "result"):
                    value = answer.get(key)
                    if isinstance(value, str) and value.strip():
                        words = value
                        break
            words = words.strip()[:300]
            if not words:
                logger.warning("[biocore] voice text from QQ: no words")
            return words[:600]
        except Exception as exc:
            logger.warning("[biocore] voice context failed: %s", type(exc).__name__)
            return ""

    async def _image_context(self, event) -> str:
        if not self._llm_allowed('image_caption'):
            return ''
        refs = self._image_refs(event)
        private = adapter_astrbot_turn.incoming_of(event).is_private
        addressed = private or self._addresses_her(event)
        if addressed and getattr(self, 'image_recognition_enabled', True):
            refs = list(dict.fromkeys(refs + await self._quoted_image_refs(event)))
        sticker_refs = self._sticker_refs(event) if getattr(self, '_stickers_on', None) and self._stickers_on() else []
        recent = []
        if addressed and not refs and not sticker_refs and getattr(self, 'image_recognition_enabled', True):
            now = time.time()
            sender = str(self._speaker(event)[0] or '')
            recent = [row for row in reversed(getattr(self, '_recent_images', {}).get(self._here(event), []))
                      if not row['seen']
                      and 0 <= now - row['ts'] <= RECENT_IMAGE_SECONDS][:RECENT_IMAGE_LOOK_LIMIT]
            recent.sort(key=lambda row: row['sender'] != sender)
            refs = list(dict.fromkeys(row['ref'] for row in recent))
        if sticker_refs:
            refs = list(dict.fromkeys(refs + sticker_refs))
        if not refs:
            return ''
        def cached(cache, ref):
            item = cache.get(_sha256(ref))
            if not isinstance(item, dict) or not item.get('caption'):
                return False
            if item.get('where') and item['where'] != self._here(event):
                return False
            owner = next((row['sender'] for row in recent if row['ref'] == ref), str(self._speaker(event)[0] or ''))
            if item.get('from_qq') and str(item['from_qq']) != owner:
                return False
            return not item.get('ts') or 0 <= time.time() - float(item['ts']) < 86400

        # Keep one selection through the lock; fetching a quote twice could change it.
        setattr(event, '_ams_image_refs', refs)
        setattr(event, '_ams_image_owners', {row['ref']: row['sender'] for row in recent})
        try:
            cache = self._load_image_cache()
            if all(cached(cache, ref) for ref in refs):
                result = "\n".join(stickers.look_line(cache[_sha256(ref)]) for ref in refs[:3]
                                   if cache[_sha256(ref)].get('caption'))
            else:
                self._group_reply_vision_active = getattr(self, '_group_reply_vision_active', 0) + 1
                try:
                    async with self._group_image_lock():
                        cache = self._load_image_cache()
                        if all(cached(cache, ref) for ref in refs):
                            result = "\n".join(stickers.look_line(cache[_sha256(ref)]) for ref in refs[:3]
                                               if cache[_sha256(ref)].get('caption'))
                        else:
                            result = await self._image_context_locked(event)
                finally:
                    self._group_reply_vision_active -= 1
            if result and not self._job_stale():
                self._image_last_used = time.time()
                cache = self._load_image_cache()
                seen = {ref for ref in refs[:3] if (cache.get(_sha256(ref)) or {}).get('caption')}
                here = self._here(event)
                sender = str(self._speaker(event)[0] or '')
                for row in getattr(self, '_recent_images', {}).get(here, []):
                    if row['ref'] in seen and (row in recent or row['sender'] == sender):
                        row['seen'] = True
                if here.startswith('group:'):
                    group = getattr(self, '_group_state', lambda: {})().get(here, {})
                    group['queue'] = [row for row in group.get('queue', [])
                                      if not (row[0] in seen and row[2] == sender)]
                    for rows in group.get('pending', []):
                        rows[:] = [row for row in rows if not (row[0] in seen and row[2] == sender)]
                if recent:
                    lines = []
                    for row in recent:
                        item = cache.get(_sha256(row['ref'])) or {}
                        line = stickers.look_line(item)
                        if line:
                            lines.append('%s%d秒前发的图：%s' % (
                                self._for_model(row.get('name') or '某人', event),
                                max(0, int(time.time() - row['ts'])), line))
                    return "\n".join(lines)
            return result
        finally:
            delattr(event, '_ams_image_refs')
            delattr(event, '_ams_image_owners')

    async def _image_context_locked(self, event) -> str:
        refs = getattr(event, '_ams_image_refs', None)
        if refs is None:
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
        where = self._here(event)
        sender = str(self._speaker(event)[0] or "")
        owners = getattr(event, '_ams_image_owners', {})
        for ref in refs:
            item = cache.get(_sha256(ref))
            if isinstance(item, dict) and (not item.get("where") or item.get("where") != where or
                                           str(item.get("from_qq") or "") != owners.get(ref, sender) or
                                           time.time() - float(item.get("ts", 0) or 0) >= 86400):
                cache.pop(_sha256(ref), None)
        missing = [r for r in refs if _sha256(r) not in cache or
                   time.time() - float(cache[_sha256(r)].get("ts", 0) or 0) >= 86400]
        if missing:
            try:
                # One look at a picture, the same question either way: what it shows, who of a
                # work is in it, what it means (stickers.LOOK_PROMPT). Always the vision provider.
                provider = self._vision_provider_for(event)
                if provider is not None:
                    for ref in missing[:3]:
                        caption, look = "", {}
                        try:
                            if stickers_on:
                                # one call: the look and whether she keeps it (step 2, 丙)
                                caption, look = await self._look_once(provider, ref, event)
                            else:
                                # the same look once; it does not go into her sticker library
                                reply = await self._model(provider).chat(
                                    prompt=stickers.LOOK_PROMPT, images=[ref])
                                look = stickers.parse_look(reply.text)
                                caption = str(look.get("caption") or "")
                        except Exception as exc:
                            logger.warning("[biocore] image caption failed: %s", exc)
                            caption, look = "", {}
                        if caption and look:
                            cache[_sha256(ref)] = stickers.cache_entry(
                                ref, look, owners.get(ref, sender), self._here(event), time.time())
                            if stickers_on and owners.get(ref, sender) == sender:
                                await self._maybe_keep(event, ref, look)
                    self._save_image_cache(cache)
            except Exception as exc:
                logger.warning("[biocore] image provider failed: %s", exc)
        lines = []
        for ref in refs[:3]:
            item = cache.get(_sha256(ref))
            if item:
                line = stickers.look_line(item)
                if line:
                    lines.append(line)
        self._image_last_used = time.time()
        if not lines:
            return ""
        return "\n".join(lines)
