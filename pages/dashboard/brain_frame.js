/* ams-life (AGPL-3.0); see NOTICE.md.
 * "她的脑子" inside the panel: the brain map (built into ./brain/ by tools/brain/build.mjs)
 * in a frame of its own, so its WebGL, worker and styles stay apart from the panel's.
 *
 * - The frame is a srcdoc frame made from brain/panel-page.js, and only on the first
 *   visit to this view. A framed page of its own would be refused: AstrBot serves
 *   pages with X-Frame-Options SAMEORIGIN / frame-ancestors 'self', and the panel's
 *   origin inside AstrBot's sandbox is "null", which never matches.
 * - The map asks this panel for its data (tools/brain/src/embed.js) and the panel asks
 *   AstrBot through its own bridge: apiGet only, the three brain routes only, a few
 *   query keys, at most MAX_WAITING at a time. There is no way here to write.
 * - Both origins are "null", so a message is told apart by its window: only what comes
 *   from the frame's window is read, and answers go only to that window, with "*" as
 *   the target origin because a "null" origin cannot be named.
 * - Leaving the view tells the map to stop drawing; coming back, to go on.
 * - "全屏" asks the browser for full screen; inside AstrBot that is not allowed (its
 *   frame has no allowfullscreen), so the button says "铺满" and fills the panel instead.
 *
 * Loaded in the browser (window.BioBrainFrame) and by the tests through node's
 * require(), so the request rules can be checked without a browser.
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.BioBrainFrame = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  const CHANNEL = "ams-brain";
  const ROUTES = ["page/brain", "page/brain/node", "page/brain/search"];
  const KEYS = ["part", "snap", "id", "reveal", "q"];
  const MAX_VALUE = 200;     // characters of one query value
  const MAX_WAITING = 8;     // reads waiting for AstrBot at one time

  /** What may be passed on of one request from the map: {id, route, query}, or
   * {id, error} for one that may not, or null for one without a usable id. */
  function cleanRequest(m) {
    const id = Number(m && m.id);
    if (!Number.isInteger(id) || id <= 0) return null;
    const route = String(m.route || "");
    if (ROUTES.indexOf(route) < 0) return { id, error: "只能读她的脑子" };
    const q = m.query && typeof m.query === "object" ? m.query : {};
    const query = {};
    for (const k of KEYS) {
      if (Object.prototype.hasOwnProperty.call(q, k) && q[k] !== undefined && q[k] !== null) {
        query[k] = String(q[k]).slice(0, MAX_VALUE);
      }
    }
    return { id, route, query };
  }

  /** The browser part. opts.bridge(): the panel's AstrBot bridge or null (a static
   * preview); opts.dark(): whether the panel is dark now. */
  function attach(opts) {
    const doc = document;
    const box = doc.getElementById("brainBox");
    const btn = doc.getElementById("brainFill");
    if (!box || !btn) return null;
    let frame = null, shown = false, waiting = 0, filled = false;
    const realFull = !!(doc.fullscreenEnabled && box.requestFullscreen);
    const label = () => {
      const on = filled || doc.fullscreenElement === box;
      btn.textContent = on ? (realFull ? "退出全屏" : "退出铺满") : (realFull ? "全屏" : "铺满");
      btn.title = realFull ? "全屏看（Esc 退出）" : "盖满整个面板（Esc 退出）；在 AstrBot 里不能真的全屏";
    };
    const tell = (msg) => {   // only to the map's own window; "*": its origin is "null"
      if (frame && frame.contentWindow) frame.contentWindow.postMessage(Object.assign({ channel: CHANNEL }, msg), "*");
    };
    const answer = (id, ok, payload) => tell(ok ? { kind: "answer", id, ok: true, data: payload }
                                                : { kind: "answer", id, ok: false, error: String(payload || "没取到") });

    function relay(m) {
      const req = cleanRequest(m);
      if (!req) return;
      if (req.error) return answer(req.id, false, req.error);
      if (waiting >= MAX_WAITING) return answer(req.id, false, "同时请求太多，稍后再试");
      const b = opts.bridge && opts.bridge();
      if (!b || typeof b.apiGet !== "function") return answer(req.id, false, "没有 AstrBot 的页面桥（预览）");
      waiting += 1;
      Promise.resolve()
        .then(() => b.apiGet(req.route, req.query))
        .then((data) => answer(req.id, true, data), (e) => answer(req.id, false, (e && e.message) || e))
        .then(() => { waiting -= 1; });
    }

    window.addEventListener("message", (ev) => {
      if (!frame || ev.source !== frame.contentWindow) return;
      const m = ev.data;
      if (!m || m.channel !== CHANNEL) return;
      if (m.kind === "hello") tell({ kind: "hello", isDark: !!(opts.dark && opts.dark()) });
      else if (m.kind === "get") relay(m);
      else if (m.kind === "exit-fill") setFill(false);
    });

    function setFill(on) {
      if (!on && doc.fullscreenElement === box && doc.exitFullscreen) doc.exitFullscreen().catch(() => {});
      filled = !!on && !realFull;
      doc.body.classList.toggle("brain-filled", filled);
      label();
    }
    btn.addEventListener("click", () => {
      if (filled || doc.fullscreenElement === box) return setFill(false);
      if (realFull) box.requestFullscreen().catch(() => { filled = true; doc.body.classList.add("brain-filled"); label(); });
      else setFill(true);
    });
    doc.addEventListener("fullscreenchange", label);
    doc.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && filled) setFill(false); });
    // the panel's light / dark follows on to the map
    new MutationObserver(() => tell({ kind: "theme", dark: !!(opts.dark && opts.dark()) }))
      .observe(doc.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

    function load() {
      frame = doc.createElement("iframe");
      frame.className = "brain-frame";
      frame.title = "她的脑子";
      frame.setAttribute("allowfullscreen", "");
      frame.srcdoc = String(window.BioBrainPage || "<p>她的脑子没有打包进来（tools/brain/build.mjs）</p>");
      box.appendChild(frame);
    }
    label();
    return {
      /** The panel switched to view `name`. */
      onView(name) {
        const on = name === "brain";
        doc.body.classList.toggle("brain-view", on);
        if (on && !frame) load();   // the first visit loads it
        else if (on !== shown) tell({ kind: "run", on });
        if (!on && filled) setFill(false);
        shown = on;
      },
    };
  }

  return { CHANNEL, ROUTES, KEYS, MAX_VALUE, MAX_WAITING, cleanRequest, attach };
});
