#!/usr/bin/env python3
"""My Agent – dịch vụ nhận form liên hệ (MẪU, CHƯA TRIỂN KHAI). Python 3.8+ chỉ dùng thư viện chuẩn.
Kênh nhận: Telegram Bot API sendMessage gửi thẳng tới Telegram của Peter (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID).
Lắng nghe 127.0.0.1:8787 (nginx proxy /api/contact). Cấu hình qua biến môi trường (file /etc/myagent/contact-api.env,
KHÔNG đưa vào repo): xem docs/lien-he-form.md và contact-api.env.example.
POST /api/contact  JSON {name, phone, email?, service?, message?, consent, _honey?, page?, estimate?}
  200 {"ok":true,"id":"..."} | 400 {"ok":false,"error":"invalid","fields":[...]} | 413 | 415 | 429 {"ok":false,"error":"rate_limited"} | 502 {"ok":false,"error":"delivery_failed"}
GET /api/contact/health -> 200 {"ok":true}"""
import json,os,re,time,uuid,threading,urllib.request,urllib.parse,logging,html,datetime
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
E=os.environ.get
HOST,PORT=E('CONTACT_HOST','127.0.0.1'),int(E('CONTACT_PORT','8787'))
ORIGINS={o.strip() for o in E('CONTACT_ALLOWED_ORIGINS','https://myagentvn.com,https://www.myagentvn.com').split(',') if o.strip()}
MAX_BODY=int(E('CONTACT_MAX_BODY','16384'))
RL_N,RL_WIN=int(E('CONTACT_RATE_N','5')),int(E('CONTACT_RATE_WINDOW','600'))   # 5 lần / 10 phút / IP
LIM={'name':100,'phone':20,'email':120,'service':100,'message':3000,'page':300,'estimate':200}
TG_API=E('TELEGRAM_API','https://api.telegram.org'); TG_TIMEOUT=float(E('TELEGRAM_TIMEOUT','4'))
PHONE=re.compile(r'^[0-9 +().-]{8,20}$'); MAIL=re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
log=logging.getLogger('contact-api'); _hits={}; _lk=threading.Lock()
def rate_ok(ip,now=None):
  now=now or time.time()
  with _lk:
    q=[t for t in _hits.get(ip,[]) if now-t<RL_WIN]
    if len(q)>=RL_N: _hits[ip]=q; return False
    q.append(now); _hits[ip]=q; return True
def clean(s,n): return re.sub(r'[\x00-\x08\x0b-\x1f\x7f]',' ',str(s or '')).strip()[:n]
def validate(d):
  if not isinstance(d,dict): return None,['body']
  v={k:clean(d.get(k),n) for k,n in LIM.items()}; bad=[]
  if len(v['name'])<2: bad.append('name')
  if not PHONE.match(v['phone']) or len(re.sub(r'\D','',v['phone']))<8: bad.append('phone')
  if v['email'] and not MAIL.match(v['email']): bad.append('email')
  if not d.get('consent'): bad.append('consent')
  return v,bad
def now_vn():
  try:
    from zoneinfo import ZoneInfo; return datetime.datetime.now(ZoneInfo('Asia/Ho_Chi_Minh'))
  except Exception: return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
def tg_text(v,i,limit=4096):
  q=lambda s:html.escape(s or '-',quote=False)
  head=(f"<b>Yêu cầu tư vấn mới</b> #{i}\n<b>Tên:</b> {q(v['name'])}\n<b>SĐT:</b> {q(v['phone'])}\n<b>Email:</b> {q(v['email'])}\n"
        f"<b>Dịch vụ:</b> {q(v['service'])}\n"+(f"<b>Tạm tính:</b> {q(v['estimate'])}\n" if v.get('estimate') else '')+
        f"<b>Trang:</b> {q(v['page'])}\n<b>Thời gian:</b> {now_vn():%H:%M %d/%m/%Y} (giờ VN)\n<b>Nội dung:</b>\n")
  room=limit-len(head); msg=v['message'] or '-'
  body=q(msg)
  if len(body)>room:  # cắt trên văn bản gốc để không cắt đôi thực thể HTML
    while len(body)>room-1 and msg: msg=msg[:max(0,len(msg)-max(1,len(body)-room+1))]; body=q(msg)
    body+='…'
  return head+body
def send_tg(v,i):
  t,c=E('TELEGRAM_BOT_TOKEN'),E('TELEGRAM_CHAT_ID')
  if not (t and c): raise RuntimeError('telegram chưa cấu hình')
  data=urllib.parse.urlencode({'chat_id':c,'text':tg_text(v,i),'parse_mode':'HTML','disable_web_page_preview':'true'}).encode()
  with urllib.request.urlopen(f'{TG_API}/bot{t}/sendMessage',data,timeout=TG_TIMEOUT) as r:
    return r.status==200 and json.loads(r.read()).get('ok') is True
def deliver(v,i):
  try: return bool(send_tg(v,i))
  except Exception as x: log.error('telegram lỗi: %s',type(x).__name__); return False
class H(BaseHTTPRequestHandler):
  server_version='contact-api'
  def _j(self,code,o):
    b=json.dumps(o).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b)))
    og=self.headers.get('Origin')
    if og in ORIGINS: self.send_header('Access-Control-Allow-Origin',og); self.send_header('Vary','Origin')
    self.end_headers(); self.wfile.write(b)
  def ip(self): return (self.headers.get('X-Real-IP') or self.client_address[0]).strip()
  def do_OPTIONS(self):
    if self.headers.get('Origin') not in ORIGINS: return self._j(403,{'ok':False,'error':'origin'})
    self.send_response(204); self.send_header('Access-Control-Allow-Origin',self.headers['Origin']); self.send_header('Access-Control-Allow-Methods','POST'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Max-Age','600'); self.end_headers()
  def do_GET(self):
    return self._j(200,{'ok':True}) if self.path.rstrip('/').endswith('/health') else self._j(404,{'ok':False})
  def do_POST(self):
    og=self.headers.get('Origin')
    if og and og not in ORIGINS: return self._j(403,{'ok':False,'error':'origin'})
    if 'application/json' not in (self.headers.get('Content-Type') or ''): return self._j(415,{'ok':False,'error':'json_required'})
    n=int(self.headers.get('Content-Length') or 0)
    if n<=0 or n>MAX_BODY: return self._j(413,{'ok':False,'error':'too_large'})
    try: d=json.loads(self.rfile.read(n))
    except Exception: return self._j(400,{'ok':False,'error':'invalid','fields':['body']})
    if isinstance(d,dict) and d.get('_honey'): return self._j(200,{'ok':True,'id':'-'})   # bot: giả vờ thành công
    if not rate_ok(self.ip()): return self._j(429,{'ok':False,'error':'rate_limited'})
    v,bad=validate(d)
    if bad: return self._j(400,{'ok':False,'error':'invalid','fields':bad})
    i=uuid.uuid4().hex[:8]
    if not deliver(v,i): return self._j(502,{'ok':False,'error':'delivery_failed'})
    log.info('đã nhận %s', i); return self._j(200,{'ok':True,'id':i})
  def log_message(self,*a): pass
def main():
  logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
  s=ThreadingHTTPServer((HOST,PORT),H); log.info('listening %s:%s',HOST,PORT); s.serve_forever()
if __name__=='__main__': main()
