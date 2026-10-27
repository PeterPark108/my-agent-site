#!/usr/bin/env python3
"""Dựng trang Tài nguyên AI Agent từ data/ai-agent-resources.json (idempotent).
- Thanh tab + ô tìm kiếm vào <!-- res:bar -->, danh sách theo nhóm vào <!-- res:list -->,
  JSON-LD CollectionPage/ItemList vào <!-- res:ld -->, ngày cập nhật vào <!-- res:updated -->.
- Chặn link affiliate/theo dõi (imp.i384100.net, utm_*, ref=, irclickid...).
Dùng: python3 scripts/resources_build.py [--check-urls]  (chạy trước scripts/tech_pass.py)"""
import json,re,sys,html,pathlib,datetime,urllib.request,urllib.parse
R=pathlib.Path(__file__).resolve().parent.parent
D=json.loads((R/'data/ai-agent-resources.json').read_text(encoding='utf-8'))
BASE='https://myagentvn.com/'; PAGE='tai-nguyen-ai-agent.html'
SV='<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICON={'video':SV+'<rect x="2" y="5" width="14" height="14" rx="2"/><path d="m16 10 6-3v10l-6-3"/></svg>',
 'github':SV+'<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 4l-4 16"/></svg>',
 'huong-dan':SV+'<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></svg>',
 'sach':SV+'<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3"/><path d="M20 4v14h-7"/></svg>',
 'nghien-cuu':SV+'<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/><path d="M7 15h10"/></svg>',
 'khoa-hoc':SV+'<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/></svg>'}
BAD_HOST=('imp.i384100.net','bit.ly','tinyurl.com','shorturl.at','click.linksynergy.com')
BAD_Q=re.compile(r'^(utm_.*|ref|ref_|aff.*|irclickid|irgwc|afsrc|fbclid|gclid|si|mc_cid|mc_eid|clickid|partner.*)$',re.I)
err=[]
for g in D['groups']:
  if g['id'] not in ICON: err.append(f'nhóm lạ {g["id"]}')
  for it in g['items']:
    for k in ('name','description_vi'):
      if not it.get(k,'').strip(): err.append(f'{g["id"]}: thiếu {k}')
    u=it.get('url','')
    if u:
      p=urllib.parse.urlsplit(u)
      if p.scheme!='https': err.append(f'{it["name"]}: url phải https')
      if p.hostname in BAD_HOST: err.append(f'{it["name"]}: link rút gọn/affiliate bị cấm ({p.hostname})')
      if any(BAD_Q.match(k) for k,_ in urllib.parse.parse_qsl(p.query)): err.append(f'{it["name"]}: url còn tham số theo dõi')
if err: print('\n'.join('LỖI: '+x for x in err)); sys.exit(1)
if '--check-urls' in sys.argv:
  bad=0
  for g in D['groups']:
    for it in g['items']:
      u=it.get('url');
      if not u: continue
      try:
        c=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36'}),timeout=25).status
      except urllib.error.HTTPError as x: c=x.code
      except Exception as x: c=str(x)[:40]
      tag='OK' if c==200 else ('CHẶN BOT?' if c in (401,403,429) else 'LỖI')
      bad+=tag=='LỖI'; print(f'{tag:9} {c} {u}')
  if bad: print(f'{bad} link lỗi'); sys.exit(1)
e=lambda x:html.escape(x,quote=True)
total=sum(len(g['items']) for g in D['groups'])
tabs=('<div class="rs-bar"><div class="rs-tabs" role="tablist" aria-label="Nhóm tài nguyên">'
 f'<a href="#rs-list" role="tab" class="chip" data-g="all" aria-selected="true" aria-controls="rs-list">Tất cả <small>{total}</small></a>'
 +''.join(f'<a href="#g-{g["id"]}" role="tab" class="chip" data-g="{g["id"]}" aria-selected="false" aria-controls="rs-list" tabindex="-1">{e(g["name"])} <small>{len(g["items"])}</small></a>' for g in D['groups'])
 +'</div><div class="rs-search"><label for="rs-q" class="sr">Tìm tài nguyên theo tên hoặc mô tả</label>'
 '<input id="rs-q" type="search" placeholder="Tìm theo tên, mô tả… (vd: MCP, Python)" autocomplete="off" aria-describedby="rs-count">'
 f'<p id="rs-count" class="mono muted" role="status" aria-live="polite">{total} tài nguyên</p></div></div>')
def card(g,it):
  meta=' · '.join(x for x in (it.get('provider'),) if x)
  lv=f'<span class="rs-lv mono">{e(it["level"])}</span>' if it.get('level') else ''
  if it.get('url'):
    host=urllib.parse.urlsplit(it['url']).hostname.removeprefix('www.')
    act=f'<a class="btn ghost sm" href="{e(it["url"])}" target="_blank" rel="noopener noreferrer">Mở tài nguyên<span class="sr"> “{e(it["name"])}” trên {e(host)} (mở tab mới)</span></a>'
  else: act='<span class="muted rs-nolink">Tìm tên khóa học trên nền tảng chính thức</span>'
  return (f'<article class="card glass rs-card rv"><div class="rs-top"><span class="nw-ic">{ICON[g["id"]]}</span>{lv}</div>'
   f'<h3 class="rs-h">{e(it["name"])}</h3>'+(f'<p class="rs-by mono">{e(meta)}</p>' if meta else '')+
   f'<p class="rs-d">{e(it["description_vi"])}</p><p class="rs-act">{act}</p></article>')
lst=('<div id="rs-list" role="tabpanel" aria-label="Danh sách tài nguyên">'+''.join(
 f'<section class="rs-group" id="g-{g["id"]}" data-g="{g["id"]}"><h2 class="rs-gh"><span class="nw-ic">{ICON[g["id"]]}</span>{e(g["name"])} <small class="mono muted">{len(g["items"])}</small></h2>'
 f'<div class="grid rs-grid">'+''.join(card(g,it) for it in g['items'])+'</div></section>' for g in D['groups'])
 +'<p class="rs-empty muted" hidden>Không tìm thấy tài nguyên phù hợp. Thử từ khóa khác hoặc chọn “Tất cả”.</p></div>')
pos=0; li=[]
for g in D['groups']:
  for it in g['items']:
    pos+=1; x={"@type":"ListItem","position":pos,"name":it['name']}
    if it.get('url'): x["url"]=it['url']
    li.append(x)
ld={"@context":"https://schema.org","@type":"CollectionPage","name":"Lộ trình học AI Agent: tài nguyên từ A đến Z","url":BASE+PAGE,"inLanguage":"vi","dateModified":D['updated'],
 "isPartOf":{"@id":BASE+"#website"},"publisher":{"@id":BASE+"#org"},"mainEntity":{"@type":"ItemList","numberOfItems":pos,"itemListElement":li}}
ldh='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>'
def vn(d): y,m,dd=d.split('-'); return f'{int(dd):02d}/{int(m):02d}/{y}'
def put(s,tag,body):
  pat=re.compile(rf'<!-- res:{tag} -->.*?<!-- /res:{tag} -->',re.S)
  if not pat.search(s): sys.exit(f'thiếu marker res:{tag}')
  return pat.sub(lambda m:f'<!-- res:{tag} -->{body}<!-- /res:{tag} -->',s,count=1)
f=R/PAGE; s=f.read_text(encoding='utf-8')
for t,b in (('bar',tabs),('list',lst),('ld',ldh),('updated',vn(D['updated']))): s=put(s,t,b)
f.write_text(s,encoding='utf-8')
print('resources:',', '.join(f'{g["id"]}={len(g["items"])}' for g in D['groups']),'| tổng',total)
