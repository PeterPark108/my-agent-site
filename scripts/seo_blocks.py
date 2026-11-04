"""v0.9.6: khối nội dung SEO cho trang chủ và combo (nguồn: kế hoạch từ khóa 28/10/2026).
Chèn/đổi giữa <!-- seo-block:<id> --> ... <!-- /seo-block:<id> -->, ngay sau section hero.
Số liệu (giảm combo, thời gian) lấy từ data/pricing.json. Chạy trước tech_pass.py (tech_pass sinh FAQPage từ <details>)."""
import json,re,pathlib,html,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from glass_icons import gi,tron_goi_key  # v0.9.30: icon glass cho ô dịch vụ
R=pathlib.Path(__file__).resolve().parent.parent
P=json.loads((R/'data/pricing.json').read_text())
SV={s['id']:s for s in P['services']}
E=lambda x:html.escape(x,quote=False)
def tier(s,t): return [x for x in SV[s]['tiers'] if x['id']==t][0]
def vnd(n): return f'{n:,}'.replace(',','.')+' đ'
def faq(items): return '<div class="faq">'+''.join(f'<details class="glass"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in items)+'</div>'
def head(k,h,p=''): return f'<div class="t rv"><span class="k">// {k}</span><h2>{h}</h2>'+(f'<p>{p}</p>' if p else '')+'</div>'
def latest_blog(n=3):
  out=[]
  for f in sorted((R/'data/blog').glob('*.md')):
    fm=f.read_text().split('---',2)[1]
    t=re.search(r'^title:\s*"?(.*?)"?\s*$',fm,re.M).group(1); d=re.search(r'^date:\s*(\S+)',fm,re.M).group(1)
    out.append((d,f.stem,t))
  out.sort(key=lambda x:(x[0],x[1]),reverse=True)
  return out[:n]
def home():
  li=[('dich-vu/thiet-ke-website.html','Thiết kế website','website giới thiệu, landing page, web bán hàng'),
      ('dich-vu/phan-mem-noi-bo.html','Thiết kế web app theo yêu cầu','hệ thống có đăng nhập, phân quyền, dashboard'),
      ('dich-vu/thiet-ke-app.html','Thiết kế app','ứng dụng iOS/Android'),
      ('combo.html','Combo dịch\u00a0vụ','gộp website, tên miền, email, marketing'),
      ('blog/thiet-ke-web-tron-goi-gom-nhung-gi.html','Thiết kế web trọn gói gồm những gì?','đọc trước khi thuê')]
  card=lambda u,n,d:(f'<a class="card glass hx-link glc" href="{u}"><div class="glt"><h3>{E(n)}</h3><p>{E(d)}</p></div>{gi(tron_goi_key(u))}</a>' if tron_goi_key(u)
                     else f'<a class="card glass hx-link" href="{u}"><h3>{E(n)}</h3><p>{E(d)}</p></a>')
  cards=''.join(card(u,n,d) for u,n,d in li)
  return ('<section class="hx-section hx-seo" id="tron-goi"><div class="hx-container">'
   '<p class="hx-eye">Trọn gói</p><h2>Thiết kế web trọn gói gồm những gì?</h2>'
   '<div class="hx-prose"><p>Thiết kế web trọn gói ở My Agent nghĩa là một đầu mối lo từ đầu đến cuối: tư vấn cấu trúc trang, giao diện theo thương hiệu, lập trình responsive, SEO nền tảng (title, meta, sitemap, schema), gắn Google Maps/Zalo, rồi bàn giao và hướng dẫn quản trị. Tên miền, hosting và email doanh nghiệp có thể đăng ký kèm trong cùng combo.</p>'
   '<p>My Agent làm việc tại TP.HCM, trao đổi online qua Zalo, Google Meet và nhận khách toàn quốc. Zalo/điện thoại: <a href="tel:0328439972">0328 439 972</a>.</p></div>'
   f'<div class="hx-linkgrid">{cards}</div>'
   '<p class="hx-rel"><span>Bài mới trên Blog:</span> '+' '.join(f'<a href="blog/{u}.html">{E(t)}</a>' for _,u,t in latest_blog())+' <a href="blog.html">Xem tất cả bài viết</a></p>'
   '</div></section>')
def home_faq():
  tg=lambda t:tier('thiet-ke-website',t)['time']
  q=[('My Agent có nhận làm web cho khách ngoài TP.HCM không?','Có. Toàn bộ quy trình làm online: trao đổi, xem bản thử, duyệt và bàn giao từ xa.'),
     ('Thiết kế web trọn gói có gồm tên miền và hosting không?','Có thể gộp trong combo; chi phí tên miền tính theo năm, hosting thương lượng theo cấu hình. Báo giá ghi rõ từng hạng mục trước khi làm. Giá tham khảo chưa bao gồm VAT.'),
     ('Bao lâu thì có website?',f'Theo bảng giá tham khảo: landing page {tg("landing")}, website giới thiệu {tg("gioi-thieu")}, website bán hàng {tg("ban-hang")}. Khoảng này chốt lại sau khi thống nhất phạm vi.'),
     ('Nên bắt đầu từ đâu?','Gửi mục tiêu, loại website và nội dung hiện có qua form hoặc Zalo. My Agent trao đổi để xác định phạm vi và báo giá, rồi phản hồi trong giờ làm việc.')]
  return ''.join(f'<details class="hx-faq-item"><summary>{E(qq)}<span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for qq,a in q)
def home_map():
  """Liên kết nội bộ text ở cuối trang chủ, để crawler thấy dịch vụ/combo/dự án dù bố cục cosmos không còn lưới cũ."""
  groups=[
    ('Website và nền tảng',[
      ('dich-vu.html','Tất cả dịch vụ'),
      ('dich-vu/thiet-ke-website.html','Thiết kế website'),
      ('dich-vu/hosting-seo.html','Hosting SEO'),
      ('dich-vu/ten-mien.html','Tên miền'),
      ('dich-vu/email-doanh-nghiep.html','Email doanh nghiệp'),
      ('dich-vu/cham-soc-website.html','Chăm sóc website'),
      ('combo.html','Combo dịch vụ'),
      ('bang-gia.html','Bảng giá'),
    ]),
    ('Marketing và nội dung',[
      ('dich-vu/seo-tong-the.html','SEO tổng thể'),
      ('dich-vu/quang-cao-google-facebook.html','Quảng cáo Google, Facebook'),
      ('dich-vu/traffic-user.html','Traffic User'),
      ('dich-vu/google-maps.html','Google Maps'),
      ('dich-vu/video-ai.html','Video'),
      ('dich-vu/cham-soc-fanpage.html','Chăm sóc Fanpage'),
      ('dich-vu/zalo-oa-mini-app.html','Zalo OA, Mini App'),
      ('dich-vu/profile-doanh-nghiep.html','Profile doanh nghiệp'),
    ]),
    ('Phần mềm, pháp lý, trang khác',[
      ('dich-vu/phan-tich-du-lieu.html','Phân tích dữ liệu'),
      ('dich-vu/ky-thuat-du-lieu.html','Kỹ thuật dữ liệu'),
      ('dich-vu/phan-mem-noi-bo.html','Phần mềm nội bộ'),
      ('dich-vu/thiet-ke-app.html','Thiết kế app'),
      ('dich-vu/bo-cong-thuong.html','Đăng ký Bộ Công Thương'),
      ('du-an.html','Dự án mẫu'),
      ('blog.html','Blog'),
      ('tin-tuc.html','Tin tức'),
      ('lien-he.html','Liên hệ'),
      ('ve-chung-toi.html','Về chúng tôi'),
      ('tra-cuu-tien-do.html','Tra cứu tiến độ'),
      ('tai-nguyen-ai-agent.html','Tài nguyên'),
      ('cong-cu.html','Công cụ miễn phí'),
      ('ghi-nguon.html','Ghi nguồn'),
      ('chinh-sach-bao-mat.html','Chính sách bảo mật'),
    ]),
  ]
  cols=''.join('<div><p class="hx-eye">'+E(title)+'</p><ul class="hx-map">'+''.join(f'<li><a href="{u}">{E(n)}</a></li>' for u,n in items)+'</ul></div>' for title,items in groups)
  demos=('Sản phẩm mẫu do Peter tự làm để minh họa năng lực, không phải dự án làm cho khách hàng. '
         '<a href="https://huongnghiep.myagentvn.com">Hướng Nghiệp 360, bản chạy</a> · '
         '<a href="https://github.com/PeterPark108/huong-nghiep-360">mã nguồn Hướng Nghiệp 360</a> · '
         '<a href="https://nhip-shoe-shop.onrender.com">NHỊP, bản chạy</a> · '
         '<a href="https://github.com/PeterPark108/nhip-shoe-shop">mã nguồn NHỊP</a> · '
         '<a href="https://github.com/PeterPark108/nhadat-viet-demo">NhàĐất Việt, mã nguồn</a> · '
         '<a href="du-an.html">trang Dự án</a>.')
  return ('<section class="hx-section hx-mapsec" id="dich-vu-chung-toi" aria-labelledby="map-title"><div class="hx-container">'
          '<p class="hx-eye">Liên kết</p><h2 id="map-title">Dịch vụ của chúng tôi</h2>'
          '<p class="hx-lead">Một đầu mối cho website, marketing và dữ liệu. Mỗi mục dưới đây là một trang riêng.</p>'
          f'<div class="hx-mapgrid">{cols}</div><p class="hx-note">{demos}</p></div></section>')
def combo():
  r=P['rules']; cd=r['comboDiscount']
  parts=', '.join(f'{x["minServices"]} dịch vụ giảm {x["percent"]}%' if i==0 else (f'từ {x["minServices"]} dịch vụ {x["percent"]}%' if i==len(cd)-1 else f'{x["minServices"]} dịch vụ {x["percent"]}%') for i,x in enumerate(cd))
  q=[('Combo có bắt buộc không?','Không, có thể chọn từng dịch vụ.'),
     ('Giảm giá áp dụng cho dịch vụ nào?','Giảm theo combo áp dụng cho các dịch vụ làm một lần được đánh dấu giảm theo combo (ví dụ thiết kế website, app, phần mềm nội bộ). Tên miền, hosting và dịch vụ tính theo tháng/năm không giảm theo combo; dịch vụ theo tháng có ưu đãi riêng khi trả trước.')]
  return ('<section id="gioi-thieu-combo"><div class="wrap">'+head('combo trọn gói','Một đầu mối cho <span class="gt">website và&nbsp;marketing</span>')+
   f'<div class="card glass rv svi"><p>Combo dành cho ai muốn một đầu mối lo trọn: website, tên miền, email theo tên miền, Google Maps, quảng cáo. Mức giảm theo số dịch vụ trong combo (theo bảng giá tham khảo, chưa bao gồm VAT): {parts} (tối đa {vnd(r["maxDiscountAmount"])}). {E(r["negotiableNote"])}</p>'
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
  print('seo_blocks: cập nhật',put('index.html','tron-goi',home())+put('index.html','home-faq',home_faq())+put('index.html','home-map',home_map())+put('combo.html','combo-intro',combo()),'file')
