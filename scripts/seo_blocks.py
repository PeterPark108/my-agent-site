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
def latest_blog(n=3):
  out=[]
  for f in sorted((R/'data/blog').glob('*.md')):
    fm=f.read_text().split('---',2)[1]
    t=re.search(r'^title:\s*"?(.*?)"?\s*$',fm,re.M).group(1); d=re.search(r'^date:\s*(\S+)',fm,re.M).group(1)
    out.append((d,f.stem,t))
  out.sort(key=lambda x:(x[0],x[1]),reverse=True)
  return out[:n]
def home():
  tg=lambda t:tier('thiet-ke-website',t)['time']
  li=[('dich-vu/thiet-ke-website.html','Thiết kế website','website giới thiệu, landing page, web bán hàng'),
      ('dich-vu/phan-mem-noi-bo.html','Thiết kế web app theo yêu cầu','hệ thống có đăng nhập, phân quyền, dashboard'),
      ('dich-vu/thiet-ke-app.html','Thiết kế app','ứng dụng iOS/Android'),
      ('combo.html','Combo dịch vụ','gộp website, tên miền, email, marketing'),
      ('blog/thiet-ke-web-tron-goi-gom-nhung-gi.html','Thiết kế web trọn gói gồm những gì?','đọc trước khi thuê')]
  cards=''.join(f'<a class="card glass rv" href="{u}"><h3>{E(n)}</h3><p>{E(d)}</p></a>' for u,n,d in li)
  q=[('My Agent có nhận làm web cho khách ngoài TP.HCM không?','Có. Toàn bộ quy trình làm online: trao đổi, xem bản thử, duyệt và bàn giao từ xa.'),
     ('Thiết kế web trọn gói có gồm tên miền và hosting không?','Có thể gộp trong combo; chi phí tên miền tính theo năm, hosting thương lượng theo cấu hình. Báo giá ghi rõ từng hạng mục trước khi làm.'),
     ('Bao lâu thì có website?',f'Theo bảng giá tham khảo: landing page {tg("landing")}, website giới thiệu {tg("gioi-thieu")}, website bán hàng {tg("ban-hang")}.')]
  return ('<section class="soft" id="tron-goi"><div class="wrap">'+head('trọn gói','Thiết kế web trọn gói <span class="gt">gồm những&nbsp;gì?</span>')+
   '<div class="card glass rv svi"><p>Thiết kế web trọn gói ở My Agent nghĩa là một đầu mối lo từ đầu đến cuối: tư vấn cấu trúc trang, giao diện theo thương hiệu, lập trình responsive, SEO nền tảng (title, meta, sitemap, schema), gắn Google Maps/Zalo, rồi bàn giao và hướng dẫn quản trị. Tên miền, hosting và email doanh nghiệp có thể đăng ký kèm trong cùng combo.</p>'
   '<p>Peter (Nguyễn Văn Tùng) làm việc tại TP.HCM, trao đổi online qua Zalo, Google Meet và nhận khách toàn quốc. Zalo/điện thoại: <a href="tel:0328439972">0328 439 972</a>.</p></div>'
   f'<div class="gap"></div><div class="grid g3">{cards}</div><div class="gap"></div>'+'<p class="relx rv"><span class="mono">Bài mới trên Blog:</span> '+' '.join(f'<a href="blog/{u}.html">{E(t)}</a>' for _,u,t in latest_blog())+' <a href="blog.html">Xem tất cả bài viết</a></p><div class="gap"></div>'+head('faq','Câu hỏi <span class="gt">thường&nbsp;gặp</span>')+faq(q)+'</div></section>')
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
  print('seo_blocks: cập nhật',put('index.html','tron-goi',home())+put('combo.html','combo-intro',combo()),'file')
