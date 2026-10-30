# -*- coding: utf-8 -*-
"""Đồng bộ khối "Bảng giá tham khảo" trên các trang dịch vụ theo data/pricing.json (nguồn sự thật).
Idempotent. Chạy: python3 scripts/svc_pricing.py  (sau pricing_publish.py, trước tech_pass.py).
- Thay 3 gói cũ bằng các mức trong pricing.json (giá theo khoảng, chưa gồm VAT; hosting/quảng cáo: Thương lượng).
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
    out.append(f'<div class="plan glass rv{hl}">{badge}<h3>{html.escape(t["name"],quote=False)}</h3>{price}<ul>{lis}</ul><a class="{btn}" href="../lien-he.html?goi-dv={s["id"]}&amp;goi={t["id"]}#form">Đăng ký</a></div>')
  return '<div class="plans" data-src="pricing">'+''.join(out)+'</div>'
RECUR={'monthly':'tháng','yearly':'năm'}
ONEOFF_DEF='Đặt cọc 30–50%, phần còn lại thanh toán khi nghiệm thu. Mỗi gói gồm 2 lần chỉnh sửa trong phạm vi đã thống nhất; sửa thêm hoặc thêm tính năng sẽ báo giá trước. Bảo hành lỗi kỹ thuật 60 ngày sau bàn giao. Sau khi thanh toán đủ, khách sở hữu mã nguồn, nội dung và tài khoản liên quan.'
ONEOFF_DATA='Đặt cọc 30–50%, phần còn lại thanh toán khi nghiệm thu. Mỗi gói gồm 2 lần chỉnh sửa trong phạm vi đã thống nhất; thêm nguồn dữ liệu hoặc báo cáo mới sẽ báo giá trước. Bảo hành lỗi kỹ thuật 60 ngày sau bàn giao. Sau khi thanh toán đủ, khách sở hữu mã nguồn, báo cáo và dữ liệu.'
TAIL='Các khoản khác tính riêng theo <a href="../bang-gia.html">Bảng giá</a>: tên miền có giá riêng; hosting/VPS và quảng cáo: Thương lượng; tiền quảng cáo trả cho nền tảng không nằm trong giá.'
def is_recurring(s): return s.get('billing') in RECUR
def terms(s):
  b=s.get('billing')
  if b=='monthly': return 'Dịch vụ tính phí theo tháng: thanh toán 100% trước theo kỳ đã chọn (tháng, 6, 12 hoặc 24 tháng), không đặt cọc.'
  if b=='yearly': return 'Dịch vụ tính phí theo năm: thanh toán 100% trước theo kỳ đăng ký hoặc gia hạn (1 hoặc 2 năm), không đặt cọc.'
  return ONEOFF_DATA if s['id'] in ('phan-tich-du-lieu','ky-thuat-du-lieu') else ONEOFF_DEF
def note(s):
  b=f'<b>{P["vatNote"]}. {P["disclaimer"]}</b>'
  if s.get('negotiable'):
    b+=' '+('Chi phí quản lý quảng cáo được báo riêng theo ngân sách; chưa gồm tiền quảng cáo trả cho nền tảng.' if 'quang-cao' in s['id'] else 'Chi phí hosting/VPS được báo riêng sau khi trao đổi nhu cầu.')
  if s['id']=='thiet-ke-website': b+=' Cần web app có đăng nhập, phân quyền, dashboard? Xem bảng giá <a href="phan-mem-noi-bo.html#bang-gia">Phần mềm nội bộ</a>.'
  return b+' '+terms(s)+' '+TAIL
OLD_TAIL=re.compile(r'Giá chưa gồm phí [^<]*?\(khách đứng tên và thanh toán trực tiếp\)\.')
FAQ_DOMAIN=('Giá đã gồm tên miền và hosting chưa?','Chưa. My Agent hỗ trợ đăng ký; khách đứng tên và thanh toán trực tiếp cho nhà cung cấp.',
  'Giá đã gồm tên miền và hosting chưa?','Chưa. Tên miền có giá riêng trong Bảng giá; hosting/VPS là Thương lượng. Các khoản này tính riêng. Giá trên trang chưa bao gồm VAT.')
FAQ_EDIT=('Được chỉnh sửa mấy lần?','Mỗi gói gồm 2 lần chỉnh sửa trong phạm vi đã thống nhất. Sửa thêm hoặc thêm tính năng ngoài phạm vi sẽ được báo giá trước khi làm.')
FAQ_WS=('Phí bản quyền Google Workspace / Microsoft 365 trả cho ai?','Bạn đăng ký và thanh toán trực tiếp với nhà cung cấp, tài khoản đứng tên bạn. Tôi chỉ tính phí cấu hình, hỗ trợ.',
  'Phí bản quyền Google Workspace / Microsoft 365 tính thế nào?','Theo bảng giá, mức Google Workspace / Microsoft 365 tính theo người mỗi tháng, gồm phí bản quyền và hỗ trợ cài đặt; tài khoản đứng tên doanh nghiệp của bạn.')
FAQ_INFRA=('Chi phí máy chủ, phần mềm tính thế nào?','Phí máy chủ, cơ sở dữ liệu hoặc phần mềm của nhà cung cấp do khách đứng tên và thanh toán trực tiếp, báo trước khi triển khai.',
  'Chi phí máy chủ, phần mềm tính thế nào?','Chi phí hạ tầng/phần mềm bên thứ ba (máy chủ, cơ sở dữ liệu, phần mềm) được báo trong báo giá trước khi triển khai và thanh toán cho My Agent.')
FAQ_STORE=('Tài khoản App Store / Google Play đứng tên ai?','Nên đứng tên doanh nghiệp của bạn. Phí tài khoản nhà phát triển do bạn trả trực tiếp cho Apple/Google.',
  'Tài khoản App Store / Google Play đứng tên ai?','Nên đứng tên doanh nghiệp của bạn. Chủ app tự trả phí tài khoản nhà phát triển (Apple Developer, Google Play Console); My Agent hỗ trợ đăng ký và cấu hình.')
FAQ_STORE2=('Tài khoản App Store / Google Play đứng tên ai?','Nên đứng tên doanh nghiệp của bạn. Phí tài khoản nhà phát triển Apple/Google được báo trong báo giá và thanh toán cho My Agent.',
  'Tài khoản App Store / Google Play đứng tên ai?','Nên đứng tên doanh nghiệp của bạn. Chủ app tự trả phí tài khoản nhà phát triển (Apple Developer, Google Play Console); My Agent hỗ trợ đăng ký và cấu hình.')
def faq_swap(x,q0,a0,q1,a1):
  for Q0,A0,Q1,A1 in ((q0,a0,q1,a1),(q0,a0.replace('"','\\"'),q1,a1.replace('"','\\"'))):
    x=x.replace(f'<summary>{Q0}</summary><p>{A0}</p>',f'<summary>{Q1}</summary><p>{A1}</p>')
    x=x.replace(f'"name": "{Q0}", "acceptedAnswer": {{"@type": "Answer", "text": "{A0}"}}',f'"name": "{Q1}", "acceptedAnswer": {{"@type": "Answer", "text": "{A1}"}}')
  return x
def faq_fix(x,s):
  x=x.replace('Các khoản này tính riêng. Giá trên trang đã bao '+'gồm VAT.','Các khoản này tính riêng. Giá trên trang chưa bao gồm VAT.')  # v0.9.23: giá chưa bao gồm VAT
  x=faq_swap(x,*FAQ_DOMAIN); x=faq_swap(x,*FAQ_WS); x=faq_swap(x,*FAQ_INFRA); x=faq_swap(x,*FAQ_STORE); x=faq_swap(x,*FAQ_STORE2)
  if s and is_recurring(s): x=faq_swap(x,*FAQ_EDIT,'Thanh toán thế nào?',terms(s))
  return x
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
    a=x.find('<small>',j)+7; e=x.find('</small>',a)
    x=x[:a]+note(s)+x[e:]
    x=faq_fix(commit_fix(x),s)
    if x!=o: f.write_text(x); n+=1
  for f in [R/'dich-vu/traffic-user.html',R/'dich-vu.html']:
    x=f.read_text(); y=faq_fix(OLD_TAIL.sub(TAIL,commit_fix(x)),None)
    if y!=x: f.write_text(y); n+=1
  print('svc_pricing: cập nhật',n,'file')

if __name__=='__main__': main()
