/* The shell's side of the bridge, as AstrBot's PluginViewPage does it: only messages from
 * its own iframe, "api:get" answered, anything else refused. The brain routes answer with
 * the brain map's invented sample (BrainSample, sample.js) as if it came from the plugin;
 * everything else (the panel's own status...) gets an error. window.__hostLog keeps what
 * was asked, for the checks. */
(function () {
  "use strict";
  const CHANNEL = "astrbot-plugin-page";
  const frame = document.getElementById("view");
  const made = window.BrainSample.make({ n: 400 });
  const graph = Object.assign({}, made.graph, { sample: false, part: 0, parts: 1, snap: "shell-1" });
  const log = window.__hostLog = { gets: [], posts: [], other: [] };

  function answer(endpoint, params) {
    params = params || {};
    if (endpoint === "page/brain") return graph;
    if (endpoint === "page/brain/node") {
      const d = made.details[params.id];
      if (!d) throw new Error("没有这颗星");
      if (params.reveal === "qq") return { qq: d.qq || "" };
      const out = Object.assign({}, d);
      delete out.qq;
      if (d.qq) out.has_qq = true;
      return out;
    }
    if (endpoint === "page/brain/search") {
      const q = String(params.q || "");
      return { ids: Object.keys(made.details).filter((id) => (made.details[id].title + (made.details[id].text || "")).includes(q)) };
    }
    throw new Error("外壳里没有这个接口：" + endpoint);
  }
  const reply = (m) => frame.contentWindow.postMessage(Object.assign({ channel: CHANNEL }, m), "*");
  window.addEventListener("message", (ev) => {
    if (ev.source !== frame.contentWindow) return;
    const m = ev.data;
    if (!m || m.channel !== CHANNEL) return;
    if (m.kind === "ready") return reply({ kind: "context", context: { isDark: true, locale: "zh-CN", pageName: "dashboard" } });
    if (m.kind !== "request") return;
    if (m.action === "api:get") {
      log.gets.push({ endpoint: m.endpoint, params: m.params || {} });
      try { reply({ kind: "response", requestId: m.requestId, ok: true, data: answer(m.endpoint, m.params) }); }
      catch (e) { reply({ kind: "response", requestId: m.requestId, ok: false, error: e.message }); }
      return;
    }
    (m.action === "api:post" ? log.posts : log.other).push({ action: m.action, endpoint: m.endpoint });
    reply({ kind: "response", requestId: m.requestId, ok: false, error: "外壳只读" });
  });
})();
