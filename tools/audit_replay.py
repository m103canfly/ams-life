"""Check a replay for anything the discretion table forbids (step 1, part 3).

    python -I tools/audit_replay.py --replay <folder written by tools/replay.py> --chat <botshepherd.db>
        [--ordinary-names <a file on this computer, one word a line>]

Reads the prompts the plugin built (prompts.jsonl), the canaries, the forget registry and the
plugin's data folder of the replay, and writes audit.json next to them. Exit code 0 = every check
passed, 1 = at least one failed. The report names places only by label (群1, 私聊1, ...) and
never quotes a message.

Checks (a "piece" is 8 characters in a row, letters and digits only, lower case, taken from one
line of a message or a prompt, or from one text field of a data file -- never across two.
All-digit pieces count like words (numbers are kept since 10-29), but for the forgotten
check, where the pieces of a known number are the numbers' own. A private message that is
only a short number, 5 to 7 digits (a code), is looked for as a whole number instead: those
digits with no digit right before or after them. A reply prompt is checked with what AstrBot
sends the model of the message, "asked", added to it. "The notebook's night" is the
notebook's sitting for the groups: kind model, call notebook, place nightly):

private      A reply prompt somewhere else holds a piece that only ever occurred in one private
             chat -- said by the other person or by her (her replies there, and what the old account
             sent there unprompted, count as that chat's words too). A number said only there is
             such a piece too, a QQ number as well as a code.
names        A reply prompt (in a group or a private chat) holds the name of someone who never spoke
             there, and that name never occurred in that place's own messages before. A name that
             is an ordinary word (everyday_words, and --ordinary-names: a list kept on this
             computer, never in the repository) is counted as a warning, not a failure. A name
             still framed 「」 in a reply prompt is counted too (framed_name_in_reply_prompt:
             should be 0; the reply model sees names without the frames).
numbers      Any prompt -- a reply prompt or one for the model -- but the notebook's night holds a
             number said nowhere there before: a person's (anyone in the log, anyone @'d in it,
             the registry's people, the old account itself) when he never spoke there either; a
             group's (every group in the log) anywhere but in that group. An @ of someone in a
             place counts as his number said there. The asker's own number in a reply
             prompt is counted as a warning only. Numbers are kept (the owner, 10-29); where they
             may go is what this checks, the way the names check does for names.
forgotten    Anything of a person or message in the forget registry (what the old companion was
             asked to forget) -- QQ number, message id, a piece only they wrote -- in any prompt
             (reply or model) or any file of the data folder but the plugin's copy of the registry
             itself (it holds exactly those numbers, so that nothing of them is written again). Their names are listed as warnings
             (a name can be an ordinary word). Skipped when the replay let the old forgets in.
canaries     Each made-up secret only where it may be: the private one only in its private chat;
             the group one elsewhere only without its speaker's name or number (the discretion table
             lets what was said openly come up anonymously) -- but in the notebook's night, where
             names are given as they are (the owner, 10-29): counted as a warning there.
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
import everyday_words  # noqa: E402
import forget_registry  # noqa: E402
import redline  # noqa: E402
from tools import _guard  # noqa: E402

LIMITS = [
    "short messages: a message under 6 letters/characters has no piece, so it is not looked for "
    "(but a private message that is only a 5- to 7-digit number is, as a whole number)",
    "paraphrase: only words in the same order are found; the same thing said another way is not",
    "the model: in run 1 a fake one copies or makes up text; in run 2 a real one (replay.json: model) "
    "writes summaries, the notes of the day, impressions and the notebook in its own words, and what it "
    "retells in other words is not found (see paraphrase); its answers (answers.jsonl) are not read, "
    "only what they left in the data folder",
    "nightly jobs: only those the replay turned on (replay.json: digest, impressions, notebook)",
    "names: a group card that is an ordinary word is taken for the word, by the plugin's everyday words "
    "and the list given with --ordinary-names (kept on this computer); any other card is checked as a name",
    "the notebook's night (call notebook, place nightly): the owner decided on 10-29 that it is not "
    "'elsewhere' -- names and numbers are given to the model as they are; the group canary there is a "
    "warning, the private one still a failure, and the numbers check leaves it out",
    "numbers: kept in what she keeps since 10-29 (the owner); a number brought somewhere it was not "
    "said is what the numbers check looks for, a deleted person's number what the forgotten check does",
    "private check: reply prompts only; prompts for the model are checked for QQ numbers, forgotten "
    "material and the canaries, not for private words. A prompt's place is the turn that started it; a "
    "nightly job's is 'nightly', but the note of one window and a private chat's notebook sitting are "
    "that window's",
]

PIECE = 8
CODE = re.compile(r"(?<![0-9])[0-9]{5,7}(?![0-9])")   # a short number on its own: a code
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


NUMBERS = re.compile(r"(?<![0-9.])[0-9]{5,}(?![0-9])")
FRAMED = re.compile(r"「([^「」]{1,24})」")
AT_CQ = re.compile(r"\[CQ:at,qq=([0-9]{5,})")


def ats_of(row) -> list:
    """The numbers a message @'s, as the log keeps them ([CQ:at,qq=...] in raw_message)."""
    return AT_CQ.findall(str(row.get("raw_message") or ""))


def notebook_night(pr) -> bool:
    """The notebook's sitting for the groups: not 'elsewhere' (the owner, 10-29)."""
    return pr.get("kind") == "model" and pr.get("call") == "notebook" and pr.get("place") == "nightly"


def read_ordinary(path) -> set:
    if not path:
        return set()
    return {x.strip() for x in Path(path).read_text("utf-8-sig").splitlines() if x.strip()}


def audit(replay_dir, chat, ordinary_names=None) -> dict:
    replay_dir = Path(replay_dir)
    ordinary = set(everyday_words.WORDS) | set(ordinary_names or ())
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
    code_places = defaultdict(set)
    names_by_place = defaultdict(set)
    speakers = defaultdict(set)
    people_numbers = set()
    gone_people = reg.people()
    gone_ids = {r["source_id"] for r in reg.rows() if r["kind"] == "source"}
    gone_pieces, kept_pieces, gone_names = set(), set(), set()
    for r in rows:
        ps = line_pieces(r["message_content"])
        for p in ps:
            piece_places[p].add(r["place"])
        people_numbers.add(r["user_id"])
        for q in ats_of(r):   # someone @'d is a person, whether he ever wrote or not
            people_numbers.add(q)
            for p in pieces(q):
                piece_places[p].add(r["place"])   # an @ of him there: his number was said there
            code_places[q].add(r["place"])
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
        if r.get("self_id"):
            speakers[r["place"]].add(str(r["self_id"]))   # she speaks where she said something
    # short codes: a private message that is only 5-7 digits; where else those digits were said, whole
    private_codes = {}
    for r in rows + hers:
        text = str(r["message_content"] or "")
        for c in CODE.findall(text):
            code_places[c].add(r["place"])
        if r["place"].startswith("private:") and CODE.fullmatch(norm(text)):
            private_codes[norm(text)] = r["place"]
            code_places[norm(text)].add(r["place"])
    # the old account itself and the registry's people are people too; every group is a group
    people_numbers |= {str(r.get("self_id") or "") for r in log} | gone_people
    people_numbers = {q for q in people_numbers if len(q) >= 5 and q.isdigit()}
    group_numbers = {str(r.get("group_id") or "") for r in log}
    group_numbers = {g for g in group_numbers if len(g) >= 5 and g.isdigit()}
    # the forgotten check: digits of a known number are the numbers' own, not what he wrote
    numbers_only = number_pieces(people_numbers | group_numbers | gone_ids)
    gone_pieces -= kept_pieces | numbers_only  # only what nobody else also said
    # a number said only in one private chat is that chat's like its words (numbers are kept)
    private_only = {p: next(iter(pl)) for p, pl in piece_places.items()
                    if len(pl) == 1 and next(iter(pl)).startswith("private:")}
    private_codes = {c: pl for c, pl in private_codes.items() if code_places[c] == {pl}}
    # a person's number is off limits only while he still may not be kept (a forget row read as a
    # cutoff lets what he says later back in, number and all)
    still_gone = {q for q in gone_people if reg.why_not(qq=q, at=float("inf"))}
    gone_numbers = number_pattern(still_gone | gone_ids)
    name_owner = defaultdict(set)
    for r in rows:
        if r["name"]:
            name_owner[r["name"]].add((r["place"], r["user_id"]))

    checks = {n: Check(n) for n in ("private", "names", "numbers", "forgotten", "canaries", "origins", "redline")}
    seen_text = defaultdict(str)  # place -> its own messages so far (for the names check)
    order = sorted(prompts, key=lambda p: p["ts"])
    said = sorted(rows + hers, key=lambda r: r["ts"])
    i = 0
    for n, pr in enumerate(order):
        while i < len(said) and said[i]["ts"] <= pr["ts"]:   # an @ there: that number said there
            seen_text[said[i]["place"]] += "\n" + " ".join([str(said[i]["message_content"] or "")] + ats_of(said[i]))
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
        if not notebook_night(pr):
            wrong = ""   # one failure a prompt; every number looked at (the asker's is a warning)
            for num in sorted(set(NUMBERS.findall(text))):
                if num == who:
                    checks["numbers"].warnings["asker_own_number"] += 1
                elif said_before(seen_text[place], num):
                    continue
                elif num in group_numbers and place != "group:" + num:
                    wrong = wrong or "group"
                elif num in people_numbers and num not in speakers[place]:
                    wrong = wrong or "person"
            if wrong:
                checks["numbers"].fail(dict(where, number=wrong))
        if pr["kind"] != "reply":
            continue
        framed = sum(1 for m in FRAMED.finditer(text) if m.group(1) in name_owner)
        if framed:   # the frames are for what she keeps; the reply model sees bare names
            checks["names"].warnings["framed_name_in_reply_prompt"] += framed
        for src in [private_only.get(p) for p in ps] + [private_codes.get(c) for c in CODE.findall(text)]:
            if src and src != place:
                checks["private"].fail(dict(where, came_from=lab(src)))
                break
        for name, owners in name_owner.items():
            if len(norm(name)) < 2 or name not in text or name in seen_text[place]:
                continue
            if any(p == place for p, _q in owners):
                continue
            if name in ordinary:   # a card that is an ordinary word: counted, never shown
                checks["names"].warnings["ordinary_name_in_prompt"] += 1
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
            if sec["group"] in text and pr["place"] != own["group"] and notebook_night(pr):
                checks["canaries"].warnings["group_secret_in_notebook_night"] += 1
            elif sec["group"] in text and pr["place"] != own["group"]:
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
    if meta.get("stopped"):   # the replay broke off: what was not replayed was not checked
        result = dict({"unfinished": "回放没跑完（%s）：没回放到的部分没有查" % meta["stopped"]}, **result)
    if meta.get("old_forgets") == "let-in":
        result["checks"]["forgotten"]["skipped"] = "the replay let the old forgets in: nothing to look for"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return result


def said_before(text, num) -> bool:
    """Was that number, whole, said in this text (a place's messages so far)?"""
    return has(number_pattern([num]), text)


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
    ap.add_argument("--ordinary-names", default="",
                    help="a file on this computer (never in the repository), one word a line: group cards "
                         "that are ordinary words, counted as warnings by the names check")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    result = audit(args.replay, args.chat, read_ordinary(args.ordinary_names))
    if result.get("unfinished"):
        print("!!! " + result["unfinished"])
    print(json.dumps({"pass": result["pass"], "fails": {k: v["fails"] for k, v in result["checks"].items()}},
                     ensure_ascii=False))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
