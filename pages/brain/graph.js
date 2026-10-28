// ams-life (AGPL-3.0); see NOTICE.md.
// Layout for the brain map: a small force simulation written for this page
// (no third-party library). Repulsion uses a Barnes-Hut quadtree, so a tick is
// O(n log n) and a few thousand points stay smooth.
//
// The picture is a brain seen from above: what she saw in groups (public)
// settles in the left half, what she heard in private chats in the right half,
// people sit wherever their places pull them (often near the middle), and the
// body nuclei are fixed in the middle.
(function (root) {
  "use strict";

  // Brain outline (world units). Each half is its own ellipse.
  const BRAIN = { a: 1000, b: 640, lobeX: 520, lobeA: 450, lobeB: 600 };

  function Sim(nodes, links) {
    this.nodes = nodes;   // {x, y, vx, vy, mass, side (-1 left, 1 right, 0 any), anchor?:{x,y,k}, fixed?}
    this.links = links;   // {a, b (node indexes), len, k}
    this.alpha = 1;
    this.alphaMin = 0.004;
    this.decay = 0.018;
    this.theta2 = 0.81;   // Barnes-Hut opening angle squared (theta 0.9)
    this.charge = -60;
    // Repulsion only reaches this far (squared), so a crowd does not press
    // everything against the outline.
    this.distMax2 = 300 * 300;
  }

  // Quadtree in flat arrays: cell i has 4 children at kids[4i..4i+3] (-1 = none).
  function buildTree(nodes) {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const n of nodes) { if (n.x < x0) x0 = n.x; if (n.x > x1) x1 = n.x; if (n.y < y0) y0 = n.y; if (n.y > y1) y1 = n.y; }
    const size = Math.max(x1 - x0, y1 - y0, 1) + 1;
    const cap = nodes.length * 4 + 16;
    const t = {
      cx: new Float64Array(cap), cy: new Float64Array(cap), m: new Float64Array(cap),
      size: new Float64Array(cap), ox: new Float64Array(cap), oy: new Float64Array(cap),
      kids: new Int32Array(cap * 4).fill(-1), leaf: new Int32Array(cap).fill(-1), count: 1,
    };
    t.size[0] = size; t.ox[0] = x0; t.oy[0] = y0;
    const insert = (cell, idx, depth) => {
      for (;;) {
        const n = nodes[idx];
        t.cx[cell] += n.x * n.mass; t.cy[cell] += n.y * n.mass; t.m[cell] += n.mass;
        const kid0 = cell * 4;
        const isLeafEmpty = t.leaf[cell] === -1 && t.kids[kid0] === -1 && t.kids[kid0 + 1] === -1 && t.kids[kid0 + 2] === -1 && t.kids[kid0 + 3] === -1;
        if (isLeafEmpty && t.m[cell] === n.mass) { t.leaf[cell] = idx; return; }
        if (depth > 40 || t.count + 4 >= cap) return;   // coincident points: just add mass
        const half = t.size[cell] / 2;
        if (t.leaf[cell] !== -1) {   // push the resident point down one level
          const old = t.leaf[cell]; t.leaf[cell] = -1;
          const o = nodes[old];
          const q = (o.x >= t.ox[cell] + half ? 1 : 0) + (o.y >= t.oy[cell] + half ? 2 : 0);
          const c = t.count++; t.kids[kid0 + q] = c;
          t.size[c] = half; t.ox[c] = t.ox[cell] + (q & 1 ? half : 0); t.oy[c] = t.oy[cell] + (q & 2 ? half : 0);
          t.cx[c] = o.x * o.mass; t.cy[c] = o.y * o.mass; t.m[c] = o.mass; t.leaf[c] = old;
        }
        const q = (n.x >= t.ox[cell] + half ? 1 : 0) + (n.y >= t.oy[cell] + half ? 2 : 0);
        let c = t.kids[kid0 + q];
        if (c === -1) {
          c = t.count++; t.kids[kid0 + q] = c;
          t.size[c] = half; t.ox[c] = t.ox[cell] + (q & 1 ? half : 0); t.oy[c] = t.oy[cell] + (q & 2 ? half : 0);
          t.cx[c] = n.x * n.mass; t.cy[c] = n.y * n.mass; t.m[c] = n.mass; t.leaf[c] = idx;
          return;
        }
        cell = c; depth++;
      }
    };
    for (let i = 0; i < nodes.length; i++) insert(0, i, 0);
    for (let c = 0; c < t.count; c++) if (t.m[c] > 0) { t.cx[c] /= t.m[c]; t.cy[c] /= t.m[c]; }
    return t;
  }

  Sim.prototype.repel = function (alpha) {
    const nodes = this.nodes, t = buildTree(nodes), th2 = this.theta2, k = this.charge * alpha, dmax2 = this.distMax2;
    const stack = new Int32Array(t.count + 8);
    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i];
      let sp = 0; stack[sp++] = 0;
      let fx = 0, fy = 0;
      while (sp) {
        const c = stack[--sp];
        if (t.m[c] === 0) continue;
        const dx = t.cx[c] - n.x, dy = t.cy[c] - n.y;
        let d2 = dx * dx + dy * dy;
        const leaf = t.leaf[c];
        const kid0 = c * 4;
        const hasKids = t.kids[kid0] !== -1 || t.kids[kid0 + 1] !== -1 || t.kids[kid0 + 2] !== -1 || t.kids[kid0 + 3] !== -1;
        if (!hasKids || (t.size[c] * t.size[c]) / (d2 || 1e-9) < th2) {
          if (leaf === i && !hasKids) continue;
          if (d2 > dmax2) continue;
          if (d2 < 1) d2 = 1;
          const m = leaf === i ? t.m[c] - n.mass : t.m[c];
          const f = k * m / d2;
          fx += dx * f; fy += dy * f;
        } else {
          for (let q = 0; q < 4; q++) { const kc = t.kids[kid0 + q]; if (kc !== -1) stack[sp++] = kc; }
        }
      }
      n.vx += fx; n.vy += fy;
    }
  };

  Sim.prototype.springs = function (alpha) {
    const nodes = this.nodes;
    for (const l of this.links) {
      const a = nodes[l.a], b = nodes[l.b];
      let dx = b.x + b.vx - a.x - a.vx, dy = b.y + b.vy - a.y - a.vy;
      const d = Math.sqrt(dx * dx + dy * dy) || 1;
      const f = (d - l.len) / d * alpha * l.k;
      dx *= f; dy *= f;
      const wa = b.mass / (a.mass + b.mass);
      b.vx -= dx * (1 - wa); b.vy -= dy * (1 - wa);
      a.vx += dx * wa; a.vy += dy * wa;
    }
  };

  Sim.prototype.shape = function (alpha) {
    for (const n of this.nodes) {
      if (n.anchor) {
        n.vx += (n.anchor.x - n.x) * n.anchor.k * alpha;
        n.vy += (n.anchor.y - n.y) * n.anchor.k * alpha;
      }
      // Keep each point inside its half (or inside the whole brain).
      // People (side 0) may sit in either half: the nearer one holds them.
      let side = n.side;
      if (!side && !n.fixed) {
        const e = (sd) => { const ex = (n.x - sd * BRAIN.lobeX) / BRAIN.lobeA, ey = n.y / BRAIN.lobeB; return ex * ex + ey * ey; };
        const l = e(-1), r = e(1);
        if (l > 1 && r > 1) side = l < r ? -1 : 1;
      }
      if (side) {
        const cx = side * BRAIN.lobeX;
        const ex = (n.x - cx) / BRAIN.lobeA, ey = n.y / BRAIN.lobeB, e = ex * ex + ey * ey;
        if (e > 1) {
          const s = 1 / Math.sqrt(e);
          n.vx += ((cx + (n.x - cx) * s) - n.x) * 0.12;
          n.vy += (n.y * s - n.y) * 0.12;
        }
      }
      // Pull things off the middle seam a little, so the two halves read.
      if (n.side && Math.abs(n.x) < 40) n.vx += n.side * 2 * alpha;
    }
  };

  Sim.prototype.tick = function () {
    if (this.alpha < this.alphaMin) return false;
    const a = this.alpha;
    this.repel(a);
    this.springs(a);
    this.shape(a);
    for (const n of this.nodes) {
      if (n.fixed) { n.vx = n.vy = 0; continue; }
      n.vx *= 0.55; n.vy *= 0.55;
      const sp = n.vx * n.vx + n.vy * n.vy;
      if (sp > 1600) { const s = 40 / Math.sqrt(sp); n.vx *= s; n.vy *= s; }
      n.x += n.vx; n.y += n.vy;
    }
    this.alpha += (0 - this.alpha) * this.decay;
    return true;
  };

  Sim.prototype.reheat = function (to) { this.alpha = Math.max(this.alpha, to || 0.3); };

  root.BrainGraph = { Sim, BRAIN, buildTree };
})(typeof window !== "undefined" ? window : globalThis);
