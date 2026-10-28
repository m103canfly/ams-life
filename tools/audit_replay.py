"""Check a replay for anything the discretion table forbids (step 1, part 3).

    python -I tools/audit_replay.py --replay <folder written by tools/replay.py> --chat <botshepherd.db>

Reads the prompts the plugin built (prompts.jsonl), the canaries, the forget registry and the
plugin's data folder of the replay, and writes audit.json next to them. Exit code 0 = every check
passed, 1 = at least one failed. The report names places only by label (群1, 私聊1, ...) and
never quotes a message.

Checks (a "piece" is 8 characters in a row, letters and digits only, lower case, taken from one
line of a message or a prompt, or from one text field of a data file -- never across two. An
all-digit piece that is part of a known number (someone's, a group's, the registry's) is the
qq check's; any other all-digit piece -- a phone number, a code -- counts like words. A reply
prompt is checked with what AstrBot sends the model of the message, "asked", added to it):

private      A reply prompt somewhere else holds a piece that only ever occurred in one private
             chat -- said by the other person or by her (her replies there, and what the old account
             sent there unprompted, count as that chat's words too).
names        A reply prompt (in a group or a private chat) holds the name of someone who never spoke
             there, and that name never occurred in that place's own messages before.
qq           Any prompt -- a reply prompt or one for the model (summaries, ranking, the notebook,
             impressions...) -- holds a number known to be someone's or some chat's: anyone in
             the log, the person asking too (the owner: no QQ number in a prompt at all), the
             old account itself, every group, and the forget registry's people and messages. The asker's own number in a reply prompt
             is also counted as a warning, so the report tells the two apart.
forgotten    Anything of a person or message in the forget registry (what the old companion was
             asked to forget) -- QQ number, message id, a piece only they wrote -- in any prompt
             (reply or model) or any file of the data folder but the plugin's copy of the registry
             itself (it holds exactly those numbers, so that nothing of them is written again). Their names are listed as warnings
             (a name can be an ordinary word). Skipped when the replay let the old forgets in.
canaries     Each made-up secret only where it may be: the private one only in its private chat;
             the group one elsewhere only without its speaker's name or number (the discretion table
             lets what was said openly come up anonymously).
origins      Every memory and event in the data folder carries an origin.
redline      Memories and events that cross a red line: counted, for a person to look at (not a failure).

What it cannot see is listed in LIMITS below, and in audit.json under "limits".
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import forget_registry  # noqa: E402
import redline  # noqa: E402
from tools import _guard  # noqa: E402

LIMITS = [
    "short messages: a message under 6 letters/characters has no piece, so it is not looked for",
    "paraphrase: only words in the same order are found; the same thing said another way is not",
    "fake model: summaries, the notebook and impressions are written by a fake model that copies or "
    "makes up text, so leaks through what a real model would rewrite are not tested by this run",
    "nightly jobs: the notebook's is not run by the replay (off by default); impressions only with "
    "--impressions, answered by the fake model",
    "private check: reply prompts only; prompts for the model are checked for QQ numbers and "
    "forgotten material, not for private words (their place is the turn that started them)",
]

PIECE = 8
EXAMPLES = 10
_KEEP = re.compile(r"[^0-9a-z㐀-鿿]")


def norm(text) -> str:
    return _KEEP.sub("", str(text or "").lower())


def pieces(text) -> set:
    """The pieces of one line."""
    t = norm(text)
    if len(t) < PIECE:
        return {t} if len(t) >= 6 else set()
    return {t[i:i + PIECE] for i in range(len(t) - PIECE + 1)}


def number_pieces(numbers) -> set:
    """The all-digit pieces that are part of these numbers (left to the qq check)."""
    out = set()
    for n in numbers:
        out |= pieces(n)
    return out


def line_pieces(text) -> set:
    """Pieces of every line, none across two lines."""
    out = set()
    for line in str(text or "").splitlines():
        out |= pieces(line)
    return out


def _strings(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield str(k)
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)
    elif isinstance(obj, str):
        yield obj


def file_pieces(path, body) -> set:
    """Pieces of a data file: field by field for JSON / JSON lines, line by line otherwise."""
    docs = []
    try:
        docs = [json.loads(body)]
    except ValueError:
        try:
            docs = [json.loads(x) for x in body.splitlines() if x.strip()]
        except ValueError:
            return line_pieces(body)
    out = set()
    for doc in docs:
        for s in _strings(doc):
            out |= line_pieces(s)
    return out


def number_pattern(numbers):
    """Whole numbers only: 12345 must not match inside 9123456."""
    nums = sorted({str(n) for n in numbers if len(str(n).lstrip("-")) >= 5}, key=len, reverse=True)
    if not nums:
        return None
    return re.compile(r"(?<![0-9.])(?:%s)(?![0-9])" % "|".join(re.escape(n) for n in nums))


def has(pattern, text) -> bool:
    return bool(pattern and pattern.search(text))


def load_log(path):
    sys.path.insert(0, str(HERE))
    import replay  # noqa: E402  (same reading of the log as the replay)
    return replay.load_log(path)


class Check:
    def __init__(self, name):
        self.name, self.fails, self.examples, self.warnings = name, 0, [], Counter()

    def fail(self, where):
        self.fails += 1
        if len(self.examples) < EXAMPLES:
            self.examples.append(where)

    def report(self):
        out = {"pass": self.fails == 0, "fails": self.fails, "examples": self.examples}
        if self.warnings:
            out["warnings"] = dict(self.warnings)
        return out


def audit(replay_dir, chat) -> dict:
    replay_dir = Path(replay_dir)
    report = _guard.output_file(replay_dir / "audit.json", "the audit report")
    meta = json.loads((replay_dir / "replay.json").read_text("utf-8"))
    label = meta["labels"]
    canaries = json.loads((replay_dir / "canaries.json").read_text("utf-8"))
    prompts = [json.loads(line) for line in (replay_dir / "prompts.jsonl").read_text("utf-8").splitlines() if line]
    for pr in prompts:  # the model sees what AstrBot sends of the message too
        if pr.get("asked"):
            pr["text"] = "%s\n%s" % (pr["text"], pr["asked"])
    log = load_log(chat)
    rows = [r for r in log if not r["sent"]]
    hers = [r for r in log if r["sent"]]  # her words: they belong to where she said them
    for c in canaries.get("rows", []):
        rows.append({"place": c["place"], "user_id": c["user_id"], "ts": c["ts"], "message_content": c["message_content"],
                     "name": "", "message_id": "", "sent": False})
    rows.sort(key=lambda r: r["ts"])
    reg = forget_registry.ForgetRegistry(replay_dir / "forget_registry.sqlite3")
    forget_registry.FORGET_ME = meta.get("forget_me") or forget_registry.FORGET_ME

    def lab(place):
        return label.get(place, "?")

    # --- who said what where
    piece_places = defaultdict(set)
    names_by_place = defaultdict(set)
    speakers = defaultdict(set)
    known_qq = set()
    gone_people = reg.people()
    gone_ids = {r["source_id"] for r in reg.rows() if r["kind"] == "source"}
    gone_pieces, kept_pieces, gone_names = set(), set(), set()
    for r in rows:
        ps = line_pieces(r["message_content"])
        for p in ps:
            piece_places[p].add(r["place"])
        known_qq.add(r["user_id"])
        if r["name"]:
            names_by_place[r["place"]].add(r["name"])
        speakers[r["place"]].add(r["user_id"])
        forgotten = reg.why_not(qq=r["user_id"], place=r["place"], at=r["ts"], source_id=r["message_id"])
        (gone_pieces if forgotten else kept_pieces).update(ps)
        if r["user_id"] in gone_people and r["name"]:
            gone_names.add(r["name"])
    for r in hers:
        for p in line_pieces(r["message_content"]):
            piece_places[p].add(r["place"])
    # the old account itself, every group, the registry's people and messages count too
    known_qq |= {str(r.get("self_id") or "") for r in log} | {str(r.get("group_id") or "") for r in log}
    known_qq |= gone_people | gone_ids
    known_qq = {q for q in known_qq if len(q) >= 5 and q.isdigit()}
    # digits of a known number are the qq check's; any other digits count like words
    numbers_only = number_pieces(known_qq)
    gone_pieces -= kept_pieces | numbers_only  # only what nobody else also said
    private_only = {p: next(iter(pl)) for p, pl in piece_places.items()
                    if len(pl) == 1 and next(iter(pl)).startswith("private:") and p not in numbers_only}
    # a person's number is off limits only while he still may not be kept (a forget row read as a
    # cutoff lets what he says later back in, number and all)
    still_gone = {q for q in gone_people if reg.why_not(qq=q, at=float("inf"))}
    gone_numbers = number_pattern(still_gone | gone_ids)
    name_owner = defaultdict(set)
    for r in rows:
        if r["name"]:
            name_owner[r["name"]].add((r["place"], r["user_id"]))

    checks = {n: Check(n) for n in ("private", "names", "qq", "forgotten", "canaries", "origins", "redline")}
    seen_text = defaultdict(str)  # place -> its own messages so far (for the names check)
    order = sorted(prompts, key=lambda p: p["ts"])
    said = sorted(rows + hers, key=lambda r: r["ts"])
    i = 0
    for n, pr in enumerate(order):
        while i < len(said) and said[i]["ts"] <= pr["ts"]:
            seen_text[said[i]["place"]] += "\n" + str(said[i]["message_content"] or "")
            i += 1
        place, text = pr["place"], pr["text"]
        where = {"prompt": n, "kind": pr["kind"], "place": lab(place)}
        ps = line_pieces(text)
        # forgotten material: in every prompt
        if has(gone_numbers, text) or ps & gone_pieces:
            checks["forgotten"].fail(where)
        for name in gone_names:
            if len(name) >= 2 and name in text:
                checks["forgotten"].warnings["name_in_prompt"] += 1
        who = str(pr.get("who") or "") if pr["kind"] == "reply" else ""
        if has(number_pattern(known_qq - {who}), text):
            checks["qq"].fail(where)
        elif who and has(number_pattern([who]), text):
            checks["qq"].fail(dict(where, asker_own=True))
            checks["qq"].warnings["asker_own_number"] += 1
        if pr["kind"] != "reply":
            continue
        for p in ps:
            src = private_only.get(p)
            if src and src != place:
                checks["private"].fail(dict(where, came_from=lab(src)))
                break
        for name, owners in name_owner.items():
            if len(norm(name)) < 2 or name not in text or name in seen_text[place]:
                continue
            if any(p == place for p, _q in owners):
                continue
            checks["names"].fail(dict(where, name_from=sorted({lab(p) for p, _q in owners})[:3]))

    # --- canaries
    if canaries.get("enabled"):
        sec = canaries["secrets"]
        rows_c = canaries["rows"]
        own = {k: next((c["place"] for c in rows_c if sec[k] in c["message_content"]), "") for k in sec}
        for n, pr in enumerate(order):
            where = {"prompt": n, "kind": pr["kind"], "place": lab(pr["place"])}
            text = pr["text"]
            if sec["private"] in text and pr["place"] != own["private"]:
                checks["canaries"].fail(dict(where, secret="private"))
            if sec["group"] in text and pr["place"] != own["group"]:
                said_by = [c for c in rows_c if sec["group"] in c["message_content"]][0]
                for line in text.splitlines():
                    if sec["group"] in line and ((said_by.get("name") and said_by["name"] in line)
                                                 or said_by["user_id"] in line):
                        checks["canaries"].fail(dict(where, secret="group_named"))
                        break
                else:
                    checks["canaries"].warnings["group_secret_elsewhere_anonymous"] += 1
        checks["canaries"].warnings.update({
            "private_secret_recalled_in_own_chat": sum(1 for p in order if p["kind"] == "reply" and p["place"] == own["private"]
                                                       and sec["private"] in p["text"]),
        })

    # --- the data folder
    data = replay_dir / "data"
    for path in sorted(p for p in data.rglob("*") if p.is_file() and p.name != forget_registry.FILE_NAME):
        body = path.read_text("utf-8", errors="replace")
        rel = path.relative_to(data).as_posix()
        if has(gone_numbers, body) or file_pieces(path, body) & gone_pieces:
            checks["forgotten"].fail({"file": _label_path(rel, label)})
    for item, what in _items(data):
        origin = item.get("origin")
        if not isinstance(origin, dict) or "where" not in origin:
            checks["origins"].fail({"store": what})
        text = " ".join(str(item.get(k) or "") for k in ("text", "event", "title", "small_summary", "big_summary"))
        hit = redline.hit(text)
        if hit:
            checks["redline"].warnings["%s:%s" % (what, hit)] += 1
    reg.close()
    result = {"pass": all(c.fails == 0 for c in checks.values()),
              "prompts": Counter(p["kind"] for p in prompts), "checks": {k: c.report() for k, c in checks.items()},
              "limits": LIMITS}
    if meta.get("old_forgets") == "let-in":
        result["checks"]["forgotten"]["skipped"] = "the replay let the old forgets in: nothing to look for"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return result


def _label_path(rel, label):
    """File names carry place ids: show the label instead."""
    out = rel
    for place, name in label.items():
        ident = place.split(":", 1)[-1]
        if ident and ident in out:
            out = out.replace(ident, name)
    return out


def _items(data):
    lib = data / "memory" / "library.json"
    if lib.exists():
        for e in json.loads(lib.read_text("utf-8")).get("entries") or []:
            yield e, "memory"
    events = data / "archives" / "events.jsonl"
    if events.exists():
        for line in events.read_text("utf-8").splitlines():
            if line.strip().startswith("{"):
                yield json.loads(line), "event"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--replay", required=True, help="folder written by tools/replay.py")
    ap.add_argument("--chat", required=True, help="the same chat log the replay read")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    result = audit(args.replay, args.chat)
    print(json.dumps({"pass": result["pass"], "fails": {k: v["fails"] for k, v in result["checks"].items()}},
                     ensure_ascii=False))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
