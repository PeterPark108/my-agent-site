/* My Agent – điền sẵn số liệu từ bang-gia.html#tinh-gia vào ô "nội dung" hiện có của form liên hệ.
   Không đổi form/endpoint; chỉ đọc ?tam-tinh=&ngan-sach=&dich-vu=. Không có ô phù hợp thì hiện bản tóm tắt để sao chép. */
(function () {
  'use strict';
  var q = new URLSearchParams(location.search), t = q.get('tam-tinh'); if (!t) return;
  var clip = function (s) { return String(s || '').replace(/[\u0000-\u001f<>]/g, ' ').slice(0, 400).trim(); };
  var dv = clip(q.get('dich-vu')), ns = clip(q.get('ngan-sach'));
  var txt = 'Tôi đã dùng công cụ tính giá trên website (bang-gia.html).\nTạm tính: ' + clip(t) + ' (đã gồm VAT, tham khảo)' +
    (dv ? '\nDịch vụ: ' + dv : '') + (ns ? '\nNgân sách quảng cáo dự kiến: ' + ns : '') + '\nNhờ My Agent báo giá chính xác. Nhu cầu cụ thể: ';
  function go() {
    var m = document.querySelector('form[data-contact] textarea[name="message"]') || document.querySelector('form textarea');
    if (m) { if (!m.value || m.value.indexOf('Nhu cầu cụ thể') >= 0) m.value = txt; return; }
    var b = document.createElement('div'); b.className = 'glass bg-copy';
    b.innerHTML = '<p><b>Số liệu từ công cụ tính giá</b> (sao chép và gửi cho My Agent):</p><textarea readonly rows="5"></textarea>';
    b.querySelector('textarea').value = txt;
    (document.querySelector('main') || document.body).prepend(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(go, 0); }); else setTimeout(go, 0);
})();
/* v0.9.5 – điền sẵn gói từ nút "Đăng ký" trên trang dịch vụ/combo: ?goi-dv=<id dịch vụ>&goi=<id gói>[&ky=6] hoặc ?combo=<id>.
   Giá chỉ lấy từ data/pricing.json (không lấy từ URL). Tham số chỉ là id [a-z0-9-], tối đa 40 ký tự; id lạ thì bỏ qua. Chỉ dùng .value. */
(function () {
  'use strict';
  var q = new URLSearchParams(location.search);
  if (q.get('tam-tinh')) return; // luồng công cụ tính giá được ưu tiên
  var id = function (k) { var v = String(q.get(k) || '').toLowerCase(); return /^[a-z0-9-]{1,40}$/.test(v) ? v : ''; };
  var sv = id('goi-dv'), tr = id('goi'), cb = id('combo'), ky = parseInt(q.get('ky'), 10);
  // v0.9.8: gói web-app (Thiết kế website) đã gộp vào Phần mềm nội bộ gói 2; link/bookmark cũ vẫn điền sẵn đúng gói mới
  if (tr === 'web-app' && (!sv || sv === 'thiet-ke-website')) { sv = 'phan-mem-noi-bo'; tr = 'tieu-chuan'; }
  if (!(sv && tr) && !cb) return;
  var norm = function (s) { return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/[^a-z0-9]+/g, ' ').trim(); };
  var ALIAS = { 'quang-cao-google-facebook': 'ads google facebook' };
  function pick(sel, name, sid) {
    if (!sel) return;
    var n = ALIAS[sid] || norm(name), best = null;
    [].forEach.call(sel.options, function (o) { var v = norm(o.value); if (!best && v && (v === n || n.indexOf(v) >= 0 || v.indexOf(n) >= 0)) best = o; });
    if (best) { sel.value = best.value; sel.dispatchEvent(new Event('change', { bubbles: true })); }
  }
  function num(v) { if (v >= 1e6) return [String(+(v / 1e6).toFixed(2)).replace('.', ','), 'triệu']; return [String(Math.round(v / 1000)), 'nghìn']; }
  function rng(a, b) { var x = num(a), y = num(b); return x[1] === y[1] ? x[0] + '–' + y[0] + ' ' + y[1] : x[0] + ' ' + x[1] + ' – ' + y[0] + ' ' + y[1]; }
  function fill(txt, name, sid) {
    var f = document.querySelector('form[data-contact]'); if (!f) return;
    var m = f.querySelector('textarea[name="message"]');
    pick(f.querySelector('select[name="service"]'), name, sid);
    if (m && (!m.value || m.value.indexOf('Nhu cầu cụ thể') >= 0)) m.value = txt.slice(0, 1500);
    f.setAttribute('data-prefill', sid);
    try { f.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); } catch (e) {}
  }
  function run() {
    if (cb) {
      var o = null, sel = document.querySelector('form[data-contact] select[name="service"]');
      var opts = sel ? [].filter.call(sel.options, function (x) { return /^Combo /.test(x.value) && norm(x.value.slice(6)) === cb.replace(/-/g, ' '); }) : [];
      if (!opts.length) return; o = opts[0].value;
      return fill('Tôi muốn đăng ký ' + o + '. Nhờ My Agent báo giá chính xác (giá đã gồm VAT, tham khảo). Nhu cầu cụ thể: ', o, cb);
    }
    fetch('data/pricing.json', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (P) {
      if (!P || !P.services) return;
      var s = P.services.filter(function (x) { return x.id === sv; })[0]; if (!s) return;
      var t = (s.tiers || []).filter(function (x) { return x.id === tr; })[0]; if (!t) return;
      var unit = s.unit ? ' / ' + s.unit : '';
      var price = s.negotiable ? 'Thương lượng' : rng(t.min, t.max) + unit + (P.vatIncluded ? ' (đã gồm VAT, tham khảo)' : ' (tham khảo)');
      var cyc = '';
      if (s.billing === 'monthly') cyc = '\nChu kỳ: theo tháng' + ([6, 12, 24].indexOf(ky) >= 0 ? ', đăng ký ' + ky + ' tháng' : '') + ' (thanh toán trước theo kỳ).';
      else if (s.billing === 'yearly') cyc = '\nChu kỳ: theo năm' + ([1, 2].indexOf(ky) >= 0 ? ', đăng ký ' + ky + ' năm' : '') + ' (thanh toán trước theo kỳ).';
      fill('Tôi muốn đăng ký gói ' + t.name + ' của dịch vụ ' + s.name + '.\nGiá tham khảo: ' + price + '.' + cyc +
        '\nNhờ My Agent báo giá chính xác. Nhu cầu cụ thể: ', s.name, s.id);
    }).catch(function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(run, 0); }); else setTimeout(run, 0);
})();
