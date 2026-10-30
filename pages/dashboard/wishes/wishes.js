(function () {
  "use strict";
  const $ = id => document.getElementById(id);
  const params = new URLSearchParams(location.search);
  let bridge = null;
  function theme(dark) { document.documentElement.dataset.theme = dark ? "dark" : "light"; }
  function findBridge() {
    try { return window.AstrBotPluginView || window.AstrBotPluginPage || window.astrbotPluginView ||
      (window.parent !== window && (window.parent.AstrBotPluginView || window.parent.AstrBotPluginPage)) || null; }
    catch (_) { return null; }
  }
  async function load() {
    try {
      const result = await bridge.apiGet("page/wishes", {});
      if (result.status === "error") throw new Error(result.message);
      const data = result.data || result;
      $("list").replaceChildren();
      if (!data.on) { $("state").textContent = "没开"; return; }
      const rows = data.items || [];
      $("state").textContent = rows.length ? "共 " + rows.length + " 条" : "还没有愿望。";
      for (const row of rows) {
        const card = document.createElement("article"); card.className = "wish";
        const title = document.createElement("h2"); title.textContent = "#" + row.id + " " + row.what;
        const why = document.createElement("p"); why.textContent = row.why || "没有填写原因";
        const meta = document.createElement("p"); meta.className = "meta";
        meta.textContent = String(row.time || "").replace("T", " ").slice(0, 16) + " · " + row.status;
        const actions = document.createElement("div"); actions.className = "actions";
        for (const status of ["好", "先放着", "不要"]) {
          const button = document.createElement("button"); button.className = "btn"; button.type = "button";
          button.textContent = status; button.setAttribute("aria-pressed", String(row.status === status));
          button.addEventListener("click", async () => {
            button.disabled = true;
            try {
              const changed = await bridge.apiPost("page/wishes/status", {id: row.id, status});
              if (changed.status === "error") throw new Error(changed.message);
              await load();
            } catch (_) { $("state").textContent = "状态没有改成，请再试一次。"; button.disabled = false; }
          });
          actions.append(button);
        }
        card.append(title, why, meta, actions); $("list").append(card);
      }
    } catch (_) { $("state").textContent = "愿望单暂时读不了。"; }
  }
  async function start() {
    theme(params.get("theme") === "dark");
    $("theme").addEventListener("click", () => theme(document.documentElement.dataset.theme !== "dark"));
    $("back").addEventListener("click", () => {
      const back = /^[a-z]{1,20}$/.test(params.get("back") || "") ? params.get("back") : "overview";
      $("back").href = "../?view=" + back + "&theme=" + document.documentElement.dataset.theme;
    });
    bridge = findBridge();
    if (!bridge) { $("state").textContent = "请从面板打开。"; return; }
    try { await Promise.race([bridge.ready(), new Promise(resolve => setTimeout(resolve, 3000))]); } catch (_) {}
    await load();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
