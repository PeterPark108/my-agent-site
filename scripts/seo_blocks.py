"""v0.9.6: khối nội dung SEO cho trang chủ và combo (nguồn: kế hoạch từ khóa 28/10/2026).
Chèn/đổi giữa <!-- seo-block:<id> --> ... <!-- /seo-block:<id> -->, ngay sau section hero.
Số liệu (giảm combo, thời gian) lấy từ data/pricing.json. Chạy trước tech_pass.py (tech_pass sinh FAQPage từ <details>)."""
import json,re,pathlib,html
R=pathlib.Path(__file__).resolve().parent.parent
P=json.loads((R/'data/pricing.json').read_text())
SV={s['id']:s for s in P['services']}
E=lambda x:html.escape(x,quote=False)
def tier(s,t): return [x for x in SV[s]['tiers'] if x['id']==t][0]
def vnd(n): return f'{n:,}'.replace(',','.')+' đ'
def faq(items): return '<div class="faq">'+''.join(f'<details class="glass"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in items)+'</div>'
def head(k,h,p=''): return f'<div class="t rv"><span class="k">// {k}</span><h2>{h}</h2>'+(f'<p>{p}</p>' if p else '')+'</div>'
def home():
  # v0.9.12 (brief SEO 01, 29/10/2026): trang chủ là trang đích "thiết kế web trọn gói TP.HCM"; số liệu lấy từ pricing.json
  import sys; sys.path.insert(0,str(R/'scripts'))
  from svc_pricing import rng
  from svc_data import S
  W=SV['thiet-ke-website']; T={x['id']:x for x in W['tiers']}; q_=W['quantity']
  g=lambda k:rng(T[k]['min'],T[k]['max']); tg=lambda k:T[k]['time']
  cd=P['rules']['comboDiscount']; cmin,cmax=cd[0]['percent'],cd[-1]['percent']
  CK='<svg class="i " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
  ul=lambda xs:'<ul class="dlv">'+''.join(f'<li class="glass rv">{CK}<span>{x}</span></li>' for x in xs)+'</ul>'
  gap='<div class="gap"></div>'
  rows=''.join(f'<tr><th scope="row">{E(T[k]["name"])}</th><td class="bg-p">{g(k)}</td><td>{E(tg(k))}</td><td>{E(T[k]["includes"])}</td></tr>' for k in ('landing','gioi-thieu','ban-hang'))
  table=('<div class="bg-sc" tabindex="0" role="region" aria-label="Bảng giá thiết kế web trọn gói, vuốt ngang nếu cần"><table class="bg-t"><thead><tr><th scope="col">Gói</th><th scope="col">Giá tham khảo</th><th scope="col">Thời gian</th><th scope="col">Bao gồm</th></tr></thead><tbody>'+rows+'</tbody></table></div>')
  extra=rng(q_['perUnitMin'],q_['perUnitMax'])
  steps='<ol class="tl" style="--c:6">'+''.join(f'<li class="rv"><span class="n mono">{i+1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></li>' for i,(a,b) in enumerate(S['thiet-ke-website']['steps']))+'</ol>'
  li=[('dich-vu/thiet-ke-website.html','Thiết kế web chuyên nghiệp theo yêu cầu','khi cần giao diện và tính năng riêng'),
      ('dich-vu/thiet-ke-app.html','Thiết kế app iOS, Android','ứng dụng di động đa nền tảng'),
      ('dich-vu/phan-mem-noi-bo.html','Thiết kế web app theo yêu cầu','hệ thống có đăng nhập, phân quyền, dashboard'),
      ('dich-vu/cham-soc-website.html','Chăm sóc website','bảo trì, cập nhật sau bàn giao'),
      ('blog/thiet-ke-web-tron-goi-gom-nhung-gi.html','Thiết kế web trọn gói giá bao nhiêu, gồm gì','đọc trước khi thuê')]
  cards=''.join(f'<a class="card glass rv" href="{u}"><h3>{E(n)}</h3><p>{E(d)}</p></a>' for u,n,d in li)
  q=[('Thiết kế web trọn gói ở TP.HCM giá bao nhiêu?',f'Landing page {g("landing")}, website giới thiệu {g("gioi-thieu")}, website bán hàng {g("ban-hang")}. Giá tham khảo, chưa bao gồm VAT.'),
     ('Bao lâu thì có website?',f'Landing page {tg("landing")}, website giới thiệu {tg("gioi-thieu")}, website bán hàng {tg("ban-hang")}, tính từ khi nhận đủ nội dung.'),
     ('Web mới có lên Google ngay không?','Không ngay: Google cần thời gian thu thập và đánh giá. My Agent không hứa thứ hạng.'),
     ('Thanh toán thế nào?','Ký hợp đồng bằng văn bản, đặt cọc 30–50%, thanh toán phần còn lại sau khi ký biên bản nghiệm thu.')]
  global BAI
  BAI=('<section id="tron-goi-bai"><div class="wrap">'
   +head('trọn gói','Trọn gói <span class="gt">gồm những&nbsp;gì?</span>')+
   '<div class="card glass rv svi"><p>Một đầu mối lo từ đầu đến cuối: cấu trúc trang, giao diện theo thương hiệu, responsive, SEO nền tảng, Google Maps/Zalo, bàn giao và hướng dẫn quản trị. Tên miền, hosting, email, quảng cáo tính riêng, ghi rõ trong báo giá; xem <a href="bang-gia.html">bảng giá</a>. Cần giao diện, tính năng riêng: <a href="dich-vu/thiet-ke-website.html">thiết kế web chuyên nghiệp theo yêu cầu</a>. Đọc thêm: <a href="blog/thiet-ke-web-tron-goi-gom-nhung-gi.html">thiết kế web trọn gói giá bao nhiêu, gồm gì</a>.</p></div>'
   +gap+head('quy trình','Quy trình <span class="gt">6&nbsp;bước</span>')+
   '<div class="card glass rv svi"><p>'+' → '.join(f'<b>{i+1}.</b> {E(a)}' for i,(a,b) in enumerate(S['thiet-ke-website']['steps']))+'.</p></div>'
   +gap+head('bàn giao','Bạn nhận được gì <span class="gt">khi bàn&nbsp;giao</span>')+
   ul(['Website trên tên miền của bạn, HTTPS, sitemap đã gửi Google','Hướng dẫn cập nhật nội dung','Mã nguồn, giao sau khi thanh toán đủ; sau bàn giao mã nguồn và dữ liệu thuộc về bạn','2 lần chỉnh sửa trong phạm vi, bảo hành lỗi kỹ thuật 60 ngày'])
   +gap+head('cam kết','Hợp đồng <span class="gt">&amp; thanh&nbsp;toán</span>')+
   '<div class="card glass rv svi"><p>My Agent là thương hiệu dịch vụ cá nhân của Nguyễn Văn Tùng (Peter), chưa đăng ký pháp nhân. Mỗi dự án có hợp đồng bằng văn bản, cọc 30–50%, phần còn lại thanh toán sau khi ký biên bản nghiệm thu. <a href="ve-chung-toi.html">Về Peter</a>.</p></div>'
   +gap+head('faq','Câu hỏi <span class="gt">thường&nbsp;gặp</span>')+faq(q)+'</div></section>')
  return ('<section class="soft" id="tron-goi"><div class="wrap">'
   +head('bảng giá','Bảng giá thiết kế web <span class="gt">trọn&nbsp;gói</span>')+
   f'<div class="card glass rv svi">{table}<p>Trang thêm: {extra} / trang. Giá tham khảo, chưa bao gồm VAT. Nhiều dịch vụ: <a href="combo.html">combo giảm {cmin}–{cmax}%</a>.</p></div><div class="acts rv" style="flex-wrap:wrap"><a class="btn mag" href="bang-gia.html#tinh-gia">Tự tính giá</a><a class="btn ghost" href="https://zalo.me/0328439972" target="_blank" rel="noopener" data-zalo>Nhắn Zalo 0328 439 972</a></div></div></section>')
HERO_H1='<h1>Thiết kế web trọn gói TP.HCM – <span class="gt">một đầu mối</span> từ tên miền đến bàn&nbsp;giao</h1>'
def hero(s):
  import sys; sys.path.insert(0,str(R/'scripts')); from svc_pricing import rng
  T={x['id']:x for x in SV['thiet-ke-website']['tiers']}
  lead=(f'<p class="lead">Tôi là Peter (Nguyễn Văn Tùng), trực tiếp làm web trọn gói tại TP.HCM: landing page {rng(T["landing"]["min"],T["landing"]["max"])} ({T["landing"]["time"]}), website giới thiệu {rng(T["gioi-thieu"]["min"],T["gioi-thieu"]["max"])} ({T["gioi-thieu"]["time"]}), website bán hàng {rng(T["ban-hang"]["min"],T["ban-hang"]["max"])}. Giá tham khảo, chưa bao gồm VAT. Nhắn Zalo <a href="https://zalo.me/0328439972" target="_blank" rel="noopener" data-zalo>0328 439 972</a> để nhận báo giá.</p>')
  i=s.index('<section class="hero'); j=s.index('</section>',i); h=s[i:j]
  h=re.sub(r'<h1>.*?</h1>',HERO_H1,h,count=1,flags=re.S); h=re.sub(r'<p class="lead">.*?</p>',lead,h,count=1,flags=re.S)
  return s[:i]+h+s[j:]
def combo():
  r=P['rules']; cd=r['comboDiscount']
  parts=', '.join(f'{x["minServices"]} dịch vụ giảm {x["percent"]}%' if i==0 else (f'từ {x["minServices"]} dịch vụ {x["percent"]}%' if i==len(cd)-1 else f'{x["minServices"]} dịch vụ {x["percent"]}%') for i,x in enumerate(cd))
  q=[('Combo có bắt buộc không?','Không, có thể chọn từng dịch vụ.'),
     ('Giảm giá áp dụng cho dịch vụ nào?','Giảm theo combo áp dụng cho các dịch vụ làm một lần được đánh dấu giảm theo combo (ví dụ thiết kế website, app, phần mềm nội bộ). Tên miền, hosting và dịch vụ tính theo tháng/năm không giảm theo combo; dịch vụ theo tháng có ưu đãi riêng khi trả trước.')]
  return ('<section id="gioi-thieu-combo"><div class="wrap">'+head('combo trọn gói','Một đầu mối cho <span class="gt">website và&nbsp;marketing</span>')+
   f'<div class="card glass rv svi"><p>Combo dành cho ai muốn một đầu mối lo trọn: website, tên miền, email theo tên miền, Google Maps, quảng cáo. Mức giảm theo số dịch vụ trong combo (theo bảng giá tham khảo, chưa gồm VAT): {parts} (tối đa {vnd(r["maxDiscountAmount"])}). {E(r["negotiableNote"])}</p>'
   '<p>Xem thêm <a href="index.html#tron-goi">thiết kế web trọn gói gồm những gì</a> và <a href="dich-vu/thiet-ke-website.html">thiết kế web chuyên nghiệp theo yêu cầu</a>. Đọc thêm: <a href="blog/thiet-ke-web-tron-goi-gom-nhung-gi.html">thiết kế web trọn gói giá bao nhiêu, gồm gì</a>.</p></div>'
   '<div class="gap"></div>'+head('faq','Câu hỏi <span class="gt">về&nbsp;combo</span>')+faq(q)+'</div></section>')
def put(f,bid,body,at=None):
  p=R/f; s=p.read_text(); blk=f'<!-- seo-block:{bid} -->{body}<!-- /seo-block:{bid} -->'
  if f'<!-- seo-block:{bid} -->' in s: n=re.sub(rf'<!-- seo-block:{bid} -->.*?<!-- /seo-block:{bid} -->',lambda m:blk,s,flags=re.S)
  elif at: i=s.index(at); n=s[:i]+blk+s[i:]
  else:
    i=s.index('<section class="hero'); j=s.index('</section>',i)+len('</section>'); n=s[:j]+blk+s[j:]
  if n!=s: p.write_text(n); return 1
  return 0
if __name__=='__main__':
  f=R/'index.html'; s=f.read_text(); n=hero(s)
  if n!=s: f.write_text(n)
  print('seo_blocks: cập nhật',put('index.html','tron-goi',home())+put('index.html','tron-goi-bai',BAI,'</main>')+put('combo.html','combo-intro',combo()),'file')
