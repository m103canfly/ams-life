/* ams-life (AGPL-3.0); see NOTICE.md.
 * "钥匙" in 设置 (move 5e-6): after the move the owner fills in her keys here, on our own panel
 * server (panel_server.py /api/keys, kept in key_store.py's encrypted file), never through Claude.
 * The tab shows only with our own server's bridge (ams-bridge.js, `standalone`). Inside AstrBot
 * the keys are still filled in AstrBot's own back end, so the tab stays hidden.
 *
 * GET /api/keys says only whether each key is there, never the key. A key typed here goes once,
 * in the body of one POST /api/keys (the bridge's apiPost, with the page's token), and the box is
 * emptied as soon as it is saved. "清掉" asks first, then sends DELETE /api/keys/<name> with the
 * token read from the page's meta line for that one request. A key is never kept anywhere else:
 * not in localStorage, not on the console, not in an address, not in any other request. An error
 * says only the HTTP status. The boxes are never taken out of the page, so a browser does not
 * take a save as a sign-in and offer to keep the "password".
 *
 * Loaded in the browser (window.BioKeys) and by the tests through node's require().
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.BioKeys = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  const PATH = "keys";              // the bridge adds /api/
  const NAMES = [["deepseek", "聊天模型"], ["vision", "看图"], ["napcat", "NapCat 口令"]];
  const DAMAGED = "钥匙文件读不了，请重新填";

  /** "<what>（HTTP 403）", or "（连不上）" when no answer came. Nothing else of the error is shown. */
  function failText(what, err) {
    const m = /HTTP (\d{3})/.exec(String((err && err.message) || ""));
    return what + "（" + (m ? "HTTP " + m[1] : "连不上") + "）";
  }

  /** One row per known key: filled true/false, or null when this server does not take it. */
  function rows(answer) {
    const keys = (answer && typeof answer.keys === "object" && answer.keys) || {};
    return NAMES.map(([name, label]) => ({ name, label,
      filled: Object.prototype.hasOwnProperty.call(keys, name) ? !!keys[name] : null }));
  }

  /** Our own server's bridge, or null (inside AstrBot, or no bridge at all). */
  function ownBridge() {
    try {
      const b = window.AstrBotPluginPage;
      return b && b.standalone ? b : null;
    } catch (e) { return null; }
  }

  async function clearKey(name) {
    const meta = document.querySelector('meta[name="ams-token"]');
    const resp = await fetch("/api/keys/" + encodeURIComponent(name), { method: "DELETE",
      headers: { "X-AMS-Token": meta ? String(meta.getAttribute("content") || "") : "" } });
    if (!resp.ok) throw new Error("HTTP " + resp.status);
  }

  function rowHtml(name, label) {
    return '<div class="setting-row key-row" data-key-name="' + name + '">' +
      '<div><b>' + label + '</b><small>' + name + ' · <span class="key-state">…</span></small></div>' +
      '<div class="key-edit">' +
      '<input type="password" autocomplete="off" spellcheck="false" placeholder="填新的 Key" aria-label="' + label + '的 Key">' +
      '<button type="button" class="btn mini primary fb-skip" data-key-save>保存</button>' +
      '<button type="button" class="btn mini danger fb-skip" data-key-clear>清掉</button>' +
      '<span class="key-msg" role="status" aria-live="polite"></span></div></div>';
  }

  function attach(opts) {
    const bridge = (opts && opts.bridge) || ownBridge;
    const doc = document;
    const $ = (id) => doc.getElementById(id);
    const tab = $("settingsKeysTab"), title = $("settingsKeysTitle"), panel = $("settingsKeys"), box = $("keysRows");
    if (!tab || !panel || !box || !bridge()) return null;
    tab.hidden = false;
    if (title) title.hidden = false;
    panel.hidden = false;
    $("keysDamaged").textContent = DAMAGED;
    box.innerHTML = NAMES.map(([name, label]) => rowHtml(name, label)).join("");
    const rowOf = (name) => box.querySelector('[data-key-name="' + name + '"]');
    const say = (row, text) => { row.querySelector(".key-msg").textContent = text; };
    const busy = (row, on) => row.querySelectorAll("input, button").forEach((el) => {
      el.disabled = on || row.dataset.off === "1";
    });

    async function refresh() {
      const state = $("keysState");
      try {
        const answer = await bridge().apiGet(PATH, {});
        $("keysDamaged").hidden = !(answer && answer.damaged);
        rows(answer).forEach((r) => {
          const row = rowOf(r.name);
          const s = row.querySelector(".key-state");
          s.textContent = r.filled === null ? "这边还不能填" : (r.filled ? "已填" : "没填");
          s.classList.toggle("on", r.filled === true);
          row.dataset.off = r.filled === null ? "1" : "";
          busy(row, false);
        });
        state.textContent = "";
      } catch (e) {
        state.textContent = failText("读不到填没填", e);
      }
    }

    async function save(row) {
      const input = row.querySelector("input");
      const value = input.value.trim();
      if (!value) { say(row, "先填上再保存"); return; }
      busy(row, true);
      say(row, "正在存…");
      try {
        await bridge().apiPost(PATH, { name: row.dataset.keyName, value: value });
        input.value = "";
        say(row, "存上了");
      } catch (e) {
        say(row, failText("没存上", e));
      }
      busy(row, false);
      await refresh();
    }

    async function clear(row) {
      const label = row.querySelector("b").textContent;
      if (!window.confirm("清掉「" + label + "」的 Key 吗？\n清掉以后这一项就用不了，要重新填。")) return;
      busy(row, true);
      say(row, "正在清…");
      try {
        await clearKey(row.dataset.keyName);
        say(row, "清掉了");
      } catch (e) {
        say(row, failText("没清掉", e));
      }
      busy(row, false);
      await refresh();
    }

    box.addEventListener("click", (ev) => {
      const row = ev.target.closest && ev.target.closest(".key-row");
      if (!row) return;
      if (ev.target.closest("[data-key-save]")) save(row);
      else if (ev.target.closest("[data-key-clear]")) clear(row);
    });
    box.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" && ev.target.matches && ev.target.matches("input")) save(ev.target.closest(".key-row"));
    });
    tab.addEventListener("click", refresh);
    refresh();
    return { refresh };
  }

  return { PATH, NAMES, DAMAGED, failText, rows, attach };
});
