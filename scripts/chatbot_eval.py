#!/usr/bin/env python3
"""Đánh giá trợ lý MJ: chạy các câu trong scripts/chatbot_eval.txt qua js/chat.js thật (Chromium + máy chủ tĩnh tạm).
Chạy: python3 scripts/chatbot_eval.py [-v]"""
import sys,threading,http.server,functools,pathlib,socketserver
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent.parent
class Q(http.server.SimpleHTTPRequestHandler):
  def __init__(s,*a,**k):super().__init__(*a,directory=str(R),**k)
  def log_message(self,*a):pass
srv=socketserver.TCPServer(('127.0.0.1',0),Q);port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
cases=[l.split('|') for l in (R/'scripts/chatbot_eval.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
def intent(a):
  t=a['t']
  if a.get('fb'):return 'fallback'
  for k,v in (('greet','Chào bạn!'),('thanks','Không có gì'),('ai','không phải người thật'),('who','Mình là MJ, trợ lý tự động của My Agent. Mình giúp'),('contact','Bạn liên hệ My Agent qua'),('tracking','Tra cứu tiến độ và nhập'),('services','dịch vụ: '),('price','Giá phụ thuộc')):
    if v in t:return k
  return ''
ok=0
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();pg.goto(f'http://127.0.0.1:{port}/lien-he.html?chat=1')
  for q,exp in cases:
    q=q.strip();exp=[e.strip() for e in exp.split(',')]
    a=pg.evaluate('q=>MJ_answer(q)',q)
    links=' '.join(l[1] for l in (a.get('l') or []))
    it=intent(a)
    hit=any((e[7:]==it) if e.startswith('intent:') else (e in links and not a.get('fb')) for e in exp)
    ok+=hit
    if not hit or '-v' in sys.argv: print(('OK  ' if hit else 'MISS'),q,'->',it or links,'|',a['t'][:90])
  b.close()
print(f'Kết quả: {ok}/{len(cases)} = {ok*100//len(cases)}%')
sys.exit(0 if ok==len(cases) else 1)
