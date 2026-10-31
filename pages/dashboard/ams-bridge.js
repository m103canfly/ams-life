/* ams-life (AGPL-3.0); see NOTICE.md. The page's way to the plugin without AstrBot (the move, card 4c web).
   Our own panel server (panel_server.py) puts <meta name="ams-token"> into every page it serves and answers
   /api/page/... itself. Only on such a page, and only when there is no AstrBot bridge, this defines
   window.AstrBotPluginPage with the same ready / apiGet / apiPost, so the page's own scripts stay as they are.
   Inside AstrBot no page has that line: nothing is done here and AstrBot's bridge is used, as before.
   The same file is in each page folder that needs it (dashboard/, dashboard/stickers/, stickers/), because AstrBot
   serves a page only from its own folder. The token is read from the page and sent only with writes
   (X-AMS-Token); it is not kept anywhere and not printed. */
(function () {
  "use strict";
  const NAMES = ["AstrBotPluginView", "AstrBotPluginPage", "astrbotPluginView"];
  function hasBridge(w) {
    try { return NAMES.some((n) => !!w[n]); } catch (e) { return false; }
  }
  const meta = document.querySelector('meta[name="ams-token"]');
  if (!meta || hasBridge(window) || (window.parent !== window && hasBridge(window.parent))) return;
  const token = String(meta.getAttribute("content") || "");

  function query(params) {
    const q = new URLSearchParams();
    if (params && typeof params === "object") {
      Object.keys(params).forEach((k) => {
        if (params[k] !== undefined && params[k] !== null) q.append(k, String(params[k]));
      });
    }
    const s = q.toString();
    return s ? "?" + s : "";
  }
  async function answer(resp) {
    if (!resp.ok) throw new Error("HTTP " + resp.status);   // only the status: no body, no token
    return resp.json();
  }

  window.AstrBotPluginPage = {
    standalone: true,
    ready: () => Promise.resolve({}),
    apiGet: (path, params) => fetch("/api/" + path + query(params)).then(answer),
    apiPost: (path, body) => fetch("/api/" + path, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-AMS-Token": token },
      body: JSON.stringify(body || {}),
    }).then(answer),
  };
})();
