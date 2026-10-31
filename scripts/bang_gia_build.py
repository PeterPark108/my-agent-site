#!/usr/bin/env python3
"""Dựng bang-gia.html (bảng giá 5 nhóm + công cụ tính giá #tinh-gia) từ data/pricing.json (bản công khai).
Khung header/footer lấy từ combo.html. Chạy: python3 scripts/bang_gia_build.py && python3 scripts/tech_pass.py"""
import json,re,html,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
P=json.loads((R/'data/pricing.json').read_text())
E=lambda x:html.escape(str(x),quote=True)
def tr(v):
  if v>=1_000_000: return (f'{v/1e6:.2f}'.rstrip('0').rstrip('.').replace('.',','))+' triệu'
  return f'{v//1000:,}'.replace(',','.')+' nghìn'
def rng(t): return f'{tr(t["min"])} – {tr(t["max"])}'
UNIT={'one-time':'','monthly':' / tháng','yearly':' / năm'}
SLUG={'01':'nen-tang-website','02':'marketing-tang-truong','03':'mang-xa-hoi-noi-dung','04':'du-lieu-phan-mem','05':'phap-ly-thu-tuc'}
DV={'quang-cao-google-facebook':'quang-cao-google-facebook'}
base=(R/'combo.html').read_text()
head=re.sub(r'<!-- tech:head -->.*?<!-- /tech:head -->','',base[:base.find('<main')],flags=re.S)
head=head.replace('<a href="combo.html" class=on>Combo</a>','<a href="combo.html">Combo</a>')
foot=base[base.find('</main>'):]
foot=re.sub(r'<script src="js/he-thong\.js[^"]*" defer></script>','',foot)
foot=foot.replace('</body>','<script src="js/combo-calculator.js?v=0" defer></script><script src="js/bang-gia.js?v=0" defer></script></body>',1)
TITLE='Bảng giá dịch vụ website, SEO, dữ liệu | My Agent'
DESC='Bảng giá tham khảo theo khoảng (chưa bao gồm VAT) cho website, SEO, mạng xã hội, dữ liệu, pháp lý, kèm công cụ tính combo. Báo giá chính xác sau trao đổi.'
head=re.sub(r'<title>.*?</title>',f'<title>{E(TITLE)}</title>',head,count=1)
head=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{E(DESC)}">',head,count=1)
groups=[]
for s in P['services']:
  c=s['category']
  if not groups or groups[-1][0]!=c: groups.append((c,[]))
  groups[-1][1].append(s)
NOTE=('<div class="bg-note glass rv" role="note"><p><b>Giá chưa bao gồm VAT.</b> Giá chỉ mang tính tham khảo theo khoảng, báo giá chính xác sau khi trao đổi nhu cầu.</p>'
      '<p class="muted">Hosting/VPS và quảng cáo Google, Facebook: <b>Thương lượng</b> (tùy cấu hình, ngân sách). Phí quảng cáo chưa gồm tiền quảng cáo trả cho nền tảng (Google, Facebook).</p></div>')
o=['<main><section class="hero sub"><canvas class="net" aria-hidden="true"></canvas><div class="wrap"><nav class="crumb mono" aria-label="breadcrumb"><a href="index.html">home</a> / bảng giá</nav>',
   '<h1 class="gt2">Bảng giá dịch vụ My&nbsp;Agent</h1><p class="lead">Khoảng giá tham khảo cho 5 nhóm dịch vụ và công cụ tự tính giá combo. Chọn dịch vụ, kỳ thanh toán để xem tạm tính, rồi gửi sang trang liên hệ để nhận báo giá chính xác.</p>',
   '<p class="acts"><a class="btn mag" href="#tinh-gia">Tự tính giá combo</a> <a class="btn ghost" href="lien-he.html">Nhận báo giá chính xác</a></p></div></section>',
   '<section><div class="wrap">'+NOTE+'<div class="bg-toc" role="navigation" aria-label="Nhóm dịch vụ">'+''.join(f'<a href="#{SLUG[c[:2]]}">{E(c)}</a>' for c,_ in groups)+'<a href="#tinh-gia">Tính giá combo</a></div>']
for c,ss in groups:
  num,name=c.split(' · ',1)
  o.append(f'<div class="gap"></div><div class="t rv" id="{SLUG[num]}"><span class="k">// {num}</span><h2>Bảng giá {E(name)}</h2></div><div class="bg-groups">')
  for s in ss:
    unit=UNIT.get(s['billing'],'')
    o.append(f'<article class="bg-card glass rv" id="gia-{s["id"]}"><h3><a href="dich-vu/{s["id"]}.html">{E(s["name"])}</a></h3>')
    if s.get('negotiable'): o.append(f'<p class="bg-neg"><b>Thương lượng</b> · {E(s.get("negotiableNote",""))}</p>')
    o.append('<div class="bg-sc" tabindex="0" role="region" aria-label="Bảng giá, vuốt ngang nếu cần"><table class="bg-t"><thead><tr><th scope="col">Gói</th><th scope="col">Giá tham khảo</th><th scope="col">Thời gian</th><th scope="col">Bao gồm</th></tr></thead><tbody>')
    for t in s['tiers']:
      price='Thương lượng' if s.get('negotiable') else rng(t)+unit
      inc=E(t.get('includes',''))+(f'<br><small class="muted">Chưa gồm: {E(t["excludes"])}</small>' if t.get('excludes') else '')
      o.append(f'<tr><th scope="row">{E(t["name"])}</th><td class="bg-p">{E(price)}</td><td>{E(t.get("time",""))}</td><td>{inc}</td></tr>')
    o.append('</tbody></table></div>')
    q=s.get('quantity')
    if q and q.get('perUnitMin'): o.append(f'<p class="muted"><small>{E(q["label"])}: {tr(q["perUnitMin"])} – {tr(q["perUnitMax"])} mỗi đơn vị.</small></p>')
    o.append('</article>')
  o.append('</div>')
Rr=P['rules']
cb=', '.join(f'{b["minServices"]}{"+" if b is Rr["comboDiscount"][-1] else ""} dịch vụ giảm {b["percent"]}%' for b in Rr['comboDiscount'])
pp=', '.join(f'{v["label"].lower()} giảm {v["percent"]}%' for k,v in Rr['prepay'].items() if v['percent'])
o.append(f'<div class="gap"></div><div class="t rv"><span class="k">// ưu đãi</span><h2>Giảm giá combo và trả trước</h2></div><ul class="dlv">'
  f'<li class="glass rv"><span>Combo khoản làm một lần: {E(cb)} (tối đa {Rr["maxDiscountPercent"]}% và {tr(Rr["maxDiscountAmount"])}).</span></li>'
  f'<li class="glass rv"><span>Khoản hằng tháng: {E(pp)}. Tên miền giảm 15% khi trả trước 2 năm.</span></li>'
  f'<li class="glass rv"><span>Mỗi khoản chỉ nhận một loại giảm, không cộng dồn, tối đa {Rr["maxLineDiscountPercent"]}% mỗi khoản.</span></li>'
  '<li class="glass rv"><span>Thanh toán: dịch vụ tính theo tháng/năm thanh toán 100% trước theo kỳ đã chọn (tháng, 6, 12 hoặc 24 tháng; tên miền theo năm), không đặt cọc. Khoản làm một lần: đặt cọc 30–50%, phần còn lại khi nghiệm thu; 2 lần chỉnh sửa trong phạm vi đã thống nhất, bảo hành lỗi kỹ thuật 60 ngày sau bàn giao.</span></li>'
  '<li class="glass rv"><span>Cần gấp: phụ phí 20% (rút ~30% thời gian) hoặc 40% (rút ~50%) trên khoản làm một lần.</span></li></ul></div></section>')
o.append('<section class="soft" id="tinh-gia"><div class="wrap"><div class="t rv"><span class="k">// tự tính giá</span><h2>Công cụ tính giá <span class="gt">combo</span></h2><p>Tích dịch vụ, chọn gói và kỳ thanh toán. Kết quả là khoảng giá tham khảo, chưa bao gồm VAT.</p></div>'
  '<div class="bg-calc" id="bg-calc"><div class="bg-list glass" id="bg-list"><noscript><p>Công cụ cần bật JavaScript. Bạn có thể xem bảng giá phía trên hoặc <a href="lien-he.html">liên hệ</a> để nhận báo giá.</p></noscript></div>'
  '<aside class="bg-sum glass" aria-live="polite"><div class="bg-ctl"><label>Kỳ thanh toán khoản tháng<select id="bg-prepay"></select></label><label>Tiến độ<select id="bg-rush"></select></label></div>'
  '<p class="mono k">Tạm tính</p><p class="bg-total" id="bg-total">Chưa chọn dịch vụ</p><div id="bg-detail" class="bg-detail"></div>'
  '<p class="bg-dis"><small>Giá chưa bao gồm VAT. Giá chỉ mang tính tham khảo theo khoảng, báo giá chính xác sau khi trao đổi nhu cầu. Quảng cáo: chưa gồm tiền quảng cáo trả cho nền tảng.</small></p>'
  '<a class="btn mag" id="bg-send" href="lien-he.html#form">Gửi số liệu sang liên hệ</a></aside></div></div></section>')
FAQ=[('Giá trên trang có bao gồm VAT không?','Chưa bao gồm VAT. Giá chỉ mang tính tham khảo theo khoảng, báo giá chính xác sau khi trao đổi nhu cầu.'),
 ('Vì sao hosting và quảng cáo ghi Thương lượng?','Chi phí hosting/VPS phụ thuộc cấu hình; phí quản lý quảng cáo phụ thuộc ngân sách và số kênh. My Agent báo riêng sau khi trao đổi. Phí quảng cáo chưa gồm tiền quảng cáo trả cho nền tảng.'),
 ('Thanh toán thế nào?','Dịch vụ tính theo tháng (chăm sóc website, hosting, email, SEO, quảng cáo, Fanpage) thanh toán 100% trước theo kỳ đã chọn: tháng, 6, 12 hoặc 24 tháng; tên miền thanh toán trước theo năm. Không đặt cọc với các dịch vụ này. Khoản làm một lần (website, app, phần mềm, dữ liệu…) đặt cọc 30–50%, phần còn lại thanh toán khi nghiệm thu.'),
 ('Giá thiết kế đã gồm tên miền và hosting chưa?','Chưa. Tên miền có giá riêng trong bảng giá; hosting/VPS là Thương lượng. Các khoản này tính riêng, chọn thêm trong công cụ tính giá nếu cần.'),
 ('Kết quả công cụ tính giá có phải báo giá chính thức không?','Không. Đây là tạm tính theo khoảng để anh/chị dự trù ngân sách. Bấm "Gửi số liệu sang liên hệ" để My Agent báo giá chính xác.')]
o.append('<section><div class="wrap"><div class="t rv"><span class="k">// faq</span><h2>Câu hỏi thường gặp</h2></div><div class="faq">'+''.join(f'<details class="glass fx"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in FAQ)+'</div>'
  '<p class="relx rv"><span class="mono">Xem thêm:</span> <a href="dich-vu.html">Hệ thống dịch vụ</a> <a href="combo.html">Combo gợi ý</a> <a href="blog.html">Blog kiến thức</a> <a class="btn sm mag" href="lien-he.html">Nhận báo giá chính xác</a></p></div></section>\n')
(R/'bang-gia.html').write_text(head+''.join(o)+foot)
print('bang-gia.html:',len(P['services']),'dịch vụ')
