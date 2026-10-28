#!/usr/bin/env python3
"""Idempotent: chèn phần chuyên sâu vào dich-vu/*.html từ scripts/svc_data.py.
Phần mới nằm giữa <!-- svc-deep --> ... <!-- /svc-deep -->; quy trình (ol.tl) và FAQ bổ sung (details.fx) được dựng lại mỗi lần chạy.
Chạy: python3 scripts/svc_deep.py && python3 scripts/tech_pass.py"""
import re,pathlib,html,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from svc_data import S
R=pathlib.Path(__file__).resolve().parent.parent
E=lambda x:html.escape(x,quote=False)
CK='<svg class="i " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
XX='<svg class="i " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>'
AR='<svg class="i " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
def T(x,y,s,a='middle',c='tx',z=13): return f'<text x="{x}" y="{y}" text-anchor="{a}" class="{c}" font-size="{z}">{E(s)}</text>'
def box(x,y,w,h,s,c='nd',z=13): return f'<g class="{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>{T(x+w/2,y+h/2+4.5,s,z=z)}</g>'
def flow(L):
  n=len(L); w=600/n; out=[]
  for i,s in enumerate(L):
    x=i*w+6; out.append(box(x,95,w-12,50,s,z=12 if len(s)>14 else 13))
    if i<n-1: out.append(f'<path class="dl" d="M{x+w-12} 120h12"/>')
  out.append(f'<path class="dl lp" d="M30 175 Q300 230 570 175"/>'); out.append(T(300,222,'đo lường → cải tiến liên tục','middle','mu',11))
  return ''.join(out)
def browser(L):
  o=['<g class="fr"><rect x="110" y="10" width="380" height="220" rx="12"/><path d="M110 34h380"/></g><circle class="dt" cx="126" cy="22" r="4"/><circle class="dt b" cx="140" cy="22" r="4"/><circle class="dt c" cx="154" cy="22" r="4"/>']
  hs=[24,52,40,34,24]; y=42
  for i,(s,h) in enumerate(zip(L,hs)):
    o.append(box(124,y,352,h,s,'nd'+(' hl' if i==1 else ''),12)); y+=h+6
  return ''.join(o)
def dash(L):
  o=[]
  for i,s in enumerate(L):
    o.append(f'<g class="nd"><rect x="{10+i*148}" y="10" width="136" height="54" rx="10"/></g>'+T(78+i*148,32,s,c='mu',z=11)+f'<rect class="kp" x="{30+i*148}" y="44" width="{60+i%2*30}" height="8" rx="4"/>')
  o.append('<g class="fr"><rect x="10" y="76" width="360" height="154" rx="10"/><rect x="384" y="76" width="206" height="154" rx="10"/></g>')
  for i,h in enumerate([50,80,64,100,90,120,108]):
    o.append(f'<rect class="bar" style="--d:{i*80}ms" x="{34+i*48}" y="{214-h}" width="28" height="{h}" rx="4"/>')
  o.append('<path class="dl" d="M400 200 L440 170 L480 182 L520 130 L570 110"/>')
  return ''.join(o)
def phone(L):
  o=[]
  for k in range(2):
    x=150+k*170
    o.append(f'<g class="fr"><rect x="{x}" y="8" width="130" height="224" rx="18"/><path d="M{x+50} 20h30"/></g>')
    for j,s in enumerate(L[k*2:k*2+2]):
      o.append(box(x+12,40+j*92,106,80,s,'nd'+(' hl' if j==0 and k==1 else ''),11))
  o.append('<path class="dl" d="M282 120h36"/>'); return ''.join(o)
def checklist(L):
  o=[]
  for i,s in enumerate(L):
    c,r=i%2,i//2; x=20+c*290; y=20+r*72
    o.append(f'<g class="nd ck" style="--d:{i*120}ms"><rect x="{x}" y="{y}" width="270" height="56" rx="10"/><path class="tk" d="M{x+18} {y+29}l7 7 13-14"/></g>'+T(x+52,y+33,s,'start',z=12))
  return ''.join(o)
def mapv(L):
  o=['<g class="fr"><rect x="10" y="10" width="250" height="220" rx="12"/></g>','<path class="grd" d="M10 80h250M10 160h250M90 10v220M180 10v220M30 230 L240 20"/>','<path class="pin" d="M135 60c-24 0-38 18-38 36 0 26 38 64 38 64s38-38 38-64c0-18-14-36-38-36z"/><circle class="pc" cx="135" cy="96" r="12"/>']
  o.append(box(290,14,300,40,L[0],'nd hl',13))
  for i,s in enumerate(L[1:]):
    o.append(f'<g class="nd ck" style="--d:{i*120}ms"><rect x="290" y="{66+i*42}" width="300" height="34" rx="8"/><path class="tk" d="M304 {83+i*42}l6 6 11-12"/></g>'+T(334,88+i*42,s,'start',z=12))
  return ''.join(o)
def funnel(L):
  o=[]; n=len(L)
  for i,s in enumerate(L):
    w=520-i*110; x=300-w/2; y=14+i*54
    o.append(f'<g class="nd fn" style="--d:{i*140}ms"><rect x="{x}" y="{y}" width="{w}" height="44" rx="10"/>{T(300,y+27,s)}</g>')
  return ''.join(o)
def calendar(L):
  days=['T2','T3','T4','T5','T6','T7','CN']; o=[]
  for i,d in enumerate(days):
    x=10+i*84; o.append(T(x+38,22,d,c='mu',z=11))
    o.append(f'<g class="fr"><rect x="{x}" y="32" width="76" height="196" rx="10"/></g>')
  pos=[(0,0),(1,2),(2,4),(3,1),(4,3),(0,5),(1,6)]
  for k,(li,di) in enumerate(pos):
    x=14+di*84; y=44+(k%3)*60
    o.append(f'<g class="nd ck{" hl" if li==1 else ""}" style="--d:{k*90}ms"><rect x="{x}" y="{y}" width="68" height="48" rx="8"/>{T(x+34,y+28,L[li],z=10)}</g>')
  return ''.join(o)
def doc(L):
  o=[]
  for i,s in enumerate(L):
    x=20+i*145; o.append(f'<g class="nd ck" style="--d:{i*120}ms"><rect x="{x}" y="20" width="125" height="176" rx="6"/><rect class="kp" x="{x+14}" y="40" width="97" height="44" rx="4"/><path class="grd" d="M{x+14} 104h97M{x+14} 120h80M{x+14} 136h90M{x+14} 152h60"/></g>'+T(x+62,220,s,z=12))
  return ''.join(o)
def arch(L):
  o=[box(10,95,110,50,L[0]),'<path class="dl" d="M120 120h20"/>',box(140,95,110,50,L[1]),'<path class="dl" d="M250 120h20"/>',box(270,95,110,50,L[2],'nd hl'),'<path class="dl" d="M380 110 L420 60M380 130 L420 180"/>',box(420,35,170,50,L[3]),box(420,155,170,50,L[4])]
  o.append(T(325,230,'HTTPS · sao lưu · nhật ký thay đổi',c='mu',z=11)); return ''.join(o)
def etl(L):
  o=[]
  for i,s in enumerate(L): o.append(box(10,12+i*56,100,40,s,z=12)); o.append(f'<path class="dl" d="M110 {32+i*56} C150 {32+i*56} 150 120 180 120"/>')
  o+= [box(180,95,90,50,'Extract'),'<path class="dl" d="M270 120h16"/>',box(286,95,90,50,'Transform'),'<path class="dl" d="M376 120h16"/>',box(392,80,100,80,'Kho dữ liệu','nd hl'),'<path class="dl" d="M492 120h16"/>',box(508,95,82,50,'Báo cáo',z=12)]
  o.append(T(335,190,'kiểm tra chất lượng sau mỗi lần nạp',c='mu',z=11)); return ''.join(o)
def timeline(L):
  o=['<g class="fr"><rect x="10" y="10" width="580" height="220" rx="12"/></g>']
  for i,t in enumerate(['Hình','Chữ / phụ đề','Âm thanh']):
    y=50+i*56; o.append(T(22,y+22,t,'start','mu',11))
    segs=[(110,120),(236,220),(462,118)] if i!=2 else [(110,468)]
    for j,(x,w) in enumerate(segs):
      o.append(f'<g class="nd ck{" hl" if i==0 and j==0 else ""}" style="--d:{(i*3+j)*90}ms"><rect x="{x}" y="{y}" width="{w-6}" height="36" rx="6"/>{T(x+w/2-3,y+23,L[j] if i==0 else ("" if i==2 else "phụ đề"),z=11)}</g>')
  o.append('<path class="dl ph" d="M110 40v176"/>'); return ''.join(o)
V=dict(flow=flow,browser=browser,dash=dash,phone=phone,checklist=checklist,map=mapv,funnel=funnel,calendar=calendar,doc=doc,arch=arch,etl=etl,timeline=timeline)
def svg(kind,L,desc,slug):
  return (f'<figure class="dg glass rv"><div class="sc" tabindex="0" aria-label="Sơ đồ, vuốt ngang để xem"><svg viewBox="0 0 600 240" role="img" aria-labelledby="dgt-{slug} dgd-{slug}" preserveAspectRatio="xMidYMid meet">'
          f'<title id="dgt-{slug}">Sơ đồ minh hoạ</title><desc id="dgd-{slug}">{E(desc)}</desc>{V[kind](L)}</svg></div><figcaption class="mono">// {E(desc)}</figcaption></figure>')
def h1of(slug):
  s=(R/f'dich-vu/{slug}.html').read_text(); return html.unescape(re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1))).replace('\xa0',' ')
TT='<a class="btn sm ghost" href="../bang-gia.html#tinh-gia">Tự tính giá</a> '
import json
from svc_pricing import rng
PJ={s['id']:s for s in json.loads((R/'data/pricing.json').read_text())['services']}
def fillp(x):
  # {gia:dv/goi} -> khoảng giá + đơn vị, {tg:dv/goi} -> thời gian; lấy từ data/pricing.json (id lạ -> lỗi)
  def f(m):
    s=PJ[m.group(2)]; t=None if m.group(1)=='pq' else [t for t in s['tiers'] if t['id']==m.group(3)][0]
    if m.group(1)=='pq': q=s['quantity']; return rng(q['perUnitMin'],q['perUnitMax'])
    if m.group(1)=='tg': return t['time']
    if m.group(1)=='so': return rng(t['min'],t['max'])
    return 'Thương lượng' if s.get('negotiable') else rng(t['min'],t['max'])+' / '+s['unit']
  return re.sub(r'\{(gia|tg|so|pq):([a-z0-9-]+)/([a-z0-9-]+)\}',f,x)
def intro(slug,d):
  o=''
  for k,h,ps,li in d.get('intro',[]):
    o+=f'<div class="gap"></div><div class="t rv"><span class="k">// {E(k)}</span><h2>{h}</h2></div><div class="card glass rv svi">'+''.join(fillp(x) if x.startswith('<div') else f'<p>{fillp(x)}</p>' for x in ps)
    if li: o+='<ul class="svi-l">'+''.join(f'<li>{CK}<span>{x}</span></li>' for x in li)+'</ul>'
    o+='</div>'
  return o
def block(slug,d):
  t,items=d['exp']; o=['<!-- svc-deep -->'+intro(slug,d)+'<div class="gap"></div><div class="t rv"><span class="k">// chuyên môn</span><h2>Góc nhìn <span class="gt">chuyên&nbsp;môn</span></h2></div>']
  o.append('<div class="xp">'+svg(*d['vis'][:1],d['vis'][1],d['vis'][2],slug)+f'<div class="xpl glass rv"><h3>{E(t)}</h3><ul>'+''.join(f'<li>{CK}<div><b>{E(a)}</b><span>{E(b)}</span></div></li>' for a,b in items)+'</ul></div></div>')
  o.append('<div class="gap"></div><div class="t rv"><span class="k">// bàn giao</span><h2>Bạn nhận <span class="gt">được&nbsp;gì</span></h2></div><ul class="dlv">'+''.join(f'<li class="glass rv">{CK}<span>{E(x)}</span></li>' for x in d['deliv'])+'</ul>')
  o.append('<div class="gap"></div><div class="t rv"><span class="k">// stack</span><h2>Công nghệ <span class="gt">&amp;&nbsp;công&nbsp;cụ</span></h2></div><ul class="tch rv" aria-label="Công nghệ và công cụ">'+''.join(f'<li>{E(x)}</li>' for x in d['tech'])+'</ul><p class="muted rv"><small>Chọn công cụ theo nhu cầu và hệ thống bạn đang dùng; không phải dự án nào cũng dùng tất cả.</small></p>')
  o.append('<div class="gap"></div><div class="t rv"><span class="k">// phù hợp?</span><h2>Phù hợp <span class="gt">với&nbsp;ai</span></h2></div><div class="fitg"><div class="glass rv fit"><h3>Phù hợp khi</h3><ul>'+''.join(f'<li>{CK}{E(x)}</li>' for x in d['fit'])+'</ul></div><div class="glass rv fit no"><h3>Chưa phù hợp khi</h3><ul>'+''.join(f'<li>{XX}{E(x)}</li>' for x in d['nofit'])+'</ul></div></div>')
  o.append('<p class="relx rv"><span class="mono">Dịch vụ liên quan:</span> '+' '.join(f'<a href="{r}.html">{E(h1of(r))}</a>' for r in d['rel'])+f' {TT if slug!='traffic-user' else ''}<a class="btn sm mag" href="../lien-he.html">Trao đổi dự án {AR}</a></p><!-- /svc-deep -->')
  return ''.join(o)
n=0
for slug,d in S.items():
  f=R/f'dich-vu/{slug}.html'; s=f.read_text()
  s=re.sub(r'<!-- svc-deep -->.*?<!-- /svc-deep -->','',s,flags=re.S)
  anchor=re.search(r'<div class="gap"></div><div class="t rv"><span class="k">// quy trình',s); assert anchor,slug
  s=s[:anchor.start()]+block(slug,d)+s[anchor.start():]
  ol=f'<ol class="tl" style="--c:{len(d["steps"])}">'+''.join(f'<li class="rv"><span class="n mono">{i+1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></li>' for i,(a,b) in enumerate(d['steps']))+'</ol>'
  s,k=re.subn(r'<ol class="tl"[^>]*>.*?</ol>',ol,s,count=1,flags=re.S); assert k,slug
  s=re.sub(r'<details class="glass fx">.*?</details>','',s,flags=re.S)
  fx=''.join(f'<details class="glass fx"><summary>{E(q)}</summary><p>{E(fillp(a))}</p></details>' for q,a in d['faq'])
  if d.get('faq_replace'): s,k=re.subn(r'<div class="faq">.*?</div>',lambda m:'<div class="faq">'+fx+'</div>',s,count=1,flags=re.S)
  else: s,k=re.subn(r'<div class="faq">',lambda m:m.group(0)+fx,s,count=1)
  assert k,slug
  # v0.9.11: FAQ chung "7–30 ngày" mâu thuẫn bảng giá app (4–6 tuần trở lên) -> bỏ trên trang app; thời gian app nằm ở FAQ "Làm app mất bao lâu?"
  if slug=='thiet-ke-app': s=re.sub(r'<details class="glass"><summary>Bao lâu thì triển khai xong\?</summary><p>[^<]*7–30 ngày[^<]*</p></details>','',s)
  # v0.9.11 (audit 29/10 + Peter chốt "sau khi bàn giao thì là của khách"): FAQ chung "ai sở hữu website?" trên trang app -> hỏi về app, cùng ý, không thêm điều khoản
  if slug=='thiet-ke-app': s=re.sub(r'<details class="glass"><summary>Sau bàn giao ai sở hữu website\?</summary><p>[^<]*</p></details>','<details class="glass"><summary>Sau bàn giao ai sở hữu app?</summary><p>Sau khi bàn giao, app là của khách: mã nguồn và dữ liệu thuộc về khách. Mã nguồn được giao sau khi thanh toán đủ, như ghi trong bảng giá.</p></details>',s)
  # v0.9.11 (audit 29/10): trang thiết kế website: "7–30 ngày" -> thời gian theo bảng giá
  if slug=='thiet-ke-website': s=re.sub(r'(<details class="glass"><summary>Bao lâu thì triển khai xong\?</summary><p>)[^<]*7–30 ngày[^<]*(</p>)',lambda m:m.group(1)+fillp('Theo bảng giá tham khảo: landing page {tg:thiet-ke-website/landing}, website giới thiệu {tg:thiet-ke-website/gioi-thieu}, website bán hàng {tg:thiet-ke-website/ban-hang}, tính từ khi chốt nội dung và nhận đủ tư liệu; tiến độ được báo rõ từng giai đoạn.')+m.group(2),s)
  if d.get('top_price'):
    i=s.find('<div class="gap" id="bang-gia"></div>'); j=s.find('<p class="muted rv" style="margin-top:18px">',i); j=s.find('</p>',j)+4
    assert i>0 and j>i,slug
    blk=s[i:j]; s=s[:i]+s[j:]
    k=s.find('<div class="t rv"><span class="k">// lợi ích'); assert k>0,slug
    s=s[:k]+blk+'<div class="gap"></div>'+s[k:] if not s[:k].endswith('<div class="gap"></div>') else s[:k]+blk+s[k:]
  f.write_text(s); n+=1
# v0.9.11 (audit 29/10, mục 2–3 + chốt Peter): FAQ dùng chung trên mọi trang dịch vụ
TIME_ALL='Tùy dịch vụ và phạm vi; thời gian tham khảo của từng gói ghi trong bảng giá, tiến độ được báo rõ từng giai đoạn.'
OWN_ALL='Sau khi bàn giao, website là của khách: mã nguồn và dữ liệu thuộc về khách. Mã nguồn được giao sau khi thanh toán đủ, như ghi trong bảng giá.'
for f in sorted(pathlib.Path('dich-vu').glob('*.html')):
  s=f.read_text(); o=s
  s=re.sub(r'(<summary>Bao lâu thì triển khai xong\?</summary><p>)[^<]*7–30 ngày[^<]*(</p>)',lambda m:m.group(1)+TIME_ALL+m.group(2),s)
  s=re.sub(r'(<summary>Sau bàn giao ai sở hữu website\?</summary><p>)[^<]*(</p>)',lambda m:m.group(1)+OWN_ALL+m.group(2),s)
  s=s.replace('Sau khi thanh toán đủ, khách sở hữu mã nguồn, nội dung và tài khoản liên quan.','Sau khi bàn giao, mã nguồn và dữ liệu thuộc về khách; mã nguồn được giao sau khi thanh toán đủ.')
  if s!=o: f.write_text(s)
print('svc_deep:',n,'pages')
