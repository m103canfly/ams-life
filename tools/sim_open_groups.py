"""Offline estimate for self-initiated group browsing; no plugin or network calls."""
import argparse
from collections import defaultdict
from contextlib import closing
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import re
import sqlite3
from pathlib import Path

ZONE = timezone(timedelta(hours=8))
IMAGE = re.compile(r"\[CQ:image,([^\]]*)\]")
SUMMARY = "[动画表情]"


def sticker_refs(raw):
    refs = []
    for match in IMAGE.finditer(str(raw or "")):
        data = {}
        for part in match.group(1).split(","):
            key, _, value = part.partition("=")
            data[key.strip()] = (value.replace("&#44;", ",").replace("&#91;", "[")
                                .replace("&#93;", "]").replace("&amp;", "&"))
        # the old chat log writes NapCat's sub_type as subType
        sub = (data.get("sub_type") or data.get("subType") or "").strip()
        if (sub == "1" or data.get("summary") == SUMMARY) and data.get("url"):
            refs.append(data["url"])
    return refs


def load_rows(path):
    uri = Path(path).resolve().as_uri() + "?mode=ro&immutable=1"
    with closing(sqlite3.connect(uri, uri=True)) as db:
        return list(db.execute("SELECT id, group_id, post_type, raw_message, timestamp, user_id "
                               "FROM messages ORDER BY timestamp, id"))


def browse_score(unread, familiar, quiet_minutes, waiting, since_open, hour, unread_minutes=0):
    """Approximate observable signals; the old log has no actual mood or sleep state."""
    if unread <= 0 or quiet_minutes < 5:
        return 0.0
    idle = min(max(quiet_minutes - 5, 0) / 60, 1.0)
    red_dot = min(unread / 8, 1.0)
    age = min(max(since_open, 0) / 180, 1.0)
    routine = 0.15 if 8 <= hour < 10 or 22 <= hour < 24 else 0.0
    return (0.35 * idle + 0.4 * red_dot + 0.25 * familiar + 0.2 * age
            + 0.2 * bool(waiting) + routine + 0.3 * min(max(unread_minutes / 720, 0), 1))


def simulate(rows, minutes):
    """Return (number of calendar days, opens, fake vision calls)."""
    if not rows:
        return 0, 0, 0
    first = datetime.fromtimestamp(float(rows[0][4]), ZONE)
    last = datetime.fromtimestamp(float(rows[-1][4]), ZONE)
    start = first.replace(hour=0, minute=0, second=0, microsecond=0)
    end = last.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    days = (end.date() - start.date()).days
    unread = defaultdict(int)
    queues = defaultdict(list)
    last_open = {}
    first_unread = {}
    people = defaultdict(set)
    interactions = defaultdict(int)
    last_sent = None
    waiting_for = {}
    seen = set()
    opens = looks = pos = 0
    next_open = float('-inf')
    tick = start
    while tick < end:
        now = tick.timestamp()
        while pos < len(rows) and float(rows[pos][4]) <= now:
            _, group, post_type, raw, stamp, *rest = rows[pos]
            pos += 1
            if post_type == "message_sent":
                last_sent = float(stamp)
                if group:
                    waiting_for[str(group)] = float(stamp)
                continue
            if not group or post_type != "message":
                continue
            group = str(group)
            first_unread.setdefault(group, float(stamp))
            person = str(rest[0] or "") if rest else ""
            if person:
                people[group].add(person)
                if group in waiting_for and float(stamp) >= waiting_for[group]:
                    interactions[person] += 1
            unread[group] += 1
            queues[group].extend((float(stamp), ref) for ref in sticker_refs(raw))
            queues[group] = queues[group][-100:]
        minute = tick.hour * 60 + tick.minute
        if not (60 <= minute < 505) and now >= next_open:
            eligible = [g for g in unread if unread[g] > 0]
            if eligible:
                quiet = (now - last_sent) / 60 if last_sent is not None else 180
                def score(g):
                    familiar = max((min(interactions[p] / 5, 1.0) for p in people[g]), default=0.0)
                    waiting = g in waiting_for and now - waiting_for[g] <= 3600
                    age = (now - last_open[g]) / 60 if g in last_open else 180
                    return browse_score(unread[g], familiar, quiet, waiting, age, tick.hour,
                                        (now - first_unread[g]) / 60)
                group = min(eligible, key=lambda g: (-score(g), last_open.get(g, float('-inf')), g))
                if score(group) < 0.8:
                    tick += timedelta(minutes=5)
                    continue
                opens += 1
                unread[group] = 0
                first_unread.pop(group, None)
                people.pop(group, None)
                waiting_for.pop(group, None)
                last_open[group] = now
                next_open = now + minutes * 60
                looks_for_open = 0
                candidates = queues.pop(group, [])
                for stamp, ref in candidates:
                    if 0 <= now - stamp <= 3600 and ref not in seen and looks_for_open < 3:
                        seen.add(ref)
                        looks += 1
                        looks_for_open += 1
        tick += timedelta(minutes=5)
    return days, opens, looks


def main():
    parser = argparse.ArgumentParser(description="离线估算自己翻群；只输出汇总数字")
    parser.add_argument("--chat", required=True, help="旧聊天 SQLite 文件")
    parser.add_argument("--price", required=True, help="每次看图的价格，单位自定")
    args = parser.parse_args()
    try:
        price = Decimal(args.price)
        if not price.is_finite() or price < 0:
            raise ValueError
        rows = load_rows(args.chat)
        for interval in (5, 15, 30):
            days, opens, looks = simulate(rows, interval)
            divisor = Decimal(days or 1)
            print(f"{interval}分钟  天数={days}  每天翻群={Decimal(opens)/divisor:.2f}  "
                  f"每天看图={Decimal(looks)/divisor:.2f}  每天费用={price * looks/divisor:.4f}")
    except (OSError, sqlite3.Error, ValueError, InvalidOperation, OverflowError):
        parser.exit(2, "输入不可用，请检查数据库格式和价格。\n")


if __name__ == "__main__":
    main()


