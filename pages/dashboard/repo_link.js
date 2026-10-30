/* ams-life (AGPL-3.0); see NOTICE.md.
 * "GitHub 仓库地址" in the panel's settings (signoff 44, 10-30). AstrBot shows a plugin page in a
 * frame without allow-popups, so a link to a new window does nothing there. The buttons show the
 * address instead, in a read-only line, with "复制":
 * - first the clipboard (navigator.clipboard.writeText);
 * - the frame does not let it (no clipboard-write for it), or there is none, or it does not answer
 *   soon: the whole line is selected and the page says to press Ctrl+C.
 * Nothing here opens a window.
 *
 * Loaded in the browser (window.BioRepoLink) and by the tests through node's require().
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.BioRepoLink = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  const WAIT_MS = 1500;   // a clipboard that has not answered by then is taken as "not allowed"
  const COPIED = "已复制，贴到浏览器地址栏就能打开";
  const SELECTED = "这里不让直接复制：地址已经选中，按 Ctrl+C 复制";
  const SHOWN = "在 AstrBot 里开不了新窗口；复制以后贴到浏览器地址栏打开";

  /** Copy the line's address: "copied", or "selected" when the page had to select it for Ctrl+C. */
  async function copyAddress(input, note, clip, wait) {
    const text = String(input.value || "");
    try {
      if (!text || !clip || typeof clip.writeText !== "function") throw new Error("no clipboard");
      let timer;
      await Promise.race([
        clip.writeText(text),
        new Promise((_, no) => { timer = setTimeout(() => no(new Error("no answer")), wait || WAIT_MS); }),
      ]).finally(() => clearTimeout(timer));
      note.textContent = COPIED;
      return "copied";
    } catch (e) {
      try { input.focus(); } catch (e2) { /* still select */ }
      input.select();
      note.textContent = SELECTED;
      return "selected";
    }
  }

  /** Wire the buttons with data-repo in `doc` to the address line. Returns refresh() for the panel. */
  function attach(doc, clip) {
    const line = doc.getElementById("repoAddr"), input = doc.getElementById("repoAddrText");
    const copy = doc.getElementById("repoCopyBtn"), note = doc.getElementById("repoCopyNote");
    if (!line || !input || !copy || !note) return { refresh() {} };
    let from = null;
    function show(btn) {
      from = btn;
      input.value = btn.dataset.repo || "";
      note.textContent = SHOWN;
      line.hidden = !input.value;
    }
    doc.querySelectorAll("button[data-repo]").forEach((btn) => btn.addEventListener("click", () => show(btn)));
    copy.addEventListener("click", () => copyAddress(input, note, clip));
    return {
      /** A button's address changed (the Gitee mirror): the line follows it, or goes when it has none. */
      refresh() {
        if (!from || line.hidden) return;
        if (from.dataset.repo && from.style.display !== "none") input.value = from.dataset.repo;
        else line.hidden = true;
      },
    };
  }

  return { WAIT_MS, COPIED, SELECTED, SHOWN, copyAddress, attach };
});
