/* My Agent – giao diện công cụ tính giá combo (bang-gia.html#tinh-gia). Dữ liệu: data/pricing.json (bản công khai). */
(function () {
  'use strict';
  var d = document, L = d.getElementById('bg-list'); if (!L) return;
  var fm = function (v) { return Math.round(v).toLocaleString('vi-VN') + 'đ'; };
  var tr = function (v) { return (v / 1e6).toLocaleString('vi-VN', { maximumFractionDigits: 2 }); };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var B = { 'one-time': 'một lần', monthly: '/tháng', yearly: '/năm' };
  var src = (d.currentScript && d.currentScript.src) || '', v = (/[?&]v=([^&]+)/.exec(src) || [])[1] || '1';
  function opt(o, sel) { return Object.keys(o).map(function (k) { return '<option value="' + k + '"' + (k === sel ? ' selected' : '') + '>' + esc(o[k].label) + (o[k].percent && o[k].months ? ' (giảm ' + o[k].percent + '%)' : o[k].percent ? ' (+' + o[k].percent + '%)' : '') + '</option>'; }).join(''); }
  fetch('data/pricing.json?v=' + v).then(function (r) { return r.json(); }).then(function (P) {
    window.setPricingData(P);
    var R = P.rules, cat = '', h = '', i = 0;
    d.getElementById('bg-rush').innerHTML = opt(R.rush, 'binh-thuong');
    d.getElementById('bg-prepay').innerHTML = opt(R.prepay, 'monthly');
    P.services.forEach(function (s) {
      if (s.category !== cat) { if (cat) h += '</fieldset>'; cat = s.category; h += '<fieldset><legend>' + esc(cat) + '</legend>'; }
      var id = 'bg-' + s.id; i++;
      h += '<div class="bg-svc" data-id="' + s.id + '"><label class="bg-h"><input type="checkbox" id="' + id + '"> <span>' + esc(s.name) + ' <small>' + (s.negotiable ? '<b class="bg-negl">Thương lượng</b>' : esc(B[s.billing] || '')) + '</small></span></label><div class="bg-opts">';
      h += '<label>Gói<select class="tier">' + s.tiers.map(function (t) { return '<option value="' + t.id + '">' + esc(t.name) + ' · ' + (s.negotiable ? 'Thương lượng' : tr(t.min) + '–' + tr(t.max) + ' tr') + '</option>'; }).join('') + '</select></label>';
      if (s.complexityApplies) h += '<label>Độ phức tạp<select class="cx">' + opt(R.complexity, 'tieu-chuan') + '</select></label>';
      if (s.quantity) h += '<label>' + esc(s.quantity.label) + '<input class="qty" type="number" inputmode="numeric" min="0" max="999" value="' + (s.quantity.default || 0) + '"></label>';
      if (s.id === 'quang-cao-google-facebook') h += '<label>Ngân sách quảng cáo dự kiến (tùy chọn)<input class="budget" type="text" maxlength="60" placeholder="VD: 10–20 triệu/tháng"></label><p class="muted"><small>Chưa gồm tiền quảng cáo trả cho nền tảng.</small></p>';
      h += '</div></div>';
    });
    L.innerHTML = h + '</fieldset>';
    run();
    d.getElementById('bg-calc').addEventListener('input', run);
    d.getElementById('bg-calc').addEventListener('change', run);
  }).catch(function () { L.innerHTML = '<p>Không tải được dữ liệu giá. Bạn xem bảng giá phía trên hoặc <a href="lien-he.html">liên hệ</a> nhé.</p>'; });
  function val(el, c) { var x = el.querySelector(c); return x ? x.value : null; }
  function run() {
    var items = [];
    d.querySelectorAll('.bg-svc').forEach(function (el) {
      var on = el.querySelector('input[type=checkbox]').checked; el.classList.toggle('on', on); if (!on) return;
      items.push({ serviceId: el.dataset.id, tierId: val(el, '.tier'), complexity: val(el, '.cx'), quantity: val(el, '.qty') || 0, budgetNote: (val(el, '.budget') || '').slice(0, 60) });
    });
    var r = window.calculateCombo({ items: items, rush: d.getElementById('bg-rush').value, prepay: d.getElementById('bg-prepay').value });
    var any = r.items.length || r.negotiable.length;
    d.getElementById('bg-total').textContent = r.items.length ? fm(r.min) + ' – ' + fm(r.max) + (r.negotiable.length ? ' + khoản thương lượng' : '') : (r.negotiable.length ? 'Thương lượng' : 'Chưa chọn dịch vụ');
    var o = r.items.map(function (i) { return '<div class="row"><span>' + esc(i.service) + '<br><small class="muted">' + esc(i.tier) + (i.multiplier > 1 ? ' × ' + i.multiplier + (i.billing === 'yearly' ? ' năm' : ' tháng') : '') + (i.discountMax ? ' · giảm ' + i.linePercent + '%' : '') + '</small></span><span>' + fm(i.min) + '<br>– ' + fm(i.max) + '</span></div>'; }).join('');
    o += r.negotiable.map(function (n) { return '<div class="row"><span>' + esc(n.service) + '<br><small class="muted">' + esc(n.tier) + (n.budgetNote ? ' · Ngân sách: ' + esc(n.budgetNote) : '') + '</small></span><span class="bg-negl">Thương lượng</span></div>'; }).join('');
    if (any) {
      o += '<hr><div class="row"><span>Giảm combo (' + r.serviceCount + ' dịch vụ)</span><span>' + (r.discountPercent ? 'giảm ' + r.discountPercent + '%' : '—') + '</span></div>';
      o += '<div class="row"><span>Trả trước (' + esc(r.prepay.label) + ')</span><span>' + (r.prepayPercent ? 'giảm ' + r.prepayPercent + '%' : '—') + '</span></div>';
      if (r.rushPercent) o += '<div class="row"><span>Phụ phí gấp</span><span>+' + r.rushPercent + '%</span></div>';
      if (r.negotiable.length) o += '<p class="muted"><small>' + esc(r.negotiableNote) + '</small></p>';
    }
    d.getElementById('bg-detail').innerHTML = o;
    var a = d.getElementById('bg-send');
    if (!any) { a.href = 'lien-he.html#form'; a.setAttribute('aria-disabled', 'true'); return; }
    a.removeAttribute('aria-disabled');
    var list = r.items.map(function (i) { return i.service + ' (' + i.tier + ')'; }).concat(r.negotiable.map(function (n) { return n.service + ' (' + n.tier + ', thương lượng)'; }));
    var q = r.negotiable.filter(function (n) { return n.budgetNote; }).map(function (n) { return n.service + ': ' + n.budgetNote; });
    a.href = 'lien-he.html?tam-tinh=' + encodeURIComponent(r.items.length ? fm(r.min) + ' – ' + fm(r.max) : 'Thương lượng') +
      (q.length ? '&ngan-sach=' + encodeURIComponent(q.join('; ')) : '') +
      '&dich-vu=' + encodeURIComponent(list.join('; ') + ' · ' + r.prepay.label + (r.rushPercent ? ' · gấp +' + r.rushPercent + '%' : '')) + '#form';
  }
})();
