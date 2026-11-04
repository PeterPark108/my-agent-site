/* GĐ0 – hero "Web của bạn trông thế này".
   Cờ: data-fx-tilt, data-fx-logo, data-fx-color, data-fx-send.
   Logo chỉ hiện qua <img> (object URL). Màu chủ đạo đọc trên máy khách, không gửi tệp. */
(function () {
  "use strict";
  var d = document, h = d.documentElement;
  h.classList.remove("no-js");
  var root = d.getElementById("hero");
  if (!root || !root.classList.contains("ma-hero")) return;
  function on(k) { return h.getAttribute("data-fx-" + k) !== "off"; }
  function $(id) { return d.getElementById(id); }
  var MAX = 2097152;
  var TYPES = ["image/png", "image/jpeg", "image/webp", "image/svg+xml"];
  var COPY = {
    cafe: ["#B5562B", "Quán ăn, cà phê", "Góc nhỏ cho buổi sáng của bạn", "Thực đơn trong ngày, đặt bàn nhanh, chỉ đường tới quán.", "Xem thực đơn", ["Thực đơn", "Không gian", "Đặt bàn"], "split"],
    clinic: ["#2F7FB8", "Phòng khám, làm đẹp", "Chăm sóc tận tâm, đặt lịch dễ dàng", "Giới thiệu dịch vụ, đội ngũ và giờ làm việc rõ ràng.", "Đặt lịch hẹn", ["Dịch vụ", "Đội ngũ", "Đặt lịch"], "center"],
    interior: ["#7A6A4F", "Nội thất, xây dựng", "Không gian sống theo cách của bạn", "Dự án mẫu, quy trình thi công và nhận tư vấn.", "Xem dự án", ["Dự án", "Quy trình", "Tư vấn"], "split"],
    edu: ["#5B4BB7", "Giáo dục, đào tạo", "Học đúng điều bạn cần", "Khóa học, lịch khai giảng và đăng ký học thử.", "Xem khóa học", ["Khóa học", "Lịch học", "Đăng ký"], "center"],
    service: ["#0F8F85", "Dịch vụ, doanh nghiệp", "Giải pháp rõ ràng cho doanh nghiệp", "Dịch vụ, cách làm việc và kênh liên hệ nhanh.", "Nhận tư vấn", ["Dịch vụ", "Cách làm", "Liên hệ"], "split"],
    shop: ["#C2185B", "Bán hàng online", "Sản phẩm bạn yêu, giao tận nơi", "Danh mục, khuyến mãi và đặt hàng qua Zalo.", "Mua ngay", ["Sản phẩm", "Ưu đãi", "Đặt hàng"], "center"]
  };
  var site = $("ma-site"), ten = $("ma-ten"), live = $("ma-live");
  var logoUrl = null, logoColor = null;

  function rgb(hex) {
    var n = parseInt(hex.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function hex(c) {
    return "#" + c.map(function (v) {
      v = Math.round(Math.max(0, Math.min(255, v)));
      return (v + 256).toString(16).slice(1);
    }).join("");
  }
  function channel(v) {
    v /= 255;
    return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  }
  function lum(c) { return 0.2126 * channel(c[0]) + 0.7152 * channel(c[1]) + 0.0722 * channel(c[2]); }
  function cr(a, b) {
    var x = lum(a), y = lum(b);
    return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
  }
  function mix(a, b, t) { return a.map(function (v, i) { return v + (b[i] - v) * t; }); }
  var WHITE = [255, 255, 255], INK = [20, 32, 31];
  function palette(base) {
    var p = rgb(base), fg = null, n = 0;
    while (n < 24) {
      if (cr(p, WHITE) >= 4.5) { fg = WHITE; break; }
      if (cr(p, INK) >= 4.5 && lum(p) > 0.35) { fg = INK; break; }
      p = mix(p, INK, 0.08);
      n++;
    }
    if (!fg) fg = WHITE;
    var soft = mix(rgb(base), WHITE, 0.88);
    var ink = mix(rgb(base), INK, 0.55);
    var g = 0;
    while (cr(ink, soft) < 7 && g < 24) { ink = mix(ink, INK, 0.12); g++; }
    return { p: hex(p), pt: hex(fg), ps: hex(soft), pi: hex(ink) };
  }
  function paint(base) {
    var c = palette(base), s = site.style;
    s.setProperty("--p", c.p);
    s.setProperty("--pt", c.pt);
    s.setProperty("--ps", c.ps);
    s.setProperty("--pi", c.pi);
  }
  function dominant(img) {
    try {
      var cv = d.createElement("canvas"), size = 48, x = cv.getContext("2d", { willReadFrequently: true });
      cv.width = cv.height = size;
      x.drawImage(img, 0, 0, size, size);
      var px = x.getImageData(0, 0, size, size).data, bag = {}, best = null, bc = 0, i;
      for (i = 0; i < px.length; i += 4) {
        var r = px[i], g = px[i + 1], b = px[i + 2], a = px[i + 3];
        if (a < 128) continue;
        var hi = Math.max(r, g, b), lo = Math.min(r, g, b);
        if (hi - lo < 40 || (hi > 245 && lo > 200) || hi < 30) continue;
        var key = (r >> 4) + "," + (g >> 4) + "," + (b >> 4);
        var e = bag[key] || (bag[key] = [0, 0, 0, 0]);
        e[0] += r; e[1] += g; e[2] += b; e[3]++;
        if (e[3] > bc) { bc = e[3]; best = e; }
      }
      return bc >= size * size * 0.02 ? hex([best[0] / bc, best[1] / bc, best[2] / bc]) : null;
    } catch (err) { return null; }
  }
  function slug(s) {
    return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/gi, "d").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 30);
  }
  function render() {
    var picked = d.querySelector("input[name=nganh]:checked");
    var key = (picked && COPY[picked.value]) ? picked.value : "cafe";
    var t = COPY[key];
    var name = (ten.value || "").trim().slice(0, 40) || "Tên của bạn";
    root.dataset.industry = key;
    site.dataset.layout = t[6];
    $("sName").textContent = name;
    $("sMark").textContent = name.charAt(0).toUpperCase();
    $("sKicker").textContent = t[1];
    $("sTitle").textContent = t[2];
    $("sSub").textContent = t[3];
    $("sBtn").textContent = t[4];
    var cards = $("sCards").children;
    for (var i = 0; i < 3; i++) cards[i].textContent = t[5][i];
    $("sUrl").textContent = (slug(name) || "ten-cua-ban") + ".vn";
    paint(on("color") && logoColor ? logoColor : t[0]);
    if (live) live.textContent = "Bản minh họa, ngành " + t[1] + ", tên " + name + ".";
  }
  var wait;
  ten.addEventListener("input", function () { clearTimeout(wait); wait = setTimeout(render, 120); });
  d.querySelectorAll("input[name=nganh]").forEach(function (r) { r.addEventListener("change", render); });

  var msg = $("ma-logo-msg"), drop = $("ma-drop"), inp = $("ma-logo");
  function say(text, ok) { if (!msg) return; msg.textContent = text; msg.className = "ma-msg" + (ok ? " ok" : ""); }
  function clearLogo() {
    if (logoUrl) URL.revokeObjectURL(logoUrl);
    logoUrl = null;
    logoColor = null;
    var old = $("sLogo").querySelector("img");
    if (old) old.remove();
    $("sMark").hidden = false;
  }
  function take(file) {
    if (!file) return;
    if (TYPES.indexOf(file.type) < 0) { say("Tệp này chưa dùng được. Anh chị chọn ảnh PNG, JPG, WebP hoặc SVG."); return; }
    if (file.size > MAX) { say("Logo hơi nặng (" + (file.size / 1048576).toFixed(1) + "MB). Anh chị chọn tệp dưới 2MB."); return; }
    clearLogo();
    logoUrl = URL.createObjectURL(file);
    var im = new Image();
    im.alt = "";
    im.decoding = "async";
    im.onload = function () {
      $("sMark").hidden = true;
      $("sLogo").appendChild(im);
      logoColor = on("color") ? dominant(im) : null;
      say(logoColor ? "Đã hiện logo và màu chủ đạo trên bản minh họa. Tệp chỉ nằm trên máy này." : "Đã hiện logo. Logo ít màu nên giữ bảng màu của ngành.", 1);
      render();
    };
    im.onerror = function () { clearLogo(); say("Không đọc được ảnh này. Anh chị thử tệp khác."); };
    im.src = logoUrl;
  }
  if (on("logo") && drop && inp) {
    inp.addEventListener("change", function () { take(inp.files && inp.files[0]); inp.value = ""; });
    drop.addEventListener("click", function () { inp.click(); });
    drop.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); inp.click(); }
    });
    ["dragenter", "dragover"].forEach(function (t) {
      drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add("over"); });
    });
    ["dragleave", "drop"].forEach(function (t) {
      drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.remove("over"); });
    });
    drop.addEventListener("drop", function (e) {
      var f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      take(f);
    });
  } else if ($("ma-logo-field")) {
    $("ma-logo-field").hidden = true;
  }
  var reset = $("ma-reset");
  if (reset) reset.addEventListener("click", function () {
    clearLogo();
    say("");
    ten.value = "";
    var cafe = d.querySelector('input[name=nganh][value=cafe]');
    if (cafe) cafe.checked = true;
    render();
    ten.focus();
  });

  var form = $("ma-ctl");
  if (form) form.addEventListener("submit", function (e) {
    if (!on("send")) return;
    e.preventDefault();
    var key = root.dataset.industry || "cafe";
    var name = (ten.value || "").trim().slice(0, 40);
    location.href = "lien-he.html?nganh=" + encodeURIComponent(key) + "&ten=" + encodeURIComponent(name) + "#form";
  });

  var stage = $("ma-stage"), frame = $("ma-browser");
  var fine = matchMedia("(hover: hover) and (pointer: fine) and (min-width: 861px)");
  var motion = matchMedia("(prefers-reduced-motion: reduce)");
  var raf = 0;
  if (on("tilt") && stage && frame) {
    stage.addEventListener("pointermove", function (e) {
      if (motion.matches || !fine.matches || e.pointerType === "touch" || raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = frame.getBoundingClientRect();
        if (!r.width || !r.height) return;
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        frame.style.setProperty("--ry", (x * 8 - 3).toFixed(2) + "deg");
        frame.style.setProperty("--rx", (-y * 6 + 2).toFixed(2) + "deg");
      });
    });
    stage.addEventListener("pointerleave", function () {
      frame.style.removeProperty("--ry");
      frame.style.removeProperty("--rx");
    });
  }
  render();
})();
