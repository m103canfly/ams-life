"""Vision adapter, accounting and short-lived caption cache."""
import asyncio
import base64
import hashlib
import io
import json
import threading
import time
import types
import urllib.error
import urllib.request
from pathlib import Path

try:
    from .common import DATA_DIR, logger
    from . import stickers, mixin_attention
except ImportError:
    from common import DATA_DIR, logger
    import stickers
    import mixin_attention

VISION_MAX_SIDE = 1280
VISION_MAX_BYTES = 1024 * 1024
_pillow_warning_lock = threading.Lock()
_pillow_warned = False


def _legacy_counts(day):
    path = DATA_DIR / 'vision_counts.json'
    try:
        data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        return data if isinstance(data, dict) and data.get('day') == day else {}
    except Exception:
        return {}


def vision_for_panel(config):
    day = time.strftime('%Y-%m-%d')
    ledger = mixin_attention._read_json(mixin_attention.SPEND_PATH, {})
    today = ledger.get(day) or {}
    count = today.get('vision_calls')
    if count is None:
        count = _legacy_counts(day).get('calls', 0)
    sources = ledger.get(day + '-vision') or {}
    result = {kind: int(sources.get(kind, 0) or 0) for kind in ('reply', 'browse', 'owner_add', 'screenshot')}
    result['calls'] = int(count or 0)
    result['unattributed'] = max(0, result['calls'] - sum(result[k] for k in ('reply', 'browse', 'owner_add', 'screenshot')))
    result['last'] = float(sources.get('last', 0) or 0)
    return result


def _response(text):
    return types.SimpleNamespace(completion_text=text)


def _bytes(ref):
    try:
        if ref.startswith('data:') and ';base64,' in ref:
            data = base64.b64decode(ref.split(',', 1)[1], validate=True)
        elif ref.startswith(('https://', 'http://')):
            if not stickers.check_image_url(ref)[0]:
                return b''
            data = stickers.fetch_picture(ref)
        else:
            path = Path(ref)
            if not path.is_file() or path.stat().st_size > stickers.MAX_BYTES:
                return b''
            with path.open('rb') as stream:
                header = stream.read(16)
                if not stickers.sniff(header):
                    return b''
                data = header + stream.read(stickers.MAX_BYTES + 1 - len(header))
        return data if len(data) <= stickers.MAX_BYTES and stickers.sniff(data) else b''
    except Exception:
        return b''


def _data_url(data):
    kind = stickers.sniff(data)
    if not kind or len(data) > stickers.MAX_BYTES:
        raise ValueError('image unavailable')
    mime = 'jpeg' if kind == 'jpg' else kind
    return 'data:image/' + mime + ';base64,' + base64.b64encode(data).decode('ascii')


def _prepared(data):
    """Adapted from AstrBot 4.29.3, astrbot/core/utils/media_utils.py, _compress_image_sync.

    Unlike AstrBot, animated images use their first frame.
    """
    global _pillow_warned
    try:
        from PIL import Image
    except ImportError:
        with _pillow_warning_lock:
            if not _pillow_warned:
                logger.warning('[ams-life] Pillow unavailable; sending original image')
                _pillow_warned = True
        return data

    try:
        with Image.open(io.BytesIO(data)) as opened:
            opened.seek(0)
            alpha = opened.mode in {'RGBA', 'LA'} or (opened.mode == 'P' and 'transparency' in opened.info)
            image = opened.convert('RGBA' if alpha else 'RGB')
    except (OSError, ValueError, EOFError) as exc:
        logger.warning('[ams-life] image preparation failed: %s', type(exc).__name__)
        return data

    with image:
        image.thumbnail((VISION_MAX_SIDE, VISION_MAX_SIDE), Image.Resampling.LANCZOS)
        while True:
            for quality in ((95,) if alpha else (95, 85, 75, 65, 55, 45, 35, 25)):
                output = io.BytesIO()
                options = {'optimize': True}
                if not alpha:
                    options['quality'] = quality
                image.save(output, 'PNG' if alpha else 'JPEG', **options)
                result = output.getvalue()
                if len(result) <= VISION_MAX_BYTES:
                    return result
            if max(image.size) <= 1:
                raise ValueError('image cannot be compressed')
            image.thumbnail((max(1, image.width * 3 // 4), max(1, image.height * 3 // 4)),
                            Image.Resampling.LANCZOS)


class ImageAPI:
    provider_config = {'id': 'image_api', 'modalities': ['text', 'image']}

    def __init__(self, plugin):
        self.plugin = plugin

    async def text_chat(self, prompt='', image_urls=None, **kwargs):
        def request():
            try:
                cfg = self.plugin.api_config.get('image') or {}
                base = str(cfg.get('base_url') or '').rstrip('/')
                key = ''
                store = getattr(self.plugin, '_key_store', None)   # the new program's 4a store
                if store is not None:
                    try:
                        key = str(store.get('vision') or '')
                    except Exception:
                        key = ''
                else:
                    key = str(cfg.get('api_key') or '')
                model = str(self.plugin.config.get(kwargs.get('model_config', 'vision_image_api_model')) or '').strip()
                if not base or not model:
                    raise ValueError()
                content = [{'type': 'text', 'text': prompt}]
                for ref in image_urls or []:
                    data = _bytes(str(ref))
                    if not data:
                        raise ValueError('image unavailable')
                    content.append({'type': 'image_url', 'image_url': {'url': _data_url(_prepared(data))}})
                payload = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': content}]}).encode('utf-8')
                req = urllib.request.Request(base + '/chat/completions', data=payload, method='POST',
                                             headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=120) as resp:
                    answer = json.loads(resp.read().decode('utf-8'))
                usage = answer.get('usage') or {}
                return types.SimpleNamespace(
                    completion_text=str(answer['choices'][0]['message']['content'] or ''),
                    usage=types.SimpleNamespace(input_other=usage.get('prompt_tokens', 0),
                                                input_cached=0, output=usage.get('completion_tokens', 0)))
            except urllib.error.HTTPError as exc:
                logger.warning('[ams-life] vision request status %d', exc.code)
            except Exception:
                logger.warning('[ams-life] vision request status %d', 0)
            raise RuntimeError('vision request failed') from None
        return await asyncio.to_thread(request)


class VisionGate:
    def __init__(self, plugin, provider, event, source="reply"):
        self.plugin, self.provider, self.event = plugin, provider, event
        self.source = source if source in ("reply", "browse", "owner_add", "screenshot") else "reply"

    def __getattr__(self, name):
        return getattr(self.provider, name)

    async def text_chat(self, prompt='', image_urls=None, **kwargs):
        p = self.plugin
        refs = image_urls or []
        images = []
        for item in refs:
            data = await asyncio.to_thread(_bytes, str(item))
            if not data:
                raise RuntimeError('image unavailable') from None
            images.append((data, _data_url(data)))
        ref = str(refs[0]) if len(refs) == 1 else ''
        digest = hashlib.sha256(images[0][0]).hexdigest() if ref else ''
        sender = str(p._speaker(self.event)[0] or '') if self.event is not None else ''
        place = str(p._here(self.event) or '') if self.event is not None else 'owner'
        scope = hashlib.sha256(place.encode('utf-8')).hexdigest()
        key = 'content:' + scope + ':' + digest
        lock = getattr(p, '_vision_lock', None)
        if lock is None:
            lock = p._vision_lock = asyncio.Lock()
        async with lock:
            cache = p._load_image_cache()
            now = time.time()
            item = cache.get(key) if digest else None
            if isinstance(item, dict) and 0 <= now - float(item.get('ts', 0)) < 86400 and item.get('caption'):
                caption = item['caption']
                senders = item.get('from_qqs') or ([item.get('from_qq')] if item.get('from_qq') else [])
                if sender and sender not in senders and not p._job_stale():
                    item['from_qqs'] = senders + [sender]
                    p._save_image_cache(cache)
                return _response(json.dumps({'caption': caption}) if prompt == stickers.LOOK_PROMPT else caption)
            try:
                day = time.strftime('%Y-%m-%d')
                counts = _legacy_counts(day)
                ledger = mixin_attention._read_json(mixin_attention.SPEND_PATH, {})
                today = ledger.setdefault(day, {})
                used = int(today.get('vision_calls', counts.get('calls', 0)) or 0)
                number = max(1, len(refs))
                today['vision_calls'] = used + number
                sources = ledger.setdefault(day + '-vision', {})
                sources[self.source] = int(sources.get(self.source, 0) or 0) + number
                sources['last'] = now
                for old in sorted(ledger)[:-30]:
                    ledger.pop(old, None)
                mixin_attention._write_json(mixin_attention.SPEND_PATH, ledger)
            except Exception:
                logger.warning('[ams-life] vision count could not be saved')
            resp = await self.provider.text_chat(prompt=prompt, image_urls=[item[1] for item in images], **kwargs)
            raw = str(getattr(resp, 'completion_text', '') or '')
            caption = stickers.parse_look(raw).get('caption', '') if prompt == stickers.LOOK_PROMPT else raw.strip()[:1600]
            if digest and caption and not p._job_stale():
                cache[key] = {'caption': caption, 'from_qq': sender, 'from_qqs': [sender] if sender else [],
                              'where': place, 'ts': now}
                p._save_image_cache(cache)
            return resp
