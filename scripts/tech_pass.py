#!/usr/bin/env python3
"""Idempotent technical pass: SEO head tags, fonts, form wiring, a11y tweaks, sitemap.
Does NOT change visible copy. Run from repo root: python3 scripts/tech_pass.py"""
import re,pathlib,json,html,subprocess,datetime,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from seo_pages import PAGES
NOINDEX={'tra-cuu-tien-do.html'}  # tiện ích: noindex,follow + loại khỏi sitemap
R=pathlib.Path(__file__).resolve().parent.parent
cfg=(R/'js/config.js').read_text()
BASE=re.search(r"siteUrl:\s*'([^']+)'",cfg).group(1)
pages=sorted([p for p in R.glob('*.html')]+list(R.glob('dich-vu/*.html')))
# redirect stubs (noindex) are skipped: no head injection, not in sitemap
pages=[p for p in pages if 'http-equiv="refresh"' not in p.read_text() and p.name!='404.html']
urls=[]
ORG={"@type":"ProfessionalService","@id":BASE+"#org","name":"My Agent","alternateName":"Công ty TNHH Thương mại và Dịch vụ My Agent","url":BASE,"logo":BASE+"assets/icon-512.png","image":BASE+"assets/og-image.png","telephone":"+84328439972","email":"vantungn044@gmail.com",
 "address":{"@type":"PostalAddress","addressLocality":"Thành phố Hồ Chí Minh","addressCountry":"VN"},
 "areaServed":[{"@type":"City","name":"Thành phố Hồ Chí Minh"},{"@type":"Country","name":"Việt Nam"}],"sameAs":[]}
def txt(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',x))).strip()
def jsonld(rel,url,s,desc):
  out=[]; C="https://schema.org"
  if rel=='index.html':
    o=dict(ORG,description=desc)
    out.append({"@context":C,"@graph":[o,{"@type":"WebSite","@id":BASE+"#website","url":BASE,"name":"My Agent","inLanguage":"vi","publisher":{"@id":BASE+"#org"}}]})
    return out
  h1=txt(re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1))
  crumbs=[("Trang chủ",BASE)]
  if rel.startswith('dich-vu/'): crumbs.append(("Dịch vụ",BASE+"dich-vu.html"))
  crumbs.append((h1,url))
  out.append({"@context":C,"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(crumbs)]})
  kw=PAGES.get(rel,{}).get('kw')
  if kw: out.append({"@context":C,"@type":"Service","name":kw,"serviceType":kw,"description":desc,"url":url,"provider":{"@type":"ProfessionalService","@id":BASE+"#org","name":"My Agent","url":BASE},"areaServed":ORG["areaServed"]})
  qa=re.findall(r'<details[^>]*><summary>(.*?)</summary>(.*?)</details>',s,re.S)
  if qa: out.append({"@context":C,"@type":"FAQPage","mainEntity":[{"@type":"Question","name":txt(q),"acceptedAnswer":{"@type":"Answer","text":txt(a)}} for q,a in qa]})
  return out
def lastmod(rel):
  d=subprocess.run(['git','log','-1','--format=%cs','--',rel],cwd=R,capture_output=True,text=True).stdout.strip()
  return d or datetime.date.today().isoformat()
for f in pages:
  rel=f.relative_to(R).as_posix(); p='../'*rel.count('/'); s=f.read_text()
  url=BASE if rel=='index.html' else BASE+rel
  if rel not in NOINDEX: urls.append((url,rel))
  e=lambda x:html.escape(x,quote=True)
  sp=PAGES.get(rel,{})
  if sp:
    s=re.sub(r'<title>.*?</title>','<title>'+e(sp['title'])+'</title>',s,count=1)
    s=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+e(sp['desc'])+'">',s,count=1)
    for k in ('h1','lead'):
      if k in sp and sp[k][1] not in s: s=s.replace(sp[k][0],sp[k][1],1)
  s=re.sub(r'<meta name="robots" content="[^"]*">','',s)
  # fonts: drop Google Fonts, use self-hosted
  s=re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"( crossorigin)?>','',s)
  s=re.sub(r'<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">',
    f'<link rel="preload" href="{p}assets/fonts/be-vietnam-pro-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{p}css/fonts.css">',s)
  s=s.replace(f'<link rel="icon" href="{p}assets/favicon.svg">','')
  s=re.sub(r'<!-- tech:head -->.*?<!-- /tech:head -->','',s,flags=re.S)
  title=html.unescape(re.search(r'<title>(.*?)</title>',s).group(1))
  m=re.search(r'<meta name="description" content="([^"]*)"',s); desc=html.unescape(m.group(1)) if m else ''
  e=lambda x:html.escape(x,quote=True)
  head=[f'<link rel="canonical" href="{url}"><link rel="alternate" hreflang="vi" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">',
   f'<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png"><link rel="manifest" href="{p}site.webmanifest">',
   f'<meta property="og:type" content="website"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="My Agent"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
   f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.png">',
   f'<script src="{p}js/config.js"></script><script src="{p}js/motion.js" defer></script>']
  if rel=='index.html':
    # intro trang chủ: script nhỏ quyết định có chạy intro không (tránh nháy nội dung); failsafe 6.5s; không JS = trang hiện bình thường
    head.append('<script>(function(h){try{var c=window.MYAGENT_CONFIG||{},q=/[?&]intro=([01])/.exec(location.search),f=q&&q[1];if(f==="0")return;if(!f&&(c.introEnabled===false||sessionStorage.getItem("myagent_intro_seen")))return;if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;h.classList.add("intro-on");setTimeout(function(){h.classList.remove("intro-on");var o=document.getElementById("ma-intro");o&&o.remove()},6500)}catch(e){h.classList.remove("intro-on")}})(document.documentElement)</script><script src="js/intro.js" defer></script>')
  if rel in NOINDEX: head.insert(0,'<meta name="robots" content="noindex, follow">')
  for ld in jsonld(rel,url,s,desc): head.append('<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>')
  s=s.replace('</head>','<!-- tech:head -->'+''.join(head)+'<!-- /tech:head --></head>',1)
  # logo images: intrinsic size (svg viewBox 260x64)
  s=s.replace('alt="My Agent" height="40">','alt="My Agent" width="163" height="40" decoding="async">')
  s=s.replace('alt="My Agent" height="44">','alt="My Agent" width="179" height="44" loading="lazy" decoding="async">')
  # heading order: menu/footer column labels are not document headings
  for tag in ('header','footer'):
    s=re.sub(rf'<{tag}\b.*?</{tag}>',lambda m:re.sub(r'<h4>(.*?)</h4>',r'<p class="h4">\1</p>',m.group(0)),s,flags=re.S)
  # footer link to credits page
  if 'ghi-nguon.html">' not in s.split('<footer',1)[-1]:
    s=s.replace(f'<a href="{p}cong-cu.html">Công cụ miễn phí</a></div></div>',f'<a href="{p}cong-cu.html">Công cụ miễn phí</a><a href="{p}ghi-nguon.html">Ghi nguồn &amp; giấy phép</a></div></div>')
  # contact form wiring
  if '<form class="card glass rv">' in s:
    s=s.replace('<form class="card glass rv">','<form class="card glass rv" data-contact method="POST" action="#" novalidate>')
    s=s.replace('<input required placeholder="Nguyễn Văn A">','<input name="name" required autocomplete="name" maxlength="100" placeholder="Nguyễn Văn A">')
    s=s.replace('<input required type="tel" placeholder="09xx xxx xxx">','<input name="phone" required type="tel" inputmode="tel" autocomplete="tel" pattern="[0-9 +().-]{8,20}" placeholder="09xx xxx xxx">')
    s=s.replace('<input type="email" placeholder="ban@congty.vn">','<input name="email" type="email" autocomplete="email" placeholder="ban@congty.vn">')
    s=re.sub(r'(<form class="card glass rv" data-contact.*?)<select>',r'\1<select name="service">',s,count=1,flags=re.S)
    s=s.replace('<textarea rows="4" placeholder','<textarea name="message" rows="4" maxlength="3000" placeholder')
    if 'name="_honey"' not in s:
      s=re.sub(r'(<form class="card glass rv" data-contact[^>]*>)',r'\1<input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">',s,count=1)
      s=re.sub(r'(data-contact.*?</button>)',r'\1<p class="form-status" role="status" aria-live="polite"></p><p class="form-alt muted"><a data-mailto href="#">Email</a> · <a data-zalo href="#" target="_blank" rel="noopener">Zalo</a></p>',s,count=1,flags=re.S)
    s=re.sub(r'(data-contact.*?)<button class="btn lg mag">',r'\1<button type="submit" class="btn lg mag">',s,count=1,flags=re.S)
  # tra cứu tiến độ: menu + footer (idempotent)
  if 'tra-cuu-tien-do.html"' not in s.split('</nav>',1)[0]:
    on=' class=on' if rel=='tra-cuu-tien-do.html' else ''
    s=re.sub(rf'(<li class="[^"]*"><a href="{re.escape(p)}lien-he.html"[^>]*>Liên hệ</a></li>)',rf'<li class=""><a href="{p}tra-cuu-tien-do.html"{on}>Tra cứu đơn</a></li>\1',s,count=1)
  if 'tra-cuu-tien-do.html">Tra cứu tiến độ' not in s:
    s=s.replace(f'<a href="{p}lien-he.html">Liên hệ</a><a href="{p}cong-cu.html">',f'<a href="{p}lien-he.html">Liên hệ</a><a href="{p}tra-cuu-tien-do.html">Tra cứu tiến độ</a><a href="{p}cong-cu.html">')
  # tin tức công nghệ: menu + footer (idempotent)
  if f'href="{p}tin-tuc.html"' not in s.split('<header',1)[-1].split('</nav>',1)[0]:
    on=' class=on' if rel=='tin-tuc.html' else ''
    s=re.sub(rf'(<li class="[^"]*"><a href="{re.escape(p)}tra-cuu-tien-do.html"[^>]*>Tra cứu đơn</a></li>)',rf'<li class=""><a href="{p}tin-tuc.html"{on}>Tin tức</a></li>\1',s,count=1)
  if f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a>' not in s:
    s=s.replace(f'<a href="{p}tra-cuu-tien-do.html">Tra cứu tiến độ</a>',f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a><a href="{p}tra-cuu-tien-do.html">Tra cứu tiến độ</a>',1)
  # tài nguyên AI agent: chỉ footer (menu trên đã chật) (idempotent)
  if f'<a href="{p}tai-nguyen-ai-agent.html">' not in s:
    s=s.replace(f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a>',f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a><a href="{p}tai-nguyen-ai-agent.html">Tài nguyên AI Agent</a>',1)
  f.write_text(s)
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{lastmod(r)}</lastmod><priority>{"1.0" if u==BASE else "0.7"}</priority></url>\n' for u,r in urls)+'</urlset>\n')
(R/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
# CSS rút gọn (giữ css/style.css làm bản nguồn dễ đọc)
c=(R/'css/style.css').read_text(); c=re.sub(r'/\*.*?\*/','',c,flags=re.S); c=re.sub(r'\s+',' ',c); c=re.sub(r'\s*([{};,>])\s*',r'\1',c).replace(';}','}')
(R/'css/style.min.css').write_text(c.strip()+'\n')
for f in pages:
  t=f.read_text(); t2=re.sub(r'(href="(?:\.\./)?css/)style\.css(\?[^"]*)?"',r'\1style.min.css\2"',t)
  if t2!=t: f.write_text(t2)
print(len(pages),'pages; base',BASE)

# cache-busting (idempotent): ?v=VERSION cho style.min.css và intro.js
_V=(R/'VERSION').read_text().strip()
for f in R.rglob('*.html'):
  if '.git' in f.parts: continue
  t=f.read_text()
  t2=re.sub(r'(css/style\.min\.css)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t)
  t2=re.sub(r'(js/intro\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/resources\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/main\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/motion\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  if t2!=t: f.write_text(t2)
