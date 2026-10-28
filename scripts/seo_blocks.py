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
  rows=''.join(f'<tr><th scope="row">{E(T[k]["name"])}</th><td class="bg-p">{g(k)}</td><td>{E(tg(k))}</td><td>{E(T[k]["includes"])}</td><td>{E(T[k]["excludes"])}</td></tr>' for k in ('landing','gioi-thieu','ban-hang'))
  table=('<div class="bg-sc" tabindex="0" role="region" aria-label="Bảng giá thiết kế web trọn gói, vuốt ngang nếu cần"><table class="bg-t"><thead><tr><th scope="col">Gói</th><th scope="col">Giá tham khảo</th><th scope="col">Thời gian</th><th scope="col">Bao gồm</th><th scope="col">Chưa gồm</th></tr></thead><tbody>'+rows+'</tbody></table></div>')
  extra=rng(q_['perUnitMin'],q_['perUnitMax'])
  steps='<ol class="tl" style="--c:6">'+''.join(f'<li class="rv"><span class="n mono">{i+1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></li>' for i,(a,b) in enumerate(S['thiet-ke-website']['steps']))+'</ol>'
  li=[('dich-vu/thiet-ke-website.html','Thiết kế web chuyên nghiệp theo yêu cầu','khi cần giao diện và tính năng riêng'),
      ('dich-vu/thiet-ke-app.html','Thiết kế app iOS, Android','ứng dụng di động đa nền tảng'),
      ('dich-vu/phan-mem-noi-bo.html','Thiết kế web app theo yêu cầu','hệ thống có đăng nhập, phân quyền, dashboard'),
      ('dich-vu/cham-soc-website.html','Chăm sóc website','bảo trì, cập nhật sau bàn giao'),
      ('blog/thiet-ke-web-tron-goi-gom-nhung-gi.html','Thiết kế web trọn gói giá bao nhiêu, gồm gì','đọc trước khi thuê')]
  cards=''.join(f'<a class="card glass rv" href="{u}"><h3>{E(n)}</h3><p>{E(d)}</p></a>' for u,n,d in li)
  q=[('Thiết kế web trọn gói ở TP.HCM giá bao nhiêu?',f'Tại My Agent, landing page {g("landing")}, website giới thiệu ≤10 trang {g("gioi-thieu")}, website bán hàng {g("ban-hang")} (giá tham khảo theo khoảng, chưa bao gồm VAT). Tên miền tính riêng theo năm, hosting thương lượng. Báo giá chính xác sau khi trao đổi nhu cầu.'),
     ('Trọn gói có gồm tên miền, hosting không?','Giá thiết kế chưa gồm tên miền và hosting. Tên miền có giá riêng theo năm trong bảng giá, hosting/VPS thương lượng theo cấu hình. Có thể gộp tên miền, email, Google Maps trong combo; báo giá ghi rõ từng hạng mục trước khi làm.'),
     ('Bao lâu thì có website?',f'Theo bảng giá tham khảo: landing page {tg("landing")}, website giới thiệu {tg("gioi-thieu")}, website bán hàng {tg("ban-hang")}. Thời gian tính từ khi chốt nội dung và nhận đủ tư liệu; tiến độ được báo theo từng bước.'),
     ('Tôi có tự sửa nội dung được không?','Được. Website giới thiệu và website bán hàng có trang quản trị (CMS) để tự sửa chữ, ảnh, sản phẩm. Khi bàn giao, tôi hướng dẫn cách cập nhật nội dung.'),
     ('Ở tỉnh khác có làm được không?','Có. Toàn bộ quy trình làm online: trao đổi qua Zalo hoặc Google Meet, xem bản thử, duyệt và bàn giao từ xa. Tôi nhận khách toàn quốc.'),
     ('Web mới có lên Google ngay không?','Không ngay. Website được làm SEO nền tảng (title, meta, sitemap, schema) và gửi sitemap cho Google, nhưng Google cần thời gian thu thập và đánh giá. My Agent không hứa thứ hạng.'),
     ('Ai trực tiếp làm web?','Tôi là Peter (Nguyễn Văn Tùng), trực tiếp trao đổi, thiết kế, lập trình và bàn giao. My Agent là thương hiệu dịch vụ cá nhân của tôi, nhận dự án vừa và nhỏ.'),
     ('Thanh toán thế nào?','Hai bên ký hợp đồng bằng văn bản. Đặt cọc 30–50% khi bắt đầu, thanh toán phần còn lại sau khi ký biên bản nghiệm thu. Mỗi gói gồm 2 lần chỉnh sửa trong phạm vi đã thống nhất và bảo hành lỗi kỹ thuật 60 ngày.')]
  return ('<section class="soft" id="tron-goi"><div class="wrap">'
   +head('trọn gói','Thiết kế web trọn gói ở My Agent <span class="gt">gồm những&nbsp;gì?</span>')+
   '<div class="card glass rv svi"><p>Trọn gói nghĩa là một đầu mối lo từ đầu đến cuối: tư vấn cấu trúc trang, giao diện theo thương hiệu, lập trình responsive, SEO nền tảng, gắn Google Maps/Zalo, rồi bàn giao và hướng dẫn quản trị. Tên miền, hosting và email tính riêng, ghi rõ trong báo giá trước khi làm.</p>'
   '<h3>Trong giá thiết kế</h3><ul class="svi-l"><li>Tư vấn cấu trúc trang và nội dung chính</li><li>Giao diện theo nhận diện thương hiệu, hiển thị tốt trên điện thoại</li><li>SEO nền tảng: title, meta, sitemap, schema</li><li>Gắn Google Maps, nút Zalo, form liên hệ</li><li>Bàn giao và hướng dẫn cập nhật nội dung</li></ul>'
   '<h3>Tính riêng</h3><ul class="svi-l"><li>Tên miền (theo năm), hosting/VPS (thương lượng), email theo tên miền</li><li>Viết nội dung số lượng lớn, ảnh bản quyền</li><li>Quảng cáo (tiền trả cho nền tảng không nằm trong giá)</li></ul><p>Chi tiết từng khoản: <a href="bang-gia.html">bảng giá chi tiết</a>.</p></div>'
   +gap+head('bảng giá','Bảng giá thiết kế web <span class="gt">trọn&nbsp;gói</span>')+
   f'<div class="card glass rv svi">{table}<p>Trang thêm ngoài gói: {extra} / trang. Giá tham khảo theo khoảng, chưa bao gồm VAT; báo giá chính xác sau khi trao đổi nhu cầu.</p></div><div class="acts rv"><a class="btn mag" href="bang-gia.html#tinh-gia">Tự tính giá combo</a><a class="btn ghost" href="https://zalo.me/0328439972" target="_blank" rel="noopener" data-zalo>Nhắn Zalo 0328 439 972</a></div>'
   +gap+head('thời gian','Mất bao lâu để <span class="gt">có&nbsp;website?</span>')+
   f'<div class="card glass rv svi"><p>Landing page khoảng {tg("landing")}, website giới thiệu {tg("gioi-thieu")}, website bán hàng {tg("ban-hang")}. Thời gian tính từ khi chốt nội dung và nhận đủ tư liệu (logo, chữ, ảnh); trang nhiều hoặc tính năng riêng sẽ được báo trước.</p></div>'
   +gap+head('quy trình','Quy trình <span class="gt">6&nbsp;bước</span>')+steps
   +gap+head('bàn giao','Bạn nhận được gì <span class="gt">khi bàn&nbsp;giao</span>')+
   ul(['Website chạy trên tên miền của bạn, có HTTPS','Sitemap đã gửi Google, SEO nền tảng','Form liên hệ, nút Zalo, Google Maps hoạt động','Hướng dẫn cập nhật nội dung (CMS với web giới thiệu, bán hàng)','2 lần chỉnh sửa trong phạm vi đã thống nhất','Bảo hành lỗi kỹ thuật 60 ngày'])
   +gap+head('thanh toán','Thanh toán <span class="gt">&amp; cam&nbsp;kết</span>')+
   '<div class="card glass rv svi"><p>My Agent là thương hiệu dịch vụ cá nhân của Nguyễn Văn Tùng (Peter), hiện chưa đăng ký pháp nhân. Mỗi dự án có báo giá ghi rõ hạng mục và hợp đồng bằng văn bản, đặt cọc 30–50%, thanh toán phần còn lại sau khi ký biên bản nghiệm thu.</p><p>Người trao đổi, làm và bàn giao là tôi, từ đầu đến cuối. Xem thêm <a href="ve-chung-toi.html">về Peter và My Agent</a>.</p></div>'
   +gap+head('sản phẩm mẫu','Sản phẩm <span class="gt">mẫu</span>')+
   '<div class="card glass rv svi"><p>Đây là sản phẩm mẫu do tôi tự làm với dữ liệu mẫu, không phải dự án của khách hàng:</p><ul class="svi-l"><li><b>NHỊP</b> (sản phẩm mẫu): web bán giày có giỏ hàng, đơn hàng</li><li><b>NhàĐất Việt</b> (sản phẩm mẫu): web bất động sản có lọc tin đăng</li></ul><p><a href="du-an.html">Xem các sản phẩm mẫu</a></p></div>'
   +gap+head('combo','Gộp thêm tên miền, email, Google Maps? <span class="gt">Xem&nbsp;combo</span>')+
   f'<div class="card glass rv svi"><p>Khi làm cùng nhiều dịch vụ làm một lần, combo giảm {cmin}–{cmax}% theo số dịch vụ. <a href="combo.html">Xem các combo</a>.</p></div>'
   +gap+'<div class="grid g3">'+cards+'</div>'
   +gap+head('faq','Câu hỏi <span class="gt">thường&nbsp;gặp</span>')+faq(q)+'</div></section>')
HERO_H1='<h1>Thiết kế web trọn gói TP.HCM – <span class="gt">một đầu mối</span> từ tên miền đến bàn&nbsp;giao</h1>'
def hero(s):
  import sys; sys.path.insert(0,str(R/'scripts')); from svc_pricing import rng
  T={x['id']:x for x in SV['thiet-ke-website']['tiers']}
  lead=(f'<p class="lead">Tôi là Peter (Nguyễn Văn Tùng), trực tiếp làm web trọn gói tại TP.HCM cho cửa hàng, hộ kinh doanh và doanh nghiệp nhỏ: landing page {rng(T["landing"]["min"],T["landing"]["max"])} ({T["landing"]["time"]}), website giới thiệu {rng(T["gioi-thieu"]["min"],T["gioi-thieu"]["max"])} ({T["gioi-thieu"]["time"]}), website bán hàng {rng(T["ban-hang"]["min"],T["ban-hang"]["max"])}. Giá tham khảo, chưa bao gồm VAT. Nhắn Zalo <a href="https://zalo.me/0328439972" target="_blank" rel="noopener" data-zalo>0328 439 972</a> để nhận báo giá.</p>')
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
   '<p>Xem thêm <a href="index.html#tron-goi">thiết kế web trọn gói gồm những gì</a> và <a href="dich-vu/thiet-ke-website.html">thiết kế web chuyên nghiệp theo yêu cầu</a>.</p></div>'
   '<div class="gap"></div>'+head('faq','Câu hỏi <span class="gt">về&nbsp;combo</span>')+faq(q)+'</div></section>')
def put(f,bid,body):
  p=R/f; s=p.read_text(); blk=f'<!-- seo-block:{bid} -->{body}<!-- /seo-block:{bid} -->'
  if f'<!-- seo-block:{bid} -->' in s: n=re.sub(rf'<!-- seo-block:{bid} -->.*?<!-- /seo-block:{bid} -->',lambda m:blk,s,flags=re.S)
  else:
    i=s.index('<section class="hero'); j=s.index('</section>',i)+len('</section>'); n=s[:j]+blk+s[j:]
  if n!=s: p.write_text(n); return 1
  return 0
if __name__=='__main__':
  f=R/'index.html'; s=f.read_text(); n=hero(s)
  if n!=s: f.write_text(n)
  print('seo_blocks: cập nhật',put('index.html','tron-goi',home())+put('combo.html','combo-intro',combo()),'file')
