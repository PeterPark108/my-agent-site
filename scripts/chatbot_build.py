#!/usr/bin/env python3
"""Tạo data/chatbot-kb.json cho trợ lý MJ từ nội dung THẬT của các trang (không thêm thông tin mới).
Chạy: python3 scripts/chatbot_build.py  (sau khi sửa trang / chạy tech_pass.py)"""
import re,json,html,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
SKIP={'404.html','ghi-nguon.html'}
def txt(x):
  x=re.sub(r'<(script|style|svg|form|select)\b.*?</\1>',' ',x,flags=re.S)
  return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).replace(' // ',' ').strip()
def short(t,n=300):
  t=re.sub(r'\s+\d{2}(\s+[a-zà-ỹ ]+)?$','',t)
  if len(t)<=n: return t
  c=t[:n]; i=max(c.rfind('. '),c.rfind('; '))
  return (c[:i+1] if i>80 else c.rsplit(' ',1)[0]+'…')
docs=[]
pages=sorted(list(R.glob('*.html'))+list(R.glob('dich-vu/*.html'))+[p for p in R.glob('tin-tuc/*.html') if not re.match(r'trang-\d+\.html$',p.name)]+sorted(R.glob('blog/*.html')))
for f in pages:
  s=f.read_text(); rel=str(f.relative_to(R))
  if rel in SKIP or 'http-equiv="refresh"' in s: continue
  m=re.search(r'<main\b.*?</main>',s,flags=re.S)
  if not m: continue
  main=m.group(0)
  h1=txt(re.search(r'<h1[^>]*>(.*?)</h1>',main,flags=re.S).group(1)) if '<h1' in main else ''
  desc=html.unescape((re.search(r'<meta name="description" content="([^"]*)"',s) or [None,''])[1])
  name=h1 or txt(re.search(r'<title>(.*?)</title>',s).group(1)).split('|')[0].strip()
  url=rel
  docs.append(dict(u=url,p=name,h=name,a=desc,x=''))
  # FAQ
  for q,a in re.findall(r'<summary[^>]*>(.*?)</summary>\s*(.*?)</details>',main,flags=re.S):
    docs.append(dict(u=url,p=name,h=txt(q),a=short(txt(a)),x='faq'))
  main2=re.sub(r'<details\b.*?</details>',' ',main,flags=re.S)
  # sections by h2
  for sec in re.split(r'(?=<h2\b)',main2)[1:]:
    h2=txt(re.search(r'<h2[^>]*>(.*?)</h2>',sec,flags=re.S).group(1))
    body=re.sub(r'<h2[^>]*>.*?</h2>','',sec,count=1,flags=re.S)
    if re.match(r'(Cùng nhóm|Câu hỏi thường gặp|Dịch vụ liên quan|Nguồn tham|Bài liên)',h2): continue
    if 'bảng giá' in h2.lower() or 'bảng giá' in txt(body[:200]).lower():
      plans=[]
      for b in re.split(r'(?=<h3\b)',body)[1:]:
        n=txt(re.search(r'<h3[^>]*>(.*?)</h3>',b,flags=re.S).group(1)); t=txt(b)
        pm=re.search(r'[\d][\d.,–-]*\s*(?:triệu|nghìn|đ|VNĐ)(?:\s*/\s*\w+)?',t)
        if pm: plans.append((n,pm.group(0)))
      if plans:
        a='Bảng giá tham khảo trên trang: '+'; '.join(f'{n}: {p}' for n,p in plans)+'. Giá cuối cùng tùy phạm vi, nên liên hệ để được báo giá chính xác.'
        docs.append(dict(u=url,p=name,h='Bảng giá '+name,a=a,x='price')); continue
    subs=re.split(r'(?=<h3\b)',body)
    lead=txt(subs[0])
    if subs[1:] and len(subs)>2:
      items=[txt(re.search(r'<h3[^>]*>(.*?)</h3>',b,flags=re.S).group(1)) for b in subs[1:]]
      a=(lead+' ' if len(lead)>20 else '')+h2+': '+', '.join(items)+'.'
      docs.append(dict(u=url,p=name,h=h2,a=short(a),x=''))
      for b in subs[1:]:
        h3=txt(re.search(r'<h3[^>]*>(.*?)</h3>',b,flags=re.S).group(1)); t=txt(re.sub(r'<h3[^>]*>.*?</h3>','',b,count=1,flags=re.S))
        if len(t)>25: docs.append(dict(u=url,p=name,h=h3,a=short(t),x=''))
    else:
      t=txt(body)
      if len(t)>25: docs.append(dict(u=url,p=name,h=h2,a=short(t),x=''))
# dedupe
seen=set();out=[]
for d in docs:
  k=(d['h'],d['a'])
  if k in seen or not d['a'] or re.search(r'24h|24/7|24 giờ',d['h']+d['a']): continue
  seen.add(k); out.append(d)
(R/'data/chatbot-kb.json').write_text(json.dumps({'v':1,'d':[[d['u'],d['p'],d['h'],d['a'],d['x']] for d in out]},ensure_ascii=False,separators=(',',':')))
print(len(out),'mục ->',(R/'data/chatbot-kb.json').stat().st_size,'bytes')
