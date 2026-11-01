// ams-life (AGPL-3.0); see NOTICE.md.
// Invented sample data for the brain map. Every name, group, number and line
// below is made up; nothing comes from a real chat.
//
// BrainSample.make({n}) returns {graph, details}:
// - graph: exactly what the read-only panel API will return (no content, no
//   names, no QQ numbers; format in docs/brain-viz.md);
// - details: what "page/brain/node" will return for one id when the owner
//   clicks a point.
(function (root) {
  "use strict";

  function rng(seed) {
    return function () {
      seed = (seed + 0x6D2B79F5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const NAMES = ["阿青", "小满", "老周", "星野", "柚子", "南风", "木木", "七七", "阿怪", "团子",
    "小鹿", "白桃", "鱼丸", "青柠", "大橘", "阿北", "十一", "米粒", "豆豆", "晚星",
    "苏打", "阿树", "阿橙", "小舟", "栗子", "夏夏", "灯灯", "山竹", "可可", "一一"];
  const GROUPS = ["摸鱼小组", "深夜电台", "画画打卡", "周末桌游", "考研互助", "猫猫图鉴",
    "编程闲聊", "做饭研究所", "跑步打卡", "读书会", "追番小队", "拍照散步"];
  const MEMORY = {
    "偏好": ["{p}说喜欢下雨天", "{p}不吃香菜", "{p}最近迷上了拼图", "{p}更喜欢猫一点", "{p}只喝冰的"],
    "经历": ["{p}说今天去爬山了", "{p}昨晚熬夜赶作业", "{p}搬家搬了一整天", "{p}第一次自己做了蛋糕"],
    "约定": ["答应周末陪{p}看新番", "说好明天提醒{p}早点睡", "跟{p}约好一起打卡"],
    "知识": ["{p}教了一个做蛋饼的办法", "{p}说附近新开了一家书店", "群里说下周有流星雨"],
    "心情": ["{p}最近有点累", "{p}考试过了很开心", "{p}说这周过得很慢"],
    "玩笑": ["{p}把猫的照片说成自己的自拍", "大家起哄让{p}唱歌", "{p}又在群里接龙接错了"],
    "计划": ["{p}打算下个月去看海", "{p}准备开始学吉他", "{p}想换一份工作"],
  };
  const PRIVATE_MEMORY = ["{p}私下说最近压力很大", "{p}说了一件只告诉她的小事", "{p}问她怎么安慰朋友",
    "{p}说想家了", "{p}讲了自己小时候的事"];
  const EVENTS = {
    "被叫到": ["{p}叫了她一声", "{p}问她今天过得怎么样"],
    "聊天": ["群里在聊周末去哪", "{p}和{q}聊起了做饭", "大家在讨论新出的漫画"],
    "图片": ["{p}发了一张猫的照片", "{p}分享了一张晚霞"],
    "争论": ["{p}和{q}为了甜粽咸粽争了几句"],
    "安静": ["群里安静了一下午"],
  };
  const NOTES = ["今天群里很热闹", "记得{p}说过下周有考试", "想多听听大家在聊什么", "{p}好像有点累，下次问问",
    "最近好多人在说流星雨", "{p}的猫叫团团", "这周说话说得有点多了"];
  const STYLES = ["爱开玩笑", "话不多但很准", "总是半夜出现", "喜欢分享图片", "很照顾新人", "说话很快"];
  const TOPICS = ["猫", "做饭", "游戏", "考试", "天气", "画画", "跑步", "书"];

  function make(opts) {
    const n = Math.max(80, Math.min(20000, Number((opts && opts.n) || 900)));
    const r = rng(Number((opts && opts.seed) || 20261028));
    const pick = (arr) => arr[Math.floor(r() * arr.length)];
    const skew = (k, p) => Math.min(k - 1, Math.floor(Math.pow(r(), p || 1.8) * k));
    const now = Date.UTC(2026, 9, 28, 4, 0, 0) / 1000;
    const DAY = 86400;
    const ago = () => now - Math.pow(r(), 1.6) * 24 * DAY;   // more of the recent days

    const nodes = [], edges = [], details = {};
    const W = Math.max(6, Math.min(40, Math.round(n / 55)));
    const WG = Math.max(3, Math.round(W * 0.45)), WP = W - WG;
    const P = Math.max(WP + 6, Math.round(n * 0.08));
    const M = Math.round(n * 0.6), E = Math.round(n * 0.2), N = Math.min(60, 8 + Math.round(n * 0.03));
    const nameOf = (k) => NAMES[k % NAMES.length] + (k >= NAMES.length ? String(1 + Math.floor(k / NAMES.length)) : "");

    const groups = [], privates = [];
    for (let i = 0; i < WG; i++) {
      const id = "w:g" + (i + 1);
      groups.push({ id, members: [] });
      nodes.push({ id, kind: "window", sub: "group", label: "群" + (i + 1), w: +(1 - i / WG * 0.8).toFixed(2) });
      details[id] = { title: "示例群·" + GROUPS[i % GROUPS.length] + (i >= GROUPS.length ? (1 + Math.floor(i / GROUPS.length)) : ""),
        lines: [["类型", "群聊"], ["她这 24 小时看到", (40 + Math.floor(r() * 900)) + " 条"]] };
    }
    const people = [];
    for (let k = 0; k < P; k++) {
      const id = "p:" + (k + 1);
      people.push({ id, k, groups: [] });
      nodes.push({ id, kind: "person", label: "人" + (k + 1), w: +(0.2 + r() * 0.8).toFixed(2) });
    }
    for (let j = 0; j < WP; j++) {
      const id = "w:p" + (j + 1);
      privates.push({ id, partner: people[j] });
      nodes.push({ id, kind: "window", sub: "private", label: "私聊" + (j + 1), w: +(0.3 + r() * 0.6).toFixed(2) });
      details[id] = { title: "跟" + nameOf(j) + "的私聊", lines: [["类型", "私聊"], ["她这 24 小时看到", (5 + Math.floor(r() * 120)) + " 条"]] };
    }
    // Who is in which group, and her impression of them there.
    for (const p of people) {
      const count = 1 + Math.floor(r() * 2.4);
      for (let c = 0; c < count; c++) {
        const g = groups[skew(groups.length, 1.5)];
        if (p.groups.includes(g)) continue;
        p.groups.push(g); g.members.push(p);
        edges.push({ s: p.id, t: g.id, kind: "impression", w: +(0.2 + r() * 0.8).toFixed(2) });
      }
      const priv = privates.find((x) => x.partner === p);
      details[p.id] = { title: nameOf(p.k), qq: "示例-" + String(1000 + p.k * 7),
        lines: [["她对这个人的印象", pick(STYLES) + "，常聊" + pick(TOPICS) + "和" + pick(TOPICS)],
          ["在哪见过", p.groups.map((g) => g.id.replace("w:g", "群")).concat(priv ? ["私聊" + priv.id.slice(3)] : []).join("、")]] };
    }
    const windows = groups.map((g) => ({ id: g.id, group: true, members: g.members }))
      .concat(privates.map((x) => ({ id: x.id, group: false, members: [x.partner] })));
    const pickWindow = () => (r() < 0.62 ? windows[skew(groups.length, 1.4)] : windows[groups.length + skew(privates.length, 1.3)]);
    const fill = (text, w) => text.replace("{p}", nameOf(pick(w.members).k)).replace("{q}", nameOf(pick(w.members).k));

    const memories = [];
    for (let i = 0; i < M; i++) {
      const w = pickWindow();
      if (!w.members.length) continue;
      const id = "m:" + (i + 1).toString(36).padStart(4, "0");
      const cat = w.group ? pick(Object.keys(MEMORY)) : (r() < 0.5 ? "私下" : pick(Object.keys(MEMORY)));
      const about = [];
      const ppl = 1 + (r() < 0.3 ? 1 : 0);
      for (let c = 0; c < ppl; c++) { const p = pick(w.members); if (!about.includes(p)) about.push(p); }
      const text = (cat === "私下" ? pick(PRIVATE_MEMORY) : pick(MEMORY[cat])).replace("{p}", nameOf(about[0].k));
      const ts = Math.round(ago());
      const m = { id, kind: "memory", cat, label: cat, where: w.id, ts, w: +(0.15 + Math.pow(r(), 1.4) * 0.85).toFixed(2),
        vis: w.group ? "public" : "private" };
      nodes.push(m); memories.push({ m, w, about });
      edges.push({ s: id, t: w.id, kind: "origin" });
      for (const p of about) edges.push({ s: id, t: p.id, kind: "about" });
      details[id] = { title: cat + "的记忆", text,
        lines: [["出处", w.id.replace("w:g", "群").replace("w:p", "私聊")], ["能在哪说", w.group ? "公开：哪里都能说，别处不带名字" : "私下：只在这个私聊里"],
          ["跟谁有关", about.map((p) => nameOf(p.k)).join("、")]] };
    }
    // Associations: two memories recalled together (entry["links"]).
    const byWindow = {};
    for (const x of memories) (byWindow[x.w.id] = byWindow[x.w.id] || []).push(x);
    for (const x of memories) {
      const count = Math.floor(Math.pow(r(), 1.3) * 3.2);
      for (let c = 0; c < count; c++) {
        const pool = r() < 0.75 ? byWindow[x.w.id] : memories;
        const y = pick(pool);
        if (y === x) continue;
        edges.push({ s: x.m.id, t: y.m.id, kind: "link", w: 1 + Math.floor(Math.pow(r(), 2) * 6), ts: Math.round(Math.max(x.m.ts, y.m.ts)) });
      }
    }
    for (let i = 0; i < E; i++) {
      const w = pickWindow();
      if (!w.members.length) continue;
      const id = "e:" + (i + 1).toString(36).padStart(4, "0");
      const cat = w.group ? pick(Object.keys(EVENTS)) : "被叫到";
      const text = fill(pick(EVENTS[cat]), w);
      nodes.push({ id, kind: "event", cat, label: cat, where: w.id, ts: Math.round(now - Math.pow(r(), 1.2) * 3 * DAY),
        w: +(0.2 + r() * 0.8).toFixed(2), vis: w.group ? "public" : "private" });
      edges.push({ s: id, t: w.id, kind: "origin" });
      const p = pick(w.members);
      edges.push({ s: id, t: p.id, kind: "about" });
      details[id] = { title: "事件 · " + cat, text, lines: [["在哪", w.id.replace("w:g", "群").replace("w:p", "私聊")]] };
    }
    for (let i = 0; i < N; i++) {
      const id = "n:" + (i + 1);
      const priv = r() < 0.3;
      const w = priv ? windows[groups.length + skew(privates.length, 1.3)] : null;
      const self = !priv && r() < 0.35;
      const text = (self ? "（她自己）" : "") + pick(NOTES).replace("{p}", nameOf(pick(w ? w.members : people).k));
      nodes.push({ id, kind: "note", cat: priv ? "私下那一页" : "群里那一页", label: "本子", where: w ? w.id : null,
        ts: Math.round(now - Math.floor(r() * 20) * DAY - 3 * 3600), w: 0.6, vis: priv ? "private" : "public", self });
      if (w) edges.push({ s: id, t: w.id, kind: "origin" });
      else for (let c = 0; c < 2; c++) edges.push({ s: id, t: pick(groups).id, kind: "origin" });
      details[id] = { title: "本子 · " + (priv ? "私下" : "群里"), text, lines: [["写于", "夜里整理本子时"]] };
    }

    // Turns: what each reply recalled, as ids only. "held" = she knows it,
    // but the discretion table kept it out of this place.
    const linkOf = {};
    for (const e of edges) if (e.kind === "link") { (linkOf[e.s] = linkOf[e.s] || []).push(e.t); (linkOf[e.t] = linkOf[e.t] || []).push(e.s); }
    const turns = [];
    const T = 16;
    for (let i = 0; i < T; i++) {
      const w = windows[r() < 0.7 ? skew(groups.length, 1.6) : groups.length + skew(privates.length, 1.3)];
      const local = (byWindow[w.id] || []);
      if (!local.length) continue;
      let cur = pick(local).m.id;
      const recalled = [cur], path = [], held = [];
      for (let step = 0; step < 4; step++) {
        const next = (linkOf[cur] || []).filter((x) => !recalled.includes(x) && !held.includes(x));
        if (!next.length) break;
        const nx = pick(next);
        const xm = memories.find((q) => q.m.id === nx);
        path.push([cur, nx]);
        if (xm && xm.m.vis === "private" && xm.w.id !== w.id) { held.push(nx); break; }
        recalled.push(nx); cur = nx;
      }
      if (!held.length) {
        const elsewhere = memories.filter((q) => q.m.vis === "private" && q.w.id !== w.id &&
          q.about.some((p) => w.members.includes(p)));
        if (elsewhere.length && r() < 0.6) held.push(pick(elsewhere).m.id);
      }
      const body = { social: +(0.3 + r() * 0.6).toFixed(2), curiosity: +(0.3 + r() * 0.6).toFixed(2), boredom: +(r() * 0.6).toFixed(2),
        seen: +(0.2 + r() * 0.6).toFixed(2), talked: +(r() * 0.8).toFixed(2), stress: +(r() * 0.5).toFixed(2), valence: +(r() * 1.4 - 0.5).toFixed(2) };
      turns.push({ id: "t" + (i + 1), ts: Math.round(now - (T - i) * 47 * 60), where: w.id, recalled, held, path, body });
    }

    const graph = {
      schema: "ams-life.brain/1",
      sample: true,
      now,
      body: { social: 0.62, curiosity: 0.71, boredom: 0.18, seen: 0.44, talked: 0.35, stress: 0.22, valence: 0.3 },
      nodes, edges, turns,
    };
    return { graph, details };
  }

  root.BrainSample = { make };
})(typeof window !== "undefined" ? window : globalThis);
