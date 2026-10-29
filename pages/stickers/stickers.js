/* ams-life (AGPL-3.0); see NOTICE.md. "她的表情包" (index.html): her stickers through AstrBot's page bridge --
   page/stickers (one page of them), page/stickers/image (one picture), page/stickers/delete, page/stickers/add.
   No picture is in this page or this repository; opened without AstrBot it shows made-up drawings. */
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const PICTURE = /^data:image\/(png|jpeg|gif|webp|svg\+xml);base64,[A-Za-z0-9+/]+={0,2}$/;
  const MAX_BYTES = 5 * 1024 * 1024;
  let bridge = null;
  let sample = null;
  const st = { sort: "saved", emotion: "", scene: "", source: "", next: 0, loading: false, items: new Map(), shown: null };
  const pictures = new Map();

  function findBridge() {
    try {
      return window.AstrBotPluginView || window.AstrBotPluginPage || window.astrbotPluginView ||
        (window.parent !== window && (window.parent.AstrBotPluginView || window.parent.AstrBotPluginPage)) || null;
    } catch (e) { return null; }
  }
  const unwrap = (r) => (r && r.data !== undefined ? r.data : r);
  async function get(route, query) {
    if (sample) return sample.get(route, query || {});
    const raw = await bridge.apiGet(route, query || {});
    if (raw && raw.status === "error") throw new Error(raw.message || "没成功");
    return unwrap(raw);
  }
  async function post(route, body) {
    if (sample) return sample.post(route, body || {});
    const raw = await bridge.apiPost(route, body || {});
    if (raw && raw.status === "error") throw new Error(raw.message || "没成功");
    return unwrap(raw);
  }

  // ---------------------------------------------------------------- words
  function ago(ts) {
    if (!ts) return "—";
    const d = Math.floor((Date.now() / 1000 - ts) / 86400);
    return d <= 0 ? "今天" : d === 1 ? "昨天" : d + " 天前";
  }
  function setTheme(dark) {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    $("themeBtn").textContent = dark ? "浅色" : "深色";
  }
  function say(id, text) { $(id).textContent = text || ""; }

  // ---------------------------------------------------------------- the list
  function fillSelect(id, values, keep) {
    const sel = $(id);
    const now = keep ? sel.value : "";
    sel.innerHTML = '<option value="">全部</option>';
    for (const v of values || []) {
      const o = document.createElement("option");
      o.value = v; o.textContent = v;
      sel.appendChild(o);
    }
    sel.value = (values || []).includes(now) ? now : "";
  }

  function card(item) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "card";
    b.dataset.id = item.id;
    const pic = document.createElement("div");
    pic.className = "pic";
    const img = document.createElement("img");
    img.alt = item.caption || "表情包";
    img.loading = "lazy";
    pic.appendChild(img);
    const cap = document.createElement("div");
    cap.className = "cap";
    cap.textContent = item.caption || "（没有说明）";
    const tags = document.createElement("div");
    tags.className = "tags";
    for (const [t, cls] of [[item.from, item.owner ? "tag owner" : "tag"], [item.emotion, "tag"], [item.scene, "tag"]]) {
      if (!t) continue;
      const s = document.createElement("span");
      s.className = cls; s.textContent = t;
      tags.appendChild(s);
    }
    b.append(pic, cap, tags);
    b.addEventListener("click", () => openDetail(item.id));
    seen.observe(b);
    return b;
  }

  async function picture(id) {
    if (pictures.has(id)) return pictures.get(id);
    const p = get("page/stickers/image", { id }).then((d) => (d && PICTURE.test(String(d.url || "")) ? d.url : ""));
    pictures.set(id, p);
    return p;
  }

  const seen = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      seen.unobserve(e.target);
      const img = e.target.querySelector("img");
      picture(e.target.dataset.id).then((url) => { if (url) img.src = url; }).catch(() => {});
    }
  }, { rootMargin: "200px" });

  async function load(reset) {
    if (st.loading || (!reset && st.next === null)) return;
    st.loading = true;
    if (reset) { st.next = 0; st.items.clear(); $("grid").innerHTML = ""; }
    try {
      const d = await get("page/stickers", { sort: st.sort, emotion: st.emotion, scene: st.scene, source: st.source,
                                             after: String(st.next || 0) });
      const c = d.counts || {};
      say("counts", "一共 " + (c.total || 0) + " 张（你给的 " + (c.owner || 0) + " 张）· 今天新存 " + (c.today || 0) +
          " 张 · 这几天要过期 " + (c.soon || 0) + " 张" + (d.on === false ? " · 表情包开关现在关着" : ""));
      fillSelect("emotion", d.emotions, true);
      fillSelect("scene", d.scenes, true);
      fillSelect("source", d.sources, true);
      for (const item of d.items || []) {
        st.items.set(item.id, item);
        $("grid").appendChild(card(item));
      }
      st.next = d.next === undefined ? null : d.next;
      $("empty").hidden = st.items.size > 0;
      say("state", "");
    } catch (e) {
      say("state", "没读出来：" + e.message);
    } finally {
      st.loading = false;
    }
  }
  new IntersectionObserver((entries) => { if (entries.some((e) => e.isIntersecting)) load(false); })
    .observe($("more"));

  // ---------------------------------------------------------------- one sticker
  async function openDetail(id) {
    const item = st.items.get(id);
    if (!item) return;
    st.shown = id;
    say("detailCaption", item.caption || "（没有说明）");
    say("detailEmotion", item.emotion || "—");
    say("detailScene", item.scene || "—");
    say("detailWhy", item.why || "—");
    say("detailFrom", item.from || "—");
    say("detailAge", ago(item.saved_at));
    say("detailUsed", item.uses ? ago(item.last_used) : "还没用过");
    say("detailUses", String(item.uses || 0));
    say("detailLeft", item.owner ? "你给的，不会自动删" : (item.days_left + " 天没用就删"));
    say("detailState", "");
    $("detailImg").removeAttribute("src");
    $("detail").showModal();
    try { const url = await picture(id); if (url && st.shown === id) $("detailImg").src = url; } catch (e) { /* stays empty */ }
  }

  $("closeBtn").addEventListener("click", () => $("detail").close());
  $("deleteBtn").addEventListener("click", async () => {
    const item = st.items.get(st.shown);
    if (!item) return;
    const ask = (item.owner ? "这张是你加的。\n" : "") + "删掉“" + (item.caption || "这张") + "”？删了不能恢复。";
    if (!window.confirm(ask)) return;
    $("deleteBtn").disabled = true;
    say("detailState", "正在删……");
    try {
      await post("page/stickers/delete", { id: item.id });
      $("detail").close();
      say("state", "删好了。");
      load(true);
    } catch (e) {
      say("detailState", "没删成：" + e.message);
    } finally {
      $("deleteBtn").disabled = false;
    }
  });

  // ---------------------------------------------------------------- the owner adds some
  function readFile(file) {
    return new Promise((resolve, reject) => {
      const r = new FileReader();
      r.onload = () => resolve(String(r.result || ""));
      r.onerror = () => reject(new Error("读不了这个文件"));
      r.readAsDataURL(file);
    });
  }
  $("files").addEventListener("change", async (ev) => {
    const files = Array.from(ev.target.files || []);
    ev.target.value = "";
    if (!files.length) return;
    let ok = 0;
    const bad = [];
    for (const [n, f] of files.entries()) {
      say("state", "正在加第 " + (n + 1) + " / " + files.length + " 张……");
      if (f.size > MAX_BYTES) { bad.push(f.name + "（太大了）"); continue; }
      try {
        await post("page/stickers/add", { picture: await readFile(f), note: $("note").value.trim() });
        ok += 1;
      } catch (e) {
        bad.push(f.name + "（" + e.message + "）");
      }
    }
    say("state", "加好了 " + ok + " 张" + (bad.length ? "；没收：" + bad.join("、") : "。"));
    load(true);
  });

  // ---------------------------------------------------------------- filters, theme
  for (const id of ["sort", "emotion", "scene", "source"]) {
    $(id).addEventListener("change", () => { st[id] = $(id).value; load(true); });
  }
  $("themeBtn").addEventListener("click", () => setTheme(document.documentElement.dataset.theme !== "dark"));

  // ---------------------------------------------------------------- made up, without AstrBot
  function makeSample() {
    const now = Date.now() / 1000;
    const kinds = [["一只在笑的猫", "开心", "夸人", "#f2a7c3"], ["一只在哭的狗", "难过", "安慰", "#9ec9e2"],
                   ["一只跳舞的兔子", "开心", "庆祝", "#f5c97a"], ["一只翻白眼的鸭子", "无语", "吐槽", "#b8d99a"],
                   ["一只捂脸的熊", "尴尬", "道歉", "#d7b8ea"], ["一只比心的仓鼠", "喜欢", "晚安", "#f7b0a0"]];
    const from = ["群1", "群2", "私聊1", "旧小爱", "主人给的"];
    const rows = [];
    for (let i = 0; i < 18; i++) {
      const [cap, emo, scene, color] = kinds[i % kinds.length];
      const owner = i % 7 === 4;
      const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><rect width="120" height="120" rx="18" fill="' +
        color + '"/><circle cx="60" cy="64" r="34" fill="#fff" opacity=".85"/><circle cx="48" cy="58" r="5" fill="#333"/>' +
        '<circle cx="72" cy="58" r="5" fill="#333"/><path d="M46 76 q14 12 28 0" stroke="#333" stroke-width="4" fill="none"/></svg>';
      rows.push({ id: "s" + i, caption: cap, emotion: emo, scene: scene, why: "好玩", from: owner ? "主人给的" : from[i % 4],
                  owner, saved_at: now - i * 86400 * 1.5, last_used: now - i * 86400, uses: (i * 7) % 5,
                  days_left: owner ? null : Math.max(0, 30 - i), url: "data:image/svg+xml;base64," + btoa(svg) });
    }
    return {
      async get(route, q) {
        if (route === "page/stickers/image") return { url: (rows.find((r) => r.id === q.id) || {}).url || "" };
        let items = rows.filter((r) => (!q.emotion || r.emotion === q.emotion) && (!q.scene || r.scene === q.scene) &&
                                       (!q.source || r.from === q.source));
        const key = { saved: (r) => -r.saved_at, used: (r) => -r.last_used, most: (r) => -r.uses,
                      soon: (r) => (r.days_left === null ? 1e9 : r.days_left) }[q.sort] || ((r) => -r.saved_at);
        items = items.slice().sort((a, b) => key(a) - key(b));
        const after = Number(q.after || 0);
        return { items: items.slice(after, after + 12), next: after + 12 < items.length ? after + 12 : null,
                 counts: { total: rows.length, owner: rows.filter((r) => r.owner).length, today: 1, soon: 2 },
                 emotions: [...new Set(rows.map((r) => r.emotion))], scenes: [...new Set(rows.map((r) => r.scene))],
                 sources: from, on: true };
      },
      async post() { throw new Error("示例里不能改"); },
    };
  }

  async function start() {
    bridge = findBridge();
    const forced = new URLSearchParams(location.search).get("theme");
    if (forced === "dark" || forced === "light") setTheme(forced === "dark");
    else setTheme(document.documentElement.dataset.theme === "dark");
    if (bridge) {
      try {
        const ctx = await Promise.race([bridge.ready(), new Promise((r) => setTimeout(() => r(null), 3000))]);
        if (!forced && ctx && typeof ctx.isDark === "boolean") setTheme(ctx.isDark);
      } catch (e) { /* the page's own theme stays */ }
    } else {
      sample = makeSample();
      $("previewBadge").hidden = false;
    }
    load(true);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
