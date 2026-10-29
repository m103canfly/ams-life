# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
# ams-life / GPT-SoVITS: an OpenAI-compatible /v1/audio/speech in front of api_v2.
#
# Why: AstrBot already speaks through "OpenAI TTS API" providers, so the whole voice can be
# plugged in from 后台 -> 服务提供商, with no plugin code at all. This file is that plug:
#
#   POST /v1/audio/speech   {"model": "...", "voice": "...", "input": "...", "response_format": "wav"}
#   GET  /v1/models         the models this server offers
#   GET  /health            is api_v2 up
#
# It starts api_v2 itself (127.0.0.1:9880) if nothing is listening, points it at the version
# in voices.json, and forwards the text. Only listens on 127.0.0.1.
import json
import os
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response

ROOT = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.join(ROOT, "voices.json")
API = "http://127.0.0.1:9880"
PORT = int(os.environ.get("GSV_OPENAI_PORT", "9881"))

DEFAULT = {
    "voice": "aimisi",
    "version": "v4",
    # the reference clip and its exact words are the owner's, set in voices.json next to this file
    # (never in this repository): {"ref_audio": "<path of a 3-10 s clip>", "prompt_text": "<its words>"}
    "ref_audio": "",
    "prompt_text": "",
    "prompt_lang": "zh",
    "text_lang": "zh",
    "speed": 1.0,
}
VOICES = {
    "v4": ("SoVITS_weights_v4/amslifev4_e5_s125_l32.pth", "GPT_weights_v4/amslifev4-e20.ckpt"),
    "v3": ("SoVITS_weights_v3/ams-life3_e5_s125_l32.pth", "GPT_weights_v2Pro/ams-life3-e20.ckpt"),
    "v2Pro": ("SoVITS_weights_v2Pro/ams-life2_e5_s125.pth", "GPT_weights_v2Pro/ams-life2-e20.ckpt"),
    "v2ProPlus": ("SoVITS_weights_v2ProPlus/ams-life2-plus_e5_s125.pth", "GPT_weights_v2Pro/ams-life2-plus-e20.ckpt"),
    "v2": ("SoVITS_weights_v2/amslifev2_e5_s125.pth", "GPT_weights_v2/amslifev2-e20.ckpt"),
    "v1": ("SoVITS_weights/amslifev1_e5_s125.pth", "GPT_weights/amslifev1-e20.ckpt"),
}

app = FastAPI(title="GPT-SoVITS (OpenAI-compatible TTS)")
_started = {"proc": None, "voice": None}


def conf() -> dict:
    data = dict(DEFAULT)
    try:
        with open(CONF, "r", encoding="utf-8") as f:
            data.update(json.load(f) or {})
    except Exception:
        pass
    return data


def listening(port: int = 9880) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.3):
            return True
    except OSError:
        return False


def ensure_api() -> bool:
    """api_v2 up on 9880, or started here (it loads the models: slow the first time)."""
    if listening():
        return True
    python = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
    if not os.path.isfile(python):
        python = sys.executable
    _started["proc"] = subprocess.Popen(
        [python, "api_v2.py", "-a", "127.0.0.1", "-p", "9880"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=0x08000000 if os.name == "nt" else 0)
    for _ in range(180):
        if listening():
            _started["voice"] = None
            return True
        if _started["proc"].poll() is not None:
            return False
        time.sleep(1)
    return False


def set_voice(version: str) -> None:
    pair = VOICES.get(version or "")
    if not pair or _started["voice"] == version:
        return
    for route, rel in zip(("/set_sovits_weights", "/set_gpt_weights"), pair):
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            continue
        url = API + route + "?weights_path=" + urllib.parse.quote(path)
        with urllib.request.urlopen(url, timeout=180) as resp:
            resp.read()
    _started["voice"] = version


def _transcode(wav: bytes, fmt: str):
    """wav -> mp3/ogg for chats that would rather not carry 300 KB a sentence."""
    ffmpeg = os.path.join(ROOT, "ffmpeg", "ffmpeg.exe")
    if not os.path.isfile(ffmpeg):
        return None
    import subprocess as sp
    import tempfile
    src = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    src.write(wav); src.close()
    dst = src.name.replace(".wav", "." + ("ogg" if fmt == "ogg" else fmt))
    try:
        codec = ["-codec:a", "libmp3lame", "-b:a", "48k"] if fmt == "mp3" else \
                ["-codec:a", "libopus", "-b:a", "32k"]
        sp.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", src.name, *codec, dst],
               check=True, timeout=120)
        with open(dst, "rb") as f:
            return f.read()
    except Exception as exc:
        print("[openai-tts] transcode failed: %s" % exc, flush=True)
        return None
    finally:
        for p in (src.name, dst):
            try:
                os.remove(p)
            except OSError:
                pass


@app.get("/health")
def health():
    return {"ok": True, "api_v2": listening(), "voice": conf().get("version")}


@app.get("/v1/models")
def models():
    return {"object": "list",
            "data": [{"id": "gpt-sovits-%s" % v, "object": "model"} for v in VOICES]}


@app.post("/v1/audio/speech")
async def speech(request: Request):
    body = await request.json()
    text = str(body.get("input") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="input is empty")
    c = conf()
    version = str(body.get("voice") or c.get("version") or "v4")
    if version not in VOICES:
        version = str(c.get("version") or "v4")
    if not ensure_api():
        raise HTTPException(status_code=503, detail="api_v2 would not start")
    try:
        set_voice(version)
    except Exception as exc:                     # keep speaking with whatever it had
        print("[openai-tts] voice switch failed: %s" % exc, flush=True)
    payload = {
        "text": text,
        "text_lang": c.get("text_lang", "zh"),
        "ref_audio_path": c.get("ref_audio"),
        "prompt_text": c.get("prompt_text", ""),
        "prompt_lang": c.get("prompt_lang", "zh"),
        "speed_factor": float(body.get("speed") or c.get("speed") or 1.0),
        "text_split_method": "cut5",
        "media_type": "wav",
        "streaming_mode": False,
    }
    req = urllib.request.Request(API + "/tts", method="POST",
                                 data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            audio = resp.read()
    except Exception as exc:
        raise HTTPException(status_code=502, detail="api_v2: %s" % str(exc)[:200])
    if not audio or len(audio) < 44:
        raise HTTPException(status_code=502, detail="api_v2 sent no audio")
    fmt = str(body.get("response_format") or "wav").lower()
    if fmt in ("mp3", "opus", "ogg"):
        audio, media = _transcode(audio, fmt), ("audio/mpeg" if fmt == "mp3" else "audio/ogg")
        if audio is None:
            raise HTTPException(status_code=500, detail="ffmpeg is not there to transcode")
        return Response(content=audio, media_type=media)
    return Response(content=audio, media_type="audio/wav")


if __name__ == "__main__":
    print("GPT-SoVITS OpenAI-compatible TTS on http://127.0.0.1:%d/v1" % PORT, flush=True)
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
