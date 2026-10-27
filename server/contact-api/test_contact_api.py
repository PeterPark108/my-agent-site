#!/usr/bin/env python3
"""Test dịch vụ mẫu với Telegram GIẢ (máy chủ HTTP cục bộ, không gọi api.telegram.org): python3 server/contact-api/test_contact_api.py"""
import json,threading,urllib.request,urllib.error,urllib.parse,sys,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
sent=[]; MODE={'v':'ok'}
class TG(BaseHTTPRequestHandler):
  def do_POST(self):
    d=urllib.parse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode()); sent.append((self.path,{k:v[0] for k,v in d.items()}))
    code,b=(200,{'ok':True}) if MODE['v']=='ok' else (400,{'ok':False,'description':'Bad Request'})
    self.send_response(code); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps(b).encode())
  def log_message(self,*a): pass
tg=ThreadingHTTPServer(('127.0.0.1',0),TG); threading.Thread(target=tg.serve_forever,daemon=True).start()
os.environ.update(TELEGRAM_API=f'http://127.0.0.1:{tg.server_address[1]}',TELEGRAM_BOT_TOKEN='123:TEST',TELEGRAM_CHAT_ID='42')
sys.path.insert(0,os.path.dirname(__file__)); import contact_api as c
c.RL_N=3
s=c.ThreadingHTTPServer(('127.0.0.1',0),c.H); threading.Thread(target=s.serve_forever,daemon=True).start(); U=f'http://127.0.0.1:{s.server_address[1]}/api/contact'
def post(d,ip,origin='https://myagentvn.com',ct='application/json'):
  r=urllib.request.Request(U,json.dumps(d).encode(),{'Content-Type':ct,'Origin':origin,'X-Real-IP':ip})
  try:
    with urllib.request.urlopen(r) as x: return x.status,json.loads(x.read()),x.headers
  except urllib.error.HTTPError as e: return e.code,json.loads(e.read() or b'{}'),e.headers
G={'name':'Nguyễn <b>A</b> & Co','phone':'0328 439 972','email':'a@b.vn','service':'Thiết kế website','message':'Cần web <script>x</script>','consent':'Đồng ý','page':'https://myagentvn.com/lien-he.html','estimate':'7.200.000đ'}
fail=[]
def ok(c_,m): c_ or fail.append(m)
st,j,h=post(G,'1.1.1.1'); ok(st==200 and j['ok'] is True and h['Access-Control-Allow-Origin']=='https://myagentvn.com','hợp lệ -> 200 {ok:true} + CORS')
ok(len(sent)==1 and sent[0][0]=='/bot123:TEST/sendMessage','gọi đúng sendMessage')
m=sent[0][1] if sent else {}
ok(m.get('chat_id')=='42' and m.get('parse_mode')=='HTML','chat_id + parse_mode HTML')
tx=m.get('text','')
for want in ['Nguyễn &lt;b&gt;A&lt;/b&gt; &amp; Co','0328 439 972','a@b.vn','Thiết kế website','Cần web &lt;script&gt;','7.200.000đ','lien-he.html','(giờ VN)']: ok(want in tx,f'tin nhắn thiếu/không escape: {want}')
ok('<script>' not in tx,'chưa escape HTML')
long=c.tg_text(dict(c.validate(G)[0],message='<&>'*1000),'x'); ok(len(long)<=4096 and long.endswith('…') and not long[:-1].endswith('&'),f'cắt 4096 ({len(long)})')
MODE['v']='fail'; st,j,_=post(G,'1.1.1.7'); ok(st==502 and j['error']=='delivery_failed','Telegram lỗi -> 502'); MODE['v']='ok'
n=len(sent); st,j,_=post(dict(G,phone='abc'),'1.1.1.2'); ok(st==400 and 'phone' in j['fields'],'SĐT sai -> 400')
st,j,_=post(dict(G,consent=''),'1.1.1.2'); ok(st==400 and 'consent' in j['fields'],'thiếu đồng ý -> 400')
st,j,_=post(dict(G,_honey='bot'),'1.1.1.3'); ok(st==200 and len(sent)==n,'honeypot -> 200 nhưng không gửi Telegram')
st,_,_=post(G,'1.1.1.4',origin='https://evil.example'); ok(st==403,'origin lạ -> 403')
st,_,_=post(G,'1.1.1.5',ct='text/plain'); ok(st==415,'không phải JSON -> 415')
st,_,_=post(dict(G,message='x'*20000),'1.1.1.6'); ok(st==413,'quá lớn -> 413')
codes=[post(G,'9.9.9.9')[0] for _ in range(4)]; ok(codes==[200,200,200,429],f'rate limit {codes}')
for f in fail: print('FAIL:',f)
print('OK: test_contact_api đạt' if not fail else f'{len(fail)} lỗi'); sys.exit(1 if fail else 0)
