/* =======================================================================
   CropAI — Animation engine (vanilla JS, no dependencies)
   Additive only: attaches behaviour to existing markup, never rewrites it.
   ======================================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------ helpers */
  function each(sel, fn, root) {
    Array.prototype.forEach.call((root || document).querySelectorAll(sel), fn);
  }

  /* ------------------------------------------------ 1. scroll reveal */
  var revealTargets = [
    ".stats-section .stat-box",
    ".l-footer",
    ".dash-grid > .dash-card",
    ".report-grid > .report-card",
    ".action-plan",
    ".history-wrap",
    ".profile-wrap > *",
    ".advisory-form",
    "#recentHistory",
  ].join(",");

  var io = null;
  if ("IntersectionObserver" in window && !reduced) {
    io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          var el = e.target;
          var d = parseInt(el.getAttribute("data-ca-delay") || "0", 10);
          setTimeout(function () {
            el.classList.add("ca-in");
          }, d);
          io.unobserve(el);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
  }

  function observe(root) {
    each(
      revealTargets,
      function (el, i) {
        if (el.hasAttribute("data-ca-reveal")) return;
        if (el.closest(".ca-no-reveal")) return;
        el.setAttribute("data-ca-reveal", el.getAttribute("data-ca-anim") || "up");
        el.setAttribute("data-ca-delay", String(Math.min(i, 8) * 70));
        if (io) io.observe(el);
        else el.classList.add("ca-in");
      },
      root
    );
  }

  /* ------------------------------------------------ 2. count-up numbers */
  function countUp(el) {
    var raw = (el.textContent || "").trim();
    var m = raw.match(/-?[\d,]*\.?\d+/);
    if (!m) return;
    var target = parseFloat(m[0].replace(/,/g, ""));
    if (!isFinite(target) || target === 0) return;
    var prefix = raw.slice(0, m.index);
    var suffix = raw.slice(m.index + m[0].length);
    var decimals = (m[0].split(".")[1] || "").length;
    var grouped = m[0].indexOf(",") > -1;
    var dur = 1100,
      start = null;

    function fmt(v) {
      var s = decimals ? v.toFixed(decimals) : String(Math.round(v));
      if (grouped) s = Number(s).toLocaleString("en-IN");
      return prefix + s + suffix;
    }
    if (reduced) return;
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * eased);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = raw;
    }
    el.textContent = fmt(0);
    requestAnimationFrame(step);
  }

  var countIO = null;
  if ("IntersectionObserver" in window) {
    countIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          countUp(e.target);
          countIO.unobserve(e.target);
        });
      },
      { threshold: 0.4 }
    );
  }

  function wireCounters(root) {
    each(
      ".stat-num, .sbar-num, .score-num",
      function (el) {
        if (el.getAttribute("data-ca-counted")) return;
        var txt = (el.textContent || "").trim();
        if (!txt || txt === "—" || !/\d/.test(txt)) return;
        el.setAttribute("data-ca-counted", "1");
        if (countIO) countIO.observe(el);
        else countUp(el);
      },
      root
    );
  }

  /* ------------------------------------------------ 3. button ripple */
  document.addEventListener("click", function (ev) {
    if (reduced) return;
    var btn = ev.target.closest(
      ".btn-cta,.btn-cta-outline,.btn-nav,.btn-small,.auth-btn,.view-btn,.btn-small-green,.pdf-btn"
    );
    if (!btn) return;
    var cs = getComputedStyle(btn);
    if (cs.position === "static") btn.style.position = "relative";
    if (cs.overflow !== "hidden") btn.style.overflow = "hidden";
    var r = btn.getBoundingClientRect();
    var span = document.createElement("span");
    span.className = "ca-ripple";
    span.style.left = ev.clientX - r.left + "px";
    span.style.top = ev.clientY - r.top + "px";
    btn.appendChild(span);
    setTimeout(function () {
      span.remove();
    }, 620);
  });

  /* ------------------------------------------------ 4. confidence bars grow */
  function wireBars(root) {
    each(
      ".conf-bar",
      function (el) {
        if (el.getAttribute("data-ca-bar")) return;
        el.setAttribute("data-ca-bar", "1");
        var w = el.style.width;
        if (!w) return;
        el.style.width = "0px";
        requestAnimationFrame(function () {
          el.style.transition = "width 1s cubic-bezier(.22,.9,.28,1)";
          el.style.width = w;
        });
      },
      root
    );
  }

  /* ------------------------------------------------ 5. floating leaves (landing/auth) */
  function leaves() {
    if (reduced) return;
    if (!document.body.classList.contains("landing-page")) return;
    var layer = document.createElement("div");
    layer.className = "ca-leaves";
    var glyphs = ["🌿", "🍃", "🌾", "🍂"];
    for (var i = 0; i < 14; i++) {
      var s = document.createElement("span");
      s.className = "ca-leaf";
      s.textContent = glyphs[i % glyphs.length];
      s.style.left = Math.random() * 100 + "vw";
      s.style.fontSize = 0.8 + Math.random() * 1.3 + "rem";
      s.style.setProperty("--ca-drift", (Math.random() * 160 - 80).toFixed(0) + "px");
      s.style.animationDuration = 14 + Math.random() * 18 + "s";
      s.style.animationDelay = "-" + (Math.random() * 20).toFixed(1) + "s";
      s.style.opacity = (0.12 + Math.random() * 0.2).toFixed(2);
      layer.appendChild(s);
    }
    document.body.insertBefore(layer, document.body.firstChild);
  }

  /* ------------------------------------------------ 6. scroll progress + back to top */
  function chrome() {
    var bar = document.createElement("div");
    bar.className = "ca-progress";
    document.body.appendChild(bar);

    var top = document.createElement("button");
    top.className = "ca-top";
    top.type = "button";
    top.setAttribute("aria-label", "Back to top");
    top.innerHTML = "↑";
    top.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
    document.body.appendChild(top);

    function onScroll() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var y = window.scrollY || 0;
      bar.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
      top.classList.toggle("ca-show", y > 320);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------ 7. form busy state */
  function wireForms() {
    each("form", function (f) {
      f.addEventListener("submit", function () {
        var b = f.querySelector('button[type=submit],.auth-btn,button:not([type="button"])');
        if (b && !b.disabled) {
          b.classList.add("ca-busy");
          var old = b.innerHTML;
          b.innerHTML = "⏳ Working…";
          setTimeout(function () {
            b.classList.remove("ca-busy");
            b.innerHTML = old;
          }, 12000);
        }
      });
    });
  }

  /* ------------------------------------------------ 8. drag & drop highlight */
  function wireUpload() {
    each(".upload-area", function (a) {
      ["dragenter", "dragover"].forEach(function (t) {
        a.addEventListener(t, function (e) {
          e.preventDefault();
          a.classList.add("ca-dragging");
        });
      });
      ["dragleave", "drop"].forEach(function (t) {
        a.addEventListener(t, function () {
          a.classList.remove("ca-dragging");
        });
      });
    });
  }

  /* ------------------------------------------------ 9. watch dynamic content */
  function watch() {
    if (!("MutationObserver" in window)) return;
    var mo = new MutationObserver(function (muts) {
      var touched = false;
      muts.forEach(function (m) {
        Array.prototype.forEach.call(m.addedNodes, function (n) {
          if (n.nodeType === 1) touched = true;
        });
      });
      if (!touched) return;
      wireCounters(document);
      wireBars(document);
      observe(document);
      wireUpload();
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }

  /* ------------------------------------------------ boot */
  function init() {
    leaves();
    chrome();
    observe(document);
    wireCounters(document);
    wireBars(document);
    wireForms();
    wireUpload();
    watch();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
