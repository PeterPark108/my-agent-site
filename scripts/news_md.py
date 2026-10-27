#!/usr/bin/env python3
"""Front-matter + Markdown an toàn (stdlib) cho mục Tin tức.
Mặc định ESCAPE mọi HTML trong bài; chỉ sinh các thẻ trong whitelist:
h2 h3 p ul ol li blockquote pre code table thead tbody tr th td strong em a img hr figure figcaption.
Link chỉ nhận https:, http:, mailto:, #neo hoặc đường dẫn tương đối; link ngoài có target=_blank rel="noopener noreferrer"."""
import re,html,unicodedata
E=lambda x:html.escape(x,quote=True)

def slugify(t):
  t=unicodedata.normalize('NFD',t.replace('đ','d').replace('Đ','D'))
  t=''.join(c for c in t if unicodedata.category(c)!='Mn').lower()
  return re.sub(r'[^a-z0-9]+','-',t).strip('-')

# ---------- front-matter (tập con YAML: key: value, list [a, b], list "- " các chuỗi/mapping) ----------
def _scalar(v):
  v=v.strip()
  if v[:1] in '"\'' and v:
    q=v[0]; j=1
    while j<len(v) and not (v[j]==q and v[j-1]!='\\'): j+=1
    if j<len(v) and re.fullmatch(r'\s*(#.*)?',v[j+1:]): v=v[:j+1]
  else: v=re.split(r'\s+#',v,1)[0].strip()
  if len(v)>=2 and v[0]==v[-1] and v[0] in '"\'':
    v=v[1:-1]
    return v.replace('\\"','"') if v else ''
  if v.lower() in ('true','yes'): return True
  if v.lower() in ('false','no'): return False
  if v.startswith('[') and v.endswith(']'):
    return [_scalar(x) for x in v[1:-1].split(',') if x.strip()]
  return v

def parse_front(text):
  """Trả về (meta, body, lỗi[])."""
  err=[]
  text=text.replace('\r\n','\n').lstrip('\ufeff')
  if not text.startswith('---\n'): return {},text,['thiếu front-matter: file phải mở đầu bằng dòng ---']
  end=text.find('\n---',4)
  if end<0: return {},text,['front-matter chưa đóng bằng dòng ---']
  fm=text[4:end]; body=text[end+4:].lstrip('\n')
  if body.startswith('-'): body=body.lstrip('-').lstrip('\n')
  meta={}; key=None; cur=None
  for n,line in enumerate(fm.split('\n'),2):
    if not line.strip() or line.lstrip().startswith('#'): continue
    m=re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$',line)
    if m and not line.startswith(' '):
      key=m.group(1); v=m.group(2)
      if key in meta: err.append(f'dòng {n}: trường "{key}" bị lặp')
      meta[key]=_scalar(v) if v.strip() else []
      cur=None; continue
    m=re.match(r'^\s+-\s*(.*)$',line)
    if m and key is not None and isinstance(meta.get(key),list):
      item=m.group(1); km=re.match(r'^([A-Za-z_]\w*):\s*(.*)$',item)
      if km: cur={km.group(1):_scalar(km.group(2))}; meta[key].append(cur)
      else: cur=None; meta[key].append(_scalar(item))
      continue
    m=re.match(r'^\s+([A-Za-z_]\w*):\s*(.*)$',line)
    if m and isinstance(cur,dict): cur[m.group(1)]=_scalar(m.group(2)); continue
    err.append(f'dòng {n} trong front-matter không hiểu được: {line.strip()[:60]}')
  return meta,body,err

# ---------- Markdown ----------
def safe_url(u):
  u=html.unescape(u.strip())
  if re.search(r'[\x00-\x20"<>]',u): return None
  low=re.sub(r'[\s\x00-\x1f]','',u).lower()
  m=re.match(r'^([a-z][a-z0-9+.-]*):',low)
  if m and m.group(1) not in ('http','https','mailto'): return None
  if u.startswith('//'): return None
  return u

def is_external(u): return re.match(r'^https?://',u) and not re.match(r'^https?://(www\.)?myagentvn\.com(/|$)',u)

INL=re.compile(r'`([^`\n]+)`|!\[([^\]\n]*)\]\(([^)\s]+)\)|\[([^\]\n]+)\]\(([^)\s]+)\)')
def _emph(s):
  s=re.sub(r'\*\*(?=\S)(.+?)(?<=\S)\*\*',r'<strong>\1</strong>',s)
  s=re.sub(r'(?<![\w*])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![\w*])',r'<em>\1</em>',s)
  return s

class Ctx:
  def __init__(s,img=None): s.err=[]; s.warn=[]; s.links=[]; s.img=img; s.imgs=[]

def inline(raw,ctx,nolink=False):
  out=[]; pos=0
  for m in INL.finditer(raw):
    out.append(_emph(E(raw[pos:m.start()]))); pos=m.end()
    if m.group(1) is not None: out.append('<code>'+E(m.group(1))+'</code>')
    elif m.group(3) is not None:
      alt=m.group(2).strip(); src=safe_url(m.group(3))
      if not alt: ctx.err.append(f'ảnh thiếu chú thích (alt): {m.group(3)[:60]}')
      if src is None: ctx.err.append(f'đường dẫn ảnh không an toàn: {m.group(3)[:60]}'); continue
      wh=ctx.img(src) if ctx.img else None
      if not wh: ctx.err.append(f'ảnh phải là file trong assets/news/ (png/jpg/webp) đọc được kích thước: {src[:60]}'); continue
      ctx.imgs.append(src)
      out.append(f'<img src="{E(wh[2])}" alt="{E(alt)}" width="{wh[0]}" height="{wh[1]}" loading="lazy" decoding="async">')
    else:
      txt=m.group(4); url=safe_url(m.group(5))
      if nolink or url is None:
        if url is None: ctx.err.append(f'link bị chặn (chỉ dùng https:, http:, mailto:, # hoặc đường dẫn tương đối): {m.group(5)[:60]}')
        out.append(inline(txt,ctx,True)); continue
      ctx.links.append(url)
      ext=' target="_blank" rel="noopener noreferrer"' if is_external(url) else ''
      out.append(f'<a href="{E(url)}"{ext}>'+inline(txt,ctx,True)+'</a>')
  out.append(_emph(E(raw[pos:])))
  return ''.join(out)

def render(md,ctx=None):
  """Markdown -> (html, danh sách (cấp,id,chữ) heading, ctx)."""
  ctx=ctx or Ctx()
  lines=md.replace('\r\n','\n').replace('\t','    ').split('\n')
  out=[]; heads=[]; used={}; i=0; n=len(lines)
  def hid(t):
    b=slugify(re.sub(r'<[^>]+>','',t)) or 'muc'; k=used.get(b,0); used[b]=k+1
    return b if not k else f'{b}-{k+1}'
  blank=lambda l:not l.strip()
  def is_start(l):
    return bool(re.match(r'^(#{1,6}\s|```|>|\s*[-*+]\s|\s*\d+[.)]\s|---+\s*$|\|)',l))
  while i<n:
    l=lines[i]
    if blank(l): i+=1; continue
    if l.startswith('```'):
      lang=slugify(l[3:].strip())[:20]; buf=[]; i+=1
      while i<n and not lines[i].startswith('```'): buf.append(lines[i]); i+=1
      if i>=n: ctx.err.append('khối code ``` chưa đóng')
      i+=1
      out.append('<pre><code'+(f' class="language-{lang}"' if lang else '')+'>'+E('\n'.join(buf))+'</code></pre>'); continue
    m=re.match(r'^(#{1,6})\s+(.*?)\s*#*\s*$',l)
    if m:
      lv=len(m.group(1))
      if lv==1: ctx.err.append('không dùng "# " (H1) trong bài: tiêu đề bài đã là H1, hãy dùng "## "')
      lv=min(max(lv,2),3); t=inline(m.group(2),ctx); h=hid(m.group(2))
      heads.append((lv,h,re.sub(r'<[^>]+>','',t)))
      out.append(f'<h{lv} id="{h}">{t}</h{lv}>'); i+=1; continue
    if re.match(r'^(---+|\*\*\*+)\s*$',l): out.append('<hr>'); i+=1; continue
    if l.startswith('>'):
      buf=[]
      while i<n and lines[i].startswith('>'): buf.append(re.sub(r'^>\s?','',lines[i])); i+=1
      inner,h2,_=render('\n'.join(buf),ctx); out.append('<blockquote>'+inner+'</blockquote>'); continue
    if l.lstrip().startswith('|') and i+1<n and re.match(r'^\s*\|?\s*:?-{3,}',lines[i+1]):
      cells=lambda r:[c.strip() for c in r.strip().strip('|').split('|')]
      hd=cells(l); i+=2; rows=[]
      while i<n and lines[i].lstrip().startswith('|'): rows.append(cells(lines[i])); i+=1
      t='<div class="nwa-table"><table><thead><tr>'+''.join(f'<th scope="col">{inline(c,ctx)}</th>' for c in hd)+'</tr></thead><tbody>'
      t+=''.join('<tr>'+''.join(f'<td>{inline(c,ctx)}</td>' for c in (r+['']*len(hd))[:len(hd)])+'</tr>' for r in rows)+'</tbody></table></div>'
      out.append(t); continue
    m=re.match(r'^\s*([-*+]|\d+[.)])\s+',l)
    if m:
      ordered=m.group(1)[0].isdigit(); items=[]
      pat=r'^\s*\d+[.)]\s+' if ordered else r'^\s*[-*+]\s+'
      while i<n and (re.match(pat,lines[i]) or (items and lines[i].startswith('  ') and lines[i].strip())):
        if re.match(pat,lines[i]): items.append(re.sub(pat,'',lines[i]))
        else: items[-1]+=' '+lines[i].strip()
        i+=1
      tg='ol' if ordered else 'ul'
      out.append(f'<{tg}>'+''.join('<li>'+inline(x,ctx)+'</li>' for x in items)+f'</{tg}>'); continue
    buf=[l]; i+=1
    while i<n and not blank(lines[i]) and not is_start(lines[i]): buf.append(lines[i]); i+=1
    p=' '.join(x.strip() for x in buf)
    if re.fullmatch(r'!\[[^\]]*\]\([^)\s]+\)',p):
      im=inline(p,ctx); alt=re.match(r'!\[([^\]]*)\]',p).group(1).strip()
      out.append(f'<figure class="nwa-fig">{im}<figcaption>{E(alt)}</figcaption></figure>' if im else '')
    else: out.append('<p>'+inline(p,ctx)+'</p>')
  return ''.join(out),heads,ctx

def words(md):
  t=re.sub(r'```.*?```',' ',md,flags=re.S); t=re.sub(r'\]\([^)]*\)',']',t)
  return len(re.findall(r'\w+',t))
