#!/usr/bin/env python3
"""Dựng mục Tin tức công nghệ từ data/news.json (idempotent).
- Ghi danh sách thẻ vào tin-tuc.html giữa <!-- news:list --> ... <!-- /news:list -->
- Ghi bộ lọc vào <!-- news:chips --> ... <!-- /news:chips -->, JSON-LD ItemList vào <!-- news:ld -->
- Ghi khối 3 tin mới nhất vào index.html giữa <!-- news:home --> ... <!-- /news:home -->
Dùng: python3 scripts/news_build.py [--check-urls]  (chạy trước scripts/tech_pass.py)"""
import json,re,sys,html,pathlib,datetime,urllib.request
R=pathlib.Path(__file__).resolve().parent.parent
D=json.loads((R/'data/news.json').read_text(encoding='utf-8'))
BASE='https://myagentvn.com/'
TOPICS={'ai':'AI','bao-mat':'Bảo mật','web-seo':'Web & SEO','du-lieu':'Dữ liệu','nen-tang':'Nền tảng & MXH'}
SV='<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICON={'ai':SV+'<rect x="5" y="5" width="14" height="14" rx="3"/><path d="M9 9h6v6H9zM9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/></svg>',
 'bao-mat':SV+'<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="M12 8v5M12 16h.01"/></svg>',
 'web-seo':SV+'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4M8 11h6M11 8v6"/></svg>',
 'du-lieu':SV+'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
 'nen-tang':SV+'<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8 11h8M8 14h5"/></svg>'}
REQ=('id','date','topic','title','summary','insight','source','url')
err=[]
items=D['items']
for i,it in enumerate(items):
  for k in REQ:
    if not str(it.get(k,'')).strip(): err.append(f'tin #{i+1} thiếu "{k}"')
  if it.get('topic') not in TOPICS: err.append(f'{it.get("id")}: topic lạ {it.get("topic")} (dùng {list(TOPICS)})')
  try: datetime.date.fromisoformat(it.get('date',''))
  except ValueError: err.append(f'{it.get("id")}: date phải là YYYY-MM-DD')
  if not str(it.get('url','')).startswith('https://'): err.append(f'{it.get("id")}: url phải là https://')
ids=[it.get('id') for it in items]
if len(set(ids))!=len(ids): err.append('id bị trùng')
if err: print('\n'.join('LỖI: '+e for e in err)); sys.exit(1)
items=sorted(items,key=lambda x:(x['date'],x['id']),reverse=True)
if '--check-urls' in sys.argv:
  bad=0
  for it in items:
    try:
      rq=urllib.request.Request(it['url'],headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36'})
      c=urllib.request.urlopen(rq,timeout=20).status
    except urllib.error.HTTPError as e: c=e.code
    except Exception as e: c=str(e)[:40]
    # 401/403/429: trang chặn bot, không phải link chết -> chỉ cảnh báo, kiểm tra tay bằng trình duyệt
    tag='OK' if c==200 else ('CHẶN BOT?' if c in (401,403,429) else 'LỖI')
    if tag=='LỖI': bad+=1
    print(f'{tag:9} {c} {it["url"]}')
  if bad: print(f'{bad} link lỗi'); sys.exit(1)
e=lambda x:html.escape(x,quote=True)
def vn(d): y,m,dd=d.split('-'); return f'{int(dd):02d}/{int(m):02d}/{y}'
def card(it,h='h2',home=False):
  t=it['topic']
  return (f'<article class="card glass news rv" data-topic="{t}" id="{e(it["id"])}"><div class="nw-top"><span class="nw-ic">{ICON[t]}</span>'
   f'<span class="nw-tg mono">{e(TOPICS[t])}</span><time class="mono" datetime="{it["date"]}">{vn(it["date"])}</time></div>'
   f'<{h} class="nw-h">{e(it["title"])}</{h}><p class="nw-s">{e(it["summary"])}</p>'
   +('' if home else f'<p class="nw-in"><b>Góc nhìn My Agent:</b> {e(it["insight"])}</p>')+
   f'<p class="nw-src"><span class="muted">Nguồn: {e(it["source"])}</span> <a class="btn ghost sm" href="{e(it["url"])}" target="_blank" rel="noopener noreferrer">Đọc nguồn<span class="sr"> bài “{e(it["title"])}” trên {e(it["source"])} (mở tab mới)</span></a></p></article>')
used=[k for k in TOPICS if any(it['topic']==k for it in items)]
chips=('<div class="chips nw-chips" role="group" aria-label="Lọc tin theo chủ đề"><button type="button" class="chip" data-f="all" aria-pressed="true">Tất cả <small>'+str(len(items))+'</small></button>'
 +''.join(f'<button type="button" class="chip" data-f="{k}" aria-pressed="false">{e(TOPICS[k])} <small>{sum(it["topic"]==k for it in items)}</small></button>' for k in used)+'</div>')
lst='<div class="grid nw-grid" id="news-list">'+''.join(card(it) for it in items)+'</div><p class="muted nw-empty" hidden>Chưa có tin cho chủ đề này.</p>'
ld={"@context":"https://schema.org","@type":"CollectionPage","name":"Tin tức công nghệ","url":BASE+"tin-tuc.html","inLanguage":"vi","dateModified":D.get('updated',items[0]['date']),
 "isPartOf":{"@id":BASE+"#website"},"publisher":{"@id":BASE+"#org"},
 "mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":[{"@type":"ListItem","position":i+1,"url":BASE+"tin-tuc.html#"+it['id'],"name":it['title']} for i,it in enumerate(items)]}}
ldh='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>'
def put(s,tag,body):
  pat=re.compile(rf'<!-- news:{tag} -->.*?<!-- /news:{tag} -->',re.S)
  if not pat.search(s): sys.exit(f'thiếu marker news:{tag}')
  return pat.sub(lambda m:f'<!-- news:{tag} -->{body}<!-- /news:{tag} -->',s,count=1)
f=R/'tin-tuc.html'; s=f.read_text(encoding='utf-8')
s=put(put(put(s,'chips',chips),'list',lst),'ld',ldh)
s=put(s,'updated',vn(D.get('updated',items[0]['date'])))
f.write_text(s,encoding='utf-8')
home=('<section class="soft nw-home"><div class="wrap"><div class="t rv"><span class="k">// tin công nghệ</span><h2>Tin công nghệ <span class="gt">mới&nbsp;nhất</span></h2>'
 '<p>Tin chọn lọc về AI, bảo mật, web &amp; SEO, có nguồn rõ ràng và góc nhìn cho doanh nghiệp nhỏ.</p></div><div class="grid nw-grid">'
 +''.join(card(it,'h3',True) for it in items[:3])+'</div><p class="rv" style="margin-top:22px"><a class="btn ghost" href="tin-tuc.html">Xem tất cả tin công nghệ</a></p></div></section>')
f=R/'index.html'; s=f.read_text(encoding='utf-8')
if '<!-- news:home -->' not in s:
  s=s.replace('</section></main>','</section><!-- news:home --><!-- /news:home --></main>',1)
s=put(s,'home',home); f.write_text(s,encoding='utf-8')
print(f'news: {len(items)} tin, chủ đề {used}')
