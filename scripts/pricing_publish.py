#!/usr/bin/env python3
"""Xuất dữ liệu bảng giá CÔNG KHAI từ nguồn nội bộ (whitelist trường) + chép hàm tính.
Chạy: python3 scripts/pricing_publish.py /workspace/bang-gia   (thư mục chứa pricing.json, combo-calculator.js)
KHÔNG chép nguyên pricing.json: bỏ positioning, sources, formula, mọi ghi chú so sánh thị trường/giá vốn.
Không bao giờ đưa Traffic User, sheet "Nội bộ", file .xlsx lên web (xem docs/bang-gia.md)."""
import sys,json,re,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
src=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '/workspace/bang-gia')
P=json.loads((src/'pricing.json').read_text())
BAD=re.compile(r'thị trường|trung vị|giá vốn|\bvốn\b|×\s?0,8|x0,8|nội bộ - không|traffic|lợi nhuận|biên lợi|margin|cost',re.I)
REWRITE={'Cam kết top cố định':'Không hứa thứ hạng cố định trên Google'}
def clean(t):
  t=REWRITE.get(str(t or '').strip(),t)
  t=re.sub(r'\s*\((?:thị trường|TT)[^)]*\)','',str(t or '')).strip()
  if BAD.search(t): raise SystemExit(f'Chuỗi không được công khai: {t!r}')
  return t
RULES=('comboDiscount','maxDiscountPercent','maxDiscountAmount','complexity','rush','roundTo','prepay','maxLineDiscountPercent','negotiableNote')
TIER=('id','name','min','max','time','includes','excludes')
SVC=('id','category','name','unit','billing','quantity','complexityApplies','discountable','negotiable','priceLabel','negotiableNote')
out={'version':P['version'],'currency':P.get('currency','VND'),'vatIncluded':False,'vatNote':'Giá chưa bao gồm VAT',
     'disclaimer':'Giá chỉ mang tính tham khảo theo khoảng, báo giá chính xác sau khi trao đổi nhu cầu.',
     'rules':{k:P['rules'][k] for k in RULES if k in P['rules']},'services':[]}
out['rules']['negotiableNote']=clean(out['rules'].get('negotiableNote',''))
for s in P['services']:
  if re.search(r'traffic',s['id']+s['name'],re.I): continue
  o={k:s[k] for k in SVC if k in s}
  for k in ('name','category','negotiableNote','priceLabel'):
    if k in o: o[k]=clean(o[k])
  if o.get('quantity'): o['quantity']=dict(o['quantity'],label=clean(o['quantity'].get('label','')))
  o['tiers']=[]
  for t in s['tiers']:
    x={k:t[k] for k in TIER if k in t}
    if s.get('negotiable'): x.pop('min',None); x.pop('max',None)
    for k in ('name','time','includes','excludes'):
      if k in x: x[k]=clean(x[k])
    o['tiers'].append(x)
  out['services'].append(o)
(R/'data/pricing.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
js=(src/'combo-calculator.js').read_text()
js=re.sub(r"\n\s*try \{ DEFAULT = require\('\./pricing\.json'\); \} catch \(e\) \{\}",'',js)
(R/'js/combo-calculator.js').write_text(js)
print('pricing:',len(out['services']),'dịch vụ ->data/pricing.json; js/combo-calculator.js')
