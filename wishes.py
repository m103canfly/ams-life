# -*- coding: utf-8 -*-
"""Wish storage and limits; the caller performs privacy checks before adding."""
import json
import os
import tempfile
import threading
from datetime import datetime, timedelta

try:
    from . import memory_meta, discretion
except ImportError:
    import memory_meta
    import discretion

# These limits keep the owner's review manageable and prevent a burst of requests.
OPEN_MAX = 30
DAILY_MAX = 5
WHAT_MIN, WHAT_MAX, WHY_MAX = 20, 60, 100
DUPLICATE_THRESHOLD = 0.88  # Same deterministic bigram similarity threshold as memory dedup.
OPEN_STATES = ("新", "好", "先放着")
STATES = OPEN_STATES + ("不要",)
LOCK = threading.RLock()
BLOCK_CATEGORIES = ("网址不能读", "点不了", "看不到图", "工具没有")
BLOCK_DAYS = 7  # A short aggregate, with no message text or addresses.
NOTEBOOK_WISH_MAX = 2


def read(path):
    if not path.exists():
        return {"next_id": 1, "items": [], "daily": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ValueError("invalid wish store")
    return data


def write(path, data):
    fd, name = tempfile.mkstemp(prefix=".wishes-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def add(path, what, why, where, people=(), source_ids=(), speaker="", now=None):
    now = datetime.now() if now is None else now
    what, why = str(what or "").strip(), str(why or "").strip()
    if not WHAT_MIN <= len(what) <= WHAT_MAX or len(why) > WHY_MAX:
        return "字数不合适"
    if where not in ("reply", "life", "notebook"):
        return "不能记下"
    with LOCK:
        data = read(path)
        items = data["items"]
        if any(memory_meta.text_similarity(what, str(x.get("what") or "")) >= DUPLICATE_THRESHOLD
               for x in items if x.get("status") in OPEN_STATES):
            return "这条已经记过了"
        if sum(x.get("status") in OPEN_STATES for x in items) >= OPEN_MAX:
            return "满了，先挑一条合并或撤掉"
        day = now.date().isoformat()
        daily = data.setdefault("daily", {})
        if int(daily.get(day, 0)) >= DAILY_MAX:
            return "今天记满了，明天再记"
        number = int(data.get("next_id", 1))
        items.append({"id": number, "what": what, "why": why, "time": now.isoformat(),
                      "where": where, "status": "新", "marked_at": "",
                      "origin": discretion.make_origin(discretion.SELF),
                      "people": sorted(set(str(p) for p in people if p)),
                      "source_ids": sorted(set(str(s) for s in source_ids if s)),
                      "speaker": str(speaker or "")})
        data["next_id"] = number + 1
        data["daily"] = {day: int(daily.get(day, 0)) + 1}
        write(path, data)
    return "记下了"


def set_status(path, number, status, now=None):
    if status not in STATES:
        return False
    with LOCK:
        data = read(path)
        for item in data["items"]:
            if str(item.get("id")) == str(number):
                if item.get("status") not in OPEN_STATES and status in OPEN_STATES and sum(
                        x.get("status") in OPEN_STATES for x in data["items"]) >= OPEN_MAX:
                    return False
                item["status"] = status
                item["marked_at"] = (now or datetime.now()).isoformat()
                write(path, data)
                return True
    return False


def forget(path, person="", source_ids=()):
    if not path.exists():
        return 0
    ids = {str(s) for s in source_ids if s}
    with LOCK:
        data = read(path)
        old = data["items"]
        data["items"] = [x for x in old if not (
            person and (str(person) == x.get("speaker") or str(person) in x.get("people", []))
            or ids.intersection(x.get("source_ids", [])))]
        if len(old) != len(data["items"]):
            write(path, data)
        return len(old) - len(data["items"])


def count_block(path, category, now=None):
    if category not in BLOCK_CATEGORIES:
        return
    day = (now or datetime.now()).date()
    with LOCK:
        data = read(path)
        counts = data.setdefault("blocks", {})
        key = day.isoformat()
        row = counts.setdefault(key, {})
        row[category] = int(row.get(category, 0)) + 1
        cutoff = (day - timedelta(days=BLOCK_DAYS - 1)).isoformat()
        data["blocks"] = {k: v for k, v in counts.items() if cutoff <= k <= key}
        write(path, data)


def materials(path, now=None):
    day = (now or datetime.now()).date()
    cutoff = (day - timedelta(days=BLOCK_DAYS - 1)).isoformat()
    data = read(path)
    lines = ["%s：%s" % (day_key, "、".join("%s %d 次" % (cat, int(row.get(cat, 0)))
              for cat in BLOCK_CATEGORIES if row.get(cat)))
             for day_key, row in sorted(data.get("blocks", {}).items())
             if cutoff <= day_key <= day.isoformat() and isinstance(row, dict)]
    lines += ["状态：%s；愿望：%s；原因：%s" % (x.get("status", ""), x.get("what", ""), x.get("why", ""))
              for x in data["items"]]
    return lines
