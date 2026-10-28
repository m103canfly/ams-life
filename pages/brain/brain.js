// ams-life (AGPL-3.0); see NOTICE.md.
// The brain map: draws the graph (graph.js lays it out), filters, search,
// click-to-open, and "what each reply recalled". Read only: the page only
// ever reads through bridge.apiGet and has no way to write.
//
// Data: from the panel API when opened inside AstrBot's plugin view (step 2 of
// this page; until then the API is missing and the invented sample is shown
// with a badge), otherwise the invented sample (sample.js).
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const params = new URLSearchParams(location.search);
  const canvas = $("brain"), ctx = canvas.getContext("2d");
  const layer = document.createElement("canvas"), lctx = layer.getContext("2d");
  const isDark = () => document.documentElement.dataset.theme === "dark";
  const DAY = 86400;

  // Colours are "r,g,b" strings like the dashboard's orb.js.
  const KIND = {
    window: { name: "窗口", light: "217,88,0", dark: "255,138,31", r: 10 },
    person: { name: "人", light: "52,150,108", dark: "96,200,150", r: 4.6 },
    memory: { name: "记忆", light: "84,112,136", dark: "140,172,196", r: 2.8 },
    event: { name: "事件", light: "196,146,32", dark: "242,193,78", r: 2.6 },
    note: { name: "本子", light: "118,78,214", dark: "167,139,250", r: 4.2 },
  };
  const EDGE = {
    link: { name: "联想", light: "84,112,136", dark: "140,172,196", a: 0.32 },
    origin: { name: "出处", light: "217,88,0", dark: "255,138,31", a: 0.09 },
    about: { name: "跟谁有关", light: "52,150,108", dark: "96,200,150", a: 0.12 },
    impression: { name: "印象", light: "52,150,108", dark: "96,200,150", a: 0.28, dash: [5, 5] },
  };
  const CORES = [
    { key: "social", name: "想说话", c: "255,138,31" },
    { key: "curiosity", name: "好奇", c: "84,181,139" },
    { key: "boredom", name: "无聊", c: "152,147,138" },
    { key: "seen", name: "想被看见", c: "242,193,78" },
    { key: "talked", name: "说多了", c: "139,92,246" },
    { key: "stress", name: "压力", c: "229,83,61" },
    { key: "valence", name: "心情", c: "91,141,239" },
  ];
  const col = (spec) => (isDark() ? spec.dark : spec.light);

  // ---------------------------------------------------------------- state
  let graph = null, source = "sample", sample = null, bridge = null;
  let N = [];          // nodes: data + layout (x, y, vx, vy, mass, side...)
  let E = [];          // edges: {a, b, kind, w}
  let adj = [];        // node index -> edge indexes
  let byId = new Map();
  let sim = null;
  let body = {};
  const view = { k: 0.5, tx: 0, ty: 0 };
  const filter = { kinds: new Set(Object.keys(KIND)), edges: new Set(Object.keys(EDGE)), win: "", vis: "all", from: 24, to: 0 };
  let shown = null, focus = null, hits = null;
  let sel = -1, hover = -1, turn = -1, turnStart = 0;
  let staticDirty = true, motion = true;
  let sparks = [];
  let W = 0, H = 0, DPR = 1;

  // ---------------------------------------------------------------- data
  function findBridge() {
    let b = null;
    try { b = window.AstrBotPluginView || window.AstrBotPluginPage || window.astrbotPluginView || null; } catch (e) { b = null; }
    try { if (!b && window.parent && window.parent !== window) b = window.parent.AstrBotPluginView || window.parent.AstrBotPluginPage || null; } catch (e) { b = null; }
    let embedded = false;
    try { embedded = !!(window.parent && window.parent !== window); } catch (e) { embedded = false; }
    return b && embedded ? b : null;
  }
  const unwrap = (raw) => (raw && raw.data !== undefined ? raw.data : raw);

  async function loadGraph() {
    bridge = findBridge();
    if (bridge) {
      try {
        const ctx0 = await Promise.race([bridge.ready(), new Promise((r) => setTimeout(() => r(null), 3000))]);
        if (!params.get("theme") && !storeGet("bio_theme")) applyTheme(!!(ctx0 && ctx0.isDark));
        const g = unwrap(await Promise.race([bridge.apiGet("page/brain", {}),
          new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), 8000))]));
        if (g && Array.isArray(g.nodes)) { source = "live"; return g; }
      } catch (e) { /* the API comes in step 2 of this page; fall back to the sample */ }
    }
    sample = window.BrainSample.make({ n: Number(params.get("n")) || 900 });
    source = bridge ? "sample-embedded" : "sample";
    return sample.graph;
  }

  // What the owner sees when a point is opened. Content only travels then.
  async function getDetail(id) {
    if (source === "live") {
      try { return unwrap(await bridge.apiGet("page/brain/node", { id })); } catch (e) { return { error: "没取到：" + (e && e.message || e) }; }
    }
    return sample && sample.details[id] || null;
  }
  async function searchContent(q) {
    if (source === "live") {
      try { const r = unwrap(await bridge.apiGet("page/brain/search", { q })); return Array.isArray(r) ? r : (r && r.ids) || []; } catch (e) { return []; }
    }
    const out = [];
    if (!sample) return out;
    for (const id in sample.details) {
      const d = sample.details[id];
      if ((d.text || "").includes(q) || (d.title || "").includes(q)) out.push(id);
    }
    return out;
  }

  function build(g) {
    graph = g;
    body = Object.assign({}, g.body || {});
    N = []; E = []; byId = new Map();
    for (const raw of g.nodes || []) {
      if (!raw || !raw.id || !KIND[raw.kind] || byId.has(raw.id)) continue;
      const n = Object.assign({}, raw, { i: N.length, x: 0, y: 0, vx: 0, vy: 0, mass: 1, side: 0 });
      byId.set(n.id, n.i); N.push(n);
    }
    // Body nuclei: fixed in the middle of the brain, in the layout so the
    // rest keeps clear of them.
    // A column down the seam between the two halves.
    CORES.forEach((c, k) => {
      const n = { id: "core:" + c.key, kind: "core", core: c, label: c.name, i: N.length, x: 0, y: (k - (CORES.length - 1) / 2) * 100,
        vx: 0, vy: 0, mass: 4, side: 0, fixed: true };
      byId.set(n.id, n.i); N.push(n);
    });
    for (const e of g.edges || []) {
      if (!EDGE[e.kind]) continue;
      const a = byId.get(e.s), b = byId.get(e.t);
      if (a === undefined || b === undefined || a === b) continue;
      E.push({ a, b, kind: e.kind, w: Number(e.w) || 1, ts: e.ts || 0 });
    }
    adj = N.map(() => []);
    E.forEach((e, k) => { adj[e.a].push(k); adj[e.b].push(k); });

    // Which half each point belongs to, and where the windows sit.
    const winSide = (wid) => { const k = byId.get(wid); return k === undefined ? -1 : (N[k].sub === "private" ? 1 : -1); };
    const groups = N.filter((n) => n.kind === "window" && n.sub !== "private");
    const privs = N.filter((n) => n.kind === "window" && n.sub === "private");
    const B = window.BrainGraph.BRAIN;
    const place = (list, side) => {
      // Sunflower spread inside the half, busiest window nearest its middle.
      list.sort((p, q) => (q.w || 0) - (p.w || 0));
      list.forEach((n, k) => {
        const rr = Math.sqrt((k + 0.6) / list.length) * 0.72, ang = k * 2.39996 + (side > 0 ? 0.8 : 0);
        n.x = side * B.lobeX + Math.cos(ang) * rr * B.lobeA; n.y = Math.sin(ang) * rr * B.lobeB;
        n.mass = 7; n.side = side; n.fixed = true;   // windows stay put; the rest gathers round them
      });
    };
    place(groups, -1); place(privs, 1);
    let seed = 7;
    const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647 - 0.5; };
    for (const n of N) {
      if (n.kind === "window" || n.kind === "core") continue;
      if (n.kind === "person") {
        n.mass = 2.2;
        const ws = adj[n.i].map((k) => E[k]).map((e) => (e.a === n.i ? e.b : e.a)).filter((j) => N[j].kind === "window");
        if (ws.length) { n.x = ws.reduce((s, j) => s + N[j].x, 0) / ws.length; n.y = ws.reduce((s, j) => s + N[j].y, 0) / ws.length; }
        n.x += rnd() * 120; n.y += rnd() * 120;
        continue;
      }
      n.side = n.where ? winSide(n.where) : -1;
      const w = n.where !== undefined && byId.get(n.where);
      const base = w !== undefined && w !== false ? N[w] : { x: n.side * B.lobeX, y: 0 };
      n.x = base.x + rnd() * 140; n.y = base.y + rnd() * 140;
    }
    const LEN = { origin: [34, 0.5], about: [80, 0.12], impression: [110, 0.06], link: [26, 0.25] };
    const links = E.map((e) => {
      let len = LEN[e.kind][0], k = LEN[e.kind][1];
      if (e.kind === "link") {
        k *= Math.min(1.6, 0.6 + e.w * 0.2);
        // An association across two places should not drag either cluster away.
        if (N[e.a].where !== N[e.b].where) { k *= 0.2; len = 160; }
      }
      return { a: e.a, b: e.b, len, k };
    });
    sim = new window.BrainGraph.Sim(N, links);
    sim.charge = -34 * Math.min(1.5, Math.max(0.35, 900 / Math.max(200, N.length)));

    // Time filter covers the oldest point.
    const now = g.now || Date.now() / 1000;
    let oldest = 1;
    for (const n of N) if (n.ts) oldest = Math.max(oldest, Math.ceil((now - n.ts) / DAY));
    filter.from = oldest; filter.to = 0;
    for (const id of ["tFrom", "tTo"]) $(id).max = String(oldest);
  }

  // ---------------------------------------------------------------- filters
  function computeShown() {
    const now = graph.now || Date.now() / 1000;
    shown = new Uint8Array(N.length);
    for (const n of N) {
      if (n.kind === "core") { shown[n.i] = 1; continue; }
      if (!filter.kinds.has(n.kind)) continue;
      if (filter.vis !== "all" && n.vis && n.vis !== filter.vis) continue;
      if (filter.vis !== "all" && n.kind === "window" && (n.sub === "private") !== (filter.vis === "private")) continue;
      if (n.ts && n.kind !== "person" && n.kind !== "window") {
        const age = (now - n.ts) / DAY;
        if (age > filter.from + 0.0001 || age < filter.to - 0.0001) continue;
      }
      shown[n.i] = 1;
    }
    computeFocus();
  }

  // focus: points drawn at full strength; the rest are dimmed. A turn wins
  // over a selection, a selection over the window filter.
  function computeFocus() {
    focus = null;
    if (turn >= 0) {
      const t = graph.turns[turn];
      focus = new Uint8Array(N.length);
      for (const id of [].concat(t.recalled || [], t.held || [], [t.where])) { const k = byId.get(id); if (k !== undefined) focus[k] = 1; }
    } else if (sel >= 0) {
      focus = new Uint8Array(N.length);
      focus[sel] = 1;
      for (const k of adj[sel]) { const e = E[k]; if (filter.edges.has(e.kind)) { focus[e.a] = 1; focus[e.b] = 1; } }
    } else if (filter.win) {
      const w = byId.get(filter.win);
      focus = new Uint8Array(N.length);
      if (w !== undefined) {
        focus[w] = 1;
        for (const n of N) if (n.where === filter.win) focus[n.i] = 1;
        for (const k of adj[w]) { const e = E[k]; if (e.kind === "impression") focus[e.a === w ? e.b : e.a] = 1; }
        for (const n of N) if (n.where === filter.win) for (const k of adj[n.i]) { const e = E[k]; if (e.kind === "about") focus[e.a === n.i ? e.b : e.a] = 1; }
      }
    }
    staticDirty = true;
    updateStat();
  }

  function updateStat() {
    let ns = 0, es = 0;
    for (const n of N) if (shown[n.i] && n.kind !== "core") ns++;
    for (const e of E) if (shown[e.a] && shown[e.b] && filter.edges.has(e.kind)) es++;
    $("statLine").textContent = "显示 " + ns + " / " + (N.length - CORES.length) + " 个点 · " + es + " 条线";
  }

  // ---------------------------------------------------------------- drawing
  const sprites = new Map();
  function glow(rgb) {
    let s = sprites.get(rgb);
    if (s) return s;
    s = document.createElement("canvas"); s.width = s.height = 64;
    const g = s.getContext("2d"), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, "rgba(" + rgb + ",1)"); gr.addColorStop(0.25, "rgba(" + rgb + ",.55)");
    gr.addColorStop(0.6, "rgba(" + rgb + ",.12)"); gr.addColorStop(1, "rgba(" + rgb + ",0)");
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    sprites.set(rgb, s);
    return s;
  }

  function resize() {
    const r = canvas.getBoundingClientRect();
    DPR = Math.min(2, window.devicePixelRatio || 1);
    W = Math.max(1, r.width); H = Math.max(1, r.height);
    for (const c of [canvas, layer]) { c.width = Math.round(W * DPR); c.height = Math.round(H * DPR); }
    staticDirty = true;
  }

  function fit() {
    const B = window.BrainGraph.BRAIN;
    const padB = 130;   // the turn strip at the bottom
    view.k = Math.min(W / (B.a * 2 + 120), (H - padB) / (B.b * 2 + 100));
    view.tx = W / 2; view.ty = (H - padB) / 2 + 8;
    staticDirty = true;
  }
  const sx = (x) => x * view.k + view.tx, sy = (y) => y * view.k + view.ty;
  const radius = (n) => {
    const base = KIND[n.kind] ? KIND[n.kind].r : 6;
    const w = n.kind === "memory" ? 0.7 + (n.w || 0.5) * 0.9 : (n.kind === "window" ? 0.7 + (n.w || 0.5) * 0.6 : 1);
    return base * w * Math.max(0.55, Math.min(2.2, Math.sqrt(view.k * 2.2)));
  };

  function drawOutline(c) {
    const B = window.BrainGraph.BRAIN;
    c.save();
    c.lineWidth = 1;
    for (const side of [-1, 1]) {
      c.beginPath();
      c.ellipse(sx(side * B.lobeX), sy(0), (B.lobeA + 40) * view.k, (B.lobeB + 30) * view.k, 0, 0, Math.PI * 2);
      c.fillStyle = isDark() ? "rgba(255,255,255,.018)" : "rgba(0,0,0,.022)";
      c.fill();
      c.strokeStyle = isDark() ? "rgba(230,225,215,.10)" : "rgba(30,30,30,.10)";
      c.setLineDash([2, 6]); c.stroke(); c.setLineDash([]);
    }
    c.fillStyle = isDark() ? "rgba(230,225,215,.32)" : "rgba(30,30,30,.32)";
    c.font = "12px Bahnschrift, 'Segoe UI', sans-serif";
    c.textAlign = "center";
    c.fillText("群里（公开）", sx(-B.lobeX), sy(-B.lobeB - 48));
    c.fillText("私聊（私下）", sx(B.lobeX), sy(-B.lobeB - 48));
    c.restore();
  }

  function inView(n, m) {
    const x = sx(n.x), y = sy(n.y);
    return x > -m && y > -m && x < W + m && y < H + m;
  }

  function drawStatic() {
    const c = lctx;
    c.setTransform(DPR, 0, 0, DPR, 0, 0);
    c.clearRect(0, 0, W, H);
    drawOutline(c);
    const dimA = isDark() ? 0.07 : 0.09;
    const zoomA = Math.max(0.55, Math.min(1.4, 0.6 + view.k * 0.6));
    // Edges, one path per kind (and per strength: dimmed / in focus).
    for (const kind of Object.keys(EDGE)) {
      if (!filter.edges.has(kind)) continue;
      const spec = EDGE[kind], rgb = col(spec);
      for (const pass of focus ? [0, 1] : [1]) {
        c.beginPath();
        let any = false;
        for (const e of E) {
          if (e.kind !== kind || !shown[e.a] || !shown[e.b]) continue;
          const inF = !focus || (focus[e.a] && focus[e.b]);
          if ((pass === 1) !== !!inF) continue;
          const a = N[e.a], b = N[e.b];
          if (!inView(a, 40) && !inView(b, 40)) continue;
          c.moveTo(sx(a.x), sy(a.y)); c.lineTo(sx(b.x), sy(b.y)); any = true;
        }
        if (!any) continue;
        const alpha = pass ? spec.a * zoomA * (focus ? 2.2 : 1) : spec.a * 0.25;
        c.strokeStyle = "rgba(" + rgb + "," + Math.min(0.9, alpha).toFixed(3) + ")";
        c.lineWidth = kind === "link" ? 0.9 : 0.7;
        c.setLineDash(spec.dash || []);
        c.stroke();
      }
    }
    c.setLineDash([]);
    // Points, one path per kind and pass. Private ones are hollow rings.
    for (const kind of Object.keys(KIND)) {
      const rgb = col(KIND[kind]);
      for (const pass of focus ? [0, 1] : [1]) {
        const fill = new Path2D(), ring = new Path2D();
        let anyF = false, anyR = false;
        for (const n of N) {
          if (n.kind !== kind || !shown[n.i]) continue;
          const inF = !focus || focus[n.i];
          if ((pass === 1) !== !!inF) continue;
          if (!inView(n, 20)) continue;
          const x = sx(n.x), y = sy(n.y), r = radius(n);
          const p = n.vis === "private" && kind !== "window" ? ring : fill;
          if (kind === "event") { p.rect(x - r, y - r, r * 2, r * 2); }
          else if (kind === "note") { p.moveTo(x, y - r * 1.25); p.lineTo(x + r, y); p.lineTo(x, y + r * 1.25); p.lineTo(x - r, y); p.closePath(); }
          else { p.moveTo(x + r, y); p.arc(x, y, r, 0, Math.PI * 2); }
          if (p === ring) anyR = true; else anyF = true;
        }
        const a = pass ? 0.9 : dimA * 1.6;
        if (anyF) { c.fillStyle = "rgba(" + rgb + "," + a + ")"; c.fill(fill); }
        if (anyR) {
          c.fillStyle = "rgba(" + rgb + "," + (a * 0.18).toFixed(3) + ")"; c.fill(ring);
          c.strokeStyle = "rgba(" + rgb + "," + a + ")"; c.lineWidth = 1.1; c.stroke(ring);
        }
      }
    }
    // Window rings and labels; people and categories when zoomed in.
    c.font = "12px Bahnschrift, 'Segoe UI', 'Microsoft YaHei', sans-serif";
    c.textAlign = "center"; c.textBaseline = "top";
    let labels = 0;
    const ink = isDark() ? "233,227,215" : "22,22,22";
    for (const n of N) {
      if (!shown[n.i] || n.kind === "core" || !inView(n, 30)) continue;
      const inF = !focus || focus[n.i];
      const want = n.kind === "window" || (n.kind === "person" && view.k > 0.75) || (view.k > 1.9 && inF) || (focus && inF && (n.kind === "person" || n.kind === "note") && view.k > 0.5);
      if (!want || labels > 420) continue;
      const x = sx(n.x), y = sy(n.y), r = radius(n);
      if (n.kind === "window") {
        c.beginPath(); c.arc(x, y, r + 4, 0, Math.PI * 2);
        c.strokeStyle = "rgba(" + col(KIND.window) + "," + (inF ? 0.5 : 0.12) + ")"; c.lineWidth = 1; c.stroke();
      }
      c.fillStyle = "rgba(" + ink + "," + (inF ? (n.kind === "window" ? 0.85 : 0.6) : 0.18) + ")";
      c.fillText(n.label || n.kind, x, y + r + 4);
      labels++;
    }
    staticDirty = false;
  }

  function drawCores(t) {
    const c = ctx;
    for (const n of N) {
      if (n.kind !== "core") continue;
      const spec = n.core;
      let v = Number(body[spec.key]);
      if (!Number.isFinite(v)) v = 0;
      let rgb = spec.c;
      if (spec.key === "valence") {   // mood: blue when low, warm yellow when high
        rgb = v >= 0 ? "242,193,78" : "91,141,239";
        v = Math.abs(v);
      }
      v = Math.max(0, Math.min(1, v));
      const breathe = motion ? 1 + Math.sin(t / 1000 * (0.8 + v * 1.6) + n.i) * (0.05 + v * 0.07) : 1;
      const r = (10 + v * 26) * Math.max(0.6, Math.min(2.2, Math.sqrt(view.k * 2.2))) * breathe;
      const x = sx(n.x), y = sy(n.y);
      c.globalAlpha = 0.35 + v * 0.65;
      c.drawImage(glow(rgb), x - r * 1.6, y - r * 1.6, r * 3.2, r * 3.2);
      c.globalAlpha = 1;
      c.beginPath(); c.arc(x, y, r * 0.32, 0, Math.PI * 2);
      c.fillStyle = "rgba(" + rgb + "," + (0.55 + v * 0.45) + ")"; c.fill();
      c.fillStyle = isDark() ? "rgba(233,227,215,.78)" : "rgba(22,22,22,.7)";
      c.font = "11px Bahnschrift, 'Segoe UI', 'Microsoft YaHei', sans-serif";
      c.textAlign = "left"; c.textBaseline = "middle";
      c.fillText(spec.name, x + Math.max(9, r * 0.5), y);
    }
  }

  // Sparks: little lights running along lines. Idle: random associations.
  // In a turn: along the path she took, in order.
  function spawnSparks(t) {
    if (!motion) { sparks = []; return; }
    if (turn >= 0) return;
    if (sparks.length < 26 && Math.random() < 0.35 && E.length) {
      for (let tries = 0; tries < 6; tries++) {
        const k = Math.floor(Math.random() * E.length), e = E[k];
        if (!shown[e.a] || !shown[e.b] || !filter.edges.has(e.kind)) continue;
        if (focus && !(focus[e.a] && focus[e.b])) continue;
        if (e.kind !== "link" && Math.random() < 0.7) continue;
        sparks.push({ k, t0: t, dur: 900 + Math.random() * 900, dir: Math.random() < 0.5 });
        break;
      }
    }
  }
  function drawSparks(t) {
    const c = ctx;
    sparks = sparks.filter((s) => t - s.t0 < s.dur);
    for (const s of sparks) {
      const e = E[s.k], a = N[s.dir ? e.a : e.b], b = N[s.dir ? e.b : e.a];
      const p = (t - s.t0) / s.dur, q = Math.max(0, p - 0.18);
      const x = sx(a.x + (b.x - a.x) * p), y = sy(a.y + (b.y - a.y) * p);
      const rgb = col(EDGE[e.kind]);
      c.strokeStyle = "rgba(" + rgb + ",.5)"; c.lineWidth = 1.4;
      c.beginPath(); c.moveTo(sx(a.x + (b.x - a.x) * q), sy(a.y + (b.y - a.y) * q)); c.lineTo(x, y); c.stroke();
      const r = 7 * Math.max(0.6, Math.min(1.6, view.k * 1.5));
      c.globalAlpha = Math.sin(p * Math.PI);
      c.drawImage(glow(rgb), x - r, y - r, r * 2, r * 2);
      c.globalAlpha = 1;
    }
  }

  const STEP = 520;   // ms between two recalled memories lighting up
  function drawTurn(t) {
    if (turn < 0) return;
    const c = ctx, tr = graph.turns[turn];
    const hot = isDark() ? "255,160,60" : "255,107,0";
    const path = (tr.path || []).map((p) => [byId.get(p[0]), byId.get(p[1])]).filter((p) => p[0] !== undefined && p[1] !== undefined);
    const order = new Map();
    (tr.recalled || []).forEach((id, k) => { const i = byId.get(id); if (i !== undefined) order.set(i, k); });
    const heldSet = new Set((tr.held || []).map((id) => byId.get(id)).filter((i) => i !== undefined));
    const cycle = (order.size + 3) * STEP + 1800;
    const local = motion ? (t - turnStart) % cycle : cycle;
    // the path she took, drawn as it is walked
    path.forEach(([i, j], k) => {
      const start = (k + 0.5) * STEP;
      if (local < start) return;
      const p = Math.min(1, (local - start) / STEP), a = N[i], b = N[j];
      const held = heldSet.has(j);
      c.strokeStyle = held ? "rgba(150,150,150,.6)" : "rgba(" + hot + ",.85)";
      c.lineWidth = 2; c.setLineDash(held ? [4, 4] : []);
      c.beginPath(); c.moveTo(sx(a.x), sy(a.y)); c.lineTo(sx(a.x + (b.x - a.x) * p), sy(a.y + (b.y - a.y) * p)); c.stroke();
      c.setLineDash([]);
    });
    // the window she was talking in
    const w = byId.get(tr.where);
    if (w !== undefined) {
      const n = N[w], r = radius(n) + 9 + (motion ? Math.sin(t / 400) * 2 : 0);
      c.beginPath(); c.arc(sx(n.x), sy(n.y), r, 0, Math.PI * 2);
      c.strokeStyle = "rgba(" + hot + ",.7)"; c.lineWidth = 1.5; c.stroke();
    }
    // Recalled memories often sit close together, so their labels go in a
    // column beside the window, each with a thin line to its point.
    const anchor = w !== undefined ? N[w] : null;
    const colX = anchor ? sx(anchor.x) + (sx(anchor.x) > W - 260 ? -150 : 46) : 20;
    const colY = anchor ? sy(anchor.y) - order.size * 9 : 20;
    for (const [i, k] of order) {
      const lit = local >= k * STEP;
      if (!lit) continue;
      const n = N[i], x = sx(n.x), y = sy(n.y);
      const fresh = Math.max(0, 1 - (local - k * STEP) / 900);
      const r = (16 + fresh * 18) * Math.max(0.7, Math.min(1.8, view.k * 1.6));
      c.drawImage(glow(hot), x - r, y - r, r * 2, r * 2);
      c.beginPath(); c.arc(x, y, Math.max(3.5, radius(n) * 1.4), 0, Math.PI * 2);
      c.fillStyle = "rgba(" + hot + ",1)"; c.fill();
      const ly = colY + k * 18;
      c.strokeStyle = "rgba(" + hot + ",.35)"; c.lineWidth = 0.8;
      c.beginPath(); c.moveTo(x, y); c.lineTo(colX - 4, ly); c.stroke();
      c.fillStyle = isDark() ? "rgba(255,230,200,.95)" : "rgba(120,50,0,.95)";
      c.font = "12px Bahnschrift, 'Segoe UI', 'Microsoft YaHei', sans-serif"; c.textAlign = "left"; c.textBaseline = "middle";
      c.fillText((k + 1) + " · " + (n.label || "") + (n.where && n.where !== tr.where ? "（" + whereLabel(n.where) + "）" : ""), colX, ly);
    }
    for (const i of heldSet) {
      const n = N[i], x = sx(n.x), y = sy(n.y);
      if (anchor && !path.some((p) => p[1] === i)) {   // held back, not reached along a line: tie it to the place
        c.setLineDash([3, 5]); c.strokeStyle = "rgba(150,150,150,.55)"; c.lineWidth = 1;
        c.beginPath(); c.moveTo(sx(anchor.x), sy(anchor.y)); c.lineTo(x, y); c.stroke(); c.setLineDash([]);
      }
      const r = Math.max(6, radius(n) * 2.2);
      c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2);
      c.fillStyle = "rgba(140,140,140,.35)"; c.fill();
      c.setLineDash([3, 3]); c.strokeStyle = "rgba(150,150,150,.95)"; c.lineWidth = 1.3; c.stroke(); c.setLineDash([]);
      c.fillStyle = isDark() ? "rgba(200,200,200,.9)" : "rgba(90,90,90,.95)";
      c.font = "11px Bahnschrift, 'Segoe UI', 'Microsoft YaHei', sans-serif"; c.textAlign = "left"; c.textBaseline = "middle";
      c.fillText("没说 · " + (n.label || "") + (n.where ? "（" + whereLabel(n.where) + "）" : ""), x + r + 4, y);
    }
  }

  function drawMarks(t) {
    const c = ctx;
    if (hits) {
      c.strokeStyle = isDark() ? "rgba(255,177,77,.95)" : "rgba(217,88,0,.95)"; c.lineWidth = 1.5;
      c.beginPath();
      for (const n of N) if (hits[n.i] && shown[n.i] && inView(n, 20)) { const r = radius(n) + 5; c.moveTo(sx(n.x) + r, sy(n.y)); c.arc(sx(n.x), sy(n.y), r, 0, Math.PI * 2); }
      c.stroke();
    }
    if (sel >= 0) {
      const n = N[sel], r = radius(n) + 7 + (motion ? Math.sin(t / 300) * 1.5 : 0);
      c.beginPath(); c.arc(sx(n.x), sy(n.y), r, 0, Math.PI * 2);
      c.strokeStyle = isDark() ? "rgba(255,255,255,.9)" : "rgba(20,20,20,.85)"; c.lineWidth = 1.6; c.stroke();
    }
    if (hover >= 0 && hover !== sel) {
      const n = N[hover];
      c.beginPath(); c.arc(sx(n.x), sy(n.y), radius(n) + 5, 0, Math.PI * 2);
      c.strokeStyle = isDark() ? "rgba(255,255,255,.6)" : "rgba(20,20,20,.5)"; c.lineWidth = 1; c.stroke();
    }
  }

  let lastStatic = 0;
  function frame(t) {
    if (sim) {
      const t0 = performance.now();
      let moved = false;
      while (performance.now() - t0 < 9 && sim.tick()) moved = true;
      if (moved && t - lastStatic > 40) staticDirty = true;   // ~25 fps while it settles
      if (!moved && sim.alpha < sim.alphaMin && $("loading").style.display !== "none") $("loading").style.display = "none";
    }
    if (staticDirty) { drawStatic(); lastStatic = t; }
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(layer, 0, 0);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    spawnSparks(t);
    drawSparks(t);
    drawCores(t);
    drawTurn(t);
    drawMarks(t);
    requestAnimationFrame(frame);
  }

  // ?bench=1: time the layout and the drawing once, shown in the top bar.
  function bench() {
    let t0 = performance.now(), ticks = 0;
    while (sim.tick()) ticks++;
    const layout = performance.now() - t0;
    t0 = performance.now();
    for (let k = 0; k < 20; k++) drawStatic();
    const full = (performance.now() - t0) / 20;
    t0 = performance.now();
    for (let k = 0; k < 200; k++) {
      const t = k * 16;
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(layer, 0, 0);
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0); spawnSparks(t); drawSparks(t); drawCores(t); drawTurn(t); drawMarks(t);
    }
    const light = (performance.now() - t0) / 200;
    $("statLine").textContent += " · 铺开 " + Math.round(layout) + " ms（" + ticks + " 步）· 整张重画 " + full.toFixed(1) + " ms · 平常一帧 " + light.toFixed(2) + " ms";
    $("loading").style.display = "none";
  }

  // ---------------------------------------------------------------- picking
  function pick(px, py) {
    let best = -1, bd = Infinity;
    for (const n of N) {
      if (!shown[n.i]) continue;
      const dx = sx(n.x) - px, dy = sy(n.y) - py, d = dx * dx + dy * dy;
      const r = (n.kind === "core" ? 22 : radius(n)) + 5;
      if (d < r * r && d < bd) { bd = d; best = n.i; }
    }
    return best;
  }

  const fmtTime = (ts) => {
    if (!ts) return "";
    const d = new Date(ts * 1000), p = (x) => String(x).padStart(2, "0");
    return (d.getMonth() + 1) + "-" + p(d.getDate()) + " " + p(d.getHours()) + ":" + p(d.getMinutes());
  };
  const ago = (ts) => {
    if (!ts) return "";
    const s = (graph.now || Date.now() / 1000) - ts;
    if (s < 3600) return Math.max(1, Math.round(s / 60)) + " 分钟前";
    if (s < DAY) return Math.round(s / 3600) + " 小时前";
    return Math.round(s / DAY) + " 天前";
  };
  const kindName = (n) => (n.kind === "core" ? "身体" : KIND[n.kind].name) + (n.kind === "window" ? (n.sub === "private" ? " · 私聊" : " · 群") : "");
  const whereLabel = (id) => { const k = byId.get(id); return k === undefined ? "" : N[k].label; };
  const shortLine = (n) => [kindName(n), n.label, n.where ? whereLabel(n.where) : "", ago(n.ts)].filter(Boolean).join(" · ");

  // ---------------------------------------------------------------- drawer
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[ch])); }

  let drawerFor = -1;
  async function openDrawer(i) {
    const n = N[i];
    drawerFor = i;
    $("drawer").hidden = false;
    $("dKind").textContent = kindName(n) + (n.cat && n.cat !== n.label ? " · " + n.cat : "");
    $("dTitle").textContent = n.label || n.id;
    const meta = [];
    if (n.kind === "core") {
      let v = Number(body[n.core.key]) || 0;
      meta.push(["现在", n.core.key === "valence" ? (v >= 0 ? "偏好 " : "偏低 ") + Math.round(Math.abs(v) * 100) + "%" : Math.round(v * 100) + "%"]);
      meta.push(["说明", "身体里的一样，只有数，不存话。越大越亮，数越高。"]);
    } else {
      if (n.ts) meta.push(["时间", fmtTime(n.ts) + "（" + ago(n.ts) + "）"]);
      if (n.where) meta.push(["窗口", "<a data-go=\"" + esc(n.where) + "\">" + esc(whereLabel(n.where)) + "</a>"]);
      if (n.vis) meta.push(["分寸", n.vis === "private" ? "私下（空心）" : "公开"]);
      if (n.kind === "memory") meta.push(["分量", Math.round((n.w || 0) * 100) + "%"]);
      if (n.kind === "note" && n.self) meta.push(["", "她写给自己的"]);
      meta.push(["编号", esc(n.id)]);
    }
    $("dMeta").innerHTML = meta.map(([k, v]) => "<dt>" + esc(k) + "</dt><dd>" + (String(v).startsWith("<a") ? v : esc(v)) + "</dd>").join("");
    $("dBody").innerHTML = n.kind === "core" ? "" : "<span class=\"muted\">取内容…</span>";
    renderLinks(i);
    if (n.kind === "core") return;
    const d = await getDetail(n.id);
    if (drawerFor !== i) return;
    if (!d) { $("dBody").innerHTML = "<span class=\"muted\">没有更多内容。</span>"; return; }
    if (d.error) { $("dBody").innerHTML = "<span class=\"muted\">" + esc(d.error) + "</span>"; return; }
    let html = "";
    if (d.title) $("dTitle").textContent = d.title;
    if (d.text) html += "<div class=\"text\">" + esc(d.text) + "</div>";
    if (Array.isArray(d.lines) && d.lines.length) html += "<dl>" + d.lines.map(([k, v]) => "<dt>" + esc(k) + "</dt><dd>" + esc(v) + "</dd>").join("") + "</dl>";
    if (d.qq) html += "<div class=\"reveal\"><button class=\"btn\" id=\"qqBtn\">显示 QQ 号</button> <span id=\"qqVal\"></span></div>";
    $("dBody").innerHTML = html || "<span class=\"muted\">没有更多内容。</span>";
    const b = $("qqBtn");
    if (b) b.onclick = () => { $("qqVal").textContent = d.qq; b.remove(); };
  }

  function renderLinks(i) {
    const groups = {};
    for (const k of adj[i]) {
      const e = E[k], j = e.a === i ? e.b : e.a;
      (groups[e.kind] = groups[e.kind] || []).push({ j, w: e.w });
    }
    let html = "<div class=\"d-links\">";
    for (const kind of Object.keys(EDGE)) {
      const list = groups[kind];
      if (!list) continue;
      list.sort((p, q) => q.w - p.w);
      html += "<h3>" + EDGE[kind].name + " · " + list.length + "</h3><ul>";
      for (const { j } of list.slice(0, 40)) {
        const n = N[j];
        const rgb = n.kind === "core" ? "150,150,150" : col(KIND[n.kind]);
        html += "<li data-node=\"" + j + "\"><span class=\"dot\" style=\"background:rgb(" + rgb + ")\"></span>" + esc(shortLine(n)) + "</li>";
      }
      if (list.length > 40) html += "<li class=\"more\">还有 " + (list.length - 40) + " 个</li>";
      html += "</ul>";
    }
    $("dLinks").innerHTML = html + "</div>";
  }

  function select(i, fly) {
    sel = i;
    if (i < 0) { $("drawer").hidden = true; drawerFor = -1; computeFocus(); return; }
    if (turn >= 0) setTurn(-1, true);
    computeFocus();
    openDrawer(i);
    if (fly) flyTo(N[i]);
  }

  function flyTo(n) {
    const k = Math.max(view.k, 1.1);
    animateView(k, W / 2 - 160 - n.x * k, (H - 130) / 2 - n.y * k);
  }
  // Zoom so that all these points fit (a turn: what she recalled and held back).
  function flyToAll(list) {
    if (!list.length) return;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const n of list) { x0 = Math.min(x0, n.x); x1 = Math.max(x1, n.x); y0 = Math.min(y0, n.y); y1 = Math.max(y1, n.y); }
    const B = window.BrainGraph.BRAIN;
    const kFit = Math.min(W / (B.a * 2 + 120), (H - 130) / (B.b * 2 + 100));
    const k = Math.max(kFit, Math.min(2.4, (W - 260) / Math.max(1, x1 - x0), (H - 260) / Math.max(1, y1 - y0)));
    animateView(k, W / 2 - (x0 + x1) / 2 * k, (H - 130) / 2 - (y0 + y1) / 2 * k);
  }
  function animateView(k, tx, ty) {
    const from = { k: view.k, tx: view.tx, ty: view.ty }, t0 = performance.now();
    const step = (t) => {
      const p = Math.max(0, Math.min(1, (t - t0) / 420)), e = p * (2 - p);
      view.k = from.k + (k - from.k) * e; view.tx = from.tx + (tx - from.tx) * e; view.ty = from.ty + (ty - from.ty) * e;
      staticDirty = true;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  // ---------------------------------------------------------------- turns
  function renderTurns() {
    const ts = graph.turns || [];
    if (!ts.length) {
      $("turnList").innerHTML = "<li class=\"more\">还没有记录。她被叫到一次，这里就多一轮。</li>";
      return;
    }
    $("turnList").innerHTML = ts.map((t, k) => "<li data-turn=\"" + k + "\"" + (k === turn ? " class=\"on\"" : "") + ">" +
      esc(fmtTime(t.ts)) + " · " + esc(whereLabel(t.where) || "?") +
      "<small>想起 " + (t.recalled || []).length + " · 没说 " + (t.held || []).length + "</small></li>").join("");
  }

  let liveBody = null;
  function setTurn(k, quiet) {
    const ts = graph.turns || [];
    if (k >= ts.length) k = ts.length - 1;
    if (k < 0 && turn >= 0 && liveBody) body = liveBody;
    if (k >= 0 && turn < 0) liveBody = body;
    turn = k;
    if (k >= 0) {
      if (sel >= 0) { sel = -1; $("drawer").hidden = true; }
      const tr = ts[k];
      if (tr.body) body = Object.assign({}, liveBody, tr.body);
      turnStart = performance.now();
      flyToAll([].concat(tr.recalled || [], tr.held || [], [tr.where]).map((id) => byId.get(id)).filter((i) => i !== undefined).map((i) => N[i]));
      $("turnHint").textContent = fmtTime(tr.ts) + " 在" + whereLabel(tr.where) + "：想起 " + (tr.recalled || []).length +
        " 条（亮的，按顺序），" + ((tr.held || []).length ? (tr.held || []).length + " 条她知道但在这里没说（灰的）。" : "没有被挡下的。") +
        (tr.body ? " 中间的核是那一刻的身体。" : "");
      sparks = [];
    } else if (!quiet) {
      $("turnHint").textContent = "点一轮看她这次想起了谁。亮的是想起的，灰的是她知道、但在这里没说的。";
    }
    renderTurns();
    const on = $("turnList").querySelector("li.on");
    if (on && on.scrollIntoView) on.scrollIntoView({ block: "nearest", inline: "nearest" });
    computeFocus();
  }

  // ---------------------------------------------------------------- search
  let searchTimer = 0;
  function runSearch() {
    const q = $("q").value.trim();
    clearTimeout(searchTimer);
    if (!q) { hits = null; $("hits").innerHTML = ""; staticDirty = true; return; }
    searchTimer = setTimeout(async () => {
      const found = new Set();
      const ql = q.toLowerCase();
      for (const n of N) {
        if (n.kind === "core") continue;
        const hay = [n.id, n.label, n.cat, KIND[n.kind].name, n.where ? whereLabel(n.where) : ""].join(" ").toLowerCase();
        if (hay.includes(ql)) found.add(n.i);
      }
      for (const id of await searchContent(q)) { const k = byId.get(id); if (k !== undefined) found.add(k); }
      if ($("q").value.trim() !== q) return;
      hits = new Uint8Array(N.length);
      for (const k of found) hits[k] = 1;
      const list = [...found].filter((k) => shown[k]).slice(0, 60);
      $("hits").innerHTML = (list.length ? "" : "<li class=\"more\">没找到（或被筛掉了）</li>") + list.map((k) => {
        const n = N[k];
        return "<li data-node=\"" + k + "\"><span class=\"chip\" style=\"width:8px;height:8px;border-radius:50%;background:rgb(" + col(KIND[n.kind]) + ")\"></span>" +
          esc(n.label) + (n.where ? " · " + esc(whereLabel(n.where)) : "") + "<span class=\"k\">" + esc(ago(n.ts) || KIND[n.kind].name) + "</span></li>";
      }).join("") + (found.size > list.length ? "<li class=\"more\">共 " + found.size + " 个，图上都圈出来了</li>" : "");
      staticDirty = true;
    }, 200);
  }

  // ---------------------------------------------------------------- controls
  function storeGet(k) { try { return localStorage.getItem(k) || ""; } catch (e) { return ""; } }
  function storeSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private window */ } }
  function applyTheme(dark) {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    $("themeBtn").textContent = dark ? "浅色" : "深色";
    staticDirty = true;
  }
  function initTheme() {
    const forced = params.get("theme");
    if (forced === "dark" || forced === "light") return applyTheme(forced === "dark");
    const saved = storeGet("bio_theme");
    if (saved === "dark" || saved === "light") return applyTheme(saved === "dark");
    const host = document.documentElement.dataset.theme;
    if (host === "dark" || host === "light") return applyTheme(host === "dark");
    applyTheme(!!(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches));
  }

  function buildControls() {
    const count = {};
    for (const n of N) count[n.kind] = (count[n.kind] || 0) + 1;
    $("kindBoxes").innerHTML = Object.keys(KIND).map((k) => "<label><input type=\"checkbox\" data-kind=\"" + k + "\" checked />" +
      "<span class=\"chip\" style=\"background:rgb(" + col(KIND[k]) + ")\"></span>" + KIND[k].name + " <span class=\"n\">" + (count[k] || 0) + "</span></label>").join("");
    const ecount = {};
    for (const e of E) ecount[e.kind] = (ecount[e.kind] || 0) + 1;
    $("edgeBoxes").innerHTML = Object.keys(EDGE).map((k) => "<label><input type=\"checkbox\" data-edge=\"" + k + "\" checked />" +
      "<span class=\"chip line\" style=\"background:rgb(" + col(EDGE[k]) + ")\"></span>" + EDGE[k].name + " <span class=\"n\">" + (ecount[k] || 0) + "</span></label>").join("");
    const wins = N.filter((n) => n.kind === "window");
    const per = {};
    for (const n of N) if (n.where) per[n.where] = (per[n.where] || 0) + 1;
    const opt = (n) => "<option value=\"" + esc(n.id) + "\">" + esc(n.label) + "（" + (per[n.id] || 0) + "）</option>";
    $("winSel").innerHTML = "<option value=\"\">全部窗口</option>" +
      "<optgroup label=\"群\">" + wins.filter((n) => n.sub !== "private").map(opt).join("") + "</optgroup>" +
      "<optgroup label=\"私聊\">" + wins.filter((n) => n.sub === "private").map(opt).join("") + "</optgroup>";
    $("tFrom").value = String(filter.from); $("tTo").value = String(filter.to);
    timeText();
  }
  function timeText() { $("timeText").textContent = filter.to === 0 ? "最近 " + filter.from + " 天" : filter.from + "–" + filter.to + " 天前"; }

  function wire() {
    $("kindBoxes").addEventListener("change", (ev) => {
      const k = ev.target.dataset.kind; if (!k) return;
      ev.target.checked ? filter.kinds.add(k) : filter.kinds.delete(k); computeShown();
    });
    $("edgeBoxes").addEventListener("change", (ev) => {
      const k = ev.target.dataset.edge; if (!k) return;
      ev.target.checked ? filter.edges.add(k) : filter.edges.delete(k); computeFocus();
    });
    $("winSel").addEventListener("change", () => { filter.win = $("winSel").value; if (sel >= 0) select(-1); else computeFocus(); });
    $("visSeg").addEventListener("click", (ev) => {
      const v = ev.target.dataset.vis; if (!v) return;
      filter.vis = v;
      for (const b of $("visSeg").children) b.classList.toggle("on", b.dataset.vis === v);
      computeShown();
    });
    const onRange = () => {
      let f = Number($("tFrom").value), t = Number($("tTo").value);
      if (t > f) { if (document.activeElement === $("tFrom")) t = f; else f = t; $("tFrom").value = f; $("tTo").value = t; }
      filter.from = f; filter.to = t; timeText(); computeShown();
    };
    $("tFrom").addEventListener("input", onRange); $("tTo").addEventListener("input", onRange);
    $("q").addEventListener("input", runSearch);
    const nodeClick = (ev) => { const li = ev.target.closest("[data-node]"); if (li) select(Number(li.dataset.node), true); };
    $("hits").addEventListener("click", nodeClick);
    $("dLinks").addEventListener("click", nodeClick);
    $("dMeta").addEventListener("click", (ev) => {
      const a = ev.target.closest("[data-go]"); if (!a) return;
      const k = byId.get(a.dataset.go); if (k !== undefined) select(k, true);
    });
    $("drawerClose").addEventListener("click", () => select(-1));
    $("turnList").addEventListener("click", (ev) => { const li = ev.target.closest("[data-turn]"); if (li) setTurn(Number(li.dataset.turn)); });
    $("turnPrev").addEventListener("click", () => setTurn(turn <= 0 ? (graph.turns || []).length - 1 : turn - 1));
    $("turnNext").addEventListener("click", () => setTurn(turn + 1 >= (graph.turns || []).length ? 0 : turn + 1));
    $("turnOff").addEventListener("click", () => setTurn(-1));
    $("fitBtn").addEventListener("click", fit);
    $("motionBtn").addEventListener("click", () => { motion = !motion; $("motionBtn").classList.toggle("on", motion); storeSet("brain_motion", motion ? "1" : "0"); });
    $("themeBtn").addEventListener("click", () => { const d = !isDark(); applyTheme(d); storeSet("bio_theme", d ? "dark" : "light"); buildControls(); });
    $("panelBtn").addEventListener("click", () => $("side").classList.toggle("open"));
    window.addEventListener("resize", () => { resize(); });
    window.addEventListener("keydown", (ev) => {
      if (ev.target && /INPUT|SELECT|TEXTAREA/.test(ev.target.tagName)) return;
      if (ev.key === "Escape") { if (turn >= 0) setTurn(-1); else select(-1); }
      else if (ev.key === "ArrowRight") $("turnNext").click();
      else if (ev.key === "ArrowLeft") $("turnPrev").click();
    });

    // pan / zoom / click
    let drag = null;
    canvas.addEventListener("pointerdown", (ev) => {
      drag = { x: ev.clientX, y: ev.clientY, tx: view.tx, ty: view.ty, moved: false };
      canvas.setPointerCapture(ev.pointerId);
    });
    canvas.addEventListener("pointermove", (ev) => {
      const r = canvas.getBoundingClientRect(), px = ev.clientX - r.left, py = ev.clientY - r.top;
      if (drag) {
        const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
        if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
        if (drag.moved) { canvas.classList.add("drag"); view.tx = drag.tx + dx; view.ty = drag.ty + dy; staticDirty = true; $("tip").hidden = true; return; }
      }
      const h = pick(px, py);
      if (h !== hover) { hover = h; }
      const tip = $("tip");
      if (h >= 0) {
        const n = N[h];
        tip.textContent = n.kind === "core" ? n.core.name + " · " + Math.round(Math.abs(Number(body[n.core.key]) || 0) * 100) + "%" : shortLine(n);
        tip.hidden = false;
        tip.style.left = Math.min(W - tip.offsetWidth - 8, px + 14) + "px"; tip.style.top = (py + 14) + "px";
      } else tip.hidden = true;
    });
    canvas.addEventListener("pointerup", (ev) => {
      canvas.classList.remove("drag");
      if (drag && !drag.moved) {
        const r = canvas.getBoundingClientRect();
        const h = pick(ev.clientX - r.left, ev.clientY - r.top);
        if (h >= 0) select(h, false); else if (sel >= 0) select(-1);
      }
      drag = null;
    });
    canvas.addEventListener("pointerleave", () => { hover = -1; $("tip").hidden = true; });
    canvas.addEventListener("wheel", (ev) => {
      ev.preventDefault();
      const r = canvas.getBoundingClientRect(), px = ev.clientX - r.left, py = ev.clientY - r.top;
      const k = Math.max(0.12, Math.min(8, view.k * Math.exp(-ev.deltaY * 0.0015)));
      view.tx = px - (px - view.tx) * k / view.k; view.ty = py - (py - view.ty) * k / view.k; view.k = k;
      staticDirty = true;
    }, { passive: false });
    canvas.addEventListener("dblclick", fit);
  }

  // ---------------------------------------------------------------- start
  async function boot() {
    initTheme();
    motion = storeGet("brain_motion") !== "0" && !(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    if (params.get("motion") === "0") motion = false;
    $("motionBtn").classList.toggle("on", motion);
    resize();
    const g = await loadGraph();
    if (source !== "live") {
      const b = $("sourceBadge");
      b.hidden = false;
      if (source === "sample-embedded") b.textContent = "示例数据（编造）· 接口还没接上";
    }
    build(g);
    buildControls();
    computeShown();
    fit();
    wire();
    renderTurns();
    // For screenshots and links: ?win=w:g2  ?sel=m:0005  ?turn=3  ?q=猫  ?settle=1
    if (params.get("bench") === "1") bench();
    if (params.get("settle") === "1") { while (sim.tick()) { /* lay out fully before the first frame */ } $("loading").style.display = "none"; }
    if (params.get("win")) { filter.win = params.get("win"); $("winSel").value = filter.win; computeFocus(); }
    if (params.get("sel") && byId.has(params.get("sel"))) select(byId.get(params.get("sel")), params.get("settle") === "1");
    if (params.get("turn")) setTurn(Number(params.get("turn")) - 1);
    if (params.get("q")) { $("q").value = params.get("q"); runSearch(); }
    requestAnimationFrame(frame);
  }
  boot();
})();
