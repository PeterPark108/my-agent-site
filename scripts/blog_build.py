#!/usr/bin/env python3
"""Dựng mục Blog / Kiến thức từ data/blog/*.md (idempotent: cùng đầu vào -> cùng đầu ra).
Khác Tin tức: bài hướng dẫn/kiến thức do My Agent tự viết, không bắt buộc nguồn ngoài.
Mỗi file: data/blog/<slug>.md = front-matter + Markdown (xem docs/blog.md, docs/blog-format.json).
Sinh ra: blog.html (danh sách; 0 bài -> trạng thái "sắp ra mắt", noindex), blog/<slug>.html, blog/feed.xml.
Dùng: python3 scripts/blog_build.py [--validate-only] [--dir DIR] [--no-chatbot]
Sau đó: python3 scripts/tech_pass.py (hoặc dùng luôn scripts/blog_publish.sh)."""
import re,sys,json,html,struct,pathlib,datetime,subprocess
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import news_md as M, news_build as N
R=N.R; BASE=N.BASE; E=N.E; vn=N.vn; today=N.today
CATS={'website':'Website','seo':'SEO','marketing':'Marketing online','du-lieu':'Dữ liệu','ai':'AI & tự động hoá'}
CAT_ICON={'website':N.ICON['web-seo'],'seo':N.ICON['web-seo'],'marketing':N.ICON['nen-tang'],'du-lieu':N.ICON['du-lieu'],'ai':N.ICON['ai']}
FIELDS={'title','slug','date','updated','description','category','tags','services','image','image_alt','draft'}
MIN_WORDS=300
FORBID=N.FORBID+[r'\b24\s*/\s*24\b',r'\b24\s*h\b',r'\btop\s*(1|một)\b',r'(đảm\s*bảo|bảo\s*đảm|cam\s*kết|chắc\s*chắn)\s*(về\s*)?(vị\s*trí|thứ\s*hạng|lên\s*(trang|top|hạng))',r'fpt\s*poly']
# số liệu/giá: phải đánh dấu là ví dụ/giả định hoặc có link nguồn trong cùng đoạn
NUMCLAIM=re.compile(r'\d[\d.,]*\s*(%|phần\s*trăm|triệu|tỷ|nghìn|ngàn|k\b|đ\b|đồng|vnđ|vnd|usd|\$|khách\s*hàng|doanh\s*nghiệp|dự\s*án)',re.I)
MARK=re.compile(r'ví\s*dụ|minh\s*h[oọ]a|giả\s*định|giả\s*sử|\]\(https://',re.I)
SYS_SLUGS={'index','feed'}

def svc_name(slug):
  f=R/'dich-vu'/f'{slug}.html'
  if not re.fullmatch(r'[a-z0-9-]+',slug) or not f.is_file(): return None
  m=re.search(r'<h1[^>]*>(.*?)</h1>',f.read_text(encoding='utf-8'),re.S)
  return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',m.group(1)))).replace('\xa0',' ').strip() if m else slug
def img_size(rel):
  rel=re.sub(r'^(\.\./)+','',rel.lstrip('/'))
  if not re.fullmatch(r'assets/(blog|news)/[\w.-]+\.(png|jpe?g|webp)',rel): return None
  return _sz(rel)
def _sz(rel):
  # N.img_size chỉ nhận assets/news/; đọc kích thước bằng cùng logic cho assets/blog/
  if rel.startswith('assets/news/'): return N.img_size(rel)
  f=R/rel
  if not f.is_file(): return None
  b=f.read_bytes()
  try:
    if b[:8]==b'\x89PNG\r\n\x1a\n': w,h=struct.unpack('>II',b[16:24]); return w,h,rel
    if b[:2]==b'\xff\xd8':
      i=2
      while i<len(b):
        while b[i]==0xff: i+=1
        mk=b[i]; i+=1; ln=struct.unpack('>H',b[i:i+2])[0]
        if mk in (0xc0,0xc1,0xc2): h,w=struct.unpack('>HH',b[i+3:i+7]); return w,h,rel
        i+=ln
    if b[:4]==b'RIFF' and b[8:12]==b'WEBP' and b[12:16]==b'VP8X': return int.from_bytes(b[24:27],'little')+1,int.from_bytes(b[27:30],'little')+1,rel
    if b[:4]==b'RIFF' and b[12:16]==b'VP8 ': w,h=struct.unpack('<HH',b[26:30]); return w&0x3fff,h&0x3fff,rel
    if b[:4]==b'RIFF' and b[12:16]==b'VP8L': v=int.from_bytes(b[21:25],'little'); return (v&0x3fff)+1,((v>>14)&0x3fff)+1,rel
  except Exception: return None
  return None

def load(d,errs):
  items=[]; slugs={}
  for f in sorted(d.glob('*.md')):
    name=f.name; L=lambda m,name=name:errs.append(f'{name}: {m}')
    m=re.fullmatch(r'([a-z0-9]+(?:-[a-z0-9]+)*)\.md',name)
    if not m: L('tên file phải dạng slug-khong-dau.md (chỉ a-z, 0-9, dấu -), ví dụ cach-chon-ten-mien.md'); continue
    meta,body,pe=M.parse_front(f.read_text(encoding='utf-8'))
    for x in pe: L(x)
    if pe: continue
    if meta.get('draft') is True: print(f'bỏ qua bản nháp: {name}'); continue
    for k in sorted(set(meta)-FIELDS): L(f'trường lạ "{k}" (chỉ dùng: {", ".join(sorted(FIELDS))})')
    it=dict(meta); it['slug']=m.group(1); it['file']=name
    if meta.get('slug') is not None and meta.get('slug')!=it['slug']: L(f'slug "{meta.get("slug")}" phải trùng tên file ({it["slug"]})')
    miss=[k for k in ('title','date','description','category') if not isinstance(it.get(k),str) or not it[k].strip()]
    for k in miss: L(f'thiếu trường bắt buộc "{k}"')
    if miss: continue
    for k in ('title','description'): it[k]=re.sub(r'\s+',' ',it[k]).strip()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',it['date']): L('date phải là YYYY-MM-DD, ví dụ 2026-10-27')
    else:
      try:
        if datetime.date.fromisoformat(it['date'])>today(): L(f'date {it["date"]} ở tương lai')
      except ValueError: L(f'date {it["date"]} không phải ngày có thật')
    if it.get('updated') not in (None,''):
      u=str(it['updated'])
      if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',u): L('updated phải là YYYY-MM-DD')
      else:
        try:
          if datetime.date.fromisoformat(u)>today(): L('updated ở tương lai')
          if u<it['date']: L('updated không được trước date')
        except ValueError: L('updated không phải ngày có thật')
    else: it['updated']=''
    if it['category'] not in CATS: L(f'category "{it["category"]}" không hợp lệ (dùng: {", ".join(CATS)})')
    lt,ld=len(it['title']),len(it['description'])
    if not 20<=lt<=70: L(f'title dài {lt} ký tự (cần 20–70)')
    if not 110<=ld<=155: L(f'description dài {ld} ký tự (cần 110–155)')
    sv=it.get('services')
    if isinstance(sv,str): sv=[sv]
    if not isinstance(sv,list) or not sv: L('cần ít nhất 1 dịch vụ liên quan trong "services" (slug trang dich-vu/, ví dụ thiet-ke-website)'); sv=[]
    if len(sv)>4: L('services tối đa 4 dịch vụ')
    it['svc']=[]
    for x in sv:
      n=svc_name(str(x))
      if not n: L(f'services: không có trang dich-vu/{x}.html')
      else: it['svc'].append((str(x),n))
    tg=it.get('tags',[])
    if isinstance(tg,str): tg=[tg]
    it['tags']=[str(t).strip() for t in (tg or []) if str(t).strip()]
    if it.get('image'):
      wh=img_size(str(it['image']))
      if not wh: L('image phải là file png/jpg/webp có thật trong assets/blog/')
      else: it['img']=wh
      if not str(it.get('image_alt','')).strip(): L('có image thì phải có image_alt (mô tả ảnh)')
    body=body.strip(); it['body']=body
    wc=M.words(body); it['words']=wc
    if wc<MIN_WORDS: L(f'nội dung chỉ có {wc} từ (tối thiểu {MIN_WORDS})')
    ctx=M.Ctx(img_size); it['html'],it['heads'],_=M.render(body,ctx)
    for x in ctx.err: L(x)
    alltext=' '.join([it['title'],it['description'],body,' '.join(it['tags'])])
    for p in FORBID:
      mm=re.search(p,alltext,re.I)
      if mm: L(f'có cụm từ bị cấm: "{mm.group(0)}" (không dùng 24/7, 24h, FPT Polytechnic, cam kết/đảm bảo top hay thứ hạng)')
    for blk in [it['title'],it['description']]+re.split(r'\n\s*\n|\n(?=\s*[-*|]|\s*\d+\.)',re.sub(r'```.*?```','',body,flags=re.S)):
      mm=NUMCLAIM.search(blk)
      if mm and not MARK.search(blk): L(f'có giá/số liệu "{mm.group(0).strip()}" chưa đánh dấu: ghi rõ "ví dụ"/"giả định" hoặc kèm link nguồn https trong cùng đoạn ("{blk.strip()[:60]}…")')
    if it['slug'] in slugs: L(f'slug "{it["slug"]}" trùng với {slugs[it["slug"]]}')
    if it['slug'] in SYS_SLUGS: L('slug này trùng tên trang hệ thống, hãy đổi')
    slugs[it['slug']]=name
    for k in ('title','description'):
      if any(x[k]==it[k] for x in items): L(f'{k} trùng với một bài khác, hãy viết khác đi')
    items.append(it)
  return items

def url_of(it): return f'blog/{it["slug"]}.html'
def shell_page(rel,title,desc,head,main,on=False):
  s=N.page(rel,title,desc,'',main)
  s=s.replace('<!-- news:head --><!-- /news:head -->','<!-- blog:head -->'+head+'<!-- /blog:head -->',1)
  hdr,rest=s.split('</header>',1)
  hdr=hdr.replace(' class=on','')
  pre=N.rel_prefix(rel)
  if on: hdr=hdr.replace(f'href="{pre}blog.html">Blog<',f'href="{pre}blog.html" class=on>Blog<',1)
  return hdr+'</header>'+rest
RSSL=f'<link rel="alternate" type="application/rss+xml" title="Blog kiến thức – My Agent" href="{BASE}blog/feed.xml">'
def card(it,pre,h='h2'):
  c=it['category']; u=pre+url_of(it)
  return (f'<article class="card glass news rv" data-topic="{c}"><div class="nw-top"><span class="nw-ic">{CAT_ICON[c]}</span><span class="nw-tg mono">{E(CATS[c])}</span><time class="mono" datetime="{it["date"]}">{vn(it["date"])}</time></div>'
    f'<{h} class="nw-h"><a class="nw-a" href="{u}">{E(it["title"])}</a></{h}><p class="nw-s">{E(it["description"])}</p>'
    f'<p class="nw-src"><span class="muted">{max(1,round(it["words"]/200))} phút đọc</span> <a class="btn ghost sm" href="{u}">Đọc bài<span class="sr"> “{E(it["title"])}”</span></a></p></article>')

def list_page(items):
  rel='blog.html'; hero=('<section class="hero sub"><canvas class="net" aria-hidden="true"></canvas><div class="wrap"><nav class="crumb mono" aria-label="breadcrumb"><a href="index.html">home</a> / blog</nav>'
    '<h1 class="gt2">Blog kiến&nbsp;thức</h1><p class="lead">Bài hướng dẫn và kiến thức thực tế về website, SEO, marketing online, dữ liệu và AI do My Agent tự viết, dành cho chủ doanh nghiệp nhỏ và người mới bắt đầu.</p></div></section>')
  if not items:
    body=('<!-- blog:empty --><section><div class="wrap"><div class="card glass rv bl-empty"><span class="k mono">sắp ra mắt</span><h2>Bài viết đầu tiên sắp ra&nbsp;mắt</h2>'
      '<p>My Agent đang biên soạn những bài hướng dẫn đầu tiên. Trong lúc chờ, bạn có thể đọc tin công nghệ mới nhất hoặc xem các dịch vụ của chúng tôi.</p>'
      '<p class="bl-act"><a class="btn mag" href="tin-tuc.html">Đọc tin tức công nghệ</a> <a class="btn ghost" href="dich-vu.html">Xem các dịch vụ</a> <a class="btn ghost" href="lien-he.html">Liên hệ My Agent</a></p></div></div></section>')
    ldo=''
  else:
    used=[c for c in CATS if any(x['category']==c for x in items)]
    body=('<section><div class="wrap"><div class="grid nw-grid" id="blog-list">'+''.join(card(x,'') for x in items)+'</div>'
      f'<p class="muted nw-note"><small>Bài viết do My Agent tự biên soạn. Chủ đề: {", ".join(E(CATS[c]) for c in used)}. Theo dõi qua <a href="blog/feed.xml">RSS</a>. Cần tư vấn cho trường hợp của bạn? <a href="lien-he.html">Liên hệ My Agent</a>.</small></p></div></section>')
    upd=max(x['updated'] or x['date'] for x in items)
    ldo=N.ld({"@context":"https://schema.org","@type":"CollectionPage","name":"Blog kiến thức","url":BASE+rel,"inLanguage":"vi","dateModified":upd,"isPartOf":{"@id":BASE+"#website"},"publisher":{"@id":BASE+"#org"},
      "mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+url_of(x),"name":x['title']} for i,x in enumerate(items)]}})
  title='Blog kiến thức website, SEO, dữ liệu | My Agent'
  desc='Blog kiến thức của My Agent: hướng dẫn thực tế về website, SEO, marketing online, dữ liệu và AI cho chủ doanh nghiệp nhỏ, viết dễ hiểu, dễ áp dụng.'
  return rel,shell_page(rel,title,desc,RSSL,hero+body+ldo,on=True)

def article_page(it,items):
  rel=url_of(it); pre='../'; c=it['category']; url=BASE+rel; upd=it['updated']
  i=items.index(it); newer=items[i-1] if i>0 else None; older=items[i+1] if i+1<len(items) else None
  rt=max(1,round(it['words']/200))
  heads=[h for h in it['heads'] if h[0]==2]
  toc=('<div class="nwa-toc card glass rv" role="navigation" aria-label="Mục lục"><p class="h4 mono">// mục lục</p><ol>'+''.join(f'<li><a href="#{h}">{E(x)}</a></li>' for _,h,x in heads)+'</ol></div>') if len(heads)>=2 else ''
  fig=''
  if it.get('img'):
    w,h,src=it['img']; fig=f'<figure class="nwa-cover rv"><img src="{pre}{src}" alt="{E(it["image_alt"])}" width="{w}" height="{h}" decoding="async" fetchpriority="high"></figure>'
  svc=('<aside class="nwa-insight card glass rv bl-svc" aria-labelledby="dich-vu-lien-quan"><h2 id="dich-vu-lien-quan">Dịch vụ liên&nbsp;quan</h2><ul>'
    +''.join(f'<li><a href="{pre}dich-vu/{s}.html">{E(n)}</a></li>' for s,n in it['svc'])+'</ul>'
    f'<p class="nwa-cta"><a class="btn mag" href="{pre}lien-he.html">Nhận tư vấn từ My Agent</a></p></aside>')
  pn=''
  if newer or older:
    pn='<div class="nwa-pn" role="navigation" aria-label="Bài trước và bài sau">'
    pn+=(f'<a class="card glass rv" rel="prev" href="{newer["slug"]}.html"><small class="mono">‹ Bài mới hơn</small><span>{E(newer["title"])}</span></a>' if newer else '<span></span>')
    pn+=(f'<a class="card glass rv nx" rel="next" href="{older["slug"]}.html"><small class="mono">Bài cũ hơn ›</small><span>{E(older["title"])}</span></a>' if older else '<span></span>')+'</div>'
  rel_items=sorted([x for x in items if x is not it],key=lambda x:(-(x['category']==c)-len(set(x['tags'])&set(it['tags'])),items.index(x)))[:3]
  related=('<section class="soft"><div class="wrap"><div class="t rv"><span class="k">đọc tiếp</span><h2>Bài liên&nbsp;quan</h2></div><div class="grid nw-grid">'+''.join(card(x,pre,'h3') for x in rel_items)+'</div></div></section>') if rel_items else ''
  tags=('<p class="muted"><small>Từ khóa: '+' · '.join(E(x) for x in it['tags'])+'</small></p>') if it['tags'] else ''
  meta=(f'<p class="nwa-meta mono"><span>Đăng <time datetime="{it["date"]}">{vn(it["date"])}</time></span>'+(f'<span>Cập nhật <time datetime="{upd}">{vn(upd)}</time></span>' if upd and upd!=it['date'] else '')
    +f'<span>{rt} phút đọc</span><span>Tác giả: My Agent</span></p>')
  main=(f'<section class="hero sub nwa-hero"><canvas class="net" aria-hidden="true"></canvas><div class="wrap"><nav class="crumb mono" aria-label="breadcrumb"><a href="{pre}index.html">home</a> / <a href="{pre}blog.html">blog</a> / {E(it["slug"])}</nav>'
    f'<div class="nw-top nwa-top"><span class="nw-ic">{CAT_ICON[c]}</span><span class="nw-tg mono">{E(CATS[c])}</span></div><h1 class="gt2 nwa-h1">{E(it["title"])}</h1><p class="lead">{E(it["description"])}</p>{meta}</div></section>'
    f'<section><div class="wrap nwa-wrap"><article class="nwa" aria-labelledby="nwa-h">{fig}{toc}<div class="nwa-body rv" id="nwa-h">{it["html"]}{tags}</div>{svc}'
    f'<p class="nwa-cta rv"><a class="btn mag" href="{pre}lien-he.html">Trao đổi với My Agent về chủ đề này</a> <a class="btn ghost" href="{pre}blog.html">Tất cả bài viết</a></p>{pn}</article></div></section>{related}')
  img=BASE+it['img'][2] if it.get('img') else BASE+'assets/og-image.png'
  ldo={"@context":"https://schema.org","@type":"Article","headline":it['title'][:110],"description":it['description'],"inLanguage":"vi",
    "datePublished":it['date']+"T08:00:00+07:00","dateModified":(upd or it['date'])+"T08:00:00+07:00","articleSection":CATS[c],
    "author":{"@type":"ProfessionalService","@id":BASE+"#org","name":"My Agent","url":BASE},"publisher":{"@type":"ProfessionalService","@id":BASE+"#org","name":"My Agent","url":BASE,"logo":{"@type":"ImageObject","@id":BASE+"#logo","url":BASE+"assets/icon-512.png","width":512,"height":512}},
    "mainEntityOfPage":{"@type":"WebPage","@id":url},"url":url,"image":[img],"wordCount":it['words']}
  if it['tags']: ldo['keywords']=', '.join(it['tags'])
  head=(RSSL+f'<meta property="article:published_time" content="{it["date"]}T08:00:00+07:00"><meta property="article:modified_time" content="{(upd or it["date"])}T08:00:00+07:00">'
    f'<meta property="article:section" content="{E(CATS[c])}">'+''.join(f'<meta property="article:tag" content="{E(x)}">' for x in it['tags'])
    +(f'<link rel="image_src" href="{img}">' if it.get('img') else ''))
  return rel,shell_page(rel,N.ptitle(it['title']),it['description'],head,main+N.ld(ldo),on=True)

def feed(items):
  X=lambda x:html.escape(str(x),quote=False)
  bd=max([x['updated'] or x['date'] for x in items] or ['2026-10-27'])
  o=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>','<title>Blog kiến thức – My Agent</title>',f'<link>{BASE}blog.html</link>',
     f'<atom:link href="{BASE}blog/feed.xml" rel="self" type="application/rss+xml"/>','<description>Bài hướng dẫn và kiến thức về website, SEO, marketing online, dữ liệu và AI do My Agent tự viết.</description>','<language>vi</language>',f'<lastBuildDate>{N.rfc822(bd)}</lastBuildDate>']
  for x in items[:20]:
    u=BASE+url_of(x)
    o.append(f'<item><title>{X(x["title"])}</title><link>{u}</link><guid isPermaLink="true">{u}</guid><pubDate>{N.rfc822(x["date"])}</pubDate><category>{X(CATS[x["category"]])}</category><description>{X(x["description"])}</description></item>')
  o.append('</channel></rss>'); return '\n'.join(o)+'\n'

def home_block(items):
  """redesign-v1: 3 bài blog mới nhất cho trang chủ, giữa <!-- blog:home --> ... <!-- /blog:home --> trong index.html."""
  E=lambda x:html.escape(x,quote=False)
  ar='<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
  def vn(d): y,m,dd=d.split('-'); return f'{dd}/{m}/{y}'
  cs=''.join(f'<article class="h-card"><span class="h-tag">{E(it["category"])}</span><h3 style="margin-top:12px"><a href="{url_of(it)}">{E(it["title"])}</a></h3><p>{E(it["description"])}</p><p class="h-links"><time datetime="{it["date"]}">{vn(it["date"])}</time></p></article>' for it in items[:3])
  return f'<div class="h-g3">{cs}</div><p class="h-more"><a class="h-a" href="blog.html">Xem tất cả bài viết {ar}</a></p>'
def put_home(items):
  f=R/'index.html'
  if not f.exists() or not items: return
  s=f.read_text(encoding='utf-8')
  if '<!-- blog:home -->' not in s: return
  n=re.sub(r'<!-- blog:home -->.*?<!-- /blog:home -->',lambda m:'<!-- blog:home -->'+home_block(items)+'<!-- /blog:home -->',s,count=1,flags=re.S)
  if n!=s: f.write_text(n,encoding='utf-8')
def main():
  a=sys.argv[1:]; d=R/'data/blog'
  if '--dir' in a: d=pathlib.Path(a[a.index('--dir')+1])
  errs=[]; items=load(d,errs) if d.is_dir() else []
  if errs:
    print('\n'.join('LỖI: '+e for e in errs)); print(f'=> {len(errs)} lỗi, chưa dựng trang. Sửa rồi chạy lại.'); return 1
  items.sort(key=lambda x:(x['date'],x['slug']),reverse=True)
  if '--validate-only' in a: print(f'OK: {len(items)} bài blog hợp lệ'); return 0
  gen={'blog/feed.xml','blog/index.html'}
  rel,s=list_page(items); N.write(rel,s)
  for it in items:
    rel,s=article_page(it,items); N.write(rel,s); gen.add(rel)
  for f in sorted((R/'blog').rglob('*')) if (R/'blog').is_dir() else []:
    r=f.relative_to(R).as_posix()
    if f.is_file() and r not in gen: f.unlink(); print('xoá trang không còn bài:',r)
  N.write('blog/feed.xml',feed(items)); put_home(items)
  N.write('blog/index.html','<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog kiến thức – My Agent</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="https://myagentvn.com/blog.html"><meta http-equiv="refresh" content="0; url=../blog.html"><script>location.replace(\'../blog.html\'+location.search+location.hash)</script><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#07090f;color:#e8ecf5;font-family:system-ui,sans-serif}a{color:#ff2d3d}</style></head><body><p>Đang chuyển tới <a href="../blog.html">Blog kiến thức</a>…</p></body></html>\n')
  print(f'blog: {len(items)} bài'+(' (trang danh sách ở trạng thái "sắp ra mắt", noindex)' if not items else ''))
  if '--no-chatbot' not in a: subprocess.run([sys.executable,str(R/'scripts/chatbot_build.py')],check=True)
  return 0
if __name__=='__main__': sys.exit(main())
