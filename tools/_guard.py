"""Where the offline tools may write.

Old chat logs and old memories are real people's words. The tools only ever write
into a fresh folder of their own: never into a running AstrBot's data folder, never
into this repository (it is public), never over something that is already there.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Refused(SystemExit):
    pass


def _inside(path, parent) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def live_reason(path) -> str:
    """Why `path` looks like (part of) a live data folder, or ''."""
    parts = [p.lower() for p in Path(path).resolve().parts]
    for a, b in zip(parts, parts[1:]):
        if a == "astrbot" and b == "data":
            return "it is inside an AstrBot data folder (astrbot/data)"
    if "plugin_data" in parts:
        return "it is inside a plugin_data folder"
    return ""


def output_file(path, label="output") -> Path:
    """Check one file a tool is about to write next to its own outputs: outside the repository
    and outside any AstrBot data folder; otherwise stop with a message."""
    out = Path(path).resolve()
    why = live_reason(out)
    if why:
        raise Refused("refusing to write %s to %s: %s" % (label, out, why))
    if _inside(out, ROOT):
        raise Refused("refusing to write %s to %s: it is inside the repository" % (label, out))
    return out


def output_dir(path, label="output") -> Path:
    """Check an output folder and create it. It must be new or empty, outside the
    repository and outside any AstrBot data folder; otherwise stop with a message."""
    out = Path(path).resolve()
    why = live_reason(out)
    if why:
        raise Refused("refusing to write %s to %s: %s" % (label, out, why))
    if _inside(out, ROOT):
        raise Refused("refusing to write %s to %s: it is inside the repository" % (label, out))
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise Refused("refusing to write %s to %s: it exists and is not an empty folder" % (label, out))
    out.mkdir(parents=True, exist_ok=True)
    return out
