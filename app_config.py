# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Her own configuration file: read it, write it, and compare it with AstrBot's copy.

The switches, lists and prices used to sit in AstrBot's plugin configuration, whose shape
is `_conf_schema.json`: flat entries of five kinds, each with a default. After the move
they sit in one `config.json` read by this module. It is not connected to the plugin yet.

A setting the file does not have takes its default. A key this version does not know is
kept as it is, so a later version or a hand edit never loses what the owner set.
`problems` names keys and the kind of trouble only, never a value: lists and prices do not
belong in a log. Only the standard library and `atomic_file`; no AstrBot.
"""
import json
import os
import tempfile
from pathlib import Path

try:
    from . import atomic_file
except ImportError:
    import atomic_file

SCHEMA_PATH = Path(__file__).with_name('_conf_schema.json')
EMPTY = {'bool': False, 'string': '', 'int': 0, 'float': 0.0, 'list': []}
UNREADABLE = 'unreadable'


class ConfigError(Exception):
    """The configuration was not written; the message never holds a value."""


def load_schema(path=SCHEMA_PATH) -> dict:
    """The schema AstrBot drew its panel from: every setting, flat, with a type."""
    with open(path, encoding='utf-8') as file:
        schema = json.load(file)
    if not isinstance(schema, dict):
        raise ConfigError('schema is not an object')
    return schema


def defaults(schema) -> dict:
    """Every setting's default: the schema's own, or the empty value of its type."""
    return {key: _default_of(item) for key, item in schema.items()}


def load(path, schema) -> tuple:
    """(config, problems) read from `path`; a missing file is simply all defaults.

    A problem is `unreadable` (no JSON object there), `unknown: <key>` (kept anyway) or
    `type: <key>` (the value was dropped and the default stands). No value in a problem.
    """
    config = defaults(schema)
    try:
        with open(path, encoding='utf-8-sig') as file:
            data = json.load(file)
    except FileNotFoundError:
        return config, []
    except (OSError, ValueError, UnicodeError):
        return defaults(schema), [UNREADABLE]
    if not isinstance(data, dict):
        return defaults(schema), [UNREADABLE]
    problems = []
    for key, value in data.items():
        if key not in schema:
            config[key] = value
            problems.append('unknown: ' + key)
            continue
        kind = schema[key].get('type')
        if not _fits(value, kind, schema[key].get('nullable', False)):
            problems.append('type: ' + key)
            continue                       # the value is dropped; the default already stands
        config[key] = float(value) if kind == 'float' and value is not None else value
    return config, problems


def save(path, config, schema) -> None:
    """Write `config` as UTF-8 JSON, two-space indents, schema order first.

    A value of the wrong type raises ConfigError and nothing is written. The write goes
    to a temp file in the same folder and then through `atomic_file.replace`, so a
    failure here leaves the old file as it was.
    """
    text = json.dumps(_checked(config, schema), ensure_ascii=False, indent=2) + '\n'
    path = Path(path)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                                         dir=path.parent, prefix='.app-config-',
                                         delete=False) as file:
            tmp = file.name
            file.write(text)
        atomic_file.replace(tmp, path)
        tmp = None
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)


def compare(ours, astrbot_config, schema) -> list:
    """The schema keys whose two values differ; a key AstrBot's copy lacks is its default."""
    different = []
    for key, item in schema.items():
        default = _default_of(item)
        left = ours[key] if key in ours else default
        right = astrbot_config[key] if key in astrbot_config else default
        if not _same(item.get('type'), left, right):
            different.append(key)
    return different


def _default_of(item):
    """The schema entry's own default, or the empty value of its type; always a copy."""
    if 'default' in item:
        return _copy(item['default'])
    return _copy(EMPTY.get(item.get('type')))


def _copy(value):
    """A list of ours, so a caller cannot change the schema through a default."""
    return list(value) if isinstance(value, list) else value


def _fits(value, kind, nullable=False):
    """Whether a value read from JSON is of the setting's type; a bool is never an int."""
    if kind == 'float' and nullable and value is None:
        return True
    if kind == 'bool':
        return type(value) is bool
    if kind == 'int':
        return type(value) is int
    if kind == 'float':
        return type(value) is int or type(value) is float
    if kind == 'string':
        return isinstance(value, str)
    if kind == 'list':
        return isinstance(value, list)
    return True    # a kind this version does not know: keep what the owner set


def _same(kind, left, right):
    """A float setting compares as a float, so 1 and 1.0 are the same value."""
    if kind == 'float':
        try:
            return float(left) == float(right)
        except (TypeError, ValueError):
            return left == right
    return left == right


def _checked(config, schema):
    """`config` in schema order with defaults filled in, or ConfigError on a wrong type."""
    ordered = {}
    for key, item in schema.items():
        kind = item.get('type')
        value = config[key] if key in config else _default_of(item)
        if not _fits(value, kind, item.get('nullable', False)):
            raise ConfigError('wrong type: ' + key)
        ordered[key] = float(value) if kind == 'float' and value is not None else _copy(value)
    for key, value in config.items():
        if key not in schema:
            ordered[key] = _copy(value)
    return ordered
