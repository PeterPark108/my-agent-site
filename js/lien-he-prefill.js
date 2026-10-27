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
