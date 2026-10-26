#!/usr/bin/env python3
"""Kiểm tra SEO (stdlib). Cục bộ: python3 scripts/seo_audit.py
Live: python3 scripts/seo_audit.py https://myagentvn.com/"""
import sys,re,json,html,pathlib,urllib.request
BASE='https://myagentvn.com/'; R=pathlib.Path(__file__).resolve().parent.parent
live=sys.argv[1] if len(sys.argv)>1 else None
def get(rel):
  if live:
    try: return urllib.request.urlopen(urllib.request.Request(live+rel,headers={'User-Agent':'MyAgent-SEO-audit'}),timeout=20).read().decode()
    except Exception as e: return None
  f=R/rel; return f.read_text() if f.exists() else None
sm=get('sitemap.xml') or ''; robots=get('robots.txt') or ''
locs=re.findall(r'<loc>(.*?)</loc>',sm)
rels=sorted({p.relative_to(R).as_posix() for p in list(R.glob('*.html'))+list(R.glob('dich-vu/*.html'))})
issues=[]; titles={}; descs={}; n=0
def bad(r,m): issues.append(f'{r}: {m}')
if f'Sitemap: {BASE}sitemap.xml' not in robots: bad('robots.txt','thiếu dòng Sitemap đúng domain')
if re.search(r'Disallow:\s*/\S',robots): bad('robots.txt','có Disallow (dùng noindex thay thế)')
if 'github.io' in sm+robots: bad('sitemap/robots','còn github.io')
for rel in rels:
  s=get(rel)
  if s is None: bad(rel,'không tải được'); continue
  if 'http-equiv="refresh"' in s or rel=='404.html':
    if 'noindex' not in s: bad(rel,'trang chuyển hướng/404 thiếu noindex')
    if BASE+rel in locs: bad(rel,'không được nằm trong sitemap')
    continue
  n+=1; url=BASE if rel=='index.html' else BASE+rel
  noidx='name="robots" content="noindex' in s
  if noidx and url in locs: bad(rel,'noindex nhưng có trong sitemap')
  if not noidx and url not in locs: bad(rel,'thiếu trong sitemap')
  t=re.search(r'<title>(.*?)</title>',s,re.S); t=html.unescape(t.group(1)) if t else ''
  d=re.search(r'<meta name="description" content="([^"]*)"',s); d=html.unescape(d.group(1)) if d else ''
  if not t or len(t)>60: bad(rel,f'title dài {len(t)} ký tự')
  if not d or len(d)>155: bad(rel,f'description dài {len(d)} ký tự')
  titles.setdefault(t,[]).append(rel); descs.setdefault(d,[]).append(rel)
  if f'<link rel="canonical" href="{url}">' not in s: bad(rel,'canonical sai')
  for k in ('github.io','/portfolio/'):
    if k in s: bad(rel,f'còn tham chiếu {k}')
  for tag in (f'property="og:url" content="{url}"',f'property="og:image" content="{BASE}assets/og-image.png"','property="og:locale" content="vi_VN"','property="og:title"','property="og:description"','name="twitter:card" content="summary_large_image"',f'hreflang="vi" href="{url}"','hreflang="x-default"'):
    if tag not in s: bad(rel,'thiếu '+tag.split('"')[1])
  h=len(re.findall(r'<h1[\s>]',s))
  if h!=1: bad(rel,f'{h} thẻ H1')
  for im in re.findall(r'<img\b[^>]*>',s):
    if 'alt=' not in im: bad(rel,'ảnh thiếu alt: '+im[:60])
    if 'width=' not in im or 'height=' not in im: bad(rel,'ảnh thiếu width/height')
  lds=re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)
  types=[]
  for x in lds:
    try: j=json.loads(x)
    except Exception as e: bad(rel,f'JSON-LD lỗi: {e}'); continue
    for o in j.get('@graph',[j]):
      types.append(o.get('@type'))
      if o.get('@context',j.get('@context'))!='https://schema.org': bad(rel,'JSON-LD thiếu @context')
      if 'offers' in o or 'price' in json.dumps(o): bad(rel,'JSON-LD có giá')
      if o.get('@type')=='FAQPage':
        vis=html.unescape(re.sub(r'<[^>]+>','',s))
        for q in o['mainEntity']:
          if q['name'] not in re.sub(r'\s+',' ',vis): bad(rel,'FAQ JSON-LD không khớp chữ hiển thị: '+q['name'][:40])
  if rel=='index.html':
    for need in ('ProfessionalService','WebSite'):
      if need not in types: bad(rel,'thiếu '+need)
  else:
    if 'BreadcrumbList' not in types: bad(rel,'thiếu BreadcrumbList')
    if rel.startswith('dich-vu/') and 'Service' not in types: bad(rel,'thiếu Service')
    if rel.startswith('dich-vu/') and '<details' in s and 'FAQPage' not in types: bad(rel,'có FAQ nhưng thiếu FAQPage')
  for a in re.findall(r'<a\b[^>]*>(.*?)</a>',s,re.S):
    tx=re.sub(r'<[^>]+>','',a).strip().lower()
    if tx in ('xem thêm','click here','tại đây','bấm vào đây'): bad(rel,f'link text chung chung: "{tx}"')
for k,v in list(titles.items())+list(descs.items()):
  if len(v)>1: issues.append(f'trùng title/description: {v}')
print(f'{"LIVE "+live if live else "LOCAL"}: {n} trang index được kiểm tra, {len(locs)} URL trong sitemap, {len(issues)} vấn đề')
for i in issues: print(' -',i)
sys.exit(1 if issues else 0)
