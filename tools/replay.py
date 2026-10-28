"""Replay an old chat log through the plugin, offline, and record every prompt it builds (step 1, part 3).

    python -I tools/replay.py --chat <botshepherd.db> --registry <forget_registry.sqlite3> --out <new empty folder>
        [--aliases <aliases.jsonl>] [--embed-url http://127.0.0.1:11434/v1/embeddings [--embed-model bge-m3]]
        [--impressions] [--old-forgets keep-out|let-in] [--forget-me optout|cutoff] [--remember-replies]
        [--no-canaries] [--limit N]
        [--notebook] [--astrbot <AstrBot data dir> --model <provider id> --model-limit N [--model-cap kind=N]]

Run 1 of the step-1 gate: no model, no network. The plugin is driven through its real hooks
(on_message for every message, on_llm_request / on_llm_response when someone woke the old
account), with the test harness's fake model and a clock that follows the log. Then
tools/audit_replay.py checks that nothing went where the discretion table forbids.

- Vectors: fake ones by default; --embed-url uses a vector service on this computer (an
  OpenAI-style embeddings endpoint, e.g. Ollama's), one request at a time.
- Nothing else can be reached: while the replay runs, every connection except to that one
  address is refused and counted (replay.json: network_refused). There is no real model in
  the process at all; the fake one's calls are counted (model_calls_fake).
- --aliases loads what people were called (tools/import_old.py: aliases.jsonl) before the log.
- --impressions turns the nightly group impressions on (the fake model answers with a fixed
  made-up line), so their prompts are recorded and checked too.
- --notebook turns her nightly notebook on (each 5-minute sweep, as her autonomy loop does).
- Run 2 (--astrbot, --model): a real model answers instead of the fake one: the chat provider
  of that id in the AstrBot at --astrbot (cmd_config.json, read only), with that AstrBot's
  default persona (data_v4.db, read only) as hers. Its key is read into memory when the replay
  starts and only goes into the request header; it is never printed, logged or written, and
  is not taken on the command line. The provider's address is the one other address the
  replay may reach (no proxy). --model-limit is a hard limit on calls (failed ones count, none
  is retried); once reached, or once a kind's --model-cap is, the plugin gets an empty answer
  and nothing is sent. Every call's kind, tokens and answer go to answers.jsonl; replay.json
  has the totals and the connections made, by address.
- Each message is handed over as AstrBot makes it from a QQ message (astrbot_message): its
  parts (text, @, quote, picture...), and message_str with the first @ of her left out and
  every other @ written " @昵称(号码) ".

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
  is copied to <out>/forget_registry.sqlite3 (what the audit reads) and into the data folder (what
  the plugin itself checks before it writes anything, as when it is installed).

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
import time
import urllib.parse
import urllib.request
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
CQ = re.compile(r"\[CQ:([a-z_]+)((?:,[^\]]*)?)\]")
# the message parts AstrBot makes of the OneBot segments it does not turn into text
PART_KIND = {"image": "Image", "face": "Face", "record": "Record", "video": "Video", "file": "File",
             "forward": "Forward", "json": "Json", "poke": "Poke", "dice": "Dice", "rps": "RPS",
             "contact": "Contact", "location": "Location", "music": "Music", "share": "Share"}


def _unescape(text) -> str:
    return text.replace("&#91;", "[").replace("&#93;", "]").replace("&#44;", ",").replace("&amp;", "&")


def segments(raw) -> list:
    """A CQ-coded message -> [(type, data)], the OneBot segments (text between the codes)."""
    out, pos = [], 0
    raw = str(raw or "")
    for m in CQ.finditer(raw):
        if m.start() > pos:
            out.append(("text", {"text": _unescape(raw[pos:m.start()])}))
        data = {}
        for kv in m.group(2).split(",")[1:]:
            k, _, v = kv.partition("=")
            data[k] = _unescape(v)
        out.append((m.group(1), data))
        pos = m.end()
    if pos < len(raw):
        out.append(("text", {"text": _unescape(raw[pos:])}))
    return out


def astrbot_message(raw, self_id, names, comps) -> tuple:
    """(message_str, parts) as AstrBot 4.29.3 makes them from a QQ message
    (astrbot/core/platform/sources/aiocqhttp/aiocqhttp_platform_adapter.py,
    _convert_handle_message_event): runs of segments of one type are taken together; a text
    run is joined and stripped; in a run of @s the first @ of her is left out of message_str
    and every other @ is written " @昵称(号码) " (AstrBot asks QQ for the member's card, then
    the nickname: here the name he last wrote under, else the name in the @); an @ of everyone,
    pictures and the like are parts only; markdown is text; keyboards and market faces are
    dropped. `comps`: the message_components module."""
    import itertools
    text, parts = "", []
    for kind, run in itertools.groupby(segments(raw), key=lambda x: x[0]):
        run = [d for _k, d in run]
        if kind == "text":
            cur = "".join(d.get("text", "") for d in run).strip()
            if cur:
                text += cur
                parts.append(comps.Plain(text=cur))
        elif kind == "at":
            first_self, ats = False, []
            for d in run:
                qq = str(d.get("qq") or "")
                if qq == "all":
                    parts.append(comps.At(qq="all", name="全体成员"))
                    continue
                name = names.get(qq) or str(d.get("name") or "")
                parts.append(comps.At(qq=qq, name=name))
                if qq == str(self_id) and not first_self:
                    first_self = True
                else:
                    ats.append(" @%s(%s) " % (name, qq))
            text += "".join(ats)
        elif kind == "reply":
            parts.extend(comps.Reply(id=d.get("id", "")) for d in run)  # filled in by astrbot_reply
        elif kind == "markdown":
            for d in run:
                cur = d.get("markdown") or d.get("content") or ""
                parts.append(comps.Plain(text=cur))
                text += cur
        elif kind in PART_KIND:
            cls = getattr(comps, PART_KIND[kind], None) or type(PART_KIND[kind], (comps._Comp,), {})
            parts.extend(cls(**{k: v for k, v in d.items() if k in ("file", "id")}) for d in run)
    return text, parts


def astrbot_reply(quoted, self_id, names, comps):
    """The quote part AstrBot makes: it fetches the quoted message and hands over who sent it,
    its text and its parts (that message's own quote is not fetched: a bare Reply)."""
    if quoted.get("raw_message"):
        text, chain = astrbot_message(quoted["raw_message"], self_id, names, comps)
    else:
        text, chain = str(quoted.get("message_content") or ""), []
    sender = str(self_id) if quoted.get("sent") else str(quoted.get("user_id") or "")
    return comps.Reply(id=quoted["message_id"], chain=chain, sender_id=sender,
                       sender_nickname=str(quoted.get("name") or ""), time=int(quoted.get("ts") or 0),
                       message_str=text, text=text, qq=sender)

# made-up people and secrets; the audit looks for the secrets
CANARY_PEOPLE = {"private": "880000001", "group": "880000002", "probe": "880000004"}
CANARY_SECRETS = {"private": "蓝鲸三号", "group": "青柠七号"}


LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def guard_network(allowed, used=None):
    """Refuse every connection but to `allowed` ({(host, port)}: the vector service on this
    computer, and in run 2 the model's address): nothing else is reached. An allowed host name
    allows the addresses it resolves to. `used` (a Counter) counts the connections let through,
    by "host:port". Returns the list the refused hosts are added to."""
    import socket
    refused, names = [], {}

    def ok(host, port):
        return (str(host), int(port or 0)) in allowed

    real_connect, real_getaddrinfo = socket.socket.connect, socket.getaddrinfo

    def connect(self, address):
        if isinstance(address, tuple) and ok(address[0], address[1]):
            if used is not None:
                used["%s:%s" % (names.get(str(address[0]), address[0]), address[1])] += 1
            return real_connect(self, address)
        refused.append(str(address[0]) if isinstance(address, tuple) else "?")
        raise OSError("network disabled in the replay")

    def getaddrinfo(host, port, *a, **k):
        if ok(host, port):
            infos = real_getaddrinfo(host, port, *a, **k)
            for info in infos:
                allowed.add((str(info[4][0]), int(port or 0)))
                names.setdefault(str(info[4][0]), str(host))
            return infos
        refused.append(str(host))
        raise OSError("network disabled in the replay")

    real_create = asyncio.base_events.BaseEventLoop.create_connection

    async def create_connection(self, protocol_factory, host=None, port=None, *a, **k):
        if host is not None and ok(host, port):
            return await real_create(self, protocol_factory, host, port, *a, **k)
        refused.append(str(host))
        raise OSError("network disabled in the replay")

    socket.socket.connect, socket.getaddrinfo = connect, getaddrinfo
    asyncio.base_events.BaseEventLoop.create_connection = create_connection
    return refused


def local_embedder(url, model, counts):
    """An _ipv4_json stand-in: embeddings from the vector service at `url`, nothing else."""
    def call(_url, headers, payload, timeout=None):
        if not str(_url).endswith("/embeddings"):
            raise OSError("network disabled in the replay: " + str(_url))
        texts = list(payload.get("input") or [])
        body = json.dumps({"model": model, "input": texts}).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        start = time.perf_counter()
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        counts["embed_requests"] += 1
        counts["embed_texts"] += len(texts)
        counts["embed_ms"] += int((time.perf_counter() - start) * 1000)
        return data
    return call


def astrbot_model(data_dir, provider_id):
    """The chat provider `provider_id` of the AstrBot whose data folder is `data_dir` (read
    only): (address, model name, post). post(messages) sends one OpenAI-style chat request and
    returns the answer's JSON. The key is read into memory here and lives only inside post();
    it is never returned, printed or written."""
    cfg = json.loads((Path(data_dir) / "cmd_config.json").read_text("utf-8-sig"))
    prov = next((p for p in cfg.get("provider") or [] if p.get("id") == provider_id), None)
    if not prov or not prov.get("enable", True):
        raise SystemExit("AstrBot has no enabled provider %r" % provider_id)
    src = next((s for s in cfg.get("provider_sources") or [] if s.get("id") == prov.get("provider_source_id")), {})
    conf = dict(src, **prov)
    base, model = str(conf.get("api_base") or "").rstrip("/"), str(prov.get("model") or "")
    keys = conf.get("key") or []
    key = next((str(k) for k in (keys if isinstance(keys, list) else [keys]) if str(k or "").strip()), "")
    timeout = int(conf.get("timeout") or 120)
    if not (base.startswith("https://") and model and key):
        raise SystemExit("provider %r: no https address, model or key in AstrBot's config" % provider_id)
    url = base + "/chat/completions"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # straight there, no proxy

    def post(messages):
        body = json.dumps({"model": model, "messages": messages, "stream": False}).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
                                                              "Authorization": "Bearer " + key})
        with opener.open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    return base, model, post


def astrbot_persona(data_dir) -> str:
    """The default persona's system prompt of the AstrBot at `data_dir` (read only)."""
    cfg = json.loads((Path(data_dir) / "cmd_config.json").read_text("utf-8-sig"))
    pid = (((cfg.get("agent_runner") or {}).get("config") or {}).get("persona") or {}).get("persona_id") or ""
    db = sqlite3.connect("file:" + (Path(data_dir) / "data_v4.db").resolve().as_posix() + "?mode=ro&immutable=1",
                         uri=True)
    try:
        row = db.execute("SELECT system_prompt FROM personas WHERE persona_id = ?", (pid,)).fetchone()
    finally:
        db.close()
    return str(row[0] or "") if row else ""


def failure(exc) -> str:
    """A model call's failure in a word or two (never the answer's body: it may echo the key)."""
    import socket
    import urllib.error
    if isinstance(exc, urllib.error.HTTPError):
        return "HTTP %s" % exc.code
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return "timeout"
    return type(exc).__name__


class ModelGate:
    """Every model call of run 2 goes through here: the hard limit on calls (failed ones count,
    none is retried), the per-kind caps, the token count, and answers.jsonl. After STOP_AFTER
    failures in a row no call is made any more (a wrong key or no way through: stop, don't
    keep trying)."""

    STOP_AFTER = 3

    def __init__(self, post, limit, caps, stats, answers, clock, current):
        self.post, self.limit, self.caps, self.stats = post, int(limit), dict(caps), stats
        self.answers, self.clock, self.current = answers, clock, current
        self.calls = self.failed_in_a_row = 0

    def chat(self, kind, prompt, system_prompt=None) -> str:
        s = self.stats
        if self.calls >= self.limit:
            s["model_refused_limit"] += 1
            return ""
        if self.failed_in_a_row >= self.STOP_AFTER:
            s["model_refused_after_failures"] += 1
            return ""
        if kind in self.caps and s["model_calls_" + kind] >= self.caps[kind]:
            s["model_refused_cap_" + kind] += 1
            return ""
        self.calls += 1
        s["model_calls"] += 1
        s["model_calls_" + kind] += 1
        messages = ([{"role": "system", "content": str(system_prompt)}] if system_prompt else []) + [
            {"role": "user", "content": str(prompt)}]
        rec = {"call": self.calls, "kind": kind, "ts": self.clock.now, "place": self.current["place"]}
        start = time.perf_counter()
        try:
            data = self.post(messages)
            text = str(((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "")
            for k, v in (data.get("usage") or {}).items():
                if isinstance(v, int):
                    s["tokens_" + k] += v
            rec.update(ok=True, usage={k: v for k, v in (data.get("usage") or {}).items() if isinstance(v, int)},
                       text=text)
            s["model_ok"] += 1
            self.failed_in_a_row = 0
        except Exception as exc:  # noqa: BLE001  (no retry: the plugin gets an empty answer)
            text = ""
            rec.update(ok=False, failure=failure(exc))
            s["model_failed"] += 1
            s["model_failed_" + rec["failure"]] += 1
            self.failed_in_a_row += 1
        s["model_ms"] += int((time.perf_counter() - start) * 1000)
        self.answers.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.answers.flush()
        return text


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
    ap.add_argument("--aliases", help="aliases.jsonl from tools/import_old.py: what people were called, loaded first")
    ap.add_argument("--embed-url", help="an embeddings endpoint on this computer (default: fake vectors)")
    ap.add_argument("--embed-model", default="bge-m3")
    ap.add_argument("--impressions", action="store_true",
                    help="run the nightly group impressions (the fake model answers)")
    ap.add_argument("--notebook", action="store_true", help="let her write her notebook each night")
    ap.add_argument("--astrbot", help="run 2: the data folder of the AstrBot whose chat provider answers (read only)")
    ap.add_argument("--model", help="run 2: that provider's id, e.g. deepseek/deepseek-flash")
    ap.add_argument("--model-limit", type=int, default=0, help="run 2: at most this many model calls in all")
    ap.add_argument("--model-cap", action="append", default=[], metavar="KIND=N",
                    help="run 2: at most N calls of one kind (event_summary, memory_summary, group_impressions, "
                         "notebook...)")
    ap.add_argument("--limit", type=int, default=0, help="only the first N messages of the log")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    if args.old_forgets == "keep-out" and not args.registry:
        ap.error("--registry is needed to keep out what was forgotten (or say --old-forgets let-in)")
    if bool(args.astrbot) != bool(args.model) or (args.astrbot and args.model_limit <= 0):
        ap.error("a real model needs --astrbot, --model and --model-limit (above 0)")
    caps = {}
    for cap in args.model_cap:
        kind, _, n = cap.partition("=")
        if not n.isdigit():
            ap.error("--model-cap is KIND=N")
        caps[kind.strip()] = int(n)
    allowed = set()
    if args.embed_url:
        u = urllib.parse.urlsplit(args.embed_url)
        if u.scheme != "http" or u.hostname not in LOCAL_HOSTS:
            ap.error("--embed-url must be a vector service on this computer (http://127.0.0.1:...)")
        allowed = {(h, u.port or 80) for h in (u.hostname, "127.0.0.1" if u.hostname == "localhost" else u.hostname)}
    post = model_base = model_name = None
    persona = PERSONA
    if args.astrbot:
        model_base, model_name, post = astrbot_model(args.astrbot, args.model)
        u = urllib.parse.urlsplit(model_base)
        allowed.add((u.hostname, u.port or 443))
        persona = astrbot_persona(args.astrbot) or PERSONA
    started = time.perf_counter()
    loop = asyncio.new_event_loop()   # before the guard: on Windows it connects to itself
    asyncio.set_event_loop(loop)
    connections = Counter()
    refused = guard_network(allowed, connections)

    out = _guard.output_dir(args.out, "the replay")
    data = out / "data"
    data.mkdir()
    reg_path = out / "forget_registry.sqlite3"
    if args.old_forgets == "keep-out":
        shutil.copyfile(args.registry, reg_path)
        shutil.copyfile(args.registry, data / "forget_registry.sqlite3")

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

    stats = Counter()

    class RecordingProvider(harness.FakeProvider):
        def __init__(self, kind=""):
            super().__init__()
            self.kind = kind

        async def text_chat(self, prompt="", system_prompt=None, **kwargs):
            stats["model_calls_fake"] += 1
            stats["model_calls_fake_" + (self.kind or "other")] += 1
            prompts.write(json.dumps({"kind": "model", "ts": clock.now, "place": current["place"], "call": self.kind,
                                      "text": "%s\n%s" % (system_prompt or "", prompt)}, ensure_ascii=False) + "\n")
            if "群里几位群友今天说的话" in str(prompt):   # impressions: one made-up line for everyone
                codes = re.findall(r"^(P\d+)：", str(prompt), re.M)
                return harness.FakeResponse(json.dumps({c: {"style": "说话简短，爱接话", "topics": ["聊天"], "aliases": []}
                                                        for c in codes}, ensure_ascii=False))
            return await super().text_chat(prompt=prompt, system_prompt=system_prompt, **kwargs)

    import astrbot.api.message_components as comps  # noqa: E402
    by_id = {r["message_id"]: r for r in rows if r.get("message_id")}
    names = {}
    for r in rows:
        if r["name"] and not r["sent"]:
            names[r["user_id"]] = r["name"]

    class ReplayEvent(harness.FakeEvent):
        def __init__(self, row):
            place = row["place"]
            group = place.split(":", 1)[1] if place.startswith("group:") else None
            if row.get("raw_message"):
                text, parts = astrbot_message(row["raw_message"], self_id, names, comps)
            else:  # the canaries: plain text
                text = str(row["message_content"] or "")
                parts = [Plain(text=text)]
            super().__init__(text, sender=row["user_id"], name=row["name"], group=group, self_id=self_id)
            self.message_obj.message_id = row["message_id"]
            quoted = row.get("quoted") or ""   # '' when it quoted something forgotten
            if not quoted:
                parts = [p for p in parts if type(p).__name__ != "Reply"]
            self._parts = [astrbot_reply(by_id[p.id], self_id, names, comps)
                           if type(p).__name__ == "Reply" and getattr(p, "id", "") in by_id else p for p in parts]

        def get_messages(self):
            return self._parts

    gate = None
    if post:
        answers = open(out / "answers.jsonl", "w", encoding="utf-8")
        gate = ModelGate(post, args.model_limit, caps, stats, answers, clock, current)

    class ModelProvider(harness.FakeProvider):
        """Run 2: the real model, through the gate, for one kind of call."""

        def __init__(self, kind):
            super().__init__()
            self.kind = kind
            self.provider_config = {"id": args.model, "model": model_name, "provider_type": "chat_completion"}

        async def text_chat(self, prompt="", system_prompt=None, **kwargs):
            prompts.write(json.dumps({"kind": "model", "ts": clock.now, "place": current["place"], "call": self.kind,
                                      "text": "%s\n%s" % (system_prompt or "", prompt)}, ensure_ascii=False) + "\n")
            return harness.FakeResponse(gate.chat(self.kind, prompt, system_prompt))

    class Personas(harness.FakePersonaManager):
        async def get_default_persona_v3(self, umo=None):
            return {"name": "default", "prompt": persona}

    ctx = harness.FakeContext()
    ctx.provider = RecordingProvider()
    ctx.persona_manager = Personas()
    plugin = plugin_main.BioCorePlugin(ctx, config={})
    plugin._ipv4_json = (local_embedder(args.embed_url, args.embed_model, stats) if args.embed_url
                         else harness.fake_ipv4_json)
    async def provider_for(kind, event=None):  # each call knows its kind, for the counts
        return ModelProvider(str(kind)) if gate else RecordingProvider(str(kind))
    plugin._provider_for = provider_for
    if args.impressions:
        plugin.llm_functions = dict(plugin.llm_functions or {},
                                    group_impressions={"enabled": True, "provider": "follow_llm"})
    if args.notebook:
        plugin.llm_functions = dict(plugin.llm_functions or {}, notebook={"enabled": True, "provider": "follow_llm"})
    if args.aliases:
        import impressions  # noqa: E402
        people = [json.loads(x) for x in Path(args.aliases).read_text("utf-8").splitlines() if x.strip()]
        day = time.strftime("%Y-%m-%d", time.localtime(timeline[0]["ts"]))
        for k, v in impressions.from_bundle(plugin._impression_store(), people, registry=reg, day=day).items():
            stats["aliases_" + k] += v
    remember = plugin._remember

    async def remember_unless_reply(event, text, role="user", core=None):
        if role == "assistant" and not args.remember_replies:
            return None
        return await remember(event, text, role, core)
    plugin._remember = remember_unless_reply

    next_sweep = timeline[0]["ts"] + SWEEP_EVERY

    def five_minutes():
        plugin._sweep_windows()
        if args.impressions:
            current.update(place="nightly", ts=clock.now)
            done = loop.run_until_complete(plugin._maybe_update_impressions(now=clock.now))
            harness.drain(loop)
            stats["impression_calls"] += sum(1 for r in done.values() if r.get("called"))
        if args.notebook:
            current.update(place="nightly", ts=clock.now)
            plugin._begin_job()
            if loop.run_until_complete(plugin._maybe_write_notebook(now=clock.now)):
                stats["notebook_nights_written"] += 1
            harness.drain(loop)

    for row in timeline:
        clock.now = max(clock.now, row["ts"])
        while clock.now >= next_sweep:
            saved, clock.now = clock.now, next_sweep
            five_minutes()
            clock.now = saved
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
        current.update(place=row["place"], ts=row["ts"])
        event = ReplayEvent(row)
        if not event.message_str.strip() and not event.get_messages():
            stats["skipped_empty"] += 1
            continue
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
            "asked": str(req.prompt or "")}, ensure_ascii=False) + "\n")  # as AstrBot sends it, after the plugin
        stats["requests"] += 1
        if row.get("reply"):
            loop.run_until_complete(plugin.on_llm_response(event, LLMResponse(row["reply"])))
            harness.drain(loop)
            stats["replies"] += 1
    five_minutes()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    prompts.close()
    reg.close()
    if gate:
        gate.answers.close()
    stats["network_refused"] = len(refused)
    from astrbot.api import logger as plugin_log  # noqa: E402  (the stand-in keeps what the plugin logged)
    with open(out / "plugin-log.txt", "w", encoding="utf-8") as f:
        f.writelines("%s %s\n" % rec for rec in getattr(plugin_log, "records", []))

    (out / "canaries.json").write_text(json.dumps({
        "enabled": bool(canaries), "people": CANARY_PEOPLE, "secrets": CANARY_SECRETS,
        "rows": [{k: c[k] for k in ("place", "user_id", "name", "ts", "message_content")} for c in canaries],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    summary = {"self_id": self_id, "old_forgets": args.old_forgets, "forget_me": args.forget_me,
               "remember_replies": args.remember_replies, "impressions": args.impressions,
               "vectors": ("%s (%s)" % (args.embed_url, args.embed_model)) if args.embed_url else "fake",
               "aliases": bool(args.aliases), "notebook": args.notebook,
               "model": ("%s (%s)" % (model_name, model_base)) if post else "fake",
               "model_limit": args.model_limit if post else 0, "model_caps": caps,
               "seconds": round(time.perf_counter() - started, 1),
               "connections": dict(connections), "refused_hosts": sorted(set(refused)),
               "log_rows": len(rows), "canaries": len(canaries), "labels": place_labels, "stats": dict(stats)}
    (out / "replay.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"log_rows": len(rows), "canaries": len(canaries), "stats": dict(stats)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
