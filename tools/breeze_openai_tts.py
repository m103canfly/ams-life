# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Local OpenAI-compatible bridge for Breeze TTS."""
import asyncio
import io
import json
import os
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import wave

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response

ROOT = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.join(ROOT, 'breeze.json')
PORT = int(os.environ.get('BREEZE_OPENAI_PORT', '9881'))
DEFAULT = {'breeze_url': 'http://127.0.0.1:7860', 'ref_audio': '', 'ref_text': '',
           'seed': 1234, 'cfg_scale': 1, 'ffmpeg': ''}
LOCK = threading.Lock()
app = FastAPI(title='Breeze TTS (OpenAI-compatible)')


class BusyError(Exception):
    pass


def conf():
    data = dict(DEFAULT)
    try:
        with open(CONF, 'r', encoding='utf-8') as f:
            values = json.load(f)
        if isinstance(values, dict):
            data.update(values)
    except (OSError, ValueError):
        pass
    return data


def local_url(url):
    try:
        parsed = urllib.parse.urlsplit(url)
        return (parsed.scheme == 'http' and parsed.hostname in ('127.0.0.1', 'localhost', '::1')
                and parsed.username is None and parsed.password is None
                and parsed.path in ('', '/') and not parsed.query and not parsed.fragment
                and (parsed.port is None or 1 <= parsed.port <= 65535)
                and not any(ch in url for ch in '\r\n\t'))
    except (ValueError, TypeError):
        return False


def ref_ok(c):
    try:
        path, text = c.get('ref_audio'), c.get('ref_text')
        return (isinstance(text, str) and bool(text.strip()) and os.path.isfile(path)
                and os.path.getsize(path) <= 20 * 1024 * 1024)
    except (OSError, TypeError, ValueError):
        return False


def select_reference(c, voice):
    tones = c.get('tones')
    if isinstance(tones, dict):
        name = voice if isinstance(voice, str) and voice not in ('', 'alloy', 'v4') and voice in tones else '平静'
        for tone in (name, '平静') if name != '平静' else (name,):
            entries = tones.get(tone)
            if isinstance(entries, list):
                for entry in entries:
                    if isinstance(entry, dict) and ref_ok(entry):
                        return dict(c, ref_audio=entry['ref_audio'], ref_text=entry['ref_text'])
    return c


def multipart(fields, file_field, filename, data):
    boundary = uuid.uuid4().hex
    chunks = []
    for name, value in fields.items():
        chunks.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
                       % (boundary, name, value)).encode('utf-8'))
    # The filename is fixed, so local path characters never enter the header.
    chunks.append(('--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\n'
                   'Content-Type: application/octet-stream\r\n\r\n'
                   % (boundary, file_field, filename)).encode('utf-8'))
    chunks.extend((data, ('\r\n--%s--\r\n' % boundary).encode('ascii')))
    return b''.join(chunks), 'multipart/form-data; boundary=' + boundary


def sample_rate_of(headers):
    try:
        rate = int(headers.get('X-Sample-Rate', ''))
        return rate if 8000 <= rate <= 48000 else 24000
    except (TypeError, ValueError, OverflowError):
        return 24000


def pcm_to_wav(pcm, rate):
    if not pcm or len(pcm) % 2:
        raise ValueError('invalid PCM')
    out = io.BytesIO()
    with wave.open(out, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes(pcm)
    return out.getvalue()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def call_breeze(text, c, *, opener=urllib.request.urlopen, sleep=time.sleep):
    with LOCK:
        if not local_url(c.get('breeze_url')) or not ref_ok(c):
            raise ValueError('invalid local configuration')
        try:
            with open(c['ref_audio'], 'rb') as f:
                audio = f.read(20 * 1024 * 1024 + 1)
            if len(audio) > 20 * 1024 * 1024:
                raise ValueError('invalid reference')
            body, content_type = multipart({'text': text, 'ref_text': c['ref_text'],
                'cfg_scale': c.get('cfg_scale', 1), 'seed': c.get('seed', 1234)},
                'ref_audio', 'reference.wav', audio)
            req = urllib.request.Request(c['breeze_url'].rstrip('/') + '/v1/audio/speech',
                data=body, headers={'Content-Type': content_type}, method='POST')
            if opener is urllib.request.urlopen:
                opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect()).open
            for attempt in range(2):
                try:
                    with opener(req, timeout=300) as resp:
                        return resp.read(), sample_rate_of(resp.headers)
                except urllib.error.HTTPError as exc:
                    if exc.code != 409:
                        raise
                    if attempt:
                        raise BusyError('busy') from None
                    sleep(2)
        except BusyError:
            raise
        except Exception:
            raise RuntimeError('Breeze request failed') from None


def listening(c):
    url = c.get('breeze_url')
    if not local_url(url):
        return False
    parsed = urllib.parse.urlsplit(url)
    try:
        with socket.create_connection((parsed.hostname, parsed.port or 80), timeout=0.3):
            return True
    except OSError:
        return False


def transcode(wav, fmt, ffmpeg):
    if not ffmpeg or not os.path.isfile(ffmpeg):
        return None
    codec = ['-codec:a', 'libmp3lame', '-b:a', '48k', '-f', 'mp3'] if fmt == 'mp3' else \
            ['-codec:a', 'libopus', '-b:a', '32k', '-f', 'ogg']
    try:
        result = subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-i', 'pipe:0',
                                 *codec, 'pipe:1'], input=wav, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, check=True, timeout=120)
        return result.stdout or None
    except (OSError, subprocess.SubprocessError):
        return None


@app.get('/health')
def health():
    return {'ok': True, 'breeze': listening(conf())}


@app.get('/v1/models')
def models():
    return {'object': 'list', 'data': [{'id': 'breeze-tts-2', 'object': 'model'}]}


@app.post('/v1/audio/speech')
async def speech(request: Request):
    body = await request.json()
    text = str(body.get('input') or '').strip()
    if not text:
        raise HTTPException(status_code=400, detail='input is empty')
    c = select_reference(conf(), body.get('voice'))
    if not local_url(c.get('breeze_url')) or not ref_ok(c):
        raise HTTPException(status_code=503, detail='invalid local configuration')
    try:
        pcm, rate = await asyncio.to_thread(call_breeze, text, c)
        audio = pcm_to_wav(pcm, rate)
    except BusyError:
        print('[breeze-tts] busy', flush=True)
        raise HTTPException(status_code=503, detail='busy') from None
    except Exception:
        print('[breeze-tts] request failed', flush=True)
        raise HTTPException(status_code=502, detail='Breeze failed') from None
    fmt = str(body.get('response_format') or 'wav').lower()
    if fmt in ('mp3', 'opus', 'ogg'):
        audio = await asyncio.to_thread(transcode, audio, fmt, c.get('ffmpeg'))
        if audio is None:
            raise HTTPException(status_code=500, detail='ffmpeg transcode failed')
        return Response(content=audio, media_type='audio/mpeg' if fmt == 'mp3' else 'audio/ogg')
    return Response(content=audio, media_type='audio/wav')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=PORT, log_level='warning', access_log=False)
