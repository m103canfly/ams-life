/* ams-life (AGPL-3.0); see NOTICE.md.
 * "像不像" (cards L1, L2): each week the owner reads 20 of her replies and 2 of her days, and says of
 * each whether it is like her: 像 / 不像 / 说不准, and a line why. Only page/likeness (one week: the
 * replies in `data`, the days in `days`, numbers already hidden and other people's names already
 * taken out) and page/likeness/rate ({week, id, rating, reason}); no other route.
 * A day shows one line per thing she did: "几点 做了什么（多久）——她的心里话".
 * Without a bridge (a static preview) it shows an invented week, saying so, and saves nothing.
 *
 * Loaded in the browser (window.BioLikeness) and by the tests through node's require().
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.BioLikeness = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  const LIST = "page/likeness";
  const RATE = "page/likeness/rate";
  const RATINGS = [["like", "像"], ["unlike", "不像"], ["unsure", "说不准"]];
  const SAMPLE_BADGE = "示例（编造）：没有连上她，下面是编出来的样子，点了也不存。";
  const WEEKDAYS = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];

  /** Monday of the week `d` is in (local time), at midnight. */
  function monday(d) {
    const t = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    t.setDate(t.getDate() - ((t.getDay() + 6) % 7));
    return t;
  }
  /** "2026-W44": the ISO week of `d` in local time, as likeness.week_of says it. */
  function weekOf(d) {
    const t = monday(d);
    t.setDate(t.getDate() + 3);                       // the Thursday decides the year
    const jan4 = new Date(t.getFullYear(), 0, 4);
    const week = 1 + Math.round((t - monday(jan4)) / (7 * 86400000));
    return t.getFullYear() + "-W" + String(week).padStart(2, "0");
  }

  /** The week's replies and days out of page/likeness's answer, through one or two wrappers. */
  function split(raw) {
    let o = raw;
    for (let i = 0; i < 4 && o; i++) {
      if (o.status === "error") throw new Error(o.message || "没取到");
      if (Array.isArray(o.data) || !o.data || typeof o.data !== "object") break;
      o = o.data;
    }
    return { replies: Array.isArray(o && o.data) ? o.data : [], days: Array.isArray(o && o.days) ? o.days : [] };
  }

  // likeness.public hides long numbers as "[number]"; the panel says it as "[号码]" everywhere
  const esc = (s) => String(s == null ? "" : s).replace(/\[number\]/g, "[号码]").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const two = (n) => String(n).padStart(2, "0");

  /** One thing she did: "21:30 看网页：讲猫的视频（40 分钟）——好想养一只". */
  function dayLine(r) {
    const what = [r.do, r.detail].filter((x) => x && String(x).trim()).map(esc).join("：");
    const long = Number(r.minutes) > 0 ? "（" + Math.round(Number(r.minutes)) + " 分钟）" : "";
    const feel = r.feel && String(r.feel).trim() ? '<span class="lk-feel">——' + esc(r.feel) + "</span>" : "";
    return '<li><span class="lk-time">' + esc(r.time) + "</span> " + (what || "（没写做什么）") + long + feel + "</li>";
  }

  /** 像 / 不像 / 说不准, the line why, and where the answer shows. */
  function rateHtml(row) {
    // the chosen one wears the panel's own "primary" look (look.css styles it in both themes)
    const buttons = RATINGS.map(([v, word]) => '<button type="button" class="btn mini lk-pick' + (row.rating === v ? " on primary" : "") +
      '" data-rating="' + v + '" aria-pressed="' + (row.rating === v) + '">' + word + "</button>").join("");
    return '<div class="lk-rate">' + buttons + '<input type="text" class="lk-why" maxlength="500" placeholder="一句为什么（可以不写）" value="' +
      esc(row.reason || "") + '" /><button type="button" class="btn mini lk-save">存理由</button><span class="hint lk-state" role="status"></span></div>';
  }

  function replyHtml(r) {
    const d = new Date(Number(r.ts || 0) * 1000);
    const head = [r.place === "private" ? "私聊" : r.place === "group" ? "群里" : "", isNaN(d) ? "" :
      two(d.getMonth() + 1) + "-" + two(d.getDate()) + " " + two(d.getHours()) + ":" + two(d.getMinutes())].filter(Boolean).join(" · ");
    const ctx = (r.context || []).map((c) => '<div class="lk-ctx"><b>' + esc(c.name) + "：</b>" + esc(c.text) + "</div>").join("");
    return '<div class="mem-card lk-card" data-id="' + esc(r.id) + '"><div class="mem-card-head"><b>' + esc(head || "一句回话") +
      "</b></div>" + ctx + '<div class="lk-her"><b>她：</b>' + esc(r.reply) + "</div>" + rateHtml(r) + "</div>";
  }

  function dayHtml(day) {
    const p = String(day.date || "").split("-").map(Number);
    const d = p.length === 3 ? new Date(p[0], p[1] - 1, p[2]) : null;
    const head = d && !isNaN(d) ? two(d.getMonth() + 1) + "-" + two(d.getDate()) + " " + WEEKDAYS[d.getDay()] : esc(day.date);
    const rows = (day.rows || []).length ? '<ul class="lk-day">' + day.rows.map(dayLine).join("") + "</ul>"
      : '<p class="hint">这一天的记录都删掉了。</p>';
    return '<div class="mem-card lk-card" data-id="' + esc(day.id) + '"><div class="mem-card-head"><b>' + head +
      "</b><span class=\"hint\">她这一天</span></div>" + rows + rateHtml(day) + "</div>";
  }

  /** An invented week, for the static preview. */
  function sample() {
    const now = Date.now() / 1000;
    return {
      replies: [
        { id: "x1", ts: now - 7200, place: "group", context: [{ name: "阿橙", text: "小爱周末去爬山吗" }], reply: "去呀！不过我要先睡个懒觉", rating: null, reason: "" },
        { id: "x2", ts: now - 86400, place: "private", context: [{ name: "柠檬", text: "今天好累" }], reply: "抱抱，先喝口水歇一会儿", rating: "like", reason: "像她会说的" },
      ],
      days: [
        { id: "day-x1", kind: "day", date: "2026-10-28", rating: null, reason: "", rows: [
          { time: "09:10", do: "看网页", detail: "讲猫的视频", minutes: 40, feel: "好想养一只" },
          { time: "14:00", do: "发呆", detail: "", minutes: 20, feel: "" },
          { time: "22:30", do: "写日记", detail: "今天在群里聊了爬山", minutes: 15, feel: "大家都挺开心的" }] },
        { id: "day-x2", kind: "day", date: "2026-10-30", rating: "unsure", reason: "", rows: [
          { time: "11:00", do: "听歌", detail: "", minutes: 30, feel: "这首有点耳熟" }] },
      ],
    };
  }

  /** The browser part. opts.bridge(): the panel's bridge or null. */
  function attach(opts) {
    const doc = document;
    const $ = (id) => doc.getElementById(id);
    const box = $("lkReplies");
    if (!box) return null;
    let shown = monday(new Date()), loaded = false, busy = false, week = weekOf(shown);
    const rows = new Map();

    function summary() {
      const all = [...rows.values()];
      const rated = all.filter((r) => r.rating).length;
      $("lkSummary").textContent = all.length ? "已经打了 " + rated + " / " + all.length + " 个" : "";
    }

    async function load() {
      if (busy) return;
      busy = true;
      week = weekOf(shown);
      $("lkWeek").textContent = week + "（" + two(shown.getMonth() + 1) + "-" + two(shown.getDate()) + " 起）";
      $("lkNext").disabled = weekOf(new Date()) === week;
      $("lkState").textContent = "正在取…";
      try {
        const b = opts.bridge && opts.bridge();
        let data;
        if (!b) { data = sample(); $("lkBadge").textContent = SAMPLE_BADGE; $("lkBadge").hidden = false; }
        else { data = split(await b.apiGet(LIST, { week })); $("lkBadge").hidden = true; }
        rows.clear();
        for (const r of data.replies.concat(data.days)) rows.set(String(r.id), r);
        box.innerHTML = data.replies.length ? data.replies.map(replyHtml).join("") : '<p class="hint">这一周还没有她的回话可看。</p>';
        $("lkDays").innerHTML = data.days.length ? data.days.map(dayHtml).join("") : '<p class="hint">这一周还没有她过日子的记录。</p>';
        $("lkState").textContent = data.replies.length + " 句回话、" + data.days.length + " 天";
        summary();
      } catch (e) {
        $("lkState").textContent = "没取到：" + String((e && e.message) || e);
      } finally {
        busy = false;
      }
    }

    async function save(card, rating) {
      const row = rows.get(card.dataset.id);
      const state = card.querySelector(".lk-state");
      if (!row) return;
      rating = rating || row.rating;
      if (!rating) { state.textContent = "先点 像 / 不像 / 说不准"; return; }
      const reason = card.querySelector(".lk-why").value.trim().slice(0, 500);
      const b = opts.bridge && opts.bridge();
      if (!b) { state.textContent = "示例里不存"; return; }
      state.textContent = "正在存…";
      try {
        const raw = await b.apiPost(RATE, { week, id: row.id, rating, reason });
        let d = raw;
        if (d && d.data && typeof d.data === "object" && d.data.status !== undefined) d = d.data;   // a bridge's own wrapper
        if (!d || d.status !== "ok") throw new Error((d && d.message) || "没存上");
        row.rating = rating; row.reason = reason;
        card.querySelectorAll(".lk-pick").forEach((x) => { const on = x.dataset.rating === rating; x.classList.toggle("on", on); x.classList.toggle("primary", on); x.setAttribute("aria-pressed", String(on)); });
        state.textContent = "存好了";
        summary();
      } catch (e) {
        state.textContent = "没存上：" + String((e && e.message) || e);
      }
    }

    function onClick(ev) {
      const t = ev.target;
      const card = t.closest ? t.closest(".lk-card") : null;
      if (!card) return;
      if (t.classList.contains("lk-pick")) save(card, t.dataset.rating);
      else if (t.classList.contains("lk-save")) save(card, "");
    }

    box.addEventListener("click", onClick);
    $("lkDays").addEventListener("click", onClick);
    $("lkPrev").addEventListener("click", () => { shown.setDate(shown.getDate() - 7); load(); });
    $("lkNext").addEventListener("click", () => { if (weekOf(new Date()) !== week) { shown.setDate(shown.getDate() + 7); load(); } });
    return {
      /** The panel switched to view `name`: this week is fetched on the first visit. */
      onView(name) {
        if (name === "likeness" && !loaded) { loaded = true; load(); }
      },
      reload() { load(); },
    };
  }

  return { LIST, RATE, RATINGS, SAMPLE_BADGE, monday, weekOf, split, dayLine, rateHtml, replyHtml, dayHtml, sample, attach };
});
