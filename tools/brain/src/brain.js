// ams-life (AGPL-3.0); see NOTICE.md.
// The brain map page. Drawing, camera and layout come from Galaxy View
// (MIT, ./galaxy, see ./galaxy/README.md); this file feeds it her graph and
// keeps the page's own parts: filters, search, the drawer, the body nuclei and
// "what each reply recalled". Read only: the page only ever reads through
// bridge.apiGet and has no way to write.
//
// Data: from the panel API (mixin_brain.py, fetched in parts by data.js) when
// opened inside AstrBot's plugin view; when the API cannot be reached, or the
// page is opened on its own, the invented sample (sample.js, loaded before this
// bundle) with a badge saying so.
import { AdditiveBlending, BufferAttribute, BufferGeometry, Color, DynamicDrawUsage, NormalBlending, Points, ShaderMaterial, Vector3 } from 'three';
import { AggregateRenderer } from './galaxy/render/AggregateRenderer';
import { WorkerForceLayout } from './galaxy/layout/WorkerForceLayout';
import { MainThreadForceLayout } from './galaxy/layout/MainThreadForceLayout';
import { buildAdjacency, neighborhood } from './galaxy/data/Adjacency';
import { seedPosition, seedRadius } from './galaxy/data/seed';
import { TIERS } from './galaxy/quality/tiers';
import { DAYLIGHT, DEEP_SPACE } from './galaxy/render/presets';
import { CURVE_BOW } from './galaxy/render/linkCurves';
import { elapsedFrameSeconds, frameDeltaSeconds } from './galaxy/timing/frameClock';
import { GlobeCamera } from './globe.js';
import { ballRadius } from './ball.js';
import { fetchGraph, sampleBadge } from './data.js';
import { inPanel, panelBridge, runGate } from './embed.js';
import { SHOW_ALL_DEFAULT, TURN, baseLinesVisible, lineMap, openedLines, turnFrame, turnSteps } from './lines.js';

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
const IN_PANEL = inPanel(document);   // shown inside the panel: data through it (embed.js)
const DAY = 86400;

// Galaxy View's default "galaxy" style (its settings.ts DEFAULT_SETTINGS).
const LOOK = {
	bloom: { strength: 0.35, radius: 0.35, threshold: 0.22 },
	linkOpacity: 0.16, linkCurve: 0.35, twinkle: 0.5, nodeSize: 1.35,
	space: { nebula: 0.35, fieldStars: 0.25, clusterClouds: 0.3 },
	frameElevDeg: 50,
};
// A ball, not Galaxy View's flat disc: no flattening, core pull or spiral; a
// force gathers the stars into a ball (ball.js), private chats lean to one side.
const PHYSICS = { charge: -170, linkDistance: 55, linkStrength: 1.1, centerPull: 0.02, flatten: 0, coreGravity: 0, spiral: 0, velocityDecay: 0.6,
	ball: 0, ballStrength: 0.6, sidePull: 0.05 };
let physics = PHYSICS;
const DIM = { lit: 1, near: 1, rest: 0.12, turnRest: 0.07 };

const KIND = { window: '窗口', person: '人', memory: '记忆', event: '事件', note: '本子' };
const EDGE = { link: '联想', origin: '出处', about: '跟谁有关', impression: '印象' };
const CORES = [
	{ key: 'social', name: '想说话', c: '#ff8a1f' },
	{ key: 'curiosity', name: '好奇', c: '#54c08b' },
	{ key: 'boredom', name: '无聊', c: '#9a958c' },
	{ key: 'seen', name: '想被看见', c: '#f2c14e' },
	{ key: 'talked', name: '说多了', c: '#9b7bf6' },
	{ key: 'stress', name: '压力', c: '#e5533d' },
	{ key: 'valence', name: '心情', c: '#5b8def' },
];
// Group clusters each get a hue; private ones share one cool, pale family
// (and are drawn hollow), so public and private read apart at a glance.
const GROUP_HUES = [28, 200, 120, 330, 50, 170, 280, 90, 0, 230, 150, 300];
const PERSON = new Color('#efe7d2');
const LIT = new Color('#ffc861');
const HELD = new Color('#7d7f88');

// ------------------------------------------------------------------ state
let raw = null, source = 'sample', sample = null, bridge = null, whyNot = '';
let rawById = new Map(), rawAdj = new Map();
let G = { nodes: [], links: [] }, idx = new Map(), adj = null, src = [];
const posCache = new Map();
let renderer = null, director = null, layout = null, graphRadius = 80, viewRadius = 300, tier = TIERS.high;
let body = {}, liveBody = null;
// Drawing (and the layout worker) stop while the panel shows something else or the
// browser tab is hidden, and go on where they were when shown again (embed.js).
const gate = runGate((on) => {
	layout?.pause?.(!on);
	if (on) { prev = null; if (layout && !layout.ticks) layoutStarted = performance.now(); tick(); }
});
const panel = IN_PANEL ? panelBridge(window, { run: (on) => gate.set('panel', on), theme: (d) => applyTheme(d) }) : null;
const filter = { kinds: new Set(Object.keys(KIND)), win: '', vis: 'all', from: 24, to: 0 };
let sel = -1, turn = -1, turnStart = 0, hits = null, hover = -1, coreSel = -1;
let motion = true, dark = true, framed = false, settledOnce = false;
let showAll = SHOW_ALL_DEFAULT, lines = new Map();
const winColor = new Map();
let overrides = new Map();

// ------------------------------------------------------------------ data
function findBridge() {
	if (IN_PANEL) return panel;   // AstrBot's bridge is not in the panel's frame; the panel answers for it
	let b = null;
	try { b = window.AstrBotPluginView || window.AstrBotPluginPage || window.astrbotPluginView || null; } catch (e) { b = null; }
	try { if (!b && window.parent && window.parent !== window) b = window.parent.AstrBotPluginView || window.parent.AstrBotPluginPage || null; } catch (e) { b = null; }
	let embedded = false;
	try { embedded = !!(window.parent && window.parent !== window); } catch (e) { embedded = false; }
	return b && embedded ? b : null;
}
const unwrap = (r) => (r && r.data !== undefined ? r.data : r);

async function loadGraph() {
	bridge = findBridge();
	if (bridge) {
		try {
			const ctx0 = await Promise.race([bridge.ready(), new Promise((r) => setTimeout(() => r(null), 3000))]);
			if (IN_PANEL && !ctx0) throw new Error('面板没回音');
			if (!params.get('theme') && !storeGet('bio_theme') && ctx0) dark = !!ctx0.isDark;
			const g = await fetchGraph((route, q) => bridge.apiGet(route, q));
			source = 'live';
			return g;
		} catch (e) { whyNot = String((e && e.message) || e || '').slice(0, 60); }   // the sample, saying so
	}
	sample = window.BrainSample.make({ n: Number(params.get('n')) || 900 });
	source = bridge ? 'sample-embedded' : 'sample';
	return sample.graph;
}

// Content only travels when the owner opens a point.
async function getDetail(id) {
	if (source === 'live') {
		try {
			const r = await bridge.apiGet('page/brain/node', { id });
			return r && r.status === 'error' ? { error: r.message || '没取到' } : unwrap(r);
		} catch (e) { return { error: '没取到：' + (e && e.message || e) }; }
	}
	const d = sample && sample.details[id];
	return d ? Object.assign({}, d, { qq: undefined, has_qq: !!d.qq }) : null;
}
// A QQ number only on a second click, fetched on its own.
async function getQQ(id) {
	if (source === 'live') {
		try { const r = await bridge.apiGet('page/brain/node', { id, reveal: 'qq' }); return (unwrap(r) || {}).qq || '没取到'; } catch (e) { return '没取到'; }
	}
	return (sample && sample.details[id] && sample.details[id].qq) || '';
}
async function searchContent(q) {
	if (source === 'live') {
		try { const r = unwrap(await bridge.apiGet('page/brain/search', { q })); return Array.isArray(r) ? r : (r && r.ids) || []; } catch (e) { return []; }
	}
	const out = [];
	if (!sample) return out;
	for (const id in sample.details) {
		const d = sample.details[id];
		if ((d.text || '').includes(q) || (d.title || '').includes(q)) out.push(id);
	}
	return out;
}

function indexRaw(g) {
	raw = g;
	body = Object.assign({}, g.body || {});
	rawById = new Map();
	for (const n of g.nodes || []) if (n && n.id && KIND[n.kind] && !rawById.has(n.id)) rawById.set(n.id, n);
	raw.edges = (g.edges || []).filter((e) => EDGE[e.kind] && rawById.has(e.s) && rawById.has(e.t) && e.s !== e.t);
	raw.turns = g.turns || [];
	rawAdj = new Map();
	for (const e of raw.edges) {
		(rawAdj.get(e.s) || rawAdj.set(e.s, []).get(e.s)).push({ other: e.t, kind: e.kind, w: Number(e.w) || 1 });
		(rawAdj.get(e.t) || rawAdj.set(e.t, []).get(e.t)).push({ other: e.s, kind: e.kind, w: Number(e.w) || 1 });
	}
	const groups = [...rawById.values()].filter((n) => n.kind === 'window' && n.sub !== 'private').sort((a, b) => (b.w || 0) - (a.w || 0));
	const privs = [...rawById.values()].filter((n) => n.kind === 'window' && n.sub === 'private');
	groups.forEach((n, k) => winColor.set(n.id, new Color().setHSL(GROUP_HUES[k % GROUP_HUES.length] / 360, 0.66, 0.6)));
	privs.forEach((n, k) => winColor.set(n.id, new Color().setHSL((236 + (k * 11) % 44) / 360, 0.32, 0.74)));
	const now = g.now || Date.now() / 1000;
	let oldest = 1;
	for (const n of rawById.values()) if (n.ts) oldest = Math.max(oldest, Math.ceil((now - n.ts) / DAY));
	filter.from = oldest; filter.to = 0;
	for (const id of ['tFrom', 'tTo']) $(id).max = String(oldest);
}

function passes(n) {
	if (!filter.kinds.has(n.kind)) return false;
	if (filter.vis !== 'all') {
		if (n.kind === 'window') { if ((n.sub === 'private') !== (filter.vis === 'private')) return false; }
		else if (n.vis && n.vis !== filter.vis) return false;
	}
	if (n.ts && n.kind !== 'person' && n.kind !== 'window') {
		const age = ((raw.now || Date.now() / 1000) - n.ts) / DAY;
		if (age > filter.from + 0.0001 || age < filter.to - 0.0001) return false;
	}
	return true;
}

function savePositions() {
	if (!layout) return;
	const p = layout.positions;
	G.nodes.forEach((n, i) => posCache.set(n.id, [p[i * 3], p[i * 3 + 1], p[i * 3 + 2]]));
}

// Turn the filtered graph into Galaxy View's GraphData and (re)start the layout.
function rebuild(initial) {
	savePositions();
	let keep = [...rawById.values()].filter(passes);
	if (tier.nodeCap && keep.length > tier.nodeCap) {   // phones: the biggest stars only
		const fixed = keep.filter((n) => n.kind === 'window' || n.kind === 'person');
		const rest = keep.filter((n) => n.kind !== 'window' && n.kind !== 'person').sort((a, b) => (b.w || 0) - (a.w || 0));
		keep = fixed.concat(rest.slice(0, Math.max(0, tier.nodeCap - fixed.length)));
	}
	src = keep;
	idx = new Map(keep.map((n, i) => [n.id, i]));
	const sideOf = (n) => {
		if (n.kind === 'person') return 0;
		const w = n.kind === 'window' ? n : rawById.get(n.where);
		return w && w.sub === 'private' ? 1 : -1;
	};
	const nodes = keep.map((n) => ({ id: n.id, name: n.label || n.id, folderTop: n.where || n.id, degree: 0, inDegree: 0, outDegree: 0,
		fileSize: 0, tags: [], unresolved: n.vis === 'private' && n.kind !== 'window', tag: false, side: sideOf(n) }));
	const links = [];
	for (const e of raw.edges) {
		const s = idx.get(e.s), t = idx.get(e.t);
		if (s === undefined || t === undefined) continue;
		links.push({ source: s, target: t, kind: e.kind });
		nodes[s].degree++; nodes[t].degree++; nodes[s].outDegree++; nodes[t].inDegree++;
	}
	G = { nodes, links };
	adj = buildAdjacency(G);
	lines = lineMap(links);
	const R = seedRadius(nodes.length);
	physics = Object.assign({}, PHYSICS, { ball: ballRadius(nodes.length) });
	const positions = new Float32Array(nodes.length * 3);
	keep.forEach((n, i) => {
		let p = posCache.get(n.id);
		if (!p) {
			const s = seedPosition(n.id, physics.ball * 0.8);
			s[0] += nodes[i].side * physics.ball * 0.3;
			const home = n.where && posCache.get(n.where);
			p = home ? [home[0] + s[0] * 0.25, home[1] + s[1] * 0.25, home[2] + s[2] * 0.25] : s;
		}
		positions.set(p, i * 3);
	});
	if (initial) graphRadius = R * 1.6;
	if (!renderer) createRenderer();
	renderer.setData(G, positions);
	initLayout(G, positions, initial ? 1 : (posCache.size ? 0.3 : 1));
	sel = -1; hover = -1;
	recolor();
	applyFocus();
	updateStat();
}

function initLayout(data, positions, alpha) {
	layout?.dispose();
	const wantMain = params.get('settle') === '1';
	try {
		layout = wantMain ? new MainThreadForceLayout() : new WorkerForceLayout();
		layout.init(data, positions, physics, alpha);
	} catch (e) {
		layout = new MainThreadForceLayout();
		layout.init(data, positions, physics, alpha);
	}
	if (wantMain) { while (layout.step()) { /* lay out fully before the first frame */ } renderer.updatePositions(); }
	layoutStarted = performance.now();
}
// A Blob URL worker may be refused inside AstrBot's sandboxed iframe without an
// exception; if it has not answered in 2 s, lay out on the main thread instead.
let layoutStarted = 0;
function workerWatchdog(now) {
	if (!(layout instanceof WorkerForceLayout) || layout.ticks > 0 || layout.isSettled() || now - layoutStarted < 2000) return;
	const positions = layout.positions;
	layout.dispose();
	layout = new MainThreadForceLayout();
	layout.init(G, positions, physics, 1);
}

// ------------------------------------------------------------------ colour and focus
function colorOf(node) {
	const o = overrides.get(node.id);
	if (o) return o;
	const n = rawById.get(node.id);
	if (!n) return PERSON;
	if (n.kind === 'person') return PERSON;
	const base = winColor.get(n.kind === 'window' ? n.id : n.where) || winColor.values().next().value || PERSON;
	if (n.kind === 'event') return base.clone().offsetHSL(0, 0.05, 0.08);
	if (n.kind === 'note') return base.clone().offsetHSL(0, -0.1, 0.16);
	return base;
}
function recolor() {
	renderer.setColorFn(colorOf);
	renderer.recolor();
}

function windowFocusSet(wid) {
	const set = new Set();
	const w = idx.get(wid);
	if (w === undefined) return set;
	set.add(w);
	for (let i = 0; i < src.length; i++) if (src[i].where === wid) set.add(i);
	G.links.forEach((l) => {
		if (l.kind === 'impression' && (l.source === w || l.target === w)) set.add(l.source === w ? l.target : l.source);
		if (l.kind === 'about' && src[l.source].where === wid) set.add(l.target);
	});
	return set;
}

// What is lit: a turn wins over a selection, a selection over search, search over the window filter.
function applyFocus() {
	if (!renderer) return;
	if (turn >= 0) { stepTurn(performance.now(), true); return; }
	let weight = null, t1 = [];
	if (sel >= 0) {   // an opened star calls up its lines while the drawer is open
		t1 = openedLines(G.links, sel);
		const near = new Set([sel]);
		for (const li of t1) { near.add(G.links[li].source); near.add(G.links[li].target); }
		weight = (i) => (near.has(i) ? DIM.lit : DIM.rest);
	} else if (hits) {
		weight = (i) => (hits.has(i) ? DIM.lit : DIM.rest);
	} else if (filter.win) {
		const set = windowFocusSet(filter.win);
		weight = (i) => (set.has(i) ? DIM.lit : DIM.rest);
	}
	renderer.setFocus(weight);
	renderer.setSelectedLinks(t1, []);
	lineAlpha(1);
}
// Galaxy View's highlight layer (its selMaterial, TypeScript-private) carries the
// lines that are called up; its opacity is how a turn's lines fade out.
function lineAlpha(a) {
	if (renderer.selMaterial) renderer.selMaterial.opacity = 0.85 * a;
}

function updateStat() {
	$('statLine').textContent = '显示 ' + G.nodes.length + ' / ' + rawById.size + ' 颗星 · ' + G.links.length + ' 条关系';
}

// ------------------------------------------------------------------ renderer
function createRenderer() {
	const stage = $('galaxy');
	renderer = new AggregateRenderer(stage, graphRadius);
	director = new GlobeCamera(renderer.camera, renderer.renderer.domElement);
	renderer.setBloomParams(LOOK.bloom);
	renderer.setNodeScale(LOOK.nodeSize * (tier.id === 'mobile' ? 1.9 : 1));   // phones: no bloom, so bigger stars
	renderer.setLinkOpacity(LOOK.linkOpacity);
	renderer.setLinkCurve(LOOK.linkCurve);
	renderer.setSizeMode('degree');
	renderer.setStarfieldEnabled(true);
	renderer.setNebulaTint('#46d4dc', '#9a7fe0');
	renderer.setSpace(LOOK.space);
	renderer.twinkleFreq = motion ? LOOK.twinkle : 0;
	renderer.applyTier(tier, LOOK.bloom.strength);
	renderer.applyTokens(dark ? DEEP_SPACE : DAYLIGHT, LOOK.bloom.strength);
	cores.build();
	sparks.build();
	marks.build();
	shell.build();
}

const tmpV = new Vector3();
const glowMaterials = [];
const nodePos = (i, out = new Vector3()) => renderer.nodePosition(i, out);

function computeFraming() {
	const n = G.nodes.length;
	if (!n) return { center: new Vector3(), radius: graphRadius };
	const center = new Vector3();
	for (let i = 0; i < n; i++) center.add(nodePos(i, tmpV));
	center.divideScalar(n);
	const d = new Float64Array(n);
	for (let i = 0; i < n; i++) d[i] = nodePos(i, tmpV).distanceTo(center);
	d.sort();
	const radius = Math.max(d[Math.min(n - 1, Math.floor(n * 0.98))] || graphRadius, graphRadius * 0.3);
	viewRadius = radius;
	ballCenter.copy(center);
	return { center, radius };
}
const ballCenter = new Vector3();
function recenter() {   // the whole ball, keeping the way it is turned
	const f = computeFraming();
	shell.place(f.center, f.radius);
	director.frame(f.center, f.radius * 1.08, null);
}
function frameIndices(list) {
	if (!list.length) return;
	const center = new Vector3();
	for (const i of list) center.add(nodePos(i, tmpV));
	center.divideScalar(list.length);
	let r = 0;
	for (const i of list) r = Math.max(r, nodePos(i, tmpV).distanceTo(center));
	director.frame(center, Math.max(r * 1.1, viewRadius * 0.35), ballCenter);   // the ball turns them towards you
}

function resize() {
	const el = $('galaxy');
	renderer?.resize(el.clientWidth, el.clientHeight);
	const ph = el.clientHeight * (renderer ? renderer.renderer.getPixelRatio() : 1);
	pixelScale = ph / (2 * Math.tan(((renderer ? renderer.camera.fov : 60) / 2) * Math.PI / 180));
	cores.setPixelScale(pixelScale); sparks.setPixelScale(pixelScale); marks.setPixelScale(pixelScale); shell.setPixelScale(pixelScale);
}
let pixelScale = 1;

// Glowing sprites for the body nuclei and the sparks: additive points.
const GLOW_VERTEX = /* glsl */ `
attribute float aSize; attribute float aAlpha; attribute vec3 aColor;
varying float vAlpha; varying vec3 vColor; uniform float uPixelScale;
void main() { vAlpha = aAlpha; vColor = aColor;
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	gl_PointSize = min(aSize * uPixelScale / max(-mv.z, 1.0), 220.0);
	gl_Position = projectionMatrix * mv; }`;
const GLOW_FRAGMENT = /* glsl */ `
varying float vAlpha; varying vec3 vColor; uniform float uLight; uniform float uFade;
void main() { float d = length(gl_PointCoord - 0.5);
	float halo = smoothstep(0.5, 0.0, d); float core = smoothstep(0.16, 0.0, d);
	float a = (halo * halo * 0.9 + core) * vAlpha * uFade; if (a < 0.01) discard;
	if (uLight > 0.5) { gl_FragColor = vec4(mix(vColor, vColor * 0.7, core), min(a, 1.0)); return; }   // on paper: plain ink
	vec3 col = mix(vColor, vec3(1.0), core * 0.7);
	gl_FragColor = vec4(col * a, a); }`;
function glowPoints(count) {
	const geo = new BufferGeometry();
	geo.setAttribute('position', new BufferAttribute(new Float32Array(count * 3), 3).setUsage(DynamicDrawUsage));
	geo.setAttribute('aSize', new BufferAttribute(new Float32Array(count), 1).setUsage(DynamicDrawUsage));
	geo.setAttribute('aAlpha', new BufferAttribute(new Float32Array(count), 1).setUsage(DynamicDrawUsage));
	geo.setAttribute('aColor', new BufferAttribute(new Float32Array(count * 3), 3).setUsage(DynamicDrawUsage));
	const mat = new ShaderMaterial({ vertexShader: GLOW_VERTEX, fragmentShader: GLOW_FRAGMENT, transparent: true, depthWrite: false,
		blending: dark ? AdditiveBlending : NormalBlending, uniforms: { uPixelScale: { value: 1 }, uLight: { value: dark ? 0 : 1 }, uFade: { value: 1 } } });
	const pts = new Points(geo, mat);
	glowMaterials.push(mat);
	pts.frustumCulled = false; pts.renderOrder = 3;
	renderer.scene.add(pts);   // Galaxy View's scene (a TypeScript-private field)
	return pts;
}

// Body nuclei: a small ring in the heart of the galaxy, bigger and brighter with the value.
const cores = {
	pts: null, pos: [],
	build() {
		this.pts = glowPoints(CORES.length);
		const col = this.pts.geometry.getAttribute('aColor');
		CORES.forEach((c, k) => { const cc = new Color(c.c); col.setXYZ(k, cc.r, cc.g, cc.b); this.pos.push(new Vector3()); });
	},
	setPixelScale(v) { if (this.pts) this.pts.material.uniforms.uPixelScale.value = v; },
	value(k) {
		let v = Number(body[CORES[k].key]);
		if (!Number.isFinite(v)) v = 0;
		return CORES[k].key === 'valence' ? v : Math.max(0, Math.min(1, v));
	},
	update(t) {
		if (!this.pts) return;
		const g = this.pts.geometry, P = g.getAttribute('position'), S = g.getAttribute('aSize'), A = g.getAttribute('aAlpha'), C = g.getAttribute('aColor');
		const ring = viewRadius * 0.24;
		CORES.forEach((c, k) => {
			const ang = k / CORES.length * Math.PI * 2;
			this.pos[k].set(Math.cos(ang) * ring, 0, Math.sin(ang) * ring);
			this.pos[k].add(ballCenter);
			P.setXYZ(k, this.pos[k].x, this.pos[k].y, this.pos[k].z);
			let v = this.value(k);
			if (c.key === 'valence') {   // mood: blue when low, warm yellow when high
				const cc = new Color(v >= 0 ? '#f2c14e' : '#5b8def');
				C.setXYZ(k, cc.r, cc.g, cc.b);
				v = Math.min(1, Math.abs(v));
			}
			const breathe = motion ? 1 + Math.sin(t / 1000 * (0.8 + v * 1.6) + k) * (0.05 + v * 0.08) : 1;
			S.setX(k, viewRadius * (0.08 + v * 0.16) * breathe);
			A.setX(k, (dark ? 0.35 : 0.55) + v * 0.65);
		});
		P.needsUpdate = S.needsUpdate = A.needsUpdate = C.needsUpdate = true;
	},
};

// Halos on the stars that matter right now: what a turn recalled (gold, a
// flash when it lights up) and held back (grey), the selected star, search hits.
const marks = {
	pts: null, max: 48,
	build() { this.pts = glowPoints(this.max); },
	setPixelScale(v) { if (this.pts) this.pts.material.uniforms.uPixelScale.value = v; },
	update(t) {
		if (!this.pts) return;
		const g = this.pts.geometry, P = g.getAttribute('position'), S = g.getAttribute('aSize'), A = g.getAttribute('aAlpha'), C = g.getAttribute('aColor');
		const list = [];
		if (turn >= 0) {
			const { rec, held } = turnInfo();
			const local = t - turnStart;
			rec.forEach((i, k) => {
				if (motion && local < k * STEP) return;
				const fresh = motion ? Math.max(0, 1 - (local - k * STEP) / 900) : 0;
				list.push([i, LIT, 0.05 * (1 + fresh * 1.6), 0.9]);
			});
			held.forEach((i) => list.push([i, HELD, 0.04, 0.55]));
		} else {
			if (sel >= 0) list.push([sel, new Color(1, 1, 1), 0.045 * (motion ? 1 + Math.sin(t / 300) * 0.12 : 1), 0.7]);
			if (hits) for (const i of hits) { if (list.length >= this.max) break; list.push([i, new Color('#ffb14d'), 0.03, 0.6]); }
		}
		for (let k = 0; k < this.max; k++) {
			const m = list[k];
			if (!m) { A.setX(k, 0); continue; }
			nodePos(m[0], tmpV);
			P.setXYZ(k, tmpV.x, tmpV.y, tmpV.z);
			S.setX(k, viewRadius * m[2]);
			A.setX(k, m[3]);
			C.setXYZ(k, m[1].r, m[1].g, m[1].b);
		}
		P.needsUpdate = S.needsUpdate = A.needsUpdate = C.needsUpdate = true;
	},
};

// A faint layer of stars on the surface, so the ball's outline shows.
const shell = {
	pts: null, count: 900,
	build() {
		this.pts = glowPoints(this.count);
		const C = this.pts.geometry.getAttribute('aColor'), A = this.pts.geometry.getAttribute('aAlpha');
		for (let k = 0; k < this.count; k++) { C.setXYZ(k, 0.72, 0.8, 1); A.setX(k, 0); }
	},
	setPixelScale(v) { if (this.pts) this.pts.material.uniforms.uPixelScale.value = v; },
	radius: 0,
	update() {   // the outline is for looking at the ball from outside: it fades as the camera comes close
		if (!this.pts || !this.radius) return;
		const d = renderer.camera.position.distanceTo(ballCenter);
		this.pts.material.uniforms.uFade.value = Math.max(0, Math.min(1, (d - this.radius * 1.6) / (this.radius * 0.8)));
	},
	place(center, radius) {
		this.radius = radius;
		if (!this.pts) return;
		const g = this.pts.geometry, P = g.getAttribute('position'), S = g.getAttribute('aSize'), A = g.getAttribute('aAlpha');
		const golden = Math.PI * (3 - Math.sqrt(5));
		let seed = 11;
		const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
		for (let k = 0; k < this.count; k++) {   // evenly over the sphere (Fibonacci), a little jitter
			const y = 1 - (k + 0.5) / this.count * 2, r = Math.sqrt(1 - y * y), th = k * golden;
			const rr = radius * (1.06 + (rnd() - 0.5) * 0.05);
			P.setXYZ(k, center.x + Math.cos(th) * r * rr, center.y + y * rr, center.z + Math.sin(th) * r * rr);
			S.setX(k, radius * (0.016 + rnd() * 0.02));
			A.setX(k, (dark ? 0.3 : 0.4) + rnd() * 0.3);
		}
		P.needsUpdate = S.needsUpdate = A.needsUpdate = true;
	},
};

// Sparks: little lights running along the lines that are called up: in a turn,
// along the path she took, in order; when a star is opened, out along its lines (Galaxy View has no particles;
// these follow its curved links).
const sparks = {
	pts: null, list: [], max: 64,
	build() { this.pts = glowPoints(this.max); },
	setPixelScale(v) { if (this.pts) this.pts.material.uniforms.uPixelScale.value = v; },
	emit(a, b, color, dur, big) { if (this.list.length < this.max) this.list.push({ a, b, color, t0: performance.now(), dur, big }); },
	ambient(t) {   // only when every line is shown; otherwise lights run only along called-up lines
		if (!showAll || !motion || turn >= 0 || !G.links.length || this.list.length > 24 || Math.random() > 0.3) return;
		for (let tries = 0; tries < 6; tries++) {
			const l = G.links[Math.floor(Math.random() * G.links.length)];
			if (l.kind !== 'link' && Math.random() < 0.75) continue;
			if (sel >= 0 && l.source !== sel && l.target !== sel) continue;
			const fwd = Math.random() < 0.5;
			const c = colorOf(G.nodes[fwd ? l.source : l.target]).clone().lerp(new Color(1, 1, 1), 0.35);
			this.emit(fwd ? l.source : l.target, fwd ? l.target : l.source, c, 1300 + Math.random() * 1200, false);
			break;
		}
	},
	update(t) {
		if (!this.pts) return;
		this.list = this.list.filter((s) => t - s.t0 < s.dur && s.a < G.nodes.length && s.b < G.nodes.length);
		const g = this.pts.geometry, P = g.getAttribute('position'), S = g.getAttribute('aSize'), A = g.getAttribute('aAlpha'), C = g.getAttribute('aColor');
		const a = new Vector3(), b = new Vector3();
		for (let k = 0; k < this.max; k++) {
			const s = this.list[k];
			if (!s) { A.setX(k, 0); continue; }
			const p = Math.max(0, Math.min(1, (t - s.t0) / s.dur));
			curvePoint(nodePos(s.a, a), nodePos(s.b, b), p, P, k);
			S.setX(k, viewRadius * (s.big ? 0.03 : 0.016));
			A.setX(k, Math.sin(p * Math.PI) * (s.big ? 1 : 0.8));
			C.setXYZ(k, s.color.r, s.color.g, s.color.b);
		}
		P.needsUpdate = S.needsUpdate = A.needsUpdate = C.needsUpdate = true;
	},
};
// Same bow as Galaxy View's fillLinkPositions: a quadratic curve bulging away from the core.
function curvePoint(s, t, u, P, k) {
	const mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2, mz = (s.z + t.z) / 2;
	const len = s.distanceTo(t), mr = Math.hypot(mx, my, mz) || 1;
	const h = LOOK.linkCurve * CURVE_BOW * len;
	const cx = mx + mx / mr * h, cy = my + my / mr * h, cz = mz + mz / mr * h;
	const w0 = (1 - u) * (1 - u), w1 = 2 * (1 - u) * u, w2 = u * u;
	P.setXYZ(k, w0 * s.x + w1 * cx + w2 * t.x, w0 * s.y + w1 * cy + w2 * t.y, w0 * s.z + w1 * cz + w2 * t.z);
}

// ------------------------------------------------------------------ turns
const STEP = TURN.step;   // ms between two recalled memories lighting up
let turnLit = -1, turnLines = -1;
function turnInfo() {
	const tr = raw.turns[turn];
	const rec = (tr.recalled || []).map((id) => idx.get(id)).filter((i) => i !== undefined);
	const held = (tr.held || []).map((id) => idx.get(id)).filter((i) => i !== undefined);
	const path = (tr.path || []).map((p) => [idx.get(p[0]), idx.get(p[1])]).filter((p) => p[0] !== undefined && p[1] !== undefined);
	return { tr, rec, held, path, where: idx.get(tr.where) };
}
// A turn plays once: the recalled stars light up in order, a line appears with a
// light running along it as she goes from one to the next, then the lines fade
// and only the stars are left. With motion on, the next turn follows.
function stepTurn(t, force) {
	if (turn < 0) return;
	const { rec, held, path, where } = turnInfo();
	const steps = turnSteps(lines, path, held);
	const local = t - turnStart;
	const f = turnFrame(steps, rec.length, local, motion);
	if (f.done && !force && raw.turns.length > 1) { setTurn((turn + 1) % raw.turns.length); return; }
	if (f.lit !== turnLit || f.lines.length !== turnLines || force) {
		turnLit = f.lit; turnLines = f.lines.length;
		const on = new Set(rec.slice(0, f.lit));
		const heldSet = new Set(held);
		renderer.setFocus((i) => (on.has(i) || i === where ? DIM.lit : heldSet.has(i) ? 0.9 : DIM.turnRest));
		renderer.setSelectedLinks(f.lines, []);
	}
	lineAlpha(f.alpha);
	if (!motion) return;
	steps.forEach(({ a, b }, k) => {   // a light along each line as it appears
		const at = (k + 0.5) * STEP;
		if (local >= at && local - at < 60 && !sparks.list.some((s) => s.a === a && s.b === b && t - s.t0 < STEP)) {
			sparks.emit(a, b, LIT, STEP * 1.4, true);
		}
	});
}

function setTurn(k) {
	const ts = raw.turns || [];
	if (k >= ts.length) k = ts.length - 1;
	if (k >= 0 && turn < 0) liveBody = body;
	if (k < 0 && turn >= 0 && liveBody) body = liveBody;
	turn = k;
	overrides = new Map();
	if (k >= 0) {
		sel = -1; $('drawer').hidden = true;
		const { tr, rec, held, where } = turnInfo();
		for (const i of rec) overrides.set(G.nodes[i].id, LIT);
		for (const i of held) overrides.set(G.nodes[i].id, HELD);
		if (tr.body) body = Object.assign({}, liveBody, tr.body);
		turnStart = performance.now(); turnLit = -1; turnLines = -1;
		sparks.list = [];
		const missing = (tr.recalled || []).length + (tr.held || []).length - rec.length - held.length;
		$('turnHint').textContent = fmtTime(tr.ts) + ' 在' + whereLabel(tr.where) + '：想起 ' + (tr.recalled || []).length +
			' 条（金色，按顺序亮，顺着线想过去），' + ((tr.held || []).length ? (tr.held || []).length + ' 条她知道但在这里没说（灰的）。' : '没有被挡下的。') +
			(tr.body ? ' 中间的核是那一刻的身体。' : '') + (missing ? '（有 ' + missing + ' 条被筛掉了）' : '');
		recolor();
		frameIndices(rec.concat(where === undefined ? [] : [where]));   // what she recalled; a held-back star may be off to the side
	} else {
		$('turnHint').textContent = '点一轮看她这次想起了谁。平常星之间不连线，她想起来时才连。';
		recolor();
	}
	renderTurns();
	const on = $('turnList').querySelector('li.on');
	if (on && on.scrollIntoView) on.scrollIntoView({ block: 'nearest', inline: 'nearest' });
	applyFocus();
}

function renderTurns() {
	const ts = raw.turns || [];
	if (!ts.length) { $('turnList').innerHTML = '<li class="more">还没有记录。她被叫到一次，这里就多一轮。</li>'; return; }
	$('turnList').innerHTML = ts.map((t, k) => '<li data-turn="' + k + '"' + (k === turn ? ' class="on"' : '') + '>' +
		esc(fmtTime(t.ts)) + ' · ' + esc(whereLabel(t.where) || '?') +
		'<small>想起 ' + (t.recalled || []).length + ' · 没说 ' + (t.held || []).length + '</small></li>').join('');
}

// ------------------------------------------------------------------ labels (DOM, projected each frame)
const labelPool = new Map();
function label(key, text, x, y, cls) {
	let el = labelPool.get(key);
	if (!el) { el = document.createElement('div'); el.className = 'lbl3'; $('labels').appendChild(el); labelPool.set(key, el); }
	if (el.textContent !== text) el.textContent = text;
	el.className = 'lbl3 ' + (cls || '');
	el.style.transform = 'translate(' + Math.round(x) + 'px,' + Math.round(y) + 'px)';
	el.dataset.seen = '1';
}
function updateLabels() {
	const el = $('galaxy'), w = el.clientWidth, h = el.clientHeight;
	for (const v of labelPool.values()) v.dataset.seen = '';
	const put = (key, i, text, cls, dy) => {
		const p = renderer.projectNode(i, w, h);
		if (p.behind || p.x < -40 || p.y < -20 || p.x > w + 40 || p.y > h + 20) return;
		label(key, text, p.x, p.y + (dy || 10), cls);
	};
	const turnOn = turn >= 0;
	const ti = turnOn ? turnInfo() : null;
	const winFocus = filter.win ? idx.get(filter.win) : undefined;
	G.nodes.forEach((n, i) => {
		if (src[i].kind !== 'window') return;
		const faded = (turnOn && i !== ti.where) || (sel >= 0 && i !== sel && !neighborOfSel(i)) || (winFocus !== undefined && i !== winFocus);
		put('w' + i, i, n.name, 'win' + (faded ? ' faded' : ''), 12);
	});
	if (sel >= 0 && src[sel].kind !== 'window') put('sel', sel, src[sel].label, 'sel', 10);
	if (turnOn) {
		const { rec, held } = ti;
		rec.slice(0, turnLit).forEach((i, k) => put('r' + k, i, (k + 1) + ' · ' + src[i].label + (src[i].where !== raw.turns[turn].where ? '（' + whereLabel(src[i].where) + '）' : ''), 'lit', -22));
		held.forEach((i, k) => put('h' + k, i, '没说 · ' + src[i].label + '（' + whereLabel(src[i].where) + '）', 'held', -22));
	}
	if (hits && !turnOn && sel < 0) {
		let k = 0;
		for (const i of hits) { if (k++ > 15) break; put('q' + i, i, src[i].label, 'hit', 10); }
	}
	const cam = renderer.camera;
	if (w >= 600) cores.pos.forEach((p, k) => {   // narrow screens: the nuclei glow without names (tap one to see it)
		const v = tmpV.copy(p).project(cam);
		if (v.z > 1) return;
		const val = cores.value(k);
		const pct = CORES[k].key === 'valence' ? (val >= 0 ? '+' : '−') + Math.round(Math.abs(val) * 100) : Math.round(val * 100);
		label('c' + k, CORES[k].name + ' ' + pct + '%', (v.x + 1) / 2 * w, (1 - v.y) / 2 * h + 14, 'core');
	});
	for (const v of labelPool.values()) v.style.display = v.dataset.seen ? '' : 'none';
}
let selNeighbors = null;
function neighborOfSel(i) {
	if (!selNeighbors || selNeighbors.sel !== sel) selNeighbors = { sel, set: neighborhood(adj, sel, 1).depthOf };
	return selNeighbors.set.has(i);
}

// ------------------------------------------------------------------ drawer
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch])); }
const fmtTime = (ts) => {
	if (!ts) return '';
	const d = new Date(ts * 1000), p = (x) => String(x).padStart(2, '0');
	return (d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
};
const ago = (ts) => {
	if (!ts) return '';
	const s = (raw.now || Date.now() / 1000) - ts;
	if (s < 3600) return Math.max(1, Math.round(s / 60)) + ' 分钟前';
	if (s < DAY) return Math.round(s / 3600) + ' 小时前';
	return Math.round(s / DAY) + ' 天前';
};
const kindName = (n) => KIND[n.kind] + (n.kind === 'window' ? (n.sub === 'private' ? ' · 私聊' : ' · 群') : '');
const whereLabel = (id) => { const n = rawById.get(id); return n ? n.label : ''; };
const shortLine = (n) => [kindName(n), n.label, n.where ? whereLabel(n.where) : '', ago(n.ts)].filter(Boolean).join(' · ');
const hex = (c) => '#' + c.getHexString();

let drawerFor = null;
async function openDrawer(n) {
	drawerFor = n.id;
	$('drawer').hidden = false;
	$('dKind').textContent = kindName(n) + (n.cat && n.cat !== n.label ? ' · ' + n.cat : '');
	$('dTitle').textContent = n.label || n.id;
	const meta = [];
	if (n.ts) meta.push(['时间', esc(fmtTime(n.ts) + '（' + ago(n.ts) + '）')]);
	if (n.where) meta.push(['窗口', '<a data-go="' + esc(n.where) + '">' + esc(whereLabel(n.where)) + '</a>']);
	if (n.vis) meta.push(['分寸', n.vis === 'private' ? '私下（空心）' : '公开']);
	if (n.kind === 'memory') meta.push(['分量', Math.round((n.w || 0) * 100) + '%']);
	if (n.kind === 'note' && n.self) meta.push(['', '她写给自己的']);
	meta.push(['编号', esc(n.id)]);
	$('dMeta').innerHTML = meta.map(([k, v]) => '<dt>' + esc(k) + '</dt><dd>' + v + '</dd>').join('');
	$('dBody').innerHTML = '<span class="muted">取内容…</span>';
	renderLinks(n);
	const d = await getDetail(n.id);
	if (drawerFor !== n.id) return;
	if (!d) { $('dBody').innerHTML = '<span class="muted">没有更多内容。</span>'; return; }
	if (d.error) { $('dBody').innerHTML = '<span class="muted">' + esc(d.error) + '</span>'; return; }
	let html = '';
	if (d.title) $('dTitle').textContent = d.title;
	if (d.text) html += '<div class="text">' + esc(d.text) + '</div>';
	if (Array.isArray(d.lines) && d.lines.length) html += '<dl>' + d.lines.map(([k, v]) => '<dt>' + esc(k) + '</dt><dd>' + esc(v) + '</dd>').join('') + '</dl>';
	if (d.has_qq) html += '<div class="reveal"><button class="btn" id="qqBtn">显示 QQ 号</button> <span id="qqVal"></span></div>';
	$('dBody').innerHTML = html || '<span class="muted">没有更多内容。</span>';
	const b = $('qqBtn');
	if (b) b.onclick = async () => { b.disabled = true; const qq = await getQQ(n.id); if (drawerFor === n.id) { $('qqVal').textContent = qq; b.remove(); } };
}
function openCoreDrawer(k) {
	drawerFor = 'core:' + k;
	const c = CORES[k], v = cores.value(k);
	$('drawer').hidden = false;
	$('dKind').textContent = '身体';
	$('dTitle').textContent = c.name;
	$('dMeta').innerHTML = '<dt>现在</dt><dd>' + (c.key === 'valence' ? (v >= 0 ? '偏好 ' : '偏低 ') + Math.round(Math.abs(v) * 100) : Math.round(v * 100)) + '%</dd>' +
		'<dt>说明</dt><dd>身体里的一样，只有数，不存话。越大越亮，数越高。</dd>';
	$('dBody').innerHTML = '';
	$('dLinks').innerHTML = '';
}
function renderLinks(n) {
	const groups = {};
	for (const e of rawAdj.get(n.id) || []) (groups[e.kind] = groups[e.kind] || []).push(e);
	let html = '<div class="d-links">';
	for (const kind of Object.keys(EDGE)) {
		const list = groups[kind];
		if (!list) continue;
		list.sort((p, q) => q.w - p.w);
		html += '<h3>' + EDGE[kind] + ' · ' + list.length + '</h3><ul>';
		for (const e of list.slice(0, 40)) {
			const o = rawById.get(e.other);
			const c = o.kind === 'person' ? PERSON : (winColor.get(o.kind === 'window' ? o.id : o.where) || PERSON);
			html += '<li data-id="' + esc(o.id) + '"><span class="dot' + (o.vis === 'private' && o.kind !== 'window' ? ' ring' : '') + '" style="--c:' + hex(c) + '"></span>' + esc(shortLine(o)) +
				(idx.has(o.id) ? '' : ' <span class="muted">（筛掉了）</span>') + '</li>';
		}
		if (list.length > 40) html += '<li class="more">还有 ' + (list.length - 40) + ' 个</li>';
		html += '</ul>';
	}
	$('dLinks').innerHTML = html + '</div>';
}

function select(i, fly) {
	coreSel = -1;
	if (i < 0) { sel = -1; drawerFor = null; $('drawer').hidden = true; applyFocus(); return; }
	if (turn >= 0) setTurn(-1);
	sel = i;
	applyFocus();
	if (motion) for (const li of openedLines(G.links, i)) {   // its lines are called up: a light runs out along each
		const l = G.links[li], other = l.source === i ? l.target : l.source;
		sparks.emit(i, other, colorOf(G.nodes[other]).clone().lerp(new Color(1, 1, 1), 0.4), 1200, false);
	}
	openDrawer(src[i]);
	if (fly) {   // frame the star together with the stars its lines reach
		const near = [i];
		for (const li of openedLines(G.links, i)) { const l = G.links[li]; near.push(l.source === i ? l.target : l.source); }
		if (near.length > 1) frameIndices(near);
		else director.frame(nodePos(i), viewRadius * 0.15, ballCenter);
	}
}
function selectId(id, fly) {
	const i = idx.get(id);
	if (i !== undefined) select(i, fly);
	else if (rawById.has(id)) { sel = -1; applyFocus(); openDrawer(rawById.get(id)); }
}

// ------------------------------------------------------------------ search
let searchTimer = 0;
function runSearch() {
	const q = $('q').value.trim();
	clearTimeout(searchTimer);
	if (!q) { hits = null; $('hits').innerHTML = ''; applyFocus(); return; }
	searchTimer = setTimeout(async () => {
		const found = new Set();
		const ql = q.toLowerCase();
		for (const n of rawById.values()) {
			const hay = [n.id, n.label, n.cat, KIND[n.kind], n.where ? whereLabel(n.where) : ''].join(' ').toLowerCase();
			if (hay.includes(ql)) found.add(n.id);
		}
		for (const id of await searchContent(q)) if (rawById.has(id)) found.add(id);
		if ($('q').value.trim() !== q) return;
		hits = new Set([...found].map((id) => idx.get(id)).filter((i) => i !== undefined));
		const list = [...found].filter((id) => idx.has(id)).slice(0, 60);
		$('hits').innerHTML = (list.length ? '' : '<li class="more">没找到（或被筛掉了）</li>') + list.map((id) => {
			const n = rawById.get(id);
			const c = n.kind === 'person' ? PERSON : (winColor.get(n.kind === 'window' ? n.id : n.where) || PERSON);
			return '<li data-id="' + esc(id) + '"><span class="dot" style="--c:' + hex(c) + '"></span>' + esc(n.label) +
				(n.where ? ' · ' + esc(whereLabel(n.where)) : '') + '<span class="k">' + esc(ago(n.ts) || KIND[n.kind]) + '</span></li>';
		}).join('') + (found.size > list.length ? '<li class="more">共 ' + found.size + ' 个，图上都亮着</li>' : '');
		applyFocus();
	}, 200);
}

// ------------------------------------------------------------------ controls
function storeGet(k) { try { return localStorage.getItem(k) || ''; } catch (e) { return ''; } }
function storeSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private window */ } }
function applyTheme(d) {
	dark = d;
	document.documentElement.dataset.theme = d ? 'dark' : 'light';
	$('themeBtn').textContent = d ? '浅色' : '深色';
	if (renderer) { renderer.applyTokens(d ? DEEP_SPACE : DAYLIGHT, LOOK.bloom.strength); recolor(); applyFocus(); }
	for (const m of glowMaterials) { m.blending = d ? AdditiveBlending : NormalBlending; m.uniforms.uLight.value = d ? 0 : 1; m.needsUpdate = true; }
}
function initTheme() {
	const forced = params.get('theme');
	if (forced === 'dark' || forced === 'light') return applyTheme(forced === 'dark');
	const saved = storeGet('bio_theme');
	if (saved === 'dark' || saved === 'light') return applyTheme(saved === 'dark');
	applyTheme(true);   // the galaxy is meant to be seen on black
}

function buildControls() {
	const count = {}, ecount = {};
	for (const n of rawById.values()) count[n.kind] = (count[n.kind] || 0) + 1;
	for (const e of raw.edges) ecount[e.kind] = (ecount[e.kind] || 0) + 1;
	const chip = { window: '#ff8a1f', person: hex(PERSON), memory: '#8cacc4', event: '#f2c14e', note: '#a78bfa' };
	$('kindBoxes').innerHTML = Object.keys(KIND).map((k) => '<label><input type="checkbox" data-kind="' + k + '"' + (filter.kinds.has(k) ? ' checked' : '') + ' />' +
		'<span class="chip" style="background:' + chip[k] + '"></span>' + KIND[k] + ' <span class="n">' + (count[k] || 0) + '</span></label>').join('');
	$('lineCount').textContent = Object.keys(EDGE).map((k) => EDGE[k] + ' ' + (ecount[k] || 0)).join(' · ');
	$('allLines').checked = showAll;
	const wins = [...rawById.values()].filter((n) => n.kind === 'window');
	const per = {};
	for (const n of rawById.values()) if (n.where) per[n.where] = (per[n.where] || 0) + 1;
	const opt = (n) => '<option value="' + esc(n.id) + '">' + esc(n.label) + '（' + (per[n.id] || 0) + '）</option>';
	$('winSel').innerHTML = '<option value="">全部窗口</option>' +
		'<optgroup label="群">' + wins.filter((n) => n.sub !== 'private').map(opt).join('') + '</optgroup>' +
		'<optgroup label="私聊">' + wins.filter((n) => n.sub === 'private').map(opt).join('') + '</optgroup>';
	$('legendWins').innerHTML = wins.filter((n) => n.sub !== 'private').slice(0, 12).map((n) =>
		'<span><i style="background:' + hex(winColor.get(n.id)) + '"></i>' + esc(n.label) + '</span>').join('') +
		'<span><i class="ring" style="--c:' + hex(winColor.get(wins.find((n) => n.sub === 'private')?.id) || PERSON) + '"></i>私聊（空心）</span>' +
		'<span><i style="background:' + hex(PERSON) + '"></i>人</span>';
	$('tFrom').value = String(filter.from); $('tTo').value = String(filter.to);
	timeText();
}
function timeText() { $('timeText').textContent = filter.to === 0 ? '最近 ' + filter.from + ' 天' : filter.from + '–' + filter.to + ' 天前'; }

let rebuildTimer = 0;
function rebuildSoon() {
	clearTimeout(rebuildTimer);
	rebuildTimer = setTimeout(() => {
		const t = turn; turn = -1;
		rebuild(false);
		settledOnce = false; framed = t >= 0;   // look at the whole of it again once it has settled
		if (t >= 0) setTurn(t);
		runSearch();
	}, 120);
}

function wire() {
	$('kindBoxes').addEventListener('change', (ev) => {
		const k = ev.target.dataset.kind; if (!k) return;
		ev.target.checked ? filter.kinds.add(k) : filter.kinds.delete(k); rebuildSoon();
	});
	$('allLines').addEventListener('change', () => { showAll = $('allLines').checked; sparks.list = []; });
	$('winSel').addEventListener('change', () => {
		filter.win = $('winSel').value;
		select(-1);
		const w = idx.get(filter.win);
		if (w !== undefined) frameIndices([...windowFocusSet(filter.win)]); else recenter();
	});
	$('visSeg').addEventListener('click', (ev) => {
		const v = ev.target.dataset.vis; if (!v) return;
		filter.vis = v;
		for (const b of $('visSeg').children) b.classList.toggle('on', b.dataset.vis === v);
		rebuildSoon();
	});
	const onRange = () => {
		let f = Number($('tFrom').value), t = Number($('tTo').value);
		if (t > f) { if (document.activeElement === $('tFrom')) t = f; else f = t; $('tFrom').value = f; $('tTo').value = t; }
		filter.from = f; filter.to = t; timeText(); rebuildSoon();
	};
	$('tFrom').addEventListener('input', onRange); $('tTo').addEventListener('input', onRange);
	$('q').addEventListener('input', runSearch);
	const idClick = (ev) => { const li = ev.target.closest('[data-id]'); if (li) selectId(li.dataset.id, true); };
	$('hits').addEventListener('click', idClick);
	$('dLinks').addEventListener('click', idClick);
	$('dMeta').addEventListener('click', (ev) => { const a = ev.target.closest('[data-go]'); if (a) selectId(a.dataset.go, true); });
	$('drawerClose').addEventListener('click', () => select(-1));
	$('turnList').addEventListener('click', (ev) => { const li = ev.target.closest('[data-turn]'); if (li) setTurn(Number(li.dataset.turn)); });
	$('turnPrev').addEventListener('click', () => setTurn(turn <= 0 ? raw.turns.length - 1 : turn - 1));
	$('turnNext').addEventListener('click', () => setTurn(turn + 1 >= raw.turns.length ? 0 : turn + 1));
	$('turnOff').addEventListener('click', () => { setTurn(-1); recenter(); });
	$('fitBtn').addEventListener('click', () => { select(-1); recenter(); });
	$('motionBtn').addEventListener('click', () => {
		motion = !motion; $('motionBtn').classList.toggle('on', motion); storeSet('brain_motion', motion ? '1' : '0');
		director.autoEnabled = motion; renderer.twinkleFreq = motion ? LOOK.twinkle : 0;
	});
	$('themeBtn').addEventListener('click', () => { const d = !dark; applyTheme(d); storeSet('bio_theme', d ? 'dark' : 'light'); });
	$('panelBtn').addEventListener('click', () => $('side').classList.toggle('open'));
	window.addEventListener('resize', resize);
	document.addEventListener('visibilitychange', () => gate.set('page', document.visibilityState !== 'hidden'));
	window.addEventListener('keydown', (ev) => {
		if (ev.key === 'Escape' && panel) panel.exitFill();   // the keys come here while the map has the focus
		if (ev.target && /INPUT|SELECT|TEXTAREA/.test(ev.target.tagName)) return;
		if (ev.key === 'Escape') { if (turn >= 0) setTurn(-1); else select(-1); }
		else if (ev.key === 'ArrowRight') $('turnNext').click();
		else if (ev.key === 'ArrowLeft') $('turnPrev').click();
		else if (ev.key === 'r' || ev.key === 'R') recenter();
	});

	// Click to open, hover for a one-line tip (Galaxy View's screen-space picking).
	const dom = renderer.renderer.domElement;
	let downX = 0, downY = 0;
	dom.addEventListener('pointerdown', (e) => { downX = e.clientX; downY = e.clientY; });
	dom.addEventListener('pointerup', (e) => {
		if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey) return;
		if (Math.hypot(e.clientX - downX, e.clientY - downY) > 5) return;
		const r = dom.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top;
		const k = pickCore(px, py, r.width, r.height);
		if (k >= 0) { select(-1); coreSel = k; openCoreDrawer(k); return; }
		const i = renderer.pickNearest(px, py, r.width, r.height, 14);
		if (i >= 0) select(i, true); else if (sel >= 0 || coreSel >= 0) select(-1);
	});
	let pending = false;
	dom.addEventListener('pointermove', (e) => {
		if (tier.hoverThrottleMs === null || pending || e.buttons) return;
		pending = true;
		setTimeout(() => {
			pending = false;
			const r = dom.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top;
			const k = pickCore(px, py, r.width, r.height);
			const i = k >= 0 ? -1 : renderer.pickNearest(px, py, r.width, r.height, 10);
			hover = i;
			const tip = $('tip');
			if (k >= 0 || i >= 0) {
				tip.textContent = k >= 0 ? CORES[k].name + ' · ' + Math.round(Math.abs(cores.value(k)) * 100) + '%' : shortLine(src[i]);
				tip.hidden = false;
				tip.style.left = Math.min(r.width - tip.offsetWidth - 8, px + 14) + 'px'; tip.style.top = (py + 14) + 'px';
				dom.style.cursor = 'pointer';
			} else { tip.hidden = true; dom.style.cursor = ''; }
		}, tier.hoverThrottleMs);
	});
	dom.addEventListener('pointerleave', () => { $('tip').hidden = true; });
}
function pickCore(px, py, w, h) {
	let best = -1, bd = 22;
	cores.pos.forEach((p, k) => {
		const v = tmpV.copy(p).project(renderer.camera);
		if (v.z > 1) return;
		const d = Math.hypot((v.x + 1) / 2 * w - px, (1 - v.y) / 2 * h - py);
		if (d < bd) { bd = d; best = k; }
	});
	return best;
}

// ------------------------------------------------------------------ loop
const debug = params.get('debug') === '1';
let frames = 0, drawn = 0;
let prev = null;
let queued = false;
function tick() {
	if (queued || !gate.running) return;
	queued = true;
	requestAnimationFrame((t) => { queued = false; frame(t); });
}
// For checks from outside (the panel shell, screenshots): is it drawing, how many frames so far.
window.__brain = { get running() { return gate.running; }, get frames() { return drawn; } };
function frame(now) {
	if (!gate.running) { prev = null; return; }
	drawn++;
	const ad = elapsedFrameSeconds(now, prev), d = frameDeltaSeconds(now, prev);
	prev = now;
	workerWatchdog(now);
	if (layout.step()) renderer.updatePositions();
	const settled = layout.isSettled();
	if (settled && !settledOnce) { settledOnce = true; renderer.refreshClusterClouds(); $('loading').style.display = 'none'; if (!framed) { framed = true; if (turn < 0 && sel < 0 && !filter.win) recenter(); } }
	director.update(d);
	stepTurn(now);
	sparks.ambient(now);
	sparks.update(now);
	cores.update(now);
	marks.update(now);
	shell.update();
	if (renderer.linkSegments) renderer.linkSegments.visible = baseLinesVisible(showAll);   // Galaxy View's layer of every line
	renderer.render(d, ad);
	updateLabels();
	if (debug && (frames++ % 30 === 0)) $('statLine').dataset.debug = (layout instanceof WorkerForceLayout ? 'worker' : 'main') + ' ticks=' + layout.ticks + ' settled=' + layout.isSettled() + ' frames=' + frames;
	tick();
}

async function boot() {
	initTheme();
	motion = storeGet('brain_motion') !== '0' && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
	if (params.get('motion') === '0') motion = false;
	if (params.get('lines') === 'all') showAll = true;
	$('motionBtn').classList.toggle('on', motion);
	const coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
	tier = TIERS[params.get('tier')] || (coarse || window.innerWidth < 820 ? TIERS.mobile : TIERS.high);
	const g = await loadGraph();
	if (source !== 'live') {
		const b = $('sourceBadge');
		b.hidden = false;
		b.textContent = sampleBadge(source === 'sample-embedded', whyNot);
	}
	indexRaw(g);
	buildControls();
	// Lay windows out first so their stars seed their clusters, then everything.
	rebuild(true);
	director.autoEnabled = motion;
	resize();
	const f = computeFraming();
	// Cold start: the stars are still seeds near the middle; frame what they will spread to.
	director.setInitial(f.center, layout.isSettled() ? f.radius * 1.08 : Math.max(f.radius, physics.ball) * 1.08);
	if (layout.isSettled()) shell.place(f.center, f.radius);
	if (layout.isSettled()) { framed = true; }
	wire();
	renderTurns();
	// For screenshots and links: ?win=w:g2  ?sel=m:0005  ?turn=3  ?q=猫  ?settle=1  ?tier=mobile
	if (params.get('win')) { $('winSel').value = params.get('win'); $('winSel').dispatchEvent(new Event('change')); }
	if (params.get('sel')) selectId(params.get('sel'), true);
	if (params.get('turn')) setTurn(Number(params.get('turn')) - 1);
	if (params.get('q')) { $('q').value = params.get('q'); runSearch(); }
	tick();
}
// AstrBot adds its bridge script at the end of the page, after this bundle: start once
// the whole page is parsed, so the bridge is there to be found.
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
else boot();
