/* ams-life (AGPL-3.0); see NOTICE.md. Her look (look.css), the two parts that need a script:
   - her pictures: the avatar and the half-body art, read once from the plugin (page/look, read only). They are
     never in this repository; the owner keeps them in the plugin's data folder. Anything that is not a small
     picture is ignored, and the panel keeps its drawn mark;
   - the glass capsule under the side tabs, sliding to the chosen one (still, when less motion is asked for). */
(function () {
  "use strict";
  const PICTURE = /^data:image\/(png|jpeg|webp);base64,[A-Za-z0-9+/]+={0,2}$/;
  const MAX_CHARS = 6 * 1024 * 1024;
  const KINDS = [["avatar", "has-avatar"], ["art", "has-art"]];

  // what page/look answered -> which pictures the page shows (returns the classes it set)
  function usePictures(raw, root) {
    root = root || document.documentElement;
    const d = raw && typeof raw === "object" && raw.data && typeof raw.data === "object" ? raw.data : raw;
    const shown = [];
    if (!d || typeof d !== "object") return shown;
    for (const [key, cls] of KINDS) {
      const v = d[key];
      if (typeof v !== "string" || v.length > MAX_CHARS || !PICTURE.test(v)) continue;
      root.style.setProperty("--" + key, 'url("' + v + '")');
      root.classList.add(cls);
      shown.push(cls);
    }
    return shown;
  }

  let asked = false;
  async function loadPictures(bridge) {
    if (asked || !bridge || typeof bridge.apiGet !== "function") return;
    asked = true;
    try { usePictures(await bridge.apiGet("page/look", {})); } catch (e) { /* no pictures: the drawn mark stays */ }
  }

  function glide() {
    const nav = document.querySelector(".nav");
    if (!nav) return;
    let g = nav.querySelector(".nav-glider");
    if (!g) {
      g = document.createElement("span");
      g.className = "nav-glider";
      g.setAttribute("aria-hidden", "true");
      nav.insertBefore(g, nav.firstChild);
      nav.classList.add("glides");
    }
    const a = nav.querySelector(".nav-item.active");
    if (!a) { g.style.opacity = "0"; return; }
    g.style.opacity = "1";
    g.style.width = a.offsetWidth + "px";
    g.style.height = a.offsetHeight + "px";
    g.style.transform = "translate(" + a.offsetLeft + "px," + a.offsetTop + "px)";
  }

  function start() {
    const nav = document.querySelector(".nav");
    if (!nav) return;
    glide();
    new MutationObserver(glide).observe(nav, { attributes: true, attributeFilter: ["class"], subtree: true });
    window.addEventListener("resize", glide);
  }

  window.BioLook = { usePictures, loadPictures, glide };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
