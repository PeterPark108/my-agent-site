/* GĐ0 – chỉ báo bước đang xem trong quy trình 5 cảnh. Không khóa cuộn.
   Tắt: data-fx-process="off". Snap proximity: data-fx-process-snap (mặc định off). */
(function () {
  "use strict";
  var h = document.documentElement, box = document.getElementById("quy-trinh");
  if (!box || h.getAttribute("data-fx-process") === "off") return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (matchMedia("(max-width: 860px)").matches) return;
  var steps = box.querySelectorAll(".q5-step");
  if (!steps.length) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var i = 0;
      steps.forEach(function (s, n) {
        var on = s === e.target;
        s.classList.toggle("is-on", on);
        if (on) i = n;
      });
      box.dataset.step = String(i + 1);
    });
  }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
  steps.forEach(function (s) { io.observe(s); });
})();
