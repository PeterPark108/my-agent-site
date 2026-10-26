#!/usr/bin/env python3
"""Idempotent technical pass: SEO head tags, fonts, form wiring, a11y tweaks, sitemap.
Does NOT change visible copy. Run from repo root: python3 scripts/tech_pass.py"""
import re,pathlib,json,html
R=pathlib.Path(__file__).resolve().parent.parent
cfg=(R/'js/config.js').read_text()
BASE=re.search(r"siteUrl:\s*'([^']+)'",cfg).group(1)
pages=sorted([p for p in R.glob('*.html')]+list(R.glob('dich-vu/*.html')))
urls=[]
for f in pages:
  rel=f.relative_to(R).as_posix(); p='../'*rel.count('/'); s=f.read_text()
  url=BASE if rel=='index.html' else BASE+rel; urls.append(url)
  # fonts: drop Google Fonts, use self-hosted
  s=re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"( crossorigin)?>','',s)
  s=re.sub(r'<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">',
    f'<link rel="preload" href="{p}assets/fonts/be-vietnam-pro-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{p}css/fonts.css">',s)
  s=s.replace(f'<link rel="icon" href="{p}assets/favicon.svg">','')
  s=re.sub(r'<!-- tech:head -->.*?<!-- /tech:head -->','',s,flags=re.S)
  title=html.unescape(re.search(r'<title>(.*?)</title>',s).group(1))
  m=re.search(r'<meta name="description" content="([^"]*)"',s); desc=html.unescape(m.group(1)) if m else ''
  e=lambda x:html.escape(x,quote=True)
  head=[f'<link rel="canonical" href="{url}">',
   f'<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png"><link rel="manifest" href="{p}site.webmanifest">',
   f'<meta property="og:type" content="website"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="My Agent"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
   f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.png">',
   f'<script src="{p}js/config.js"></script>']
  if rel=='index.html':
    ld={"@context":"https://schema.org","@type":"ProfessionalService","name":"Công ty TNHH Thương mại và Dịch vụ My Agent","alternateName":"My Agent","url":BASE,"logo":BASE+"assets/icon-512.png","image":BASE+"assets/og-image.png","description":desc,"telephone":"","email":"","taxID":"","address":{"@type":"PostalAddress","streetAddress":"","addressLocality":"","addressCountry":"VN"},"sameAs":[]}
    head.append('<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>')
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
  f.write_text(s)
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>{"1.0" if u==BASE else "0.7"}</priority></url>\n' for u in urls)+'</urlset>\n')
(R/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
print(len(pages),'pages; base',BASE)
