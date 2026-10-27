#!/usr/bin/env python3
"""Dựng mục Tin tức công nghệ từ data/news/*.md (idempotent: cùng đầu vào -> cùng đầu ra).
Mỗi file: data/news/YYYY-MM-DD-<slug>.md, front-matter + nội dung Markdown (xem docs/tin-tuc.md).
  type: article (mặc định) -> có trang riêng tin-tuc/<slug>.html
  type: link               -> chỉ là thẻ trỏ ra bài gốc (các tin tuyển chọn cũ)
Sinh ra: tin-tuc.html (+ tin-tuc/trang-N.html), tin-tuc/chu-de/<chủ-đề>.html, tin-tuc/<slug>.html,
tin-tuc/feed.xml (RSS 2.0), khối 3 tin mới nhất ở index.html, rồi chạy scripts/chatbot_build.py.
Dùng: python3 scripts/news_build.py [--check-urls] [--validate-only] [--dir DIR]
Sau đó: python3 scripts/tech_pass.py (hoặc dùng luôn scripts/news_publish.sh)."""
import re,sys,json,html,struct,pathlib,datetime,subprocess,urllib.request,urllib.error
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import news_md as M
R=pathlib.Path(__file__).resolve().parent.parent
BASE='https://myagentvn.com/'
PER=int(__import__('os').environ.get('NEWS_PER','12'))  # NEWS_PER chỉ dùng để test phân trang
TOPICS={'ai':'AI','bao-mat':'Bảo mật','web-seo':'Web & SEO','du-lieu':'Dữ liệu','nen-tang':'Nền tảng & MXH'}
TOPIC_DESC={'ai':'Tin AI chọn lọc: mô hình mới, trợ lý AI, tự động hoá công việc, kèm link nguồn gốc và góc nhìn My Agent cho doanh nghiệp nhỏ.',
 'bao-mat':'Tin bảo mật chọn lọc: lỗ hổng, bản vá, cảnh báo cho website và máy chủ, kèm link nguồn gốc và góc nhìn My Agent cho doanh nghiệp nhỏ.',
 'web-seo':'Tin web và SEO chọn lọc: cập nhật Google Search, kỹ thuật website, nội dung, kèm link nguồn gốc và góc nhìn My Agent cho doanh nghiệp nhỏ.',
 'du-lieu':'Tin dữ liệu chọn lọc: Power BI, phân tích, kỹ thuật dữ liệu, báo cáo, kèm link nguồn gốc và góc nhìn My Agent cho doanh nghiệp nhỏ.',
 'nen-tang':'Tin nền tảng và mạng xã hội: Zalo OA, ZBS, Google, Facebook, kèm link nguồn gốc và góc nhìn My Agent cho doanh nghiệp nhỏ.'}
TOPIC_SVC={'ai':[('dich-vu/phan-mem-noi-bo.html','Phần mềm nội bộ'),('dich-vu/video-ai.html','Edit Video - Video AI'),('dich-vu/thiet-ke-website.html','Thiết kế website')],
 'bao-mat':[('dich-vu/cham-soc-website.html','Chăm sóc website'),('dich-vu/hosting-seo.html','Hosting SEO'),('dich-vu/thiet-ke-website.html','Thiết kế website')],
 'web-seo':[('dich-vu/seo-tong-the.html','SEO tổng thể'),('dich-vu/thiet-ke-website.html','Thiết kế website'),('dich-vu/google-maps.html','Google Maps')],
 'du-lieu':[('dich-vu/phan-tich-du-lieu.html','Data Analyst'),('dich-vu/ky-thuat-du-lieu.html','Data Engineer'),('dich-vu/phan-mem-noi-bo.html','Phần mềm nội bộ')],
 'nen-tang':[('dich-vu/zalo-oa-mini-app.html','Zalo OA - Mini App'),('dich-vu/cham-soc-fanpage.html','Chăm sóc Fanpage'),('dich-vu/quang-cao-google-facebook.html','ADS Google, Facebook')]}
SV='<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICON={'ai':SV+'<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9zM9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/></svg>',
 'bao-mat':SV+'<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="M12 8v5M12 16h.01"/></svg>',
 'web-seo':SV+'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4M8 11h6M11 8v6"/></svg>',
 'du-lieu':SV+'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
 'nen-tang':SV+'<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8 11h8M8 14h5"/></svg>'}
FORBID=[r'24\s*/\s*7',r'fpt\s*polytechnic',r'cam\s*kết\s*(lên\s*)?top',r'đảm\s*bảo\s*(lên\s*)?top',r'100\s*%\s*(lên\s*)?top',r'bảo\s*đảm\s*(lên\s*)?top',r'chắc\s*chắn\s*lên\s*top',r'cam\s*kết\s*(lên\s*)?(trang\s*1|top\s*1|hạng\s*1)']
FIELDS={'type','title','date','updated','topic','summary','insight','sources','image','image_alt','tags','draft'}
MIN_WORDS=250
E=lambda x:html.escape(str(x),quote=True)
def vn(d): y,m,dd=d.split('-'); return f'{int(dd):02d}/{int(m):02d}/{y}'
def today():
  return (datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=7)).date()

def img_size(rel):
  """(w,h,rel) cho ảnh trong assets/news/ (png/jpg/webp), None nếu không hợp lệ."""
  rel=rel.lstrip('/')
  if rel.startswith('../'): rel=re.sub(r'^(\.\./)+','',rel)
  if not re.fullmatch(r'assets/news/[\w.-]+\.(png|jpe?g|webp)',rel): return None
  f=R/rel
  if not f.is_file(): return None
  b=f.read_bytes()
  try:
    if b[:8]==b'\x89PNG\r\n\x1a\n': w,h=struct.unpack('>II',b[16:24]); return w,h,rel
    if b[:4]==b'RIFF' and b[8:12]==b'WEBP':
      k=b[12:16]
      if k==b'VP8 ': w,h=struct.unpack('<HH',b[26:30]); return w&0x3fff,h&0x3fff,rel
      if k==b'VP8L': v=int.from_bytes(b[21:25],'little'); return (v&0x3fff)+1,((v>>14)&0x3fff)+1,rel
      if k==b'VP8X': return int.from_bytes(b[24:27],'little')+1,int.from_bytes(b[27:30],'little')+1,rel
    if b[:2]==b'\xff\xd8':
      i=2
      while i<len(b):
        while b[i]==0xff: i+=1
        mk=b[i]; i+=1; ln=struct.unpack('>H',b[i:i+2])[0]
        if mk in (0xc0,0xc1,0xc2): h,w=struct.unpack('>HH',b[i+3:i+7]); return w,h,rel
        i+=ln
  except Exception: return None
  return None

def load(d,errs,warns):
  items=[]; slugs={}; it_type=['article']
  for f in sorted(d.glob('*.md')):
    name=f.name; L=lambda m:errs.append(f'{name}: {m}'); W=lambda m:warns.append(f'{name}: {m}'+(' [type: link]' if it_type[0]=='link' else ''))
    m=re.fullmatch(r'(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md',name)
    if not m: L('tên file phải dạng YYYY-MM-DD-slug-khong-dau.md (chỉ a-z, 0-9, dấu -)'); continue
    meta,body,pe=M.parse_front(f.read_text(encoding='utf-8'))
    for x in pe: L(x)
    if pe: continue
    if meta.get('draft') is True: print(f'bỏ qua bản nháp: {name}'); continue
    for k in sorted(set(meta)-FIELDS): L(f'trường lạ "{k}" (chỉ dùng: {", ".join(sorted(FIELDS))})')
    it_type[0]=meta.get('type','article')
    it=dict(meta); it['slug']=m.group(2); it['file']=name; it.setdefault('type','article')
    if it['type'] not in ('article','link'): L('type phải là article hoặc link')
    art=it['type']=='article'
    for k in ('title','date','topic','summary','insight'):
      if not isinstance(it.get(k),str) or not it.get(k).strip(): L(f'thiếu trường bắt buộc "{k}"')
    if any(not isinstance(it.get(k),str) for k in ('title','date','topic','summary','insight')): continue
    for k in ('title','summary','insight'): it[k]=re.sub(r'\s+',' ',it[k]).strip()
    try:
      dt=datetime.date.fromisoformat(it['date'])
      if dt>today(): L(f'date {it["date"]} ở tương lai')
      if it['date']!=m.group(1): L(f'date trong front-matter ({it["date"]}) khác ngày ở tên file ({m.group(1)})')
    except ValueError: L('date phải là YYYY-MM-DD')
    if it.get('updated'):
      try:
        u=datetime.date.fromisoformat(str(it['updated']))
        if u>today(): L('updated ở tương lai')
        if str(it['updated'])<it['date']: L('updated không được trước date')
      except ValueError: L('updated phải là YYYY-MM-DD')
    if it['topic'] not in TOPICS: L(f'topic "{it["topic"]}" không hợp lệ (dùng: {", ".join(TOPICS)})')
    lt,ls,li=len(it['title']),len(it['summary']),len(it['insight'])
    (L if art else W)(f'title dài {lt} ký tự (tối đa 70)') if lt>70 else None
    if lt<20: L(f'title quá ngắn ({lt} ký tự, tối thiểu 20)')
    if not 120<=ls<=200: (L if art else W)(f'summary dài {ls} ký tự (cần 120–200)')
    if not 40<=li<=400: (L if art else W)(f'insight dài {li} ký tự (cần 40–400, 1–3 câu)')
    src=it.get('sources')
    if not isinstance(src,list) or not src: L('cần ít nhất 1 nguồn trong "sources" (mỗi nguồn có name và url)'); src=[]
    for j,s in enumerate(src,1):
      if not isinstance(s,dict) or not s.get('name') or not s.get('url'): L(f'nguồn #{j} phải có name và url'); continue
      if not re.fullmatch(r'https://[^\s"<>]+',str(s['url'])): L(f'nguồn #{j}: url phải bắt đầu bằng https:// và không có khoảng trắng')
      if s.get('date'):
        try: datetime.date.fromisoformat(str(s['date']))
        except ValueError: L(f'nguồn #{j}: date phải là YYYY-MM-DD')
      if re.search(r'[?&](utm_|aff|ref=|irclickid|clickid)|imp\.i\d+\.net|/aff/',str(s['url']),re.I): L(f'nguồn #{j}: link có mã theo dõi/affiliate, hãy dùng link gốc')
    it['sources']=[s for s in src if isinstance(s,dict)]
    tg=it.get('tags',[])
    if isinstance(tg,str): tg=[tg]
    it['tags']=[str(t) for t in tg if str(t).strip()]
    if it.get('image'):
      wh=img_size(str(it['image']))
      if not wh: L('image phải là file png/jpg/webp nằm trong assets/news/')
      else: it['img']=wh
      if not str(it.get('image_alt','')).strip(): L('có image thì phải có image_alt (mô tả ảnh)')
    body=body.strip(); it['body']=body
    if art:
      wc=M.words(body); it['words']=wc
      if wc<MIN_WORDS: L(f'nội dung bài chỉ có {wc} từ (tối thiểu {MIN_WORDS})')
      ctx=M.Ctx(img_size); it['html'],it['heads'],_=M.render(body,ctx)
      for x in ctx.err: L(x)
    elif body: W('type: link không dùng phần nội dung, phần này bị bỏ qua')
    alltext=' '.join([it['title'],it['summary'],it['insight'],body,' '.join(it['tags'])])
    for p in FORBID:
      mm=re.search(p,alltext,re.I)
      if mm: L(f'có cụm từ bị cấm: "{mm.group(0)}" (không dùng 24/7, FPT Polytechnic, cam kết/đảm bảo lên top)')
    if it['slug'] in slugs: L(f'slug "{it["slug"]}" trùng với {slugs[it["slug"]]}')
    slugs[it['slug']]=name
    if art and it['slug'] in ('index','feed') or re.fullmatch(r'trang-\d+',it['slug']): L('slug này trùng tên trang hệ thống, hãy đổi')
    for k in ('title','summary'):
      if any(x[k]==it[k] for x in items): L(f'{k} trùng với một tin khác, hãy viết khác đi')
    items.append(it)
  return items

def check_urls(items):
  bad=0
  for it in items:
    for s in it['sources']:
      try:
        rq=urllib.request.Request(s['url'],headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36'})
        c=urllib.request.urlopen(rq,timeout=20).status
      except urllib.error.HTTPError as e: c=e.code
      except Exception as e: c=str(e)[:40]
      tag='OK' if c==200 else ('CHẶN BOT?' if c in (401,403,429) else 'LỖI')
      if tag=='LỖI': bad+=1
      print(f'{tag:9} {c} {s["url"]}')
  return bad

# ---------------- HTML ----------------
def rel_prefix(rel): return '../'*rel.count('/')
def rewrite(s,pre):
  if not pre: return s
  return re.sub(r'\b(href|src)="(?!https?:|mailto:|tel:|#|/|data:|javascript:)([^"]*)"',lambda m:f'{m.group(1)}="{pre}{m.group(2)}"',s)
def shell():
  s=(R/'tin-tuc.html').read_text(encoding='utf-8')
  s=re.sub(r'<!-- tech:head -->.*?<!-- /tech:head -->','',s,flags=re.S)
  s=re.sub(r'<!-- news:head -->.*?<!-- /news:head -->','',s,flags=re.S)
  a,rest=s.split('<main>',1); _,b=rest.split('</main>',1)
  return a,b
def page(rel,title,desc,head,main):
  a,b=shell(); pre=rel_prefix(rel)
  a=re.sub(r'<title>.*?</title>','<title>'+E(title)+'</title>',a,count=1,flags=re.S)
  a=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+E(desc)+'">',a,count=1)
  a=a.replace('</head>','<!-- news:head -->'+head+'<!-- /news:head --></head>',1)
  return rewrite(a,pre)+'<main>'+main+'</main>'+rewrite(b,pre)
def cut(t,n):
  if len(t)<=n: return t
  c=t[:n-1].rsplit(' ',1)[0].rstrip(',;:–-'); return c+'…'
def ptitle(t):
  B=' | My Agent'
  return t+B if len(t+B)<=60 else cut(t,60)
def meta_desc(s): return cut(s,155)
def url_of(it): return f'tin-tuc/{it["slug"]}.html'
def src_names(it): return ', '.join(s['name'] for s in it['sources'])
def card(it,pre,h='h2',home=False):
  t=it['topic']; art=it['type']=='article'
  head=f'<div class="nw-top"><span class="nw-ic">{ICON[t]}</span><span class="nw-tg mono">{E(TOPICS[t])}</span><time class="mono" datetime="{it["date"]}">{vn(it["date"])}</time></div>'
  if art:
    u=pre+url_of(it)
    return (f'<article class="card glass news rv" data-topic="{t}" id="{E(it["slug"])}">{head}<{h} class="nw-h"><a class="nw-a" href="{u}">{E(it["title"])}</a></{h}><p class="nw-s">{E(it["summary"])}</p>'
      +('' if home else f'<p class="nw-in"><b>Góc nhìn My Agent:</b> {E(it["insight"])}</p>')+
      f'<p class="nw-src"><span class="muted">Nguồn: {E(src_names(it))}</span> <a class="btn ghost sm" href="{u}">Đọc bài<span class="sr"> “{E(it["title"])}”</span></a></p></article>')
  s=it['sources'][0]
  return (f'<article class="card glass news rv" data-topic="{t}" id="{E(it["slug"])}">{head}<{h} class="nw-h">{E(it["title"])}</{h}><p class="nw-s">{E(it["summary"])}</p>'
   +('' if home else f'<p class="nw-in"><b>Góc nhìn My Agent:</b> {E(it["insight"])}</p>')+
   f'<p class="nw-src"><span class="muted">Nguồn: {E(s["name"])}</span> <a class="btn ghost sm" href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">Đọc nguồn<span class="sr"> bài “{E(it["title"])}” trên {E(s["name"])} (mở tab mới)</span></a></p></article>')
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False).replace('</','<\\/')+'</script>'
RSSL=f'<link rel="alternate" type="application/rss+xml" title="Tin tức công nghệ – My Agent" href="{BASE}tin-tuc/feed.xml">'

def list_pages(items,topic=None):
  """Trả về [(rel, html)] cho danh sách tổng hoặc một chủ đề, mỗi trang PER tin."""
  its=[x for x in items if topic is None or x['topic']==topic]
  n=max(1,(len(its)+PER-1)//PER); out=[]
  def relp(k):
    if topic is None: return 'tin-tuc.html' if k==1 else f'tin-tuc/trang-{k}.html'
    return f'tin-tuc/chu-de/{topic}.html' if k==1 else f'tin-tuc/chu-de/{topic}-trang-{k}.html'
  for k in range(1,n+1):
    rel=relp(k); pre=rel_prefix(rel); chunk=its[(k-1)*PER:k*PER]
    used=[t for t in TOPICS if any(x['topic']==t for x in items)]
    cur=lambda c:' aria-current="page"' if c else ''
    chips=('<div class="chips nw-chips" role="navigation" aria-label="Lọc tin theo chủ đề"><a class="chip" href="'+pre+'tin-tuc.html"'+cur(topic is None)+'>Tất cả <small>'+str(len(items))+'</small></a>'
      +''.join(f'<a class="chip" href="{pre}tin-tuc/chu-de/{t}.html"{cur(topic==t)}>{E(TOPICS[t])} <small>{sum(x["topic"]==t for x in items)}</small></a>' for t in used)+'</div>')
    lst='<div class="grid nw-grid" id="news-list">'+''.join(card(x,pre) for x in chunk)+'</div>'
    pg=''
    if n>1:
      pg='<div class="nw-pages mono" role="navigation" aria-label="Phân trang">'+(f'<a class="btn ghost sm" rel="prev" href="{pre}{relp(k-1)}">‹ Trang trước</a>' if k>1 else '')
      pg+=''.join((f'<span class="pg on" aria-current="page">{j}</span>' if j==k else f'<a class="pg" href="{pre}{relp(j)}">{j}</a>') for j in range(1,n+1))
      pg+=(f'<a class="btn ghost sm" rel="next" href="{pre}{relp(k+1)}">Trang sau ›</a>' if k<n else '')+'</div>'
    head=RSSL+(f'<link rel="prev" href="{BASE}{relp(k-1)}">' if k>1 else '')+(f'<link rel="next" href="{BASE}{relp(k+1)}">' if k<n else '')
    upd=max(str(x.get('updated') or x['date']) for x in its) if its else today().isoformat()
    name='Tin tức công nghệ' if topic is None else f'Tin {TOPICS[topic]}'
    ldo={"@context":"https://schema.org","@type":"CollectionPage","name":name+(f' – trang {k}' if k>1 else ''),"url":BASE+rel,"inLanguage":"vi","dateModified":upd,
      "isPartOf":{"@id":BASE+"#website"},"publisher":{"@id":BASE+"#org"},
      "mainEntity":{"@type":"ItemList","numberOfItems":len(chunk),"itemListElement":[{"@type":"ListItem","position":(k-1)*PER+i+1,"url":BASE+(url_of(x) if x['type']=='article' else rel+'#'+x['slug']),"name":x['title']} for i,x in enumerate(chunk)]}}
    note=(f'<p class="muted nw-note"><small>Tin dạng thẻ là tóm tắt do My Agent tự viết, nội dung đầy đủ thuộc về nguồn gốc; bài có trang riêng do My Agent biên soạn và ghi nguồn. Cập nhật lần cuối: <!-- news:updated -->{vn(upd)}<!-- /news:updated -->. '
      f'Theo dõi qua <a href="{pre}tin-tuc/feed.xml">RSS</a>. Cần tư vấn áp dụng cho website của bạn? <a href="{pre}lien-he.html">Liên hệ My Agent</a> hoặc xem <a href="{pre}dich-vu.html">18 dịch vụ</a>.</small></p>')
    body=f'<!-- news:chips -->{chips}<!-- /news:chips --><!-- news:list -->{lst}{pg}<!-- /news:list -->'
    if rel=='tin-tuc.html':
      out.append((rel,dict(head=head,body=body,note=note,ld=ld(ldo),upd=upd))); continue
    crumb=f'<a href="{pre}index.html">home</a> / <a href="{pre}tin-tuc.html">tin-tuc</a> / '+(f'trang-{k}' if topic is None else (f'<a href="{pre}tin-tuc/chu-de/{topic}.html">{topic}</a> / trang-{k}' if k>1 else topic))
    h1=(f'Tin tức công nghệ – trang&nbsp;{k}' if topic is None else f'Tin {E(TOPICS[topic])}'+(f' – trang&nbsp;{k}' if k>1 else ''))
    lead=(f'Trang {k}/{n} của mục Tin tức công nghệ: tin AI, bảo mật, web &amp; SEO, dữ liệu và nền tảng số có nguồn rõ ràng.' if topic is None else E(TOPIC_DESC[topic]))
    title=ptitle(re.sub('&nbsp;',' ',html.unescape(h1)))
    desc=(f'Trang {k} mục Tin tức công nghệ của My Agent: tin AI, bảo mật, web & SEO, dữ liệu, nền tảng số, có link nguồn gốc và góc nhìn cho doanh nghiệp nhỏ.' if topic is None
      else TOPIC_DESC[topic]+(f' Trang {k}.' if k>1 else ''))
    main=(f'<section class="hero sub"><canvas class="net" aria-hidden="true"></canvas><div class="wrap"><nav class="crumb mono" aria-label="breadcrumb">{crumb}</nav><h1 class="gt2">{h1}</h1><p class="lead">{lead}</p></div></section>'
      f'<section><div class="wrap">{body}{note}</div></section>{ld(ldo)}')
    out.append((rel,page(rel,title,meta_desc(desc),head,main)))
  return out

def article_page(it,arts,items):
  rel=url_of(it); pre='../'; t=it['topic']; url=BASE+rel
  i=arts.index(it); newer=arts[i-1] if i>0 else None; older=arts[i+1] if i+1<len(arts) else None
  rt=max(1,round(it['words']/200)); upd=str(it.get('updated') or '')
  heads=[h for h in it['heads'] if h[0]==2]
  toc=('<div class="nwa-toc card glass rv" role="navigation" aria-label="Mục lục"><p class="h4 mono">// mục lục</p><ol>'+''.join(f'<li><a href="#{h}">{E(x)}</a></li>' for _,h,x in heads)+'</ol></div>') if len(heads)>=4 else ''
  fig=''
  if it.get('img'):
    w,h,src=it['img']; fig=f'<figure class="nwa-cover rv"><img src="{pre}{src}" alt="{E(it["image_alt"])}" width="{w}" height="{h}" decoding="async" fetchpriority="high"></figure>'
  srcs='<ol>'+''.join(f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(s["name"])}<span class="sr"> (mở tab mới)</span></a>'+(f' <span class="muted mono">· {vn(str(s["date"]))}</span>' if s.get('date') else '')+f'<br><small class="muted nwa-u">{E(re.sub(r"^https://","",s["url"]))}</small></li>' for s in it['sources'])+'</ol>'
  pn=''
  if newer or older:
    pn='<div class="nwa-pn" role="navigation" aria-label="Bài trước và bài sau">'
    pn+=(f'<a class="card glass rv" rel="prev" href="{newer["slug"]}.html"><small class="mono">‹ Bài mới hơn</small><span>{E(newer["title"])}</span></a>' if newer else '<span></span>')
    pn+=(f'<a class="card glass rv nx" rel="next" href="{older["slug"]}.html"><small class="mono">Bài cũ hơn ›</small><span>{E(older["title"])}</span></a>' if older else '<span></span>')+'</div>'
  rel_items=[x for x in items if x['topic']==t and x is not it][:3]
  related=('<section class="soft"><div class="wrap"><div class="t rv"><span class="k">// cùng chủ đề</span><h2>Bài liên&nbsp;quan</h2></div><div class="grid nw-grid">'+''.join(card(x,pre,'h3',True) for x in rel_items)+'</div></div></section>') if rel_items else ''
  svc='<p class="nwa-svc"><b>Dịch vụ liên quan:</b> '+' · '.join(f'<a href="{pre}{u}">{E(n)}</a>' for u,n in TOPIC_SVC[t])+'</p>'
  tags=(' · '.join(E(x) for x in it['tags'])) if it['tags'] else ''
  meta=(f'<p class="nwa-meta mono"><span>Đăng <time datetime="{it["date"]}">{vn(it["date"])}</time></span>'+(f'<span>Cập nhật <time datetime="{upd}">{vn(upd)}</time></span>' if upd and upd!=it['date'] else '')
    +f'<span>{rt} phút đọc</span><span>Biên tập: My Agent</span></p>')
  main=(f'<section class="hero sub nwa-hero"><canvas class="net" aria-hidden="true"></canvas><div class="wrap"><nav class="crumb mono" aria-label="breadcrumb"><a href="{pre}index.html">home</a> / <a href="{pre}tin-tuc.html">tin-tuc</a> / <a href="chu-de/{t}.html">{t}</a></nav>'
    f'<div class="nw-top nwa-top"><span class="nw-ic">{ICON[t]}</span><a class="nw-tg mono" href="chu-de/{t}.html">{E(TOPICS[t])}</a></div><h1 class="gt2 nwa-h1">{E(it["title"])}</h1><p class="lead">{E(it["summary"])}</p>{meta}</div></section>'
    f'<section><div class="wrap nwa-wrap"><article class="nwa" aria-labelledby="nwa-h">{fig}{toc}<div class="nwa-body rv" id="nwa-h">{it["html"]}</div>'
    f'<aside class="nwa-insight card glass rv"><h2>Góc nhìn My&nbsp;Agent</h2><p>{E(it["insight"])}</p>{svc}</aside>'
    f'<section class="nwa-src card glass rv" aria-labelledby="nguon-tham-khao"><h2 id="nguon-tham-khao">Nguồn tham&nbsp;khảo</h2>{srcs}<p class="muted"><small>Bài viết do My Agent tự biên soạn bằng lời của mình dựa trên các nguồn trên; nội dung gốc thuộc về nguồn.'+(f' Từ khóa: {tags}.' if tags else '')+'</small></p></section>'
    f'<p class="nwa-cta rv"><a class="btn mag" href="{pre}lien-he.html">Trao đổi với My Agent về chủ đề này</a> <a class="btn ghost" href="{pre}tin-tuc.html">Tất cả tin công nghệ</a></p>{pn}</article></div></section>{related}')
  img=BASE+it['img'][2] if it.get('img') else BASE+'assets/og-image.png'
  ldo={"@context":"https://schema.org","@type":"NewsArticle","headline":it['title'][:110],"description":it['summary'],"inLanguage":"vi",
    "datePublished":it['date']+"T08:00:00+07:00","dateModified":(upd or it['date'])+"T08:00:00+07:00","articleSection":TOPICS[t],
    "author":{"@type":"ProfessionalService","@id":BASE+"#org","name":"My Agent","url":BASE},"publisher":{"@type":"ProfessionalService","@id":BASE+"#org","name":"My Agent","url":BASE,"logo":{"@type":"ImageObject","@id":BASE+"#logo","url":BASE+"assets/logo.png","width":780,"height":192}},
    "mainEntityOfPage":{"@type":"WebPage","@id":url},"url":url,"image":[img],"wordCount":it['words'],"citation":[s['url'] for s in it['sources']]}
  if it['tags']: ldo['keywords']=', '.join(it['tags'])
  head=(RSSL+f'<meta property="article:published_time" content="{it["date"]}T08:00:00+07:00"><meta property="article:modified_time" content="{(upd or it["date"])}T08:00:00+07:00">'
    f'<meta property="article:section" content="{E(TOPICS[t])}">'+''.join(f'<meta property="article:tag" content="{E(x)}">' for x in it['tags'])
    +(f'<link rel="image_src" href="{img}">' if it.get('img') else ''))
  return rel,page(rel,ptitle(it['title']),meta_desc(it['summary']),head,main+ld(ldo))

def rfc822(d):
  dt=datetime.datetime.fromisoformat(d+'T08:00:00+07:00')
  return dt.strftime('%a, %d %b %Y %H:%M:%S +0700')
def feed(items):
  X=lambda x:html.escape(str(x),quote=False)
  last=items[:20]; bd=max(str(x.get('updated') or x['date']) for x in items)
  o=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>',
     '<title>Tin tức công nghệ – My Agent</title>',f'<link>{BASE}tin-tuc.html</link>',f'<atom:link href="{BASE}tin-tuc/feed.xml" rel="self" type="application/rss+xml"/>',
     '<description>Tin AI, bảo mật, web &amp; SEO, dữ liệu và nền tảng số do My Agent chọn lọc, có nguồn rõ ràng.</description>','<language>vi</language>',
     f'<lastBuildDate>{rfc822(bd)}</lastBuildDate>',f'<image><url>{BASE}assets/icon-512.png</url><title>Tin tức công nghệ – My Agent</title><link>{BASE}tin-tuc.html</link></image>']
  for x in last:
    art=x['type']=='article'; link=BASE+url_of(x) if art else x['sources'][0]['url']
    guid=f'<guid isPermaLink="true">{X(link)}</guid>' if art else f'<guid isPermaLink="false">myagentvn-news-{x["slug"]}</guid>'
    o.append(f'<item><title>{X(x["title"])}</title><link>{X(link)}</link>{guid}<pubDate>{rfc822(x["date"])}</pubDate><category>{X(TOPICS[x["topic"]])}</category>'
      f'<description>{X(x["summary"]+" Góc nhìn My Agent: "+x["insight"])}</description></item>')
  o.append('</channel></rss>')
  return '\n'.join(o)+'\n'

def put(s,tag,body):
  pat=re.compile(rf'<!-- news:{tag} -->.*?<!-- /news:{tag} -->',re.S)
  if not pat.search(s): sys.exit(f'thiếu marker news:{tag}')
  return pat.sub(lambda m:f'<!-- news:{tag} -->{body}<!-- /news:{tag} -->',s,count=1)
def write(rel,s):
  f=R/rel; f.parent.mkdir(parents=True,exist_ok=True)
  if not f.exists() or f.read_text(encoding='utf-8')!=s: f.write_text(s,encoding='utf-8')

def main():
  a=sys.argv[1:]; d=R/'data/news'
  if '--dir' in a: d=pathlib.Path(a[a.index('--dir')+1])
  errs=[]; warns=[]; items=load(d,errs,warns)
  for w in warns:
    if '-v' in a or 'type: link' not in w: print('CẢNH BÁO:',w)
  if warns and '-v' not in a: print(f'({len(warns)} cảnh báo cho thẻ link cũ, chạy -v để xem)')
  if errs:
    print('\n'.join('LỖI: '+e for e in errs)); print(f'=> {len(errs)} lỗi, chưa dựng trang. Sửa rồi chạy lại.'); return 1
  if not items: print('LỖI: không có tin nào'); return 1
  items.sort(key=lambda x:(x['date'],x['slug']),reverse=True)
  if '--check-urls' in a and check_urls(items): print('có link nguồn lỗi'); return 1
  if '--validate-only' in a: print(f'OK: {len(items)} tin hợp lệ'); return 0
  arts=[x for x in items if x['type']=='article']
  gen=set()
  # trang danh sách
  pages=list_pages(items)
  for t in TOPICS:
    if any(x['topic']==t for x in items): pages+=list_pages(items,t)
  for rel,v in pages:
    if rel=='tin-tuc.html':
      f=R/rel; s=f.read_text(encoding='utf-8')
      s=re.sub(r'<!-- news:chips -->.*?<!-- /news:list -->','<!-- news:chips --><!-- /news:chips --><!-- news:list --><!-- /news:list -->',s,count=1,flags=re.S)
      s=re.sub(r'<p class="muted nw-note">.*?</p>','<!-- news:note --><!-- /news:note -->',s,count=1,flags=re.S) if '<!-- news:note -->' not in s else s
      if '<!-- news:head -->' not in s: s=s.replace('</head>','<!-- news:head --><!-- /news:head --></head>',1)
      s=put(put(put(put(put(s,'chips',''),'list',''),'note',v['note']),'ld',v['ld']),'head',v['head'])
      s=s.replace('<!-- news:chips --><!-- /news:chips --><!-- news:list --><!-- /news:list -->',v['body'],1)
      write(rel,s)
    else: write(rel,v); gen.add(rel)
  for it in arts:
    rel,s=article_page(it,arts,items); write(rel,s); gen.add(rel)
  # dọn trang cũ không còn nguồn
  for f in sorted((R/'tin-tuc').rglob('*.html')):
    rel=f.relative_to(R).as_posix()
    if rel=='tin-tuc/index.html': continue
    if rel not in gen: f.unlink(); print('xoá trang không còn bài:',rel)
  write('tin-tuc/index.html','<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tin tức công nghệ – My Agent</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="https://myagentvn.com/tin-tuc.html"><meta http-equiv="refresh" content="0; url=../tin-tuc.html"><script>location.replace(\'../tin-tuc.html\'+location.search+location.hash)</script><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#07090f;color:#e8ecf5;font-family:system-ui,sans-serif}a{color:#ff2d3d}</style></head><body><p>Đang chuyển tới <a href="../tin-tuc.html">Tin tức công nghệ</a>…</p></body></html>\n')
  write('tin-tuc/feed.xml',feed(items))
  # trang chủ
  home=('<section class="soft nw-home"><div class="wrap"><div class="t rv"><span class="k">// tin công nghệ</span><h2>Tin công nghệ <span class="gt">mới&nbsp;nhất</span></h2>'
   '<p>Tin chọn lọc về AI, bảo mật, web &amp; SEO, có nguồn rõ ràng và góc nhìn cho doanh nghiệp nhỏ.</p></div><div class="grid nw-grid">'
   +''.join(card(x,'','h3',True) for x in items[:3])+'</div><p class="rv" style="margin-top:22px"><a class="btn ghost" href="tin-tuc.html">Xem tất cả tin công nghệ</a></p></div></section>')
  f=R/'index.html'; s=f.read_text(encoding='utf-8')
  if '<!-- news:home -->' not in s: s=s.replace('</section></main>','</section><!-- news:home --><!-- /news:home --></main>',1)
  if '<!-- news:head -->' not in s: s=s.replace('</head>','<!-- news:head --><!-- /news:head --></head>',1)
  s=put(put(s,'home',home),'head',RSSL); write('index.html',s)
  print(f'news: {len(items)} tin ({len(arts)} bài có trang riêng, {len(items)-len(arts)} thẻ link), {len(pages)} trang danh sách, feed {min(20,len(items))} mục')
  if '--no-chatbot' not in a:
    subprocess.run([sys.executable,str(R/'scripts/chatbot_build.py')],check=True)
  return 0
if __name__=='__main__': sys.exit(main())
