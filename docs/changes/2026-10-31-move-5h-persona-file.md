# 2026-10-31 move-5h: the persona file

The owner is moving the plugin out of AstrBot (design note: `pending\设计-脱离AstrBot-20261030.md`).
Section 1 asks for the persona card to become one file, `persona.md` in the plugin's data
folder, that one page of the panel shows and changes and only the owner may change; section 12
(borrowed from OpenMinis) asks for a length limit and for lines like "ignore your previous
instructions" to be taken out before the persona reaches her. This card writes only that layer:
it is not wired into the plugin, no real persona is exported (that is step 7, at the machine)
and no panel page is written.

New files only; no existing file is changed, so behaviour is unchanged and the golden traces
stay the same:

* `persona_file.py`: `MAX_CHARS` (20000), `NAME` ("persona.md"), `INJECTION_PATTERNS`,
  `Persona` (a frozen dataclass: `text`, `digest`, `removed`, `truncated`), `PersonaError`,
  and `load(path)`, `save(path, text)`, `clean(text)`. Only the standard library and
  `atomic_file`: no plugin framework, no log, no network. `clean` takes off a leading BOM,
  makes every newline `\n`, and drops a whole line as soon as any part of it matches one of
  the patterns (case-insensitive), noting the 1-based line numbers. `load` gives an empty
  `Persona` when there is no file, `PersonaError("unreadable")` when the file is not UTF-8,
  cleans the rest, cuts it to `MAX_CHARS` at the end of a whole line (`truncated` says
  whether it had to), and takes `digest` from the sha256 of the whole file as it is on disk.
  `save` refuses anything that is not a string or is longer than `MAX_CHARS`, writes the
  owner's words as they are (UTF-8, `\n`), puts the temp file in the same folder and swaps it
  in with `atomic_file.replace`, then gives back `load(path)`. No error message holds the
  persona's text.
* `tests/test_persona_file.py`: the cases below; every file is made in the test's own
  temporary folder and every line of persona text is made up.

Borrowed from OpenMinis: `INJECTION_PATTERNS`, our own guard against lines that try to replace
her setup. It is a plain tuple of case-insensitive patterns, Chinese and English, with a
comment saying where it comes from, so another one is easy to add later. A line is dropped
whole, not rewritten: a half-filtered sentence would still be read by the model.

The owner's words are saved exactly as written and only the prompt is filtered on load. The
file is the owner's; the panel will show what really stands in it, its `digest` tells the page
whether the file was changed, and `removed` tells the owner which lines will not reach her. If
`save` filtered, a line the owner wrote would silently vanish from the file she just saved.

Only the owner may change it: `save` is for the panel's settings page, this module offers her
no other writer, and it holds no tool at all (nothing a tool table could take), so nothing of
hers can call it. Her side only ever reads.

New module line for README's table of modules (brought up to date later):

| `persona_file.py` | 人设文件（插件数据目录里的 `persona.md`）：读时滤掉像“忽略之前的指令”的行、在行尾截到长度上限，行号给主人的页面；只有主人的设置页能写，写的原文不滤、读时才挑 |

Tests (13, `python -m unittest tests.test_persona_file`): no file is an empty persona; a
folder is `PersonaError`; the words come back with the file's sha256 as `digest`; one changed
character changes it; a BOM and `\r\n` are taken off; each `INJECTION_PATTERNS` entry loses
its line with the right numbers (the English one is written in capitals); her own setting
lines stay; a line with only a part that reads like an instruction goes whole; a long file is
cut at the end of a whole line and `truncated` is set; saving more than `MAX_CHARS`, or
something that is not a string, is refused and leaves the file as it was; a file that is not
UTF-8 is `PersonaError` without its words; `save` keeps an "ignore the instructions" line on
disk while the prompt leaves it out with its line number; and the module's source is read to
check it imports no framework and no log and holds no tool.

Full suite: 1289 tests OK outside the sandbox with `venv-ams-life` (main e39fb76 had 1276; +13 in `tests/test_persona_file.py`),
the file tests included. Golden traces unchanged.
