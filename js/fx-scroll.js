/* GĐ0 – hiệu ứng cuộn trang chủ. Tắt từng phần: data-fx-reveal / parallax / progress = "off"
   (js/config.js + scripts/tech_pass.py). Không đụng H1 hero (giữ LCP). */
(function () {
  "use strict";
  var d = document, h = d.documentElement;
  function on(k) { return h.getAttribute("data-fx-" + k) !== "off"; }
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (on("progress") && !reduce) {
    var bar = d.querySelector(".fx-prog");
    if (bar) {
      var cssScroll = false;
      try { cssScroll = CSS.supports("animation-timeline: scroll()") || CSS.supports("animation-timeline", "scroll()"); } catch (e) {}
      if (!cssScroll) {
        var tick = 0;
        var paint = function () {
          tick = 0;
          var max = h.scrollHeight - innerHeight;
          bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, scrollY / max) : 0) + ")";
        };
        addEventListener("scroll", function () { if (!tick) { tick = 1; requestAnimationFrame(paint); } }, { passive: true });
        paint();
      } else {
        bar.classList.add("is-css");
      }
    }
  }

  if (on("reveal") && !reduce) {
    var viewOk = false;
    try { viewOk = CSS.supports("animation-timeline: view()") || CSS.supports("animation-timeline", "view()"); } catch (e2) {}
    if (!viewOk) {
      h.classList.add("fx-io");
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add("fx-in"); io.unobserve(e.target); }
        });
      }, { threshold: 0.2 });
      d.querySelectorAll("main section:not(.q5) .t").forEach(function (el) { io.observe(el); });
    }
  }
})();
