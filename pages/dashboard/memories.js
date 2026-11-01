/* ams-life (AGPL-3.0); see NOTICE.md.
 * "她记住了什么": what she keeps, as a list (page/memories, memory_list.py): memories, events,
 * her notebook, what she thinks of people. Newest first, a page at a time, filtered by kind,
 * place, where it may be said, dates and words. Every row says where it came from, when,
 * where it may be said and who it is about. Long numbers come hidden ("[号码]"); "显示号码"
 * asks for that one row as kept (page/memories/number).
 *
 * Read only, but for one thing: a memory can be deleted, through the panel's existing
 * page/memory/delete (it takes everything from the same messages with it and registers it),
 * after the owner confirms. Without AstrBot's bridge (a static preview) the list is an
 * invented sample, saying so.
 *
 * Loaded in the browser (window.BioMemoryList) and by the tests through node's require().
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.BioMemoryList = api;
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  const LIST = "page/memories";
  const NUMBER = "page/memories/number";
  const DELETE = "page/memory/delete/default/";   // the existing route; its session part is not used
  const FILTERS = ["kind", "place", "vis", "from", "to", "q"];
  const SAMPLE_BADGE = "示例数据（编造）：没有连上 AstrBot，下面是编出来的样子。";

  /** The query of one call: only the filters that are set, as strings; `after` for the next page. */
  function query(filters, after) {
    const q = {};
    for (const k of FILTERS) {
      const v = filters && filters[k];
      if (v !== undefined && v !== null && String(v).trim() !== "") q[k] = String(v).trim().slice(0, 50);
    }
    if (after) q.after = String(after);
    return q;
  }

  /** An invented page, for the static preview. */
  function sample() {
    const rows = [
      ["memory", "群1", "public", ["阿橙"], "小爱 周末一起去爬山吗"],
      ["event", "群1", "public", ["柠檬", "阿橙"], "爬山的约定\n柠檬约大家周末去爬山"],
      ["note", "她自己", "self", [], "想多听听大家在聊什么"],
      ["memory", "私聊1", "private", ["阿橙"], "小爱，跟你说个悄悄话，我在准备一个惊喜"],
      ["impression", "群2", "public", ["桃子"], "叫“桃子”；称呼：桃桃；说话：话不多；常聊：猫"],
      ["memory", "群2", "public", ["小鱼"], "我的游戏号是 [号码]，加我"],
    ];
    const names = { memory: "记忆", event: "事件", note: "本子", impression: "群友印象" };
    const may = { public: "公开：哪里都能说，别处不带名字", private: "私下：只在那个私聊里", self: "她自己的：哪里都能说" };
    const now = 1793000000;
    return {
      items: rows.map((r, i) => ({ id: "x:" + i, kind: r[0], kind_name: names[r[0]], where: r[1], vis: r[2],
        may: may[r[2]], who: r[3], text: r[4], has_number: r[4].includes("[号码]"), ts: now - i * 3600,
        date: "2026-10-28 " + String(20 - i).padStart(2, "0") + ":00", entry: "" })),
      places: [{ id: "w:1", label: "群1" }, { id: "w:2", label: "群2" }, { id: "w:3", label: "私聊1" }],
      next: "", total: rows.length,
    };
  }

  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const unwrap = (r) => (r && r.data !== undefined && (r.status !== undefined || r.data.items !== undefined) ? r.data : r);

  /** One row's html. */
  function rowHtml(r) {
    const head = [r.kind_name, r.where, r.date].filter(Boolean).map(esc).join(" · ");
    const who = r.who && r.who.length ? '<div class="hint">跟谁有关：' + esc(r.who.join("、")) + "</div>" : "";
    const buttons = (r.has_number ? '<button type="button" class="btn" data-number="' + esc(r.id) + '">显示号码</button>' : "") +
      (r.kind === "memory" && r.entry ? '<button type="button" class="btn danger" data-delete="' + esc(r.entry) + '">删这条</button>' : "");
    return '<div class="mem-card" data-row="' + esc(r.id) + '"><div class="mem-card-head"><b>' + head + '</b><span class="hint">' +
      esc(r.may) + "</span></div>" + who + '<div class="mem-text">' + esc(r.text).replace(/\n/g, "<br>") + "</div>" +
      (buttons ? '<div class="mem-row-actions">' + buttons + '<span class="mem-row-state hint"></span></div>' : "") + "</div>";
  }

  /** The browser part. opts.bridge(): AstrBot's bridge or null. */
  function attach(opts) {
    const doc = document;
    const $ = (id) => doc.getElementById(id);
    const list = $("memList");
    if (!list) return null;
    let next = "", loaded = false, busy = false;
    const filters = () => ({ kind: $("memKind").value, place: $("memPlace").value, vis: $("memVis").value,
      from: $("memFrom").value, to: $("memTo").value, q: $("memQ").value });

    function fillPlaces(places) {
      const sel = $("memPlace");
      const keep = sel.value;
      sel.innerHTML = '<option value="">哪儿都看</option>' + (places || []).map((p) =>
        '<option value="' + esc(p.id) + '">' + esc(p.label) + "</option>").join("");
      sel.value = keep;
    }

    async function load(more) {
      if (busy) return;
      busy = true;
      const b = opts.bridge && opts.bridge();
      $("memMore").disabled = true;
      $("memState").textContent = "正在取…";
      try {
        let data;
        if (!b) { data = sample(); $("memBadge").textContent = SAMPLE_BADGE; $("memBadge").hidden = false; }
        else {
          const raw = await b.apiGet(LIST, query(filters(), more ? next : ""));
          data = unwrap(raw);
          if (!data || data.status === "error") throw new Error((data && data.message) || "没取到");
          $("memBadge").hidden = true;
        }
        if (!more) { list.innerHTML = ""; fillPlaces(data.places); }
        list.insertAdjacentHTML("beforeend", (data.items || []).map(rowHtml).join(""));
        next = data.next || "";
        $("memMore").hidden = !next;
        $("memState").textContent = (data.items || []).length || more ? "共 " + (data.total || 0) + " 条" : "没有这样的";
      } catch (e) {
        $("memState").textContent = String((e && e.message) || e);
      } finally {
        busy = false;
        $("memMore").disabled = false;
      }
    }

    async function onClick(ev) {
      const t = ev.target;
      const b = opts.bridge && opts.bridge();
      const card = t.closest ? t.closest(".mem-card") : null;
      const state = card ? card.querySelector(".mem-row-state") : null;
      if (t.dataset && t.dataset.number) {
        if (!b) { if (state) state.textContent = "示例里没有号码"; return; }
        t.disabled = true;
        try {
          const d = unwrap(await b.apiGet(NUMBER, { id: t.dataset.number }));
          if (!d || d.status === "error") throw new Error((d && d.message) || "没取到");
          card.querySelector(".mem-text").innerHTML = esc(d.text).replace(/\n/g, "<br>");
          t.remove();
        } catch (e) { t.disabled = false; if (state) state.textContent = String((e && e.message) || e); }
      } else if (t.dataset && t.dataset.delete) {
        if (!b) { if (state) state.textContent = "示例里不能删"; return; }
        if (!window.confirm("确定删掉这条记忆吗？\n从同一批消息来的事件、本子、手机里的话也会一起删掉，并记进遗忘登记，删了不能恢复。")) return;
        t.disabled = true;
        if (state) state.textContent = "正在删…";
        try {
          const d = unwrap(await b.apiPost(DELETE + encodeURIComponent(t.dataset.delete), {}));
          if (!d || d.status === "error") throw new Error((d && d.message) || "没删成");
          card.remove();
        } catch (e) { t.disabled = false; if (state) state.textContent = "没删成：" + String((e && e.message) || e); }
      }
    }

    $("memGo").addEventListener("click", () => load(false));
    $("memQ").addEventListener("keydown", (ev) => { if (ev.key === "Enter") load(false); });
    $("memMore").addEventListener("click", () => load(true));
    list.addEventListener("click", onClick);
    return {
      /** The panel switched to view `name`: the list is fetched on the first visit. */
      onView(name) {
        if (name === "memories" && !loaded) { loaded = true; load(false); }
      },
      reload() { load(false); },
    };
  }

  return { LIST, NUMBER, DELETE, FILTERS, SAMPLE_BADGE, query, sample, rowHtml, attach };
});
