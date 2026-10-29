"""Her pictures for the panel's look (pages/dashboard/look.css, look.js), read only.

The avatar and the half-body art are Kuro Games' art, so they never ship with ams-life. The owner copies them
into <data dir>/ui/ when installing: avatar.png and art.png (or .jpg / .webp). page/look hands them to the panel
as data URLs. A missing file, a file too big, a link, or anything that does not start like a picture is left out,
and the panel shows its own drawn mark instead.
"""
from __future__ import annotations

import base64
from pathlib import Path

UI_FOLDER = "ui"
NAMES = ("avatar", "art")
EXTS = (".png", ".jpg", ".jpeg", ".webp")
MAX_BYTES = 4 * 1024 * 1024


def picture_kind(head: bytes) -> str:
    """'png', 'jpeg' or 'webp' from a file's first bytes; '' for anything else."""
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return ""


def _read_one(folder: Path, name: str) -> str:
    for ext in EXTS:
        p = folder / (name + ext)
        try:
            if p.is_symlink() or not p.is_file() or p.stat().st_size > MAX_BYTES:
                continue
            data = p.read_bytes()
        except OSError:
            continue
        kind = picture_kind(data[:16])
        if kind and len(data) <= MAX_BYTES:
            return "data:image/%s;base64,%s" % (kind, base64.b64encode(data).decode("ascii"))
    return ""


def read_ui_images(data_dir) -> dict:
    """{'avatar': data URL or '', 'art': data URL or ''} from <data_dir>/ui/."""
    folder = Path(data_dir) / UI_FOLDER
    return {name: _read_one(folder, name) for name in NAMES}
