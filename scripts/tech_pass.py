#!/usr/bin/env python3
"""Idempotent technical pass: SEO head tags, fonts, form wiring, a11y tweaks, sitemap.
Does NOT change visible copy. Run from repo root: python3 scripts/tech_pass.py"""
import re,pathlib,json,html,subprocess,datetime,sys,struct
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from seo_pages import PAGES
NOINDEX={'tra-cuu-tien-do.html'}  # tiện ích: noindex,follow + loại khỏi sitemap
R=pathlib.Path(__file__).resolve().parent.parent
cfg=(R/'js/config.js').read_text()
BASE=re.search(r"siteUrl:\s*'([^']+)'",cfg).group(1)

def image_meta(path):
  """(width, height, mime) từ png/jpg/webp, hoặc None."""
  f=pathlib.Path(path)
  if not f.is_file(): return None
  b=f.read_bytes()
  try:
    if b[:8]==b"\x89PNG\r\n\x1a\n":
      w,h=struct.unpack(">II",b[16:24]); return w,h,"image/png"
    if b[:2]==b"\xff\xd8":
      i=2
      while i<len(b):
        while b[i]==0xff: i+=1
        mk=b[i]; i+=1; ln=struct.unpack(">H",b[i:i+2])[0]
        if mk in (0xc0,0xc1,0xc2):
          h,w=struct.unpack(">HH",b[i+3:i+7]); return w,h,"image/jpeg"
        i+=ln
    if b[:4]==b"RIFF" and b[8:12]==b"WEBP":
      k=b[12:16]
      if k==b"VP8X": return int.from_bytes(b[24:27],"little")+1,int.from_bytes(b[27:30],"little")+1,"image/webp"
      if k==b"VP8 ":
        w,h=struct.unpack("<HH",b[26:30]); return w&0x3fff,h&0x3fff,"image/webp"
      if k==b"VP8L":
        v=int.from_bytes(b[21:25],"little"); return (v&0x3fff)+1,((v>>14)&0x3fff)+1,"image/webp"
  except Exception:
    return None
  return None
THEME_ON=re.search(r'themeEnabled:\s*true',cfg) is not None
_td=re.search(r"themeDefault:\s*'(light|system|dark)'",cfg)
THEME_DEFAULT=_td.group(1) if _td else 'light'
_htd=re.search(r"homeThemeDefault:\s*'(light|system|dark)'",cfg)
HOME_THEME=_htd.group(1) if _htd else None
def fx_attr(key):
  m=re.search(rf'{key}:\s*(true|false)',cfg)
  return 'off' if (m and m.group(1)=='false') else 'on'
HOME_FX=[('cosmos',fx_attr('homeCosmos')),('orbit',fx_attr('homeOrbit')),('pin',fx_attr('homePin')),('glow-m',fx_attr('homeGlowM')),('snap',fx_attr('homeSnap')),('reveal',fx_attr('homeReveal'))]
THEME_BOOT=('<script id="ma-theme-boot">(function(){var d=document.documentElement;if(d.getAttribute("data-fx-theme")==="off")return;'
 'var t;try{t=localStorage.getItem("ma-theme")}catch(e){}'
 'if(t!=="light"&&t!=="dark"){var def=d.getAttribute("data-theme-default")||"light";'
 'if(def==="system"){try{t=matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light"}catch(e){t="light"}}'
 'else t=def==="dark"?"dark":"light"}'
 'd.setAttribute("data-theme",t);d.style.colorScheme=t;var m=document.querySelector(\'meta[name="theme-color"]\');if(m)m.setAttribute("content",t==="light"?"#F4F7FB":"#05070F")})();</script>')
THEME_BTN=('<button type="button" class="theme-btn" aria-pressed="false" aria-label="Chuyển sang giao diện tối">'
 '<svg class="i theme-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4"/></svg>'
 '<svg class="i theme-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4 6.5 6.5 0 0 0 20 14.5z"/></svg>'
 '<span class="theme-lbl"></span></button>')
def inject_theme(s, theme_default=None):
  """Cờ data-fx-theme + script chống nháy + nút header + logo sáng. Idempotent."""
  td=theme_default or THEME_DEFAULT
  val='on' if THEME_ON else 'off'
  if re.search(r'data-fx-theme="(?:on|off)"',s):
    s=re.sub(r'data-fx-theme="(?:on|off)"',f'data-fx-theme="{val}"',s,count=1)
  else:
    s=s.replace('<html lang="vi">',f'<html lang="vi" data-fx-theme="{val}" data-fx-theme-anim="on" data-theme-default="{td}">',1)
  if 'data-fx-theme-anim=' not in s:
    s=s.replace(f'data-fx-theme="{val}"',f'data-fx-theme="{val}" data-fx-theme-anim="on"',1)
  if 'data-theme-default=' in s:
    s=re.sub(r'data-theme-default="[^"]*"',f'data-theme-default="{td}"',s,count=1)
  else:
    s=s.replace('data-fx-theme-anim="on"',f'data-fx-theme-anim="on" data-theme-default="{td}"',1)
  if 'id="ma-theme-boot"' in s:
    s=re.sub(r'<script id="ma-theme-boot">.*?</script>',THEME_BOOT,s,count=1,flags=re.S)
  else:
    s=re.sub(r'(<link rel="(?:preload|stylesheet)")',THEME_BOOT+r'\1',s,count=1)
  if 'class="theme-btn"' in s:
    s=re.sub(r'<button type="button" class="theme-btn"[\s\S]*?</button>',THEME_BTN,s,count=1)
  elif '<button class="burger"' in s:
    s=s.replace('<button class="burger"',THEME_BTN+'<button class="burger"',1)
  def logos(m):
    pre,w,h,rest=m.groups()
    a=f'<img class="logo-dk" src="{pre}logo-dark.svg" alt="My Agent" width="{w}" height="{h}"{rest}>'
    b=f'<img class="logo-lt" src="{pre}logo.svg" alt="My Agent" width="{w}" height="{h}"{rest}>'
    return a+b
  s=re.sub(r'<img (?![^>]*\blogo-dk\b)src="((?:\.\./|/)*assets/)logo-dark\.svg" alt="My Agent" width="(\d+)" height="(\d+)"([^>]*)>',logos,s)
  return s
pages=sorted([p for p in R.glob('*.html')]+list(R.glob('dich-vu/*.html'))+list(R.glob('tin-tuc/**/*.html'))+list(R.glob('blog/**/*.html')))
# redirect stubs (noindex) are skipped: no head injection, not in sitemap
pages=[p for p in pages if 'http-equiv="refresh"' not in p.read_text() and p.name!='404.html']
urls=[]
# Thực thể (v0.9.7, bản chốt SEO My Agent 28/10/2026): chỉ dùng tên "My Agent" (không tên pháp nhân/MST),
# không địa chỉ, không giá; Organization.sameAs chỉ chứa kênh chính thức thật (v0.9.10: Fanpage facebook.com/myagentvn); link cá nhân nằm ở founder.
FB_PAGE="https://www.facebook.com/myagentvn"
ORG={"@type":"ProfessionalService","@id":BASE+"#org","name":"My Agent","url":BASE,
 "logo":{"@type":"ImageObject","@id":BASE+"#logo","url":BASE+"assets/icon-512.png","contentUrl":BASE+"assets/icon-512.png","width":512,"height":512,"caption":"My Agent"},
 "image":BASE+"assets/og-image.png","telephone":"+84328439972","email":"vantungn044@gmail.com","founder":{"@id":BASE+"#founder"},
 "areaServed":[{"@type":"City","name":"Thành phố Hồ Chí Minh"},{"@type":"Country","name":"Việt Nam"}],
 "contactPoint":{"@type":"ContactPoint","telephone":"+84328439972","contactType":"customer service","areaServed":"VN","availableLanguage":["vi"]},
 "sameAs":[FB_PAGE]}
FOUNDER={"@type":"Person","@id":BASE+"#founder","name":"Nguyễn Văn Tùng","alternateName":"Peter","jobTitle":"Nhà sáng lập","worksFor":{"@id":BASE+"#org"},
 "sameAs":["https://www.facebook.com/nguyen.van.tung.109588","https://www.linkedin.com/in/peterpark108/"]}
def txt(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',x))).strip()
def jsonld(rel,url,s,desc):
  out=[]; C="https://schema.org"
  if rel=='index.html':
    o=dict(ORG,description=desc)
    out.append({"@context":C,"@graph":[o,FOUNDER,{"@type":"WebSite","@id":BASE+"#website","url":BASE,"name":"My Agent","inLanguage":"vi","publisher":{"@id":BASE+"#org"}}]})
    return out+faqld(s)
  h1=txt(re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1))
  crumbs=[("Trang chủ",BASE)]
  if rel.startswith('dich-vu/'): crumbs.append(("Dịch vụ",BASE+"dich-vu.html"))
  if rel.startswith('tin-tuc/'): crumbs.append(("Tin tức công nghệ",BASE+"tin-tuc.html"))
  if rel.startswith('blog/'): crumbs.append(("Blog kiến thức",BASE+"blog.html"))
  crumbs.append((h1,url))
  out.append({"@context":C,"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(crumbs)]})
  if rel in ('ve-chung-toi.html','lien-he.html'): out.append({"@context":C,"@type":"AboutPage" if rel=='ve-chung-toi.html' else "ContactPage","name":h1,"url":url,"inLanguage":"vi","isPartOf":{"@id":BASE+"#website"},"mainEntity":{"@id":BASE+"#org"}})
  if rel=='bang-gia.html': out.append({"@context":C,"@type":"WebPage","name":h1,"url":url,"description":desc,"inLanguage":"vi","isPartOf":{"@id":BASE+"#website"},"publisher":{"@id":BASE+"#org"}})
  kw=PAGES.get(rel,{}).get('kw')
  if kw: out.append({"@context":C,"@type":"Service","name":kw,"serviceType":kw,"description":desc,"url":url,"provider":{"@id":BASE+"#org"},"areaServed":ORG["areaServed"]})
  return out+faqld(s)
def faqld(s):
  qa=re.findall(r'<details[^>]*><summary>(.*?)</summary>(.*?)</details>',s,re.S)
  return [{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":txt(q),"acceptedAnswer":{"@type":"Answer","text":txt(a)}} for q,a in qa]}] if qa else []
def lastmod(rel):
  m=re.search(r'property="article:modified_time" content="(\d{4}-\d{2}-\d{2})',(R/rel).read_text())
  if m: return m.group(1)
  d=subprocess.run(['git','log','-1','--format=%cs','--',rel],cwd=R,capture_output=True,text=True).stdout.strip()
  return d or datetime.date.today().isoformat()
for f in pages:
  rel=f.relative_to(R).as_posix(); p='../'*rel.count('/'); s=f.read_text()
  url=BASE if rel=='index.html' else BASE+rel
  if '<!-- blog:empty -->' in s: NOINDEX.add(rel)  # blog chưa có bài: noindex + không vào sitemap
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
  ogt='article' if 'property="article:published_time"' in s else 'website'
  im=re.search(r'<link rel="image_src" href="([^"]+)">',s); ogi=im.group(1) if im else BASE+'assets/og-image.png'
  _meta=image_meta(R/ogi[len(BASE):]) if ogi.startswith(BASE) else None
  ow,oh,ot=(_meta if _meta else (1200,630,'image/png'))
  head=[f'<link rel="canonical" href="{url}"><link rel="alternate" hreflang="vi" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">',
   f'<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png"><link rel="manifest" href="{p}site.webmanifest">',
   f'<meta property="og:type" content="{ogt}"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="My Agent"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogi}"><meta property="og:image:width" content="{ow}"><meta property="og:image:height" content="{oh}"><meta property="og:image:type" content="{ot}">',
   f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{ogi}">',
   f'<script src="{p}js/config.js"{" defer" if rel=="index.html" else ""}></script><script src="{p}js/theme.js" defer></script><script src="{p}js/motion.js" defer></script><script src="{p}js/chat.js" defer></script>']
  # v0.9.28: trang chủ dùng màn intro 3D (#i3d trong body, js/intro3d.js tải sau sự kiện load); bỏ overlay intro.js 6,5s cũ
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
    s=s.replace('<input required type="tel" placeholder="09xx xxx xxx">','<input name="phone" required type="tel" inputmode="tel" autocomplete="tel" pattern="[0-9 +.\\(\\)\\-]{8,20}" placeholder="09xx xxx xxx">')
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
  # khu vực phục vụ (v0.9.29, Peter duyệt 01/11: GBP dạng phục vụ tận nơi, không công khai địa chỉ cụ thể): footer + trang Liên hệ (idempotent, thay dòng cũ)
  ADDR='Khu vực phục vụ: TP. Hồ Chí Minh và toàn Việt Nam'
  s=re.sub(r'<p class="ct-ad">.*?</p>','',s)
  if '<footer' in s:
    a,b=s.split('<footer',1)
    b=b.replace('(mở tab mới)">Facebook</a></p>','(mở tab mới)">Facebook</a></p><p class="ct-ad">'+ADDR+'</p>',1)
    s=a+'<footer'+b
  if rel=='lien-he.html':
    s=s.replace('>Chat Zalo</a></p><div class="radar"','>Chat Zalo</a></p><p class="ct-ad">'+ADDR+'</p><div class="radar"',1)
  # blog / kiến thức: menu (sau Tin tức) + footer (idempotent)
  if f'href="{p}blog.html"' not in s.split('<header',1)[-1].split('</nav>',1)[0]:
    on=' class=on' if rel=='blog.html' or rel.startswith('blog/') else ''
    s=re.sub(rf'(<li class="[^"]*"><a href="{re.escape(p)}tin-tuc.html"[^>]*>Tin tức</a></li>)',rf'\1<li class=""><a href="{p}blog.html"{on}>Blog</a></li>',s,count=1)
  if '<footer' in s and f'<a href="{p}blog.html">Blog / Kiến thức</a>' not in s.split('<footer',1)[1]:
    a,b=s.split('<footer',1)
    s=a+'<footer'+b.replace(f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a>',f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a><a href="{p}blog.html">Blog / Kiến thức</a>',1)
  # v0.8.1 menu gọn: "Về chúng tôi" chỉ ở footer, "Thiết kế website" nằm trong dropdown Dịch vụ (idempotent)
  if '</nav>' in s:
    hd,tl=s.split('</nav>',1)
    hd=re.sub(rf'<li class="[^"]*"><a href="{re.escape(p)}ve-chung-toi.html"[^>]*>Về chúng tôi</a></li>','',hd)
    hd=re.sub(rf'<li class="[^"]*"><a href="{re.escape(p)}dich-vu/thiet-ke-website.html"[^>]*>Thiết kế website</a></li>','',hd)
    if rel=='dich-vu.html' or rel.startswith('dich-vu/'):
      hd=hd.replace(f'<li class="has"><a href="{p}dich-vu.html">Dịch vụ<',f'<li class="has"><a href="{p}dich-vu.html" class=on>Dịch vụ<',1)
    s=hd+'</nav>'+tl
  if '<footer' in s and f'href="{p}ve-chung-toi.html"' not in s.split('<footer',1)[1]:
    a,b=s.split('<footer',1)
    s=a+'<footer'+b.replace(f'<a href="{p}index.html">Trang chủ</a>',f'<a href="{p}index.html">Trang chủ</a><a href="{p}ve-chung-toi.html">Về chúng tôi</a>',1)
  # bảng giá: menu (sau Combo) + footer (sau Combo dịch vụ) + script điền sẵn trên lien-he (idempotent)
  if f'href="{p}bang-gia.html"' not in s.split('<header',1)[-1].split('</nav>',1)[0]:
    on=' class=on' if rel=='bang-gia.html' else ''
    s=re.sub(rf'(<li class="[^"]*"><a href="{re.escape(p)}combo.html"[^>]*>Combo</a></li>)',rf'\1<li class=""><a href="{p}bang-gia.html"{on}>Bảng giá</a></li>',s,count=1)
  if '<footer' in s and f'<a href="{p}bang-gia.html">Bảng giá</a>' not in s.split('<footer',1)[1]:
    a,b=s.split('<footer',1)
    s=a+'<footer'+b.replace(f'<a href="{p}combo.html">Combo dịch vụ</a>',f'<a href="{p}combo.html">Combo dịch vụ</a><a href="{p}bang-gia.html">Bảng giá</a>',1)
  if rel=='lien-he.html' and 'js/lien-he-prefill.js' not in s:
    s=s.replace('</body>','<script src="js/lien-he-prefill.js" defer></script></body>',1)
  # tài nguyên AI agent: chỉ footer (menu trên đã chật) (idempotent)
  if f'<a href="{p}tai-nguyen-ai-agent.html">' not in s:
    s=s.replace(f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a>',f'<a href="{p}tin-tuc.html">Tin tức công nghệ</a><a href="{p}tai-nguyen-ai-agent.html">Tài nguyên AI Agent</a>',1)
  # footer: Fanpage chính thức (v0.9.10, idempotent)
  if '<footer' in s and FB_PAGE not in s.split('<footer',1)[1]:
    a,b=s.split('<footer',1)
    s=a+'<footer'+b.replace('rel="noopener">Chat Zalo</a></p>','rel="noopener">Chat Zalo</a> · <a href="'+FB_PAGE+'" target="_blank" rel="noopener" aria-label="Fanpage Facebook My Agent (mở tab mới)">Facebook</a></p>',1)
  td=HOME_THEME if rel=='index.html' and HOME_THEME else THEME_DEFAULT
  if rel=='index.html':
    for name,val in HOME_FX:
      attr=f'data-fx-{name}'
      if re.search(rf'{attr}="(?:on|off)"',s):
        s=re.sub(rf'{attr}="(?:on|off)"',f'{attr}="{val}"',s,count=1)
      else:
        s=s.replace('<html lang="vi"',f'<html lang="vi" {attr}="{val}"',1)
  f.write_text(inject_theme(s, td))
# 404: không qua head tech, chỉ cần config.js để đo lường (GA) – nguồn tải duy nhất (idempotent)
f404=R/'404.html'
if f404.exists():
  t=f404.read_text()
  if 'js/config.js' not in t: t=t.replace('</head>','<script src="/js/config.js"></script></head>',1)
  if 'js/theme.js' not in t: t=t.replace('</head>','<script src="/js/theme.js" defer></script></head>',1)
  # 404 đang dùng logo chữ đậm (logo.svg) trên nền tối: thêm bản logo-dark, CSS chọn theo theme
  if 'logo-dk' not in t and 'src="/assets/logo.svg"' in t:
    t=t.replace('<img src="/assets/logo.svg" alt="My Agent" width="163" height="40">','<img class="logo-dk" src="/assets/logo-dark.svg" alt="My Agent" width="163" height="40"><img class="logo-lt" src="/assets/logo.svg" alt="My Agent" width="163" height="40">',1)
  f404.write_text(inject_theme(t))
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{lastmod(r)}</lastmod><priority>{"1.0" if u==BASE else ("0.6" if r.startswith(("tin-tuc/","blog/")) else "0.7")}</priority></url>\n' for u,r in urls)+'</urlset>\n')
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
  t2=re.sub(r'(js/intro3d\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(css/intro3d\.css)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/resources\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/main\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/config\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/chat\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/theme\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/motion\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/(?:combo-calculator|bang-gia|lien-he-prefill)\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(css/home\.css)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/home\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  t2=re.sub(r'(js/vendor/gsap/(?:gsap|ScrollTrigger)\.min\.js)(\?v=[^"]*)?"',r'\1?v='+_V+'"',t2)
  if t2!=t: f.write_text(t2)
hj=R/'js/home.js'
if hj.exists():
  t=hj.read_text(); t2=t
  t2=re.sub(r'(js/vendor/gsap/(?:gsap|ScrollTrigger)\.min\.js)(\?v=[^"\']*)?',r'\1?v='+_V,t2)
  if t2!=t: hj.write_text(t2)
