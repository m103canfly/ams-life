# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
# ams-life — her voice: what of a reply is said out loud, and how it is asked for.
"""GPT-SoVITS runs as a local service (api_v2.py on 127.0.0.1); this module only turns one
of her replies into words to speak, builds the JSON body api_v2 expects, and posts it.

Nothing here imports AstrBot, so it can be tested on its own: `speakable`, `payload`,
`post` (the HTTP call). A failing service must never cost her the reply, so the caller
never waits on this before the words go out.
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

# the shortest useful line: below this it is not worth a voice message
MIN_CHARS = 1

# what she picked as a QQ face: said out loud it would be "[表情:微笑]"
_FACE = re.compile(r"\[表情[:：][^\]\n]{0,12}\]")
_STICKER = re.compile(r"\[表情包[^\]\n]*\]")
_NEXT_MESSAGE = re.compile(r"【下一条】")
# the other things a message can carry, which are not words
_CARRIED = re.compile(r"\[(?:图片|语音|视频|文件|聊天记录|戳一戳|卡片|分享|位置|音乐|骰子|猜拳|名片|消息)\]")
# links, inline code and code blocks are read aloud as noise
_NOT_SPOKEN = re.compile(r"```.*?```|`[^`\n]*`|https?://\S+|www\.\S+", re.S)
# markdown marks, kept out of the mouth
_MARKS = re.compile(r"[*_#>]+")
_SPACES = re.compile(r"[ \t\u3000]+")
_END = re.compile(r"[。！？!?…～~.]$")


def speakable(text, limit: int = 100) -> str:
    """What of `text` she says: no faces, no tags, no links, no markdown marks; at most
    `limit` characters, cut back to a sentence end when there is one to cut back to."""
    s = str(text or "")
    if not s.strip():
        return ""
    s = _NOT_SPOKEN.sub(" ", s)
    s = _FACE.sub(" ", s)
    s = _STICKER.sub(" ", s)
    s = _NEXT_MESSAGE.sub(" ", s)
    s = _CARRIED.sub(" ", s)
    s = _MARKS.sub("", s)
    s = _SPACES.sub(" ", s)
    s = "\n".join(line.strip() for line in s.splitlines() if line.strip())
    s = s.strip()
    if limit and len(s) > int(limit):
        cut = s[: int(limit)]
        for i in range(len(cut) - 1, max(0, int(limit) // 2), -1):
            if _END.match(cut[i]):
                cut = cut[: i + 1]
                break
        s = cut.strip()
    return s if len(s) >= MIN_CHARS else ""


def payload(text: str, ref_audio: str, prompt_text: str = "", prompt_lang: str = "zh",
            text_lang: str = "zh", speed: float = 1.0, media_type: str = "wav") -> dict:
    """The body of one /tts call: the fields api_v2.py reads, the rest left to its defaults."""
    return {
        "text": str(text or ""),
        "text_lang": str(text_lang or "zh"),
        "ref_audio_path": str(ref_audio or ""),
        "prompt_text": str(prompt_text or ""),
        "prompt_lang": str(prompt_lang or "zh"),
        "top_k": 15,
        "top_p": 1,
        "temperature": 1,
        "text_split_method": "cut5",
        "batch_size": 1,
        "speed_factor": float(speed or 1.0),
        "media_type": str(media_type or "wav"),
        "streaming_mode": False,
        "parallel_infer": True,
        "repetition_penalty": 1.35,
    }


def post(base_url: str, body: dict, timeout: float = 30.0) -> bytes:
    """One /tts call; the wav bytes back, or an exception. Called from a worker thread."""
    url = str(base_url or "").rstrip("/") + "/tts"
    req = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
        method="POST")
    with urllib.request.urlopen(req, timeout=float(timeout)) as resp:
        data = resp.read()
    if not data or len(data) < 44:   # a wav header alone is no sound
        raise RuntimeError("tts: the service sent no audio")
    return data

# ---------------------------------------------------------------------------
# her voices: the weights each version reads, from the fine-tunes of 2026-10-30.
# Relative to the GPT-SoVITS folder (tts_dir). A version with no fine-tune of its
# own (v2ProPlus here) points at the stock one, so the list never lies.
VOICES = {
    "v4":        ("SoVITS_weights_v4/amslifev4_e5_s125_l32.pth", "GPT_weights_v4/amslifev4-e20.ckpt"),
    "v3":        ("SoVITS_weights_v3/ams-life3_e5_s125_l32.pth", "GPT_weights_v2Pro/ams-life3-e20.ckpt"),
    "v2Pro":     ("SoVITS_weights_v2Pro/ams-life2_e5_s125.pth", "GPT_weights_v2Pro/ams-life2-e20.ckpt"),
    "v2ProPlus": ("SoVITS_weights_v2ProPlus/ams-life2-plus_e5_s125.pth", "GPT_weights_v2Pro/ams-life2-plus-e20.ckpt"),
    "v2":        ("SoVITS_weights_v2/amslifev2_e5_s125.pth", "GPT_weights_v2/amslifev2-e20.ckpt"),
    "v1":        ("SoVITS_weights/amslifev1_e5_s125.pth", "GPT_weights/amslifev1-e20.ckpt"),
}
VERSION_ORDER = list(VOICES)


def voice_files(root, version: str):
    """The (sovits, gpt) paths of one version, absolute; ("", "") when it is not there."""
    pair = VOICES.get(str(version or "").strip())
    if not pair:
        return "", ""
    out = []
    for rel in pair:
        p = Path(str(root)) / rel
        out.append(str(p) if p.is_file() else "")
    return (out[0], out[1]) if all(out) else ("", "")


def set_weights(base_url: str, gpt_path: str, sovits_path: str, timeout: float = 120.0) -> None:
    """Tell a running api_v2 which weights to speak with (it writes them back to its yaml)."""
    for route, path in (("/set_gpt_weights", gpt_path), ("/set_sovits_weights", sovits_path)):
        if not path:
            continue
        url = str(base_url).rstrip("/") + route + "?weights_path=" + urllib.parse.quote(path)
        with urllib.request.urlopen(url, timeout=float(timeout)) as resp:
            resp.read()
