/* ams-life (AGPL-3.0); see NOTICE.md.
 * "小黑盒" in 钥匙 (card 1d, panel half): the owner signs her 小黑盒 account in by scanning a code.
 * Only page/heybox/status, page/heybox/login and page/heybox/logout (all POST, through the bridge
 * with the page's token). The plugin keeps the sign-in itself; this block only says which state
 * it is in, and never shows anything of it.
 *
 * The code is drawn here, by qrcodegen.js (Nayuki's QR Code generator, MIT, next to this file),
 * as an SVG made of squares. qr_url goes only into that encoder: it is never put on the page as
 * text, never in an attribute, never on the console, never sent anywhere (no image, no address).
 * While a code is shown, status is asked every 3 seconds until it is not "waiting" or the code's
 * time is up; leaving 设置 or 钥匙 stops it (取消 does too, on this side only).
 *
 * The routes are only on our own panel server (ams-bridge.js, `standalone`); inside AstrBot this
 * block stays hidden. Without a bridge (a static preview) it shows an invented code, saying so,
 * and sends nothing.
 *
 * Loaded in the browser (window.BioHeybox) and by the tests through node's require().
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.BioHeybox = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  const STATUS = "page/heybox/status";
  const LOGIN = "page/heybox/login";
  const LOGOUT = "page/heybox/logout";
  const POLL_MS = 3000;
  const SAMPLE_BADGE = "示例（编造）：没有连上她，下面是编出来的样子，点了也不发。";
  const SAMPLE_CODE = "ams-life 示例：这不是登录用的二维码";
  const SCAN = "用她那个号的小黑盒 App 扫一下";
  const LOGOUT_ASK = "退出小黑盒登录吗？\n退出以后她就刷不了小黑盒，要重新扫码。";
  // state → what it says, and its one button
  const STATES = {
    idle: ["没登录", "login"],
    waiting: ["等扫码", "cancel"],
    logged_in: ["已登录", "logout"],
    relogin: ["要重新扫码", "login"],
    captcha: ["小黑盒要人工验证，先停了；退出登录以后可以重新扫码", "logout"],
    review_required: ["第一次真跑没成功，先停了，等审核看", "logout"],
    failed: ["没拿到二维码", "retry"],
    expired: ["二维码过期了", "retry"],
  };
  const BUTTONS = { login: "登录", logout: "退出登录", cancel: "取消", retry: "再试" };

  /** The plugin's answer through one or two wrappers: the object that has `state`. */
  function unwrap(raw) {
    let o = raw;
    for (let i = 0; i < 4 && o && typeof o === "object"; i++) {
      if (o.status === "error") throw new Error(o.message || "没有回音");
      if (typeof o.state === "string") return o;
      o = o.data;
    }
    return {};
  }

  /** "（HTTP 403）" or "（连不上）": only the status of an error, nothing else of it. */
  function failText(what, err) {
    const m = /HTTP (\d{3})/.exec(String((err && err.message) || ""));
    return what + "（" + (m ? "HTTP " + m[1] : "连不上") + "）";
  }

  /** The code for `text` as an SVG of dark squares on white, drawn here. Throws when it cannot. */
  function qrSvg(text, qrcodegen) {
    const qr = qrcodegen.QrCode.encodeText(String(text), qrcodegen.QrCode.Ecc.MEDIUM);
    const border = 4, n = qr.size + border * 2;
    let d = "";
    for (let y = 0; y < qr.size; y++) {
      for (let x = 0; x < qr.size; x++) if (qr.getModule(x, y)) d += "M" + (x + border) + "," + (y + border) + "h1v1h-1z";
    }
    return '<svg class="hb-code" viewBox="0 0 ' + n + " " + n + '" role="img" aria-label="小黑盒登录二维码" shape-rendering="crispEdges">' +
      '<rect width="' + n + '" height="' + n + '" fill="#fff"/><path d="' + d + '" fill="#000"/></svg>';
  }

  /** The browser part. opts.bridge(): the panel's bridge or null; opts.qrcodegen: the encoder. */
  function attach(opts) {
    const doc = document;
    const $ = (id) => doc.getElementById(id);
    const box = $("heyboxBox");
    if (!box) return null;
    const pollMs = (opts && opts.pollMs) || POLL_MS;
    const tickMs = (opts && opts.tickMs) || 1000;
    const encoder = () => (opts && opts.qrcodegen) || (typeof window !== "undefined" && window.qrcodegen) || null;
    const el = (cls) => box.querySelector("." + cls);
    let mode = null, gen = 0, poll = null, tick = null, deadline = 0, pending = false, keysShown = false;
    const KEYS_PARTS = ["settingsKeysTab", "settingsKeysTitle", "settingsKeys"];

    /** "live" on our own server, "sample" with no bridge at all, "off" inside AstrBot. */
    function modeNow() {
      const b = opts && opts.bridge && opts.bridge();
      return b ? (b.standalone ? "live" : "off") : "sample";
    }
    const bridge = () => opts.bridge();

    function stop() {
      gen++;
      clearTimeout(poll); clearInterval(tick);
      poll = tick = null;
    }

    function say(text) { el("hb-msg").textContent = text || ""; }

    function show(state, extra) {
      const known = STATES[state] || ["说不清现在是什么状态", "login"];
      el("hb-state").textContent = extra && extra.text || known[0];
      el("hb-state").classList.toggle("on", state === "logged_in");
      const qr = el("hb-qr");
      if (!(extra && extra.svg)) { qr.innerHTML = ""; qr.hidden = true; el("hb-tip").textContent = ""; }
      const action = extra && extra.action || known[1];
      el("hb-actions").innerHTML = '<button type="button" class="btn mini fb-skip' + (action === "logout" ? " danger" : " primary") +
        '" data-hb="' + action + '">' + BUTTONS[action] + "</button>";
      box.dataset.state = state;
    }

    function left() {
      const s = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      el("hb-tip").textContent = SCAN + "（还剩 " + s + " 秒）";
      return s;
    }

    /** One code on the page: draw it, count down, ask status every few seconds. */
    function waitFor(url, expire) {
      const q = encoder();
      let svg;
      try { svg = qrSvg(url, q); } catch (e) { show("failed", { text: q ? "二维码画不出来" : "画二维码的文件没载上" }); return; }
      url = null;                                        // only the drawing is kept
      const qr = el("hb-qr");
      qr.innerHTML = svg; qr.hidden = false;
      show("waiting", { svg: true });
      deadline = Date.now() + Math.max(1, Math.min(Number(expire) || 120, 180)) * 1000;
      left();
      const mine = gen;
      tick = setInterval(() => {
        if (mine !== gen) return;
        if (left() <= 0) { stop(); show("expired"); }
      }, tickMs);
      const ask = async () => {
        if (mine !== gen) return;
        let state;
        try { state = unwrap(await bridge().apiPost(STATUS, {})).state; } catch (e) { if (mine === gen) say(failText("问不到扫好没有", e)); }
        if (mine !== gen) return;
        if (state && state !== "waiting") { stop(); say(""); show(state); return; }
        poll = setTimeout(ask, pollMs);
      };
      poll = setTimeout(ask, pollMs);
    }

    async function refresh() {
      stop();
      if (mode !== "live") return;
      const mine = gen;
      say("");
      try {
        const state = unwrap(await bridge().apiPost(STATUS, {})).state || "idle";
        if (mine !== gen) return;
        // a code from before is no longer on this side: ask for a new one to scan
        if (state === "waiting") show("waiting", { text: "在等扫码，这边的二维码已经收起来了", action: "retry" });
        else show(state);
      } catch (e) {
        if (mine === gen) { show("idle", { text: "…" }); say(failText("读不到登录没有", e)); }
      }
    }

    function sample() {
      el("hb-badge").hidden = false;
      el("hb-badge").textContent = SAMPLE_BADGE;
      try {
        const qr = el("hb-qr");
        qr.innerHTML = qrSvg(SAMPLE_CODE, encoder()); qr.hidden = false;
        show("waiting", { svg: true });
        el("hb-tip").textContent = SCAN + "（示例，不走秒）";
      } catch (e) { show("idle"); }
    }

    async function login() {
      stop();
      const mine = gen;
      pending = true;
      say("正在要二维码…");
      try {
        const a = unwrap(await bridge().apiPost(LOGIN, {}));
        if (mine !== gen) return;
        say("");
        if (a.state === "waiting" && typeof a.qr_url === "string" && a.qr_url) waitFor(a.qr_url, a.expire);
        else show(STATES[a.state] && a.state !== "waiting" ? a.state : "failed");
      } catch (e) {
        if (mine === gen) { show("failed"); say(failText("没要到二维码", e)); }
      } finally {
        pending = false;
      }
    }

    async function logout() {
      if (!window.confirm(LOGOUT_ASK)) return;
      stop();
      const mine = gen;
      say("正在退出…");
      try {
        const a = unwrap(await bridge().apiPost(LOGOUT, {}));
        if (mine !== gen) return;
        say("退出了");
        show(a.state || "idle");
      } catch (e) {
        if (mine === gen) say(failText("没退出", e));
      }
    }

    /** 设置 or 钥匙 opened: which mode it is now, and the state asked once when live. The mode is
     *  worked out again each time: a panel opened straight on 设置 (?view=settings) gets there before
     *  app.js has its bridge, and must not stay on the invented code once the bridge is there. */
    function enter() {
      const now = modeNow();
      if (now !== mode) {
        const was = mode;
        mode = now;
        if (mode === "off") {
          stop(); box.hidden = true;
          if (keysShown) { KEYS_PARTS.forEach((id) => { if ($(id)) $(id).hidden = true; }); keysShown = false; }
          return;
        }
        box.hidden = false;
        if (mode === "sample") {
          // a static preview has no 钥匙 tab of its own (keys.js needs our server): show it for this block
          KEYS_PARTS.forEach((id) => { if ($(id)) $(id).hidden = false; });
          keysShown = true;
          sample();
          return;
        }
        if (was === "sample") { el("hb-badge").hidden = true; el("hb-badge").textContent = ""; }
      }
      if (mode === "live" && !poll && !tick) refresh();
    }

    box.addEventListener("click", (ev) => {
      const btn = ev.target && ev.target.closest ? ev.target.closest("[data-hb]") : null;
      if (!btn) return;
      if (mode === "sample") { say("示例里不发"); return; }
      if (mode !== "live" || pending) return;
      const what = btn.dataset.hb;
      if (what === "login" || what === "retry") login();
      else if (what === "logout") logout();
      else if (what === "cancel") { stop(); show("idle", { text: "取消了：这边不再等扫码", action: "login" }); }
    });
    // another tab of 设置: the code is put away
    const tabs = $("settingsTabs");
    if (tabs) tabs.addEventListener("click", (ev) => {
      const tab = ev.target && ev.target.closest ? ev.target.closest(".settings-tab") : null;
      if (!tab) return;
      if (tab.dataset.settingsTarget === "settingsKeys") { if (!poll && !tick) enter(); }
      else if (poll || tick) { stop(); show("idle", { text: "离开了这一页，这边不再等扫码", action: "login" }); }
    });

    return {
      /** The panel switched to view `name`: settings shows this block (and asks once); any other stops the asking. */
      onView(name) {
        if (name !== "settings") {
          if (poll || tick) { stop(); show("idle", { text: "离开了这一页，这边不再等扫码", action: "login" }); }
          return;
        }
        enter();
      },
      stop,
    };
  }

  return { STATUS, LOGIN, LOGOUT, POLL_MS, STATES, BUTTONS, SAMPLE_BADGE, SCAN, LOGOUT_ASK, unwrap, failText, qrSvg, attach };
});
