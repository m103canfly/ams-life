# Vendored: Galaxy View

The brain map's drawing, camera and layout are taken from **Galaxy View**
(<https://github.com/longwind1984/galaxy-view>), version 0.6.1, commit
`b49b60cb04687783153f24ff7f9b0a0af59334af`, Copyright (c) 2026 Rick, MIT License
(`LICENSE` in this folder). Galaxy View is an Obsidian plugin; only the parts that
do not depend on Obsidian were copied, with their folder layout:

- `render/`: `AggregateRenderer.ts` (stars, links, focus dimming, bloom), `shaders.ts`,
  `starfield.ts`, `nebula.ts` (nebula dome, cluster clouds), `linkCurves.ts`,
  `graphTransform.ts`, `reveal.ts`, `presets.ts` (deep space / daylight),
  `palette.ts`, `stylePresets.ts` (reference for the style values)
- `interactions/CameraDirector.ts` (orbit, fly-to, cruise; see below)
- `layout/` (d3-force-3d in a Web Worker, main-thread fallback, galaxy forces)
- `quality/tiers.ts` (high / low / mobile), `timing/frameClock.ts`
- `data/Adjacency.ts`, `data/seed.ts`, `data/tagLens.ts` (needed by `palette.ts`),
  `constants.ts`, `types.ts`, `typings/d3-force-3d.d.ts`

Not copied: the Obsidian view and settings, reading notes, the control panel,
overlays, tour, search modal, i18n, bench.

Changes made here (everything else is unchanged):

- `render/shaders.ts`: a point marked `aGhost` (Galaxy View: an unresolved note,
  drawn dimmer) is drawn as a hollow ring; ams-life uses it for private memories.
- `types.ts`, `layout/forceWorker.ts`, `layout/WorkerForceLayout.ts`,
  `layout/MainThreadForceLayout.ts`: optional `ball` / `ballStrength` / `sidePull`
  layout parameters and a per-node `side`, so the stars gather into a ball
  (`../ball.js`, `forceBall`) with private chats leaning to one side. With the
  parameters left out the layout is Galaxy View's as before.
- `layout/forceWorker.ts`, `layout/WorkerForceLayout.ts`: a `pause` message, so
  the worker stops ticking while the map is hidden in the panel and goes on when
  it is shown again.

`interactions/CameraDirector.ts` is kept for reference but no longer used: the
brain map turns like a globe (`../globe.js`), which its orbit controls cannot.

ams-life's own code that drives it is `../brain.js`. Galaxy View lists
3d-force-graph and three-spritetext as dependencies but its renderer does not
import them, so they are not used here either.
