# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Move AstrBot's plugin configuration into her own config.json.

    python tools/migrate_config.py --astrbot <AstrBot's plugin config> --out <new config.json>
    python tools/migrate_config.py --astrbot <AstrBot's plugin config> --check <existing config.json>

The switches, lists and prices used to sit in AstrBot's plugin configuration, shaped by
`_conf_schema.json`. `app_config` reads, writes and compares them; this is the run on the
moving day. It reads AstrBot's copy and never writes it, and it prints key names, counts and
paths only, never a value: lists and prices do not belong on a screen or in a log.

Exit codes:
    0  written (or compared) and every setting agrees;
    1  written (or compared), but a person should look: a `type:` problem or a key that differs;
    2  stopped, nothing written.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import app_config  # noqa: E402
from tools import _guard  # noqa: E402


def _stop(message) -> int:
    """Print one line that names a key or a path only, and give back the exit code for stopping."""
    print(message, file=sys.stderr)
    return 2


def _astrbot(path):
    """AstrBot's copy as a plain dict, or None when it cannot be read (never a value)."""
    try:
        with open(path, encoding='utf-8-sig') as file:
            data = json.load(file)
    except (OSError, ValueError, UnicodeError):
        return None
    return data if isinstance(data, dict) else None


def _say(schema, problems, different) -> None:
    """The screen: how many settings, the problems, the keys that differ. No value."""
    print('settings: %d' % len(schema))
    for problem in problems:
        print('problem: %s' % problem)
    for key in different:
        print('differs: %s' % key)


def convert(astrbot, out) -> int:
    """Write `out` from AstrBot's copy, read it back and compare; give back the exit code."""
    astrbot = Path(astrbot)
    if not astrbot.is_file():
        return _stop('cannot read: %s (nothing written)' % astrbot)
    schema = app_config.load_schema()
    config, problems = app_config.load(astrbot, schema)
    if app_config.UNREADABLE in problems:
        return _stop('cannot read: %s (nothing written)' % astrbot)
    try:
        target = _guard.output_file(out, 'the new config')
    except _guard.Refused as refused:
        return _stop(str(refused))
    if target.exists():
        return _stop('%s is already there (nothing written)' % target)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        app_config.save(target, config, schema)
    except app_config.ConfigError as error:
        return _stop('%s (nothing written): %s' % (target, error))
    except OSError:
        return _stop('%s cannot be written (nothing written)' % target)
    theirs = _astrbot(astrbot)      # read again, with json, for the item-by-item comparison
    if theirs is None:
        return _stop('cannot read: %s (the file was written)' % astrbot)
    read_back, _problems = app_config.load(target, schema)
    different = app_config.compare(read_back, theirs, schema)
    _say(schema, problems, different)
    print('wrote: %s' % target)
    if any(problem.startswith('type:') for problem in problems) or different:
        return 1
    return 0


def check(astrbot, path) -> int:
    """Compare an existing config.json with AstrBot's copy; write nothing; give back the exit code."""
    astrbot, path = Path(astrbot), Path(path)
    if not astrbot.is_file():
        return _stop('cannot read: %s (nothing compared)' % astrbot)
    theirs = _astrbot(astrbot)
    if theirs is None:
        return _stop('cannot read: %s (nothing compared)' % astrbot)
    schema = app_config.load_schema()
    ours, problems = app_config.load(path, schema)
    if app_config.UNREADABLE in problems:
        return _stop('cannot read: %s (nothing compared)' % path)
    different = app_config.compare(ours, theirs, schema)
    _say(schema, (), different)
    return 1 if different else 0


def main(argv=None) -> int:
    """The command line: --out writes her config.json, --check compares one; give back the code."""
    parser = argparse.ArgumentParser(description="Move AstrBot's plugin configuration into her own config.json.")
    parser.add_argument('--astrbot', required=True, help="AstrBot's plugin configuration: read only")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--out', help='the new config.json (not in the repository, not in AstrBot data)')
    group.add_argument('--check', help="an existing config.json to compare with AstrBot's copy")
    args = parser.parse_args(argv)
    if args.out:
        return convert(args.astrbot, args.out)
    return check(args.astrbot, args.check)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
