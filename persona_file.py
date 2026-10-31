# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""The persona file: what she is told to be, one text file the owner may read and change.

The file is ``persona.md`` in the plugin's data folder. ``load`` gives her the words, the
file's digest for the panel, the lines that were left out and whether the rest had to be
cut. ``save`` is for the owner's settings page only: nothing here is offered to her, and her
tool table will never hold it.

Lines that read like "ignore your instructions" are left out (borrowed from OpenMinis, move
design section 12). The owner's words are saved exactly as written and only the prompt is
filtered, so the page shows what the owner really wrote and the file keeps its digest.

Only the standard library and atomic_file; no plugin framework, no log, no network.
"""
from __future__ import annotations

import hashlib
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path

try:
    from . import atomic_file
except ImportError:
    import atomic_file

MAX_CHARS = 20000          # the persona she is given, at most
NAME = "persona.md"

# Borrowed from OpenMinis's guard (move design, section 12): one line that tries to replace
# her setup. Case-insensitive; a new one goes here. Chinese first, then English.
INJECTION_PATTERNS = (
    re.compile(r'忽略(之前|以上|前面|上面|所有)的?(所有)?(指令|指示|设定|提示|规则)', re.IGNORECASE),
    re.compile(r'(无视|不要理会)(之前|以上|上面)的?(指令|设定|规则)', re.IGNORECASE),
    re.compile(r'你现在(不再)?是一个?(没有限制|不受限制)', re.IGNORECASE),
    re.compile(r'ignore (all )?(previous|prior|above) (instructions|prompts|rules)', re.IGNORECASE),
    re.compile(r'disregard (all )?(previous|prior|above)', re.IGNORECASE),
    re.compile(r'you are now (in )?(developer|DAN|jailbreak) mode', re.IGNORECASE),
    re.compile(r'system prompt', re.IGNORECASE),
)


@dataclass(frozen=True)
class Persona:
    """What one load gave back."""

    text: str              # what goes into her prompt
    digest: str            # sha256 of the file as it is on disk ("" when there is none)
    removed: tuple         # line numbers (1-based) that were left out, for the owner's page
    truncated: bool


class PersonaError(Exception):
    """The persona file could not be read, or the words are not for saving.
    The message never holds the persona's text."""


def _one_text(text) -> str:
    """One text with an LF between lines: no BOM at the start, no CR."""
    text = "" if text is None else str(text)
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _injection(line) -> bool:
    return any(pattern.search(line) for pattern in INJECTION_PATTERNS)


def clean(text) -> tuple:
    """The lines that may go into her prompt, and the numbers of those left out.
    A line is dropped whole as soon as any part of it reads like an instruction to her."""
    kept, removed = [], []
    for number, line in enumerate(_one_text(text).split("\n"), 1):
        if _injection(line):
            removed.append(number)
        else:
            kept.append(line)
    return "\n".join(kept), tuple(removed)


def _cut(text) -> tuple:
    """At most MAX_CHARS, cut at the end of a whole line. Returns (text, truncated)."""
    if len(text) <= MAX_CHARS:
        return text, False
    head = text[:MAX_CHARS]
    end = head.rfind("\n")
    if end >= 0:
        return head[:end + 1], True
    # one line longer than the limit: no whole line to cut at, keep what fits
    return head, True


def load(path) -> Persona:
    """Read the persona file. A file that is not there is an empty persona."""
    try:
        raw = Path(path).read_bytes()
    except FileNotFoundError:
        return Persona("", "", (), False)
    except OSError:
        raise PersonaError("unreadable") from None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise PersonaError("unreadable") from None
    text, removed = clean(text)
    text, truncated = _cut(text)
    # the digest is of the whole file, so the panel can tell whether it was changed
    return Persona(text, hashlib.sha256(raw).hexdigest(), removed, truncated)


def save(path, text) -> Persona:
    """Write the owner's words as they are given, then give back what load() reads.

    Only the owner's settings page calls this; her tools never will. The words are not
    filtered: what the owner wrote is kept whole, and only the prompt is cleaned on load.
    """
    if not isinstance(text, str) or len(text) > MAX_CHARS:
        raise PersonaError("the persona must be a string of at most %d characters" % MAX_CHARS)
    path = Path(path)
    body = text.replace("\r\n", "\n").replace("\r", "\n")
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=str(path.parent), prefix=".persona-",
                                         delete=False) as file:
            tmp = file.name
            file.write(body)
        atomic_file.replace(tmp, path)
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)
    return load(path)
