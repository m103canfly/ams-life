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
| 2026-10-28 | Added the read-only brain map page (`pages/brain/`, built from `tools/brain/`), with invented sample data only. |
| 2026-10-27 | Split `main.py` into `common.py`, `body.py` and eight `mixin_*.py` modules without changing behaviour (golden traces identical). Dashboard backup now archives every `.py` module. |
| 2026-10-27 | Renamed the plugin to `astrbot_plugin_ams_life` (register name, data directory, dashboard routes, backup archive paths, update-check repository). Moved upstream README/CHANGELOG/UPDATE to `docs/upstream/`. Added an offline test suite (`tests/`) with golden traces recorded from the unmodified code. |

Modified source files carry a header line pointing to this file.

## Third-party code

The brain map page (`pages/brain/brain.bundle.js`) bundles:

- **Galaxy View** 0.6.1 (<https://github.com/longwind1984/galaxy-view>), Copyright (c) 2026 Rick,
  MIT License. Its rendering, camera and layout code is vendored in `tools/brain/src/galaxy/`
  (see the README there for what was copied and changed).
- **three.js** 0.184.0, Copyright 2010-2026 Three.js Authors, MIT License.
- **d3-force-3d** 3.0.6 and its d3 dependencies (d3-binarytree, d3-octree: MIT; d3-dispatch,
  d3-quadtree, d3-timer: ISC).

The license text of each is in `pages/brain/licenses/`.
