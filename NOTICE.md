# NOTICE

ams-life is a modified version of **BioCore · 拟态生物情绪核心**
(<https://github.com/Johnhmzm/astrbot_plugin_biocore>), version 1.2.99, upstream commit
`b3c214c80c85f3e35d82fdb5e04c1809dfac9b28`, Copyright (C) 2026 Johnhmzm,
licensed under the GNU Affero General Public License v3.0.

ams-life is distributed under the same license (see `LICENSE`). The first commit of this
repository is the unmodified upstream snapshot; every later change is in the git history.

## Modifications (summary, newest first)

| Date | Change |
| --- | --- |
| 2026-10-29 | The brain map in the panel ("她的脑子", `pages/dashboard/brain_frame.js`): `tools/brain/build.mjs` writes the page twice, byte for byte, to `pages/brain/` and `pages/dashboard/brain/` (AstrBot serves a plugin page only from its own folder), from sources now in `tools/brain/src/page/`; the panel shows it in a srcdoc frame on the first visit, passes on its reads (`apiGet`, the three brain routes only) by postMessage (`tools/brain/src/embed.js`), stops its drawing while another view is shown (a `pause` message added to Galaxy View's layout worker) and fills the panel instead of full screen inside AstrBot. `tests/panel_shell/` stands in for AstrBot's web panel in the tests. |
| 2026-10-29 | Small fixes, second batch: turning the red-line switch on also sweeps each place's copy of its events (archived first); the panel's red-line count reads her group windows without writing them back; what she writes in her notebook is scrubbed when kept; `_scrub_stores` makes `_write_library` reread the library after rewriting it; the long-term insight is noted as not ready to be switched on (it mixes windows). |
| 2026-10-29 | Small fixes, first batch: the replay checks `--out` before it starts a model ledger, and feeds a quote of a forgotten message in as AstrBot hands it over; the replay audit looks for a short private code (5-7 digits) as a whole number; `_write_library` also scrubs numbers from (and checks red lines in) memories whose words changed; the brain map treats an all-digit card as no name. |
| 2026-10-28 | Review of PR #11: the brain map reads files on the event loop's thread (where she writes them) and builds in a worker thread from memory and a copy of the forget registry (`ForgetRegistry.copy_of`); her temp-file writes go through `atomic_file.replace`, which retries `os.replace` briefly on `PermissionError`; the brain pages answer errors with a short reason only. |
| 2026-10-28 | Brain map stage 2: read-only panel routes `page/brain`, `page/brain/node`, `page/brain/search` (`mixin_brain.py`, `brain_graph.py`); each reply's recall noted as ids only (`brain_turns.json`, last 200 turns), pruned by the owner's deletes and after a restore. |
| 2026-10-28 | Added the read-only brain map page (`pages/brain/`, built from `tools/brain/`), with invented sample data only. |
| 2026-10-27 | Split `main.py` into `common.py`, `body.py` and eight `mixin_*.py` modules without changing behaviour (golden traces identical). Dashboard backup now archives every `.py` module. |
| 2026-10-27 | Renamed the plugin to `astrbot_plugin_ams_life` (register name, data directory, dashboard routes, backup archive paths, update-check repository). Moved upstream README/CHANGELOG/UPDATE to `docs/upstream/`. Added an offline test suite (`tests/`) with golden traces recorded from the unmodified code. |

Modified source files carry a header line pointing to this file.

## Third-party code

The brain map page (`pages/brain/brain.bundle.js`, and the same file in `pages/dashboard/brain/`) bundles:

- **Galaxy View** 0.6.1 (<https://github.com/longwind1984/galaxy-view>), Copyright (c) 2026 Rick,
  MIT License. Its rendering, camera and layout code is vendored in `tools/brain/src/galaxy/`
  (see the README there for what was copied and changed).
- **three.js** 0.184.0, Copyright 2010-2026 Three.js Authors, MIT License.
- **d3-force-3d** 3.0.6 and its d3 dependencies (d3-binarytree, d3-octree: MIT; d3-dispatch,
  d3-quadtree, d3-timer: ISC).

The license text of each is in `pages/brain/licenses/` (and `pages/dashboard/brain/licenses/`).
