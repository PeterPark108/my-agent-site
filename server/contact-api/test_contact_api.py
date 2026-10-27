#!/usr/bin/env python3
"""Test dịch vụ mẫu (không gửi mail thật — deliver được thay bằng hàm giả): python3 server/contact-api/test_contact_api.py"""
import json,threading,urllib.request,urllib.error,sys,os
sys.path.insert(0,os.path.dirname(__file__)); import contact_api as c
sent=[]; c.deliver=lambda v,i:(sent.append(v),True)[1]; c.RL_N=3
s=c.ThreadingHTTPServer(('127.0.0.1',0),c.H); threading.Thread(target=s.serve_forever,daemon=True).start(); U=f'http://127.0.0.1:{s.server_address[1]}/api/contact'
def post(d,ip,origin='https://myagentvn.com',ct='application/json'):
  r=urllib.request.Request(U,json.dumps(d).encode(),{'Content-Type':ct,'Origin':origin,'X-Real-IP':ip})
  try:
    with urllib.request.urlopen(r) as x: return x.status,json.loads(x.read()),x.headers
  except urllib.error.HTTPError as e: return e.code,json.loads(e.read() or b'{}'),e.headers
G={'name':'Nguyễn Văn A','phone':'0328 439 972','email':'a@b.vn','service':'Thiết kế website','message':'x','consent':'Đồng ý'}
fail=[]
def ok(c_,m): c_ or fail.append(m)
st,j,h=post(G,'1.1.1.1'); ok(st==200 and j['ok'] and h['Access-Control-Allow-Origin']=='https://myagentvn.com','hợp lệ -> 200 + CORS')
st,j,_=post(dict(G,phone='abc'),'1.1.1.2'); ok(st==400 and 'phone' in j['fields'],'SĐT sai -> 400')
st,j,_=post(dict(G,consent=''),'1.1.1.2'); ok(st==400 and 'consent' in j['fields'],'thiếu đồng ý -> 400')
st,j,_=post(dict(G,_honey='bot'),'1.1.1.3'); ok(st==200 and len(sent)==1,'honeypot -> 200 nhưng không gửi')
st,_,_=post(G,'1.1.1.4',origin='https://evil.example'); ok(st==403,'origin lạ -> 403')
st,_,_=post(G,'1.1.1.5',ct='text/plain'); ok(st==415,'không phải JSON -> 415')
st,_,_=post(dict(G,message='x'*20000),'1.1.1.6'); ok(st==413,'quá lớn -> 413')
codes=[post(G,'9.9.9.9')[0] for _ in range(4)]; ok(codes==[200,200,200,429],f'rate limit {codes}')
for f in fail: print('FAIL:',f)
print('OK: test_contact_api đạt' if not fail else f'{len(fail)} lỗi'); sys.exit(1 if fail else 0)
