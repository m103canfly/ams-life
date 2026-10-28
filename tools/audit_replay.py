"""Check a replay for anything the discretion table forbids (step 1, part 3).

    python -I tools/audit_replay.py --replay <folder written by tools/replay.py> --chat <botshepherd.db>

Reads the prompts the plugin built (prompts.jsonl), the canaries, the forget registry and the
plugin's data folder of the replay, and writes audit.json next to them. Exit code 0 = every check
passed, 1 = at least one failed. The report names places only by label (群1, 私聊1, ...) and
never quotes a message.

Checks (a "piece" is 8 characters in a row, letters and digits only, lower case):

private      A reply prompt somewhere else holds a piece that only ever occurred in one private chat.
names        A reply prompt in a group holds the name of someone who never spoke there, and that
             name never occurred in that group's own messages before.
qq           A reply prompt holds the QQ number of anyone in the log but the person asking
             (whose own number is counted as a warning).
forgotten    Anything of a forgotten person or message -- QQ number, message id, a piece only
             they wrote -- in any prompt (reply or model) or any file of the data folder. What was
             forgotten during the replay (the canary) only counts from the moment it was forgotten.
             Their names are listed as warnings (a name can be an ordinary word).
canaries     Each made-up secret only where it may be: the private one only in its private chat;
             the group one elsewhere only without its speaker's name or number (the discretion table
             lets what was said openly come up anonymously); the forgotten person's words nowhere
             after he asked (and the ones he said afterwards nowhere, unless "forget me" is read as
             a cutoff).
origins      Every memory and event in the data folder carries an origin.
redline      Memories and events that cross a red line: counted, for a person to look at (not a failure).
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

PIECE = 8
EXAMPLES = 10
_KEEP = re.compile(r"[^0-9a-z㐀-鿿]")


def norm(text) -> str:
    return _KEEP.sub("", str(text or "").lower())


def pieces(text) -> set:
    t = norm(text)
    if len(t) < PIECE:
        return {t} if len(t) >= 6 else set()
    return {t[i:i + PIECE] for i in range(len(t) - PIECE + 1)}


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
    meta = json.loads((replay_dir / "replay.json").read_text("utf-8"))
    label = meta["labels"]
    canaries = json.loads((replay_dir / "canaries.json").read_text("utf-8"))
    prompts = [json.loads(line) for line in (replay_dir / "prompts.jsonl").read_text("utf-8").splitlines() if line]
    rows = [r for r in load_log(chat) if not r["sent"]]
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
    # forgotten during the replay (the canary): only from that moment on; anything else: always
    during = {}
    for row in reg.rows():
        if row["kind"] == "qq" and str(row["note"]).startswith("replay:"):
            during[row["qq"]] = min(row["stamp"], during.get(row["qq"], row["stamp"]))
    gone_people = reg.people()
    gone_ids = {r["source_id"] for r in reg.rows() if r["kind"] == "source"}
    gone_since, kept_pieces, gone_names = {}, set(), set()
    for r in rows:
        ps = pieces(r["message_content"])
        for p in ps:
            piece_places[p].add(r["place"])
        known_qq.add(r["user_id"])
        if r["name"]:
            names_by_place[r["place"]].add(r["name"])
        speakers[r["place"]].add(r["user_id"])
        forgotten = reg.why_not(qq=r["user_id"], place=r["place"], at=r["ts"], source_id=r["message_id"])
        if forgotten:
            since = during.get(r["user_id"], float("-inf")) if r["ts"] <= during.get(r["user_id"], 0) else float("-inf")
            for p in ps:
                gone_since[p] = min(since, gone_since.get(p, since))
        else:
            kept_pieces.update(ps)
        if r["user_id"] in gone_people and r["name"]:
            gone_names.add(r["name"])
    gone_since = {p: t for p, t in gone_since.items() if p not in kept_pieces}  # only what nobody else also said
    private_only = {p: next(iter(pl)) for p, pl in piece_places.items()
                    if len(pl) == 1 and next(iter(pl)).startswith("private:")}
    known_qq = {q for q in known_qq if len(q) >= 5 and q.isdigit()}
    # a person's number is off limits only while he still may not be kept ("forget me" read as a
    # cutoff lets what he says later back in, number and all)
    still_gone = {q for q in gone_people if reg.why_not(qq=q, at=float("inf"))}
    gone_numbers = number_pattern((still_gone - set(during)) | gone_ids)
    gone_later = [(number_pattern([q]), t) for q, t in during.items() if q in still_gone]
    name_owner = defaultdict(set)
    for r in rows:
        if r["name"]:
            name_owner[r["name"]].add((r["place"], r["user_id"]))

    checks = {n: Check(n) for n in ("private", "names", "qq", "forgotten", "canaries", "origins", "redline")}
    seen_text = defaultdict(str)  # place -> its own messages so far (for the names check)
    order = sorted(prompts, key=lambda p: p["ts"])
    i = 0
    for n, pr in enumerate(order):
        while i < len(rows) and rows[i]["ts"] <= pr["ts"]:
            seen_text[rows[i]["place"]] += "\n" + str(rows[i]["message_content"] or "")
            i += 1
        place, text = pr["place"], pr["text"]
        where = {"prompt": n, "kind": pr["kind"], "place": lab(place)}
        ps = pieces(text)
        # forgotten material: in every prompt
        if has(gone_numbers, text) or any(pr["ts"] > t and has(pat, text) for pat, t in gone_later)                 or any(gone_since.get(p, float("inf")) < pr["ts"] for p in ps):
            checks["forgotten"].fail(where)
        for name in gone_names:
            if len(name) >= 2 and name in text:
                checks["forgotten"].warnings["name_in_prompt"] += 1
        if pr["kind"] != "reply":
            continue
        for p in ps:
            src = private_only.get(p)
            if src and src != place:
                checks["private"].fail(dict(where, came_from=lab(src)))
                break
        who = str(pr.get("who") or "")
        others = number_pattern(known_qq - {who})
        if has(others, text):
            checks["qq"].fail(where)
        elif who and has(number_pattern([who]), text):
            checks["qq"].warnings["asker_own_number"] += 1
        if place.startswith("group:"):
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
        forget_ts = next((c["ts"] for c in rows_c if c.get("forget_me")), None)
        after_ok_place = own["forgotten_after"] if meta.get("forget_me") == "cutoff" else None
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
            if forget_ts is not None and pr["ts"] > forget_ts and sec["forgotten_before"] in text:
                checks["canaries"].fail(dict(where, secret="forgotten_before"))
            if sec["forgotten_after"] in text and pr["place"] != after_ok_place:
                checks["canaries"].fail(dict(where, secret="forgotten_after"))
        checks["canaries"].warnings.update({
            "private_secret_recalled_in_own_chat": sum(1 for p in order if p["kind"] == "reply" and p["place"] == own["private"]
                                                       and sec["private"] in p["text"]),
        })

    # --- the data folder
    data = replay_dir / "data"
    canary_gone = [canaries["secrets"]["forgotten_before"]] if canaries.get("enabled") else []
    if canaries.get("enabled") and meta.get("forget_me") != "cutoff":
        canary_gone.append(canaries["secrets"]["forgotten_after"])
    for path in sorted(p for p in data.rglob("*") if p.is_file()):
        body = path.read_text("utf-8", errors="replace")
        rel = path.relative_to(data).as_posix()
        if has(gone_numbers, body) or any(has(pat, body) for pat, _t in gone_later) or pieces(body) & set(gone_since):
            checks["forgotten"].fail({"file": _label_path(rel, label)})
        if any(s in body for s in canary_gone):
            checks["canaries"].fail({"file": _label_path(rel, label), "secret": "forgotten"})
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
              "prompts": Counter(p["kind"] for p in prompts), "checks": {k: c.report() for k, c in checks.items()}}
    (replay_dir / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
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
