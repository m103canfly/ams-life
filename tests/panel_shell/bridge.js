/* A small stand-in for AstrBot's plugin page bridge (dashboard/plugin_page_bridge.js in
 * AstrBot 4.29.3), added to every page serve.py hands out, as AstrBot adds its own.
 * Same messages: {channel: "astrbot-plugin-page", kind: "ready" | "request" | ...} to
 * window.parent, answers read only from window.parent. Invented data only (host.js). */
(function () {
  "use strict";
  const CHANNEL = "astrbot-plugin-page";
  const pending = new Map();
  let n = 0, context = null, readyResolve;
  const ready = new Promise((r) => { readyResolve = r; });
  const send = (kind, payload) => window.parent.postMessage(Object.assign({ channel: CHANNEL, kind }, payload || {}), "*");
  window.addEventListener("message", (ev) => {
    if (ev.source !== window.parent) return;
    const m = ev.data;
    if (!m || m.channel !== CHANNEL) return;
    if (m.kind === "context") { context = m.context; if (readyResolve) { readyResolve(context); readyResolve = null; } }
    if (m.kind === "response" && pending.has(m.requestId)) {
      const p = pending.get(m.requestId);
      pending.delete(m.requestId);
      if (m.ok) p.ok(m.data); else p.no(new Error(m.error || "request failed"));
    }
  });
  const request = (action, payload) => new Promise((ok, no) => {
    const requestId = "shell_req_" + (++n);
    pending.set(requestId, { ok, no });
    send("request", Object.assign({ requestId, action }, payload));
  });
  window.AstrBotPluginView = window.AstrBotPluginPage = {
    ready: () => ready,
    getContext: () => context,
    apiGet: (endpoint, params) => request("api:get", { endpoint, params }),
    apiPost: (endpoint, body) => request("api:post", { endpoint, body }),
  };
  send("ready");
})();
