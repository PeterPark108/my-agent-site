#!/usr/bin/env python3
"""Kiểm tra form liên hệ (lien-he.html) bằng Chromium/Playwright, giả lập máy chủ nhận form:
  python3 scripts/test_contact_form.py            # tự chạy máy chủ tĩnh tạm
  python3 scripts/test_contact_form.py http://127.0.0.1:8947/
Trường hợp: thành công (200 {success:"true"}), timeout, lỗi mạng, HTTP 500, success:false, formEndpoint (JSON),
khung dự phòng mailto/Zalo/tel, nút bật lại, dữ liệu giữ nguyên, chống gửi trùng, điền sẵn từ công cụ tính giá.
Tuỳ chọn: SHOT=/thu-muc -> lưu ảnh khung dự phòng desktop/mobile."""
import sys,os,json,threading,functools,http.server,socketserver,pathlib,urllib.parse
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent
if len(sys.argv)>1: B=sys.argv[1].rstrip('/')+'/'
else:
  class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
  h=functools.partial(Q,directory=str(ROOT))
  srv=socketserver.TCPServer(('127.0.0.1',0),h); threading.Thread(target=srv.serve_forever,daemon=True).start()
  B=f'http://127.0.0.1:{srv.server_address[1]}/'
fail=[]; SHOT=os.environ.get('SHOT')
def chk(c,m):
  if not c: fail.append(m)
FIELDS={'name':'Nguyễn Văn Test','phone':'+84 328 439 972','email':'khach@vidu.vn','message':'Cần làm website bán hàng\ncó giỏ hàng'}
def run(b,case,mode,vp=(1280,900),cfg=None,url='lien-he.html'):
  pg=b.new_page(viewport={'width':vp[0],'height':vp[1]}); err=[]; pg.on('pageerror',lambda e:err.append(str(e))); hits=[]
  over=dict({'formTimeoutMs':1500},**(cfg or {}))
  pg.route('**/js/config.js*',lambda r:r.fulfill(status=200,content_type='application/javascript',body=(ROOT/'js/config.js').read_text()+'\nObject.assign(window.MYAGENT_CONFIG,'+json.dumps(over)+');'))
  def h(r):
    hits.append(r.request)
    if mode=='ok': r.fulfill(status=200,content_type='application/json',body='{"success":"true","message":"The form was submitted successfully."}')
    elif mode=='okjson': r.fulfill(status=200,content_type='application/json',body='{"ok":true}')
    elif mode=='500': r.fulfill(status=500,content_type='text/html',body='Server Error')
    elif mode=='false': r.fulfill(status=200,content_type='application/json',body='{"success":"false","message":"error"}')
    elif mode=='neterr': r.abort('failed')
    elif mode=='hang': pass
  pg.route('https://formsubmit.co/**',h); pg.route('**/api/contact',h)
  pg.route('https://www.googletagmanager.com/**',lambda r:r.abort())
  pg.goto(B+url,wait_until='domcontentloaded'); pg.wait_for_timeout(300)
  f='form[data-contact]'
  for k,v in FIELDS.items():
    if 'tam-tinh' in url and k=='message': continue
    pg.fill(f+f' [name={k}]',v)
  pg.select_option(f+' [name=service]','Thiết kế website'); pg.check(f+' [name=consent]')
  pg.evaluate("()=>{const f=document.querySelector('form[data-contact]');f.requestSubmit();f.requestSubmit();f.requestSubmit()}")
  res={'err':err,'pg':pg}
  if mode in('ok','okjson'):
    pg.wait_for_selector(f+' h3:has-text("Cảm ơn")',timeout=5000); res['done']=True
  else:
    pg.wait_for_selector('.form-status.fb',timeout=8000)
    res.update(pg.evaluate("""()=>{const f=document.querySelector('form[data-contact]'),q=s=>f.querySelector(s);
      return {btn:q('button[type=submit]').disabled,status:q('.form-status').innerText,
        mailto:(q('[data-fb=mailto]')||{}).href||'',zalo:(q('[data-fb=zalo]')||{}).href||'',tel:(q('[data-fb=tel]')||{}).href||'',
        vals:Object.fromEntries(['name','phone','email','message','service'].map(n=>[n,f.elements[n].value])),hs:document.documentElement.scrollWidth-innerWidth}}"""))
  pg.wait_for_timeout(200); res['hits']=len(hits)
  if res['hits']!=1: fail.append(f'{case}: gửi {res["hits"]} lần (phải đúng 1, chống gửi trùng)')
  if err: fail.append(f'{case}: lỗi JS {err}')
  return res
def fb_ok(case,r,cfg_email='vantungn044@gmail.com'):
  chk(r['btn'] is False,f'{case}: nút gửi chưa được bật lại')
  chk(r['mailto'].startswith('mailto:'+cfg_email),f'{case}: thiếu nút mailto ({r["mailto"][:60]})')
  chk(r['zalo']=='https://zalo.me/0328439972',f'{case}: thiếu link Zalo')
  chk(r['tel'].startswith('tel:0328439972'),f'{case}: thiếu link Gọi ngay')
  for k,v in FIELDS.items(): chk(r['vals'][k]==v,f'{case}: mất dữ liệu ô {k}')
  chk('giữ nguyên' in r['status'],f'{case}: thông báo dự phòng chưa đúng')
  chk(r['hs']<=0,f'{case}: cuộn ngang')
  q=urllib.parse.parse_qs(urllib.parse.urlparse(r['mailto']).query); body=q.get('body',[''])[0]
  chk('Yêu cầu tư vấn' in q.get('subject',[''])[0],f'{case}: mailto thiếu tiêu đề')
  for want in ['Họ tên: Nguyễn Văn Test','SĐT: +84 328 439 972','Email: khach@vidu.vn','Dịch vụ: Thiết kế website','Cần làm website bán hàng\ncó giỏ hàng']:
    chk(want in body,f'{case}: mailto thiếu "{want}"')
def close(r):
  r['pg'].unroute_all(behavior='ignoreErrors'); r['pg'].close()
def shot(r,n):
  pg=r['pg']; pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
  pg.locator('.form-status').scroll_into_view_if_needed(); pg.evaluate('scrollBy(0,180)'); pg.wait_for_timeout(500); pg.screenshot(path=os.path.join(SHOT,n))
with sync_playwright() as p:
  b=p.chromium.launch()
  r=run(b,'success','ok'); close(r)
  r=run(b,'success-endpoint','okjson',cfg={'formEndpoint':'/api/contact'}); close(r)
  for case,mode in [('timeout','hang'),('network-error','neterr'),('http-500','500'),('success-false','false')]:
    r=run(b,case,mode); fb_ok(case,r)
    if case=='timeout': chk('quá lâu' in r['status'],'timeout: thiếu thông báo phản hồi quá lâu')
    if case=='timeout' and SHOT: shot(r,'form-fallback-desktop.png')
    close(r)
  r=run(b,'endpoint-500','500',cfg={'formEndpoint':'/api/contact'}); fb_ok('endpoint-500',r); close(r)
  r=run(b,'mobile-timeout','hang',vp=(390,844)); fb_ok('mobile-timeout',r)
  if SHOT: shot(r,'form-fallback-mobile.png')
  close(r)
  r=run(b,'prefill','neterr',url='lien-he.html?tam-tinh=7.200.000%C4%91&dich-vu=Thi%E1%BA%BFt+k%E1%BA%BF+website')
  body=urllib.parse.unquote(r['mailto'])
  chk('Tạm tính: 7.200.000đ' in body,'prefill: mailto thiếu số liệu công cụ tính giá'); close(r)
  b.close()
fail=[x for x in fail if x]
for f in fail: print('FAIL:',f)
print('OK: test_contact_form đạt (9 trường hợp)' if not fail else f'{len(fail)} lỗi'); sys.exit(1 if fail else 0)
