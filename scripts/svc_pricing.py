# -*- coding: utf-8 -*-
"""Đồng bộ khối "Bảng giá tham khảo" trên các trang dịch vụ theo data/pricing.json (nguồn sự thật).
Idempotent. Chạy: python3 scripts/svc_pricing.py  (sau pricing_publish.py, trước tech_pass.py).
- Thay 3 gói cũ bằng các mức trong pricing.json (giá theo khoảng, đã gồm VAT; hosting/quảng cáo: Thương lượng).
- Không đụng trang traffic-user (không công khai giá Traffic User), chỉ bỏ cam kết "24 giờ".
- Bỏ các cam kết "phản hồi trong 24 giờ" / "báo giá trong 24h" trên trang dịch vụ và dich-vu.html.
"""
import json,re,pathlib,html
R=pathlib.Path(__file__).resolve().parent.parent
P=json.loads((R/'data/pricing.json').read_text())
CHK='<svg class="i " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
def num(v):
  if v>=1_000_000:
    s=f'{v/1_000_000:.2f}'.rstrip('0').rstrip('.').replace('.',','); return s,'triệu'
  s=f'{v/1000:.0f}'; return s,'nghìn'
def rng(a,b):
  (x,u1),(y,u2)=num(a),num(b)
  return f'{x}–{y} {u2}' if u1==u2 else f'{x} {u1} – {y} {u2}'
UNIT={'dự án':'/ dự án','tháng':'/ tháng','năm':'/ năm','địa điểm':'/ địa điểm','gói':'/ gói','bộ':'/ bộ','website':'/ website'}
OLD_BOLD='<b>Giá tham khảo, báo giá chính xác sau khi trao đổi.</b>'
def plans(s):
  T=s['tiers']; out=[]
  for i,t in enumerate(T):
    hl=' hl' if i==1 else ''
    badge='<span class=badge>Khuyên dùng</span>' if i==1 else ''
    if s.get('negotiable'):
      price='<div class="price" style="font-size:1.4rem">Thương lượng</div>'
    else:
      price=f'<div class="price">{rng(t["min"],t["max"])}<small>{UNIT.get(s["unit"],"/ "+s["unit"])}</small></div>'
    items=[x.strip() for x in re.split(r',\s*',t.get('includes','')) if x.strip()]
    items=[x[0].upper()+x[1:] for x in items]
    lis=''.join(f'<li>{CHK}{html.escape(x,quote=False)}</li>' for x in items)
    btn='btn ' if i==1 else 'btn ghost'
    out.append(f'<div class="plan glass rv{hl}">{badge}<h3>{html.escape(t["name"],quote=False)}</h3>{price}<ul>{lis}</ul><a class="{btn}" href="../lien-he.html">Đăng ký</a></div>')
  return '<div class="plans" data-src="pricing">'+''.join(out)+'</div>'
def note(s):
  b=f'<b>{P["vatNote"]}. {P["disclaimer"]}</b>'
  if s.get('negotiable'):
    b+=' '+('Chi phí quản lý quảng cáo được báo riêng theo ngân sách; chưa gồm tiền quảng cáo trả cho nền tảng.' if 'quang-cao' in s['id'] else 'Chi phí hosting/VPS được báo riêng sau khi trao đổi nhu cầu.')
  return b
def commit_fix(x):
  x=x.replace('Hỗ trợ ưu tiên trong giờ làm việc, phản hồi trong 24 giờ','Hỗ trợ ưu tiên trong giờ làm việc')
  x=x.replace('hỗ trợ kỹ thuật trong giờ làm việc, phản hồi trong 24 giờ.','hỗ trợ kỹ thuật trong giờ làm việc.')
  x=x.replace('<h3>Nhận báo giá trong 24h</h3>','<h3>Nhận báo giá</h3>')
  return x
def main():
  n=0
  for s in P['services']:
    f=R/'dich-vu'/f'{s["id"]}.html'
    if not f.exists(): print('thiếu',f); continue
    x=f.read_text(); o=x
    i=x.find('<div class="plans"'); j=x.find('<p class="muted rv" style="margin-top:18px">',i)
    assert i>0 and j>i, f
    x=x[:i]+plans(s)+x[j:]
    j=x.find('<p class="muted rv" style="margin-top:18px">',i)
    m=re.compile(r'<b>[^<]*</b>(?: Chi phí (?:quản lý quảng cáo được báo riêng theo ngân sách; chưa gồm tiền quảng cáo trả cho nền tảng|hosting/VPS được báo riêng sau khi trao đổi nhu cầu)\.)?').search(x,j)
    x=x[:m.start()]+note(s)+x[m.end():]
    x=commit_fix(x)
    if x!=o: f.write_text(x); n+=1
  for f in [R/'dich-vu/traffic-user.html',R/'dich-vu.html']:
    x=f.read_text(); y=commit_fix(x)
    if y!=x: f.write_text(y); n+=1
  print('svc_pricing: cập nhật',n,'file')

if __name__=='__main__': main()
