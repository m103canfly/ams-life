/* ams-life (AGPL-3.0); see NOTICE.md.
 * Click feedback for the panel (10-29, the owner: "很多点击都没有动效"). A button that starts
 * a call to the plugin (AstrBot's bridge: apiGet / apiPost) shows "正在……" next to it and
 * cannot be pressed again; when the call ends it shows "好了" or "没成功：原因" for a few
 * seconds. Nothing else changes: the same calls, the same answers, the pages' own messages.
 * Calls nobody clicked for (the regular refresh) show nothing.
 */
(function () {
  "use strict";
  const CLICK_MS = 1500;     // a call this soon after a click belongs to that button
  const SHOW_MS = 3200;      // how long "好了" / "没成功" stays
  let last = { el: null, at: 0 };

  document.addEventListener("click", function (e) {
    const el = e.target && e.target.closest && e.target.closest("button, [role=button], summary, .fold-panel");
    if (el) last = { el: el, at: Date.now() };
  }, true);

  function tipOf(btn) {
    let tip = btn.nextElementSibling;
    if (!tip || !tip.classList.contains("fb-tip")) {
      tip = document.createElement("span");
      tip.className = "fb-tip";
      tip.setAttribute("role", "status");
      tip.setAttribute("aria-live", "polite");
      btn.insertAdjacentElement("afterend", tip);
    }
    clearTimeout(tip._fbTimer);
    return tip;
  }

  function failed(res) {
    if (!res || typeof res !== "object") return "";
    if (res.status === "error" || res.ok === false) return String(res.message || res.error || "没有回音");
    return "";
  }

  /** Show the life of one call on `btn`: busy, then done or failed. Returns the promise. */
  function show(btn, promise) {
    if (!btn || !btn.isConnected || btn.classList.contains("fb-skip")) return promise;
    const tip = tipOf(btn);
    const wasDisabled = !!btn.disabled;
    btn.classList.add("is-busy");
    btn.setAttribute("aria-busy", "true");
    if ("disabled" in btn) btn.disabled = true;
    tip.className = "fb-tip fb-busy";
    tip.textContent = "正在……";
    const end = function (ok, why) {
      btn.classList.remove("is-busy");
      btn.removeAttribute("aria-busy");
      if ("disabled" in btn && !wasDisabled) btn.disabled = false;
      tip.className = "fb-tip " + (ok ? "fb-ok" : "fb-fail");
      tip.textContent = ok ? "好了" : "没成功：" + why;
      tip._fbTimer = setTimeout(function () { tip.remove(); }, SHOW_MS);
    };
    Promise.resolve(promise).then(function (res) {
      const why = failed(res);
      end(!why, why);
    }, function (err) {
      end(false, String((err && err.message) || err || "出错了"));
    });
    return promise;
  }

  function clicked() {
    return last.el && Date.now() - last.at < CLICK_MS ? last.el : null;
  }

  const wrapped = new WeakMap();
  /** The bridge with apiGet / apiPost passed through show() when a click started them. */
  function wrap(bridge) {
    if (!bridge || typeof bridge !== "object") return bridge;
    if (wrapped.has(bridge)) return wrapped.get(bridge);
    const own = {};
    ["apiGet", "apiPost"].forEach(function (name) {
      if (typeof bridge[name] !== "function") return;
      own[name] = function () {
        const p = bridge[name].apply(bridge, arguments);
        const btn = clicked();
        return btn ? show(btn, p) : p;
      };
    });
    // everything else is the bridge's own, called on the bridge itself
    const w = new Proxy(bridge, {
      get: function (target, prop) {
        if (Object.prototype.hasOwnProperty.call(own, prop)) return own[prop];
        const v = target[prop];
        return typeof v === "function" ? v.bind(target) : v;
      }
    });
    wrapped.set(bridge, w);
    return w;
  }

  window.BioFeedback = { show: show, wrap: wrap };
})();
