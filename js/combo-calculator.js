/* My Agent – Tính giá combo tham khảo (JS thuần, giá đã gồm VAT).
 * calculateCombo({items:[{serviceId,tierId,complexity,quantity,budgetNote}], rush, prepay}[, pricing])
 * -> {min,max,discountPercent,items[], ...} */
(function (root) {
  'use strict';
  var DEFAULT = null;
  function rnd(x, step, up) { return (up ? Math.ceil(x / step) : Math.floor(x / step)) * step; }
  function calculateCombo(selection, pricing) {
    pricing = pricing || DEFAULT;
    if (!pricing) throw new Error('Thiếu dữ liệu pricing');
    var R = pricing.rules, sel = selection || {}, list = sel.items || [];
    var pp = R.prepay[sel.prepay] || R.prepay.monthly, months = pp.months;
    var years = Math.max(1, Math.ceil(months / 12));
    var yearPct = years >= 2 ? R.prepay['24m'].percent : 0;
    var rush = R.rush[sel.rush] || R.rush['binh-thuong'];
    var CAP = R.maxLineDiscountPercent || 25;
    var lines = [], seen = {}, negotiable = [];
    list.forEach(function (it) {
      var svc = pricing.services.find(function (s) { return s.id === it.serviceId; });
      if (!svc) return;
      var tier = svc.tiers.find(function (t) { return t.id === it.tierId; }) || svc.tiers[0];
      if (svc.negotiable) { negotiable.push({ serviceId: svc.id, service: svc.name, tierId: tier.id, tier: tier.name,
        priceLabel: svc.priceLabel || 'Thương lượng', note: svc.negotiableNote || '', budgetNote: it.budgetNote || '' }); seen[svc.id] = 1; return; }
      var lo, hi, mult = 1, extra = {};
      {
        var cx = svc.complexityApplies ? (R.complexity[it.complexity] || R.complexity['tieu-chuan']).factor : 1;
        lo = tier.min * cx; hi = tier.max * cx;
        var q = svc.quantity, n = Math.max(0, parseInt(it.quantity, 10) || 0);
        if (q) {
          if (q.multiplyAll || (q.multiplyTier && q.multiplyTier.indexOf(tier.id) >= 0)) { n = Math.max(1, n || q.default || 1); lo *= n; hi *= n; }
          else if (q.perUnitMin) { lo += n * q.perUnitMin; hi += n * q.perUnitMax; }
        }
        mult = svc.billing === 'monthly' ? months : svc.billing === 'yearly' ? years : 1;
      }
      var L = { serviceId: svc.id, service: svc.name, tierId: tier.id, tier: tier.name, billing: svc.billing, unit: svc.unit,
        unitMin: Math.round(lo), unitMax: Math.round(hi), multiplier: mult,
        grossMin: Math.round(lo * mult), grossMax: Math.round(hi * mult), discountType: null, linePercent: 0 };
      for (var k in extra) L[k] = extra[k];
      if (svc.billing === 'monthly') { L.discountType = 'prepay'; L.linePercent = pp.percent; }
      else if (svc.billing === 'yearly') { L.discountType = 'prepay'; L.linePercent = yearPct; }
      else if (svc.billing === 'one-time' && svc.discountable) L.discountType = 'combo';
      lines.push(L); seen[svc.id] = 1;
    });
    var count = Object.keys(seen).length, comboPct = 0;
    R.comboDiscount.forEach(function (b) { if (count >= b.minServices) comboPct = b.percent; });
    comboPct = Math.min(comboPct, R.maxDiscountPercent);
    var comboBase = [0, 0];
    lines.forEach(function (L) { if (L.discountType === 'combo') { comboBase[0] += L.grossMin; comboBase[1] += L.grossMax; } });
    if (!comboBase[1]) comboPct = 0;
    // trần tuyệt đối combo: quy về % hiệu dụng cho từng biên
    var effMin = comboBase[0] ? Math.min(comboPct, R.maxDiscountAmount / comboBase[0] * 100) : 0;
    var effMax = comboBase[1] ? Math.min(comboPct, R.maxDiscountAmount / comboBase[1] * 100) : 0;
    var tot = { one: [0, 0], rec: [0, 0], disc: [0, 0], monthly: [0, 0] };
    lines.forEach(function (L) {
      var pMin = L.discountType === 'combo' ? effMin : L.linePercent, pMax = L.discountType === 'combo' ? effMax : L.linePercent;
      if (L.discountType === 'combo') L.linePercent = comboPct;
      pMin = Math.min(pMin, CAP); pMax = Math.min(pMax, CAP);
      L.discountMin = Math.round(L.grossMin * pMin / 100); L.discountMax = Math.round(L.grossMax * pMax / 100);
      L.min = L.grossMin - L.discountMin; L.max = L.grossMax - L.discountMax;
      if (L.min > L.max) L.min = L.max;
      tot.disc[0] += L.discountMin; tot.disc[1] += L.discountMax;
      var b = L.billing === 'one-time' ? tot.one : tot.rec;
      b[0] += L.min; b[1] += L.max;
      if (L.billing === 'monthly') { tot.monthly[0] += L.unitMin; tot.monthly[1] += L.unitMax; }
    });
    var rushAmt = [tot.one[0] * rush.percent / 100, tot.one[1] * rush.percent / 100];
    var step = R.roundTo || 100000;
    var min = rnd(tot.one[0] + rushAmt[0] + tot.rec[0], step, false);
    var max = rnd(tot.one[1] + rushAmt[1] + tot.rec[1], step, true);
    if (min > max) min = max;
    return { min: min, max: max, discountPercent: comboPct, prepayPercent: pp.percent, prepayYearPercent: yearPct,
      prepay: { label: pp.label, months: months, years: years }, serviceCount: count, items: lines,
      oneTime: { min: Math.round(tot.one[0] + rushAmt[0]), max: Math.round(tot.one[1] + rushAmt[1]) },
      recurring: { min: tot.rec[0], max: tot.rec[1] }, negotiable: negotiable, negotiableNote: negotiable.length ? R.negotiableNote : '',
      monthlyRunRate: { min: tot.monthly[0], max: tot.monthly[1] },
      discountAmount: { min: tot.disc[0], max: tot.disc[1] },
      rushPercent: rush.percent, rushAmount: { min: Math.round(rushAmt[0]), max: Math.round(rushAmt[1]) },
      vatIncluded: true,
      note: 'Giá chỉ mang tính tham khảo theo khoảng, báo giá chính xác sau khi trao đổi nhu cầu. Giá đã bao gồm VAT.' };
  }
  function setPricing(p) { DEFAULT = p; }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { calculateCombo: calculateCombo, setPricing: setPricing };
  } else { root.calculateCombo = calculateCombo; root.setPricingData = setPricing; if (root.PRICING) DEFAULT = root.PRICING; }
})(typeof window !== 'undefined' ? window : this);
