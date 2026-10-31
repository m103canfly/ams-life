# 2026-10-31 move-5e4a: the new program's persona and its config write-back

The new program has no AstrBot, so two places that reach for AstrBot have to be able to do
without it: `_persona_text` asked AstrBot's persona management for her words, and
`_persist_plugin_config` asked AstrBot's configuration object to save the switches the panel
changed. Move 5h gave her a `persona.md` (`persona_file`) and move 5g a `config.json`
(`app_config`); this card lets both methods use them, and leaves the AstrBot path exactly as
it was.

## What changed

`mixin_llm._persona_text` looks for `_neutral_persona` before its old body. When the new
program set it (5e-5 sets it to the text `persona_file.load(...)` gives back), the method
returns `str(_neutral_persona)` and never touches `self.context.persona_manager`. On AstrBot
the attribute does not exist, `getattr` gives `None`, and the old code runs unchanged.

`mixin_settings._persist_plugin_config` gains one branch at the end of its chain. It still
updates the configuration dict in memory first, then calls `save_config_async` if the object
has it, then `save_config`, and only when neither exists does it look at
`self._config_path` (5e-5 sets it to the new program's `config.json`). With a path it calls
`app_config.save(path, self.config, schema)`, where `schema` is `self._config_schema` when
the new program gave one, and the repository's `_conf_schema.json` through
`app_config.load_schema()` otherwise. The import is written like the module's other imports
(`try: from . import ... / except ImportError: import ...`). A write that fails (a wrong
type, a full disk) is caught by the method's existing `except` and logged with the same
warning as before, so the panel does not break.

`tests/test_persona_config_neutral.py` (new) covers both sides:

* `_persona_text` with `_neutral_persona` set returns it (also the empty string) and asks
  AstrBot's persona management nothing; without it, eight AstrBot cases (a dict or an object
  by id and by default, an id the manager cannot find, a lookup that raises, persona
  management gone) give the same answer as the frozen `_persona_text` copied from 97faf6e;
* `_persist_plugin_config` on a plain dict and a `_config_path` in the test's own temporary
  folder writes the changed key and `app_config.load` reads it back; with no
  `_config_schema` the repository schema is used; with no `_config_path` nothing is written
  and memory still changes; with either AstrBot saver only that saver is called and the new
  file is not touched; a save of a wrong type only warns and writes nothing;
* the source of `mixin_llm` and `mixin_settings` is read: neither imports AstrBot.

## Behavior

Unchanged on AstrBot: without `_neutral_persona`, `_persona_text` is the old method line for
line, and without `_config_path` the save chain does exactly what it did. Neither attribute
is set anywhere in the plugin yet, so nothing is wired in and no golden trace moves. The
method count stays 504: both changes are inside existing methods, and no plugin method is
added. No dependency is added; `app_config` and the standard library are already in the
repository.

## Tests

Tests: run by the dispatcher outside the sandbox (dsh's sandbox cannot write temporary
folders), one file at a time with `venv-ams-life`: `tests.test_persona_config_neutral` (8),
`test_basics` (504), `test_golden` (unchanged), `test_app_config`, `test_persona_file`,
`test_plugin_pages` and `test_panel_api` all pass. The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).

The new file has eight tests (2 + 5 + 1). Here the sandbox cannot write temporary files: the
five config write-back tests stopped at their temporary folder and the run had to be stopped,
so this file did not finish in the sandbox. `test_basics` (504), `test_golden` (unchanged),
`test_app_config`, `test_persona_file`, `test_plugin_pages` and `test_panel_api` were not
run here for the same reason; the dispatcher runs them.

The two spot checks stay for the last round: A, `_persona_text` ignoring `_neutral_persona`,
must fail test 1; B, `_persist_plugin_config` not writing `_config_path`, must fail test 2.
