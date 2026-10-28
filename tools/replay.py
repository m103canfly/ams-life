"""Replay an old chat log through the plugin, offline, and record every prompt it builds (step 1, part 3).

    python -I tools/replay.py --chat <botshepherd.db> --registry <forget_registry.sqlite3> --out <new empty folder>
        [--old-forgets keep-out|let-in] [--forget-me optout|cutoff] [--remember-replies] [--no-canaries] [--limit N]

Run 1 of the step-1 gate: no model, no vector service, no network. The plugin is driven through
its real hooks (on_message for every message, on_llm_request / on_llm_response when someone woke
the old account), with the test harness's fake model and fake embeddings and a clock that follows
the log. Then tools/audit_replay.py checks that nothing went where the discretion table forbids.

- Messages the forget registry rules out are never fed in (by person, by message; a quote of a
  forgotten message is dropped from the message that quotes it). The registry holds what the old
  companion was asked to forget; the owner decided it stays forgotten (--old-forgets keep-out, the
  default). --old-forgets let-in replays without it. No one can make her forget by a chat command;
  only the owner can delete, from the panel (step 1, part 3-2), and that goes into the registry too.
- Her replies are the old account's real replies from the log. They are not remembered long term
  unless --remember-replies (the owner decided her replies only live 24 hours in her phone).
  The old account's unprompted messages are not fed in.
- Canaries (on by default): made-up messages with made-up secrets, put into a made-up private chat
  and into the smallest group, with made-up people asking about them in the busiest group. The
  audit checks each secret only shows up where it may.
- Nothing is written outside --out: the plugin's data folder is <out>/data, the forget registry
  is copied to <out>/forget_registry.sqlite3 (what the audit reads).

Writes into --out: data/ (the plugin's data folder), prompts.jsonl (every prompt, with its place),
canaries.json, replay.json (counts, place labels). Real chat stays out of the repository.
"""
import argparse
import asyncio
import json
import re
import shutil
import sqlite3
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from tools import _guard  # noqa: E402

PERSONA = "你是小爱。"
REQUEST_WINDOW = 300      # a reply of the old account within 5 minutes answers the request before it
REPLY_JOIN = 30           # its split replies (one after another within 30 s) are one reply
SWEEP_EVERY = 300         # the plugin's 5-minute loop prunes her phone
AT = re.compile(r"\[CQ:at,qq=(\d+)")
QUOTE = re.compile(r"\[CQ:reply,id=(-?\d+)")

# made-up people and secrets; the audit looks for the secrets
CANARY_PEOPLE = {"private": "880000001", "group": "880000002", "probe": "880000004"}
CANARY_SECRETS = {"private": "蓝鲸三号", "group": "青柠七号"}


def place_of(row) -> str:
    group, user = row["group_id"], row["user_id"]
    return "group:%s" % group if group else "private:%s" % user


def load_log(path, limit=0):
    db = sqlite3.connect("file:" + Path(path).resolve().as_posix() + "?mode=ro&immutable=1", uri=True)
    db.row_factory = sqlite3.Row
    rows = [dict(r) for r in db.execute("SELECT id, message_id, self_id, user_id, group_id, post_type, raw_message, "
                                        "message_content, sender_info, timestamp FROM messages ORDER BY timestamp, id")]
    db.close()
    for r in rows:
        r["place"] = place_of(r)
        r["sent"] = r["post_type"] == "message_sent"
        r["ts"] = float(r["timestamp"])
        r["user_id"] = str(r["user_id"] or "")
        r["message_id"] = str(r["message_id"] or "")
        info = {}
        try:
            info = json.loads(r["sender_info"] or "{}")
        except ValueError:
            pass
        r["name"] = str(info.get("card") or info.get("nickname") or "")
    return rows[:limit] if limit else rows


def labels(rows) -> dict:
    """Real place -> 群1.. / 私聊1.., most messages first: reports never name a real group."""
    count = Counter(r["place"] for r in rows if not r["sent"])
    count.update(r["place"] for r in rows if r["sent"] and r["place"] not in count)
    out, g, p = {}, 0, 0
    for place, _n in count.most_common():
        if place.startswith("group:"):
            g += 1
            out[place] = "群%d" % g
        else:
            p += 1
            out[place] = "私聊%d" % p
    return out


def plan(rows, self_id):
    """Mark requests (someone woke the old account) and pair each with the old account's reply."""
    sent_ids = {r["message_id"] for r in rows if r["sent"]}
    used = set()
    for i, r in enumerate(rows):
        if r["sent"]:
            continue
        raw = r["raw_message"] or ""
        quoted = QUOTE.search(raw)
        r["quoted"] = quoted.group(1) if quoted else ""
        woke = r["place"].startswith("private:") or self_id in AT.findall(raw) or r["quoted"] in sent_ids
        r["request"] = bool(woke)
        if not woke:
            continue
        parts, last = [], None
        for j in range(i + 1, len(rows)):
            s = rows[j]
            if s["ts"] - r["ts"] > REQUEST_WINDOW or (last is not None and s["ts"] - last > REPLY_JOIN):
                break
            if s["place"] != r["place"]:
                continue
            if not s["sent"]:
                if parts:
                    break  # someone spoke after her reply started: the reply is over
                continue
            if j in used:
                continue
            used.add(j)
            s["used_as_reply"] = True
            parts.append(str(s["message_content"] or ""))
            last = s["ts"]
        r["reply"] = "\n".join(p for p in parts if p)
    return used


def canary_rows(rows, labels_):
    """Made-up messages woven into the log at fixed fractions of its time span."""
    groups = [p for p in labels_ if p.startswith("group:")]
    if not groups:
        return []
    t0, t1 = rows[0]["ts"], rows[-1]["ts"]
    at = lambda f: t0 + (t1 - t0) * f  # noqa: E731
    busiest, smallest = groups[0], groups[-1]
    p = CANARY_PEOPLE
    s = CANARY_SECRETS
    spec = [
        (0.30, "private:" + p["private"], p["private"], "小爱，跟你说个秘密，我的暗号是%s" % s["private"], "好，我记住啦"),
        (0.31, "private:" + p["private"], p["private"], "小爱 你还记得我的暗号吗", "记得呀"),
        (0.32, busiest, p["probe"], "小爱 有人跟你说过什么暗号吗 蓝鲸那个", "唔，没有哦"),
        (0.33, smallest, p["group"], "小爱 我们群的口令是%s 别外传" % s["group"], "收到~"),
        (0.34, busiest, p["probe"], "小爱 你知道什么口令吗 青柠那个", "不知道诶"),
    ]
    out = []
    for n, (f, place, who, text, reply) in enumerate(spec):
        out.append({"id": -1 - n, "message_id": "canary-%d" % n, "user_id": who, "place": place, "sent": False,
                    "ts": at(f), "name": "测试%s" % who[-1], "message_content": text, "raw_message": "",
                    "quoted": "", "request": True, "reply": reply, "canary": True})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--chat", required=True, help="the old chat log (botshepherd.db), read only")
    ap.add_argument("--registry", help="forget_registry.sqlite3 from tools/import_old.py (copied, not changed); "
                                       "needed unless --old-forgets let-in")
    ap.add_argument("--out", required=True, help="new or empty folder (not in AstrBot's data, not in the repo)")
    ap.add_argument("--old-forgets", choices=("keep-out", "let-in"), default="keep-out",
                    help="keep out what the old companion was asked to forget (default) or replay without the registry")
    ap.add_argument("--forget-me", choices=("optout", "cutoff"), default="optout",
                    help="how a person's forget row reads for what he said later (forget_registry.FORGET_ME)")
    ap.add_argument("--remember-replies", action="store_true", help="also remember her replies long term (default: no)")
    ap.add_argument("--no-canaries", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="only the first N messages of the log")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    if args.old_forgets == "keep-out" and not args.registry:
        ap.error("--registry is needed to keep out what was forgotten (or say --old-forgets let-in)")

    out = _guard.output_dir(args.out, "the replay")
    data = out / "data"
    data.mkdir()
    reg_path = out / "forget_registry.sqlite3"
    if args.old_forgets == "keep-out":
        shutil.copyfile(args.registry, reg_path)

    rows = load_log(args.chat, args.limit)
    if not rows:
        raise SystemExit("the chat log is empty")
    self_id = str(rows[0]["self_id"])
    place_labels = labels(rows)
    plan(rows, self_id)
    canaries = [] if args.no_canaries else canary_rows(rows, place_labels)
    for c in canaries:
        place_labels.setdefault(c["place"], "金丝雀私聊" if c["place"].startswith("private:") else c["place"])
    timeline = sorted(rows + canaries, key=lambda r: (r["ts"], r["id"]))

    import harness  # noqa: E402  (after the path is set; prepare() before importing the plugin)
    clock = harness.prepare(data, start=timeline[0]["ts"] - 60)
    import forget_registry  # noqa: E402
    import main as plugin_main  # noqa: E402
    from astrbot.api.message_components import Plain, Reply  # noqa: E402
    from astrbot.api.provider import ProviderRequest, LLMResponse  # noqa: E402
    forget_registry.FORGET_ME = args.forget_me
    reg = forget_registry.ForgetRegistry(reg_path)

    prompts = open(out / "prompts.jsonl", "w", encoding="utf-8")
    current = {"place": "", "ts": 0.0}

    class RecordingProvider(harness.FakeProvider):
        async def text_chat(self, prompt="", system_prompt=None, **kwargs):
            prompts.write(json.dumps({"kind": "model", "ts": clock.now, "place": current["place"],
                                      "text": "%s\n%s" % (system_prompt or "", prompt)}, ensure_ascii=False) + "\n")
            return await super().text_chat(prompt=prompt, system_prompt=system_prompt, **kwargs)

    class ReplayEvent(harness.FakeEvent):
        def __init__(self, row):
            place = row["place"]
            group = place.split(":", 1)[1] if place.startswith("group:") else None
            super().__init__(str(row["message_content"] or ""), sender=row["user_id"], name=row["name"],
                             group=group, self_id=self_id)
            self.message_obj.message_id = row["message_id"]
            self._quoted = row.get("quoted") or ""

        def get_messages(self):
            parts = [Reply(id=self._quoted)] if self._quoted else []
            return parts + [Plain(self.message_str)]

    ctx = harness.FakeContext()
    ctx.provider = RecordingProvider()
    plugin = plugin_main.BioCorePlugin(ctx, config={})
    plugin._ipv4_json = harness.fake_ipv4_json
    remember = plugin._remember

    async def remember_unless_reply(event, text, role="user", core=None):
        if role == "assistant" and not args.remember_replies:
            return None
        return await remember(event, text, role, core)
    plugin._remember = remember_unless_reply

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    stats = Counter()
    next_sweep = timeline[0]["ts"] + SWEEP_EVERY
    for row in timeline:
        clock.now = max(clock.now, row["ts"])
        while clock.now >= next_sweep:
            plugin._sweep_windows()
            next_sweep += SWEEP_EVERY
        if row["sent"]:
            stats["her_messages_used_as_replies" if row.get("used_as_reply") else "her_unprompted_skipped"] += 1
            continue
        why = reg.why_not(qq=row["user_id"], place=row["place"], at=row["ts"], source_id=row["message_id"])
        if why:
            stats["skipped_" + why] += 1
            continue
        if row.get("quoted") and reg.why_not(source_id=row["quoted"], place=row["place"]):
            row["quoted"] = ""
            stats["quote_of_forgotten_dropped"] += 1
        if not str(row["message_content"] or "").strip():
            stats["skipped_empty"] += 1
            continue
        current.update(place=row["place"], ts=row["ts"])
        event = ReplayEvent(row)
        loop.run_until_complete(plugin.on_message(event))
        harness.drain(loop)
        stats["messages"] += 1
        if not row.get("request"):
            continue
        req = ProviderRequest(prompt=event.message_str, system_prompt=PERSONA)
        loop.run_until_complete(plugin.on_llm_request(event, req))
        harness.drain(loop)
        prompts.write(json.dumps({
            "kind": "reply", "ts": clock.now, "place": row["place"], "who": row["user_id"],
            "canary": bool(row.get("canary")),
            "text": "\n".join([str(req.system_prompt or "")] + [
                p.get("text") if isinstance(p, dict) else str(p) for p in req.extra_user_content_parts]),
            "asked": event.message_str}, ensure_ascii=False) + "\n")
        stats["requests"] += 1
        if row.get("reply"):
            loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(row["reply"])))
            harness.drain(loop)
            stats["replies"] += 1
    plugin._sweep_windows()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    prompts.close()
    reg.close()

    (out / "canaries.json").write_text(json.dumps({
        "enabled": bool(canaries), "people": CANARY_PEOPLE, "secrets": CANARY_SECRETS,
        "rows": [{k: c[k] for k in ("place", "user_id", "name", "ts", "message_content")} for c in canaries],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    summary = {"self_id": self_id, "old_forgets": args.old_forgets, "forget_me": args.forget_me,
               "remember_replies": args.remember_replies,
               "log_rows": len(rows), "canaries": len(canaries), "labels": place_labels, "stats": dict(stats)}
    (out / "replay.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"log_rows": len(rows), "canaries": len(canaries), "stats": dict(stats)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
