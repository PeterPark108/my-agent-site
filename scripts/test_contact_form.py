#!/usr/bin/env python3
"""Kiểm tra form liên hệ (lien-he.html) bằng Chromium/Playwright, giả lập máy chủ nhận form:
  python3 scripts/test_contact_form.py            # tự chạy máy chủ tĩnh tạm
  python3 scripts/test_contact_form.py http://127.0.0.1:8947/
Mặc định formEndpoint=/api/contact (chỉ JSON {ok:true} mới là thành công), FormSubmit tắt, timeout 5s thật.
Trường hợp: thành công, timeout 5s, 404 HTML, 405, 200 HTML, 200 JSON ok:false, 500, lỗi mạng, FormSubmit tuỳ chọn,
khung dự phòng mailto/Zalo/tel, nút bật lại, dữ liệu giữ nguyên, chống gửi trùng, điền sẵn từ công cụ tính giá.
Tuỳ chọn: SHOT=/thu-muc -> lưu ảnh khung dự phòng desktop/mobile."""
import sys,os,json,time,threading,functools,http.server,socketserver,pathlib,urllib.parse
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
  pg=b.new_page(viewport={'width':vp[0],'height':vp[1]}); err=[]; pg.on('pageerror',lambda e:err.append(str(e))); pg.on('console',lambda m:'Pattern attribute' in m.text and err.append(m.text)); hits=[]
  over=dict(cfg or {})
  pg.route('**/js/config.js*',lambda r:r.fulfill(status=200,content_type='application/javascript',body=(ROOT/'js/config.js').read_text()+'\nObject.assign(window.MYAGENT_CONFIG,'+json.dumps(over)+');'))
  def h(r):
    hits.append(r.request)
    if mode in('ok','fsjson'): r.fulfill(status=200,content_type='application/json',body='{"success":"true","message":"The form was submitted successfully."}')
    elif mode=='okjson': r.fulfill(status=200,content_type='application/json',body='{"ok":true}')
    elif mode=='500': r.fulfill(status=500,content_type='text/html',body='Server Error')
    elif mode=='404': r.fulfill(status=404,content_type='text/html',body='<!doctype html><title>404</title>')
    elif mode=='405': r.fulfill(status=405,content_type='text/html',body='<html>405 Not Allowed</html>')
    elif mode=='html200': r.fulfill(status=200,content_type='text/html',body='<!doctype html><html>trang tĩnh</html>')
    elif mode=='okfalse': r.fulfill(status=200,content_type='application/json',body='{"ok":false}')
    elif mode=='false': r.fulfill(status=200,content_type='application/json',body='{"success":"false","message":"error"}')
    elif mode=='neterr': r.abort('failed')
    elif mode=='hang': pass
  fs=[]; pg.route('https://formsubmit.co/**',lambda r:(fs.append(1),h(r))); pg.route('**/api/contact',h)
  pg.route('https://www.googletagmanager.com/**',lambda r:r.abort())
  pg.goto(B+url,wait_until='domcontentloaded'); pg.wait_for_timeout(300)
  f='form[data-contact]'
  if pg.evaluate("()=>{const i=document.querySelector('form[data-contact] [name=phone]');i.value='abc';const v=i.checkValidity();i.value='';return v}"): fail.append(f'{case}: SĐT "abc" vẫn hợp lệ (pattern hỏng)')
  for k,v in FIELDS.items():
    if 'tam-tinh' in url and k=='message': continue
    pg.fill(f+f' [name={k}]',v)
  pg.select_option(f+' [name=service]','Thiết kế website'); pg.check(f+' [name=consent]')
  pg.evaluate("()=>{const f=document.querySelector('form[data-contact]');f.requestSubmit();f.requestSubmit();f.requestSubmit()}")
  t0=time.time(); res={'err':err,'pg':pg}
  if mode in('ok','okjson'):
    pg.wait_for_selector(f+' h3:has-text("Cảm ơn")',timeout=5000); res['done']=True
  else:
    pg.wait_for_selector('.form-status.fb',timeout=8000); res['t']=time.time()-t0
    if res['t']>5.5: fail.append(f'{case}: hiện dự phòng sau {res["t"]:.1f}s (> 5,5s)')
    chk(pg.locator('text=Cảm ơn').count()==0,f'{case}: hiện "Cảm ơn" khi lỗi')
    res.update(pg.evaluate("""()=>{const f=document.querySelector('form[data-contact]'),q=s=>f.querySelector(s);
      return {btn:q('button[type=submit]').disabled,status:q('.form-status').innerText,
        mailto:(q('[data-fb=mailto]')||{}).href||'',zalo:(q('[data-fb=zalo]')||{}).href||'',tel:(q('[data-fb=tel]')||{}).href||'',
        vals:Object.fromEntries(['name','phone','email','message','service'].map(n=>[n,f.elements[n].value])),hs:document.documentElement.scrollWidth-innerWidth}}"""))
  pg.wait_for_timeout(200); res['hits']=len(hits)
  if fs and not (cfg or {}).get('formSubmitEnabled'): fail.append(f'{case}: có request tới formsubmit.co')
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
  pg.evaluate("()=>{const c=document.querySelector('.chat-bubble,.mj-hint');document.querySelectorAll('[class*=chat]').forEach(e=>{if(e.closest('form'))return;e.style.visibility='hidden'})}")
  f=pg.locator('form[data-contact]'); bb=f.bounding_box(); pg.set_viewport_size({'width':pg.viewport_size['width'],'height':int(bb['height'])+140})
  pg.evaluate("()=>{const f=document.querySelector('form[data-contact]');scrollTo(0,f.getBoundingClientRect().top+scrollY-90)}"); pg.wait_for_timeout(500); pg.screenshot(path=os.path.join(SHOT,n))
with sync_playwright() as p:
  b=p.chromium.launch()
  r=run(b,'success-endpoint','okjson'); close(r)
  r=run(b,'formsubmit-optional','ok',cfg={'formEndpoint':'','formSubmitEnabled':True}); close(r)
  r=run(b,'endpoint-success-key-wrong','fsjson')  # {success:"true"} không phải {ok:true} -> phải là lỗi
  fb_ok('endpoint-success-key-wrong',r); close(r)
  for case,mode in [('timeout-5s','hang'),('http-404-html','404'),('http-405','405'),('http-200-html','html200'),('json-ok-false','okfalse'),('http-500','500'),('network-error','neterr')]:
    r=run(b,case,mode); fb_ok(case,r)
    if case=='timeout-5s':
      chk('quá lâu' in r['status'],'timeout: thiếu thông báo phản hồi quá lâu'); chk(r['t']>=4.5,f'timeout: dự phòng quá sớm {r["t"]:.1f}s')
      if SHOT: shot(r,'form-fallback-desktop.png')
    close(r)
  r=run(b,'mobile-404','404',vp=(390,844)); fb_ok('mobile-404',r)
  if SHOT: shot(r,'form-fallback-mobile.png')
  close(r)
  r=run(b,'prefill','neterr',url='lien-he.html?tam-tinh=7.200.000%C4%91&dich-vu=Thi%E1%BA%BFt+k%E1%BA%BF+website')
  body=urllib.parse.unquote(r['mailto'])
  chk('Tạm tính: 7.200.000đ' in body,'prefill: mailto thiếu số liệu công cụ tính giá'); close(r)
  # --- kiểm tra dữ liệu (không gửi request nào) ---
  V={'name':'Nguyễn Văn Test','phone':'0328 439 972','email':'khach@vidu.vn'}
  def vpage(vp=(1280,900)):
    pg=b.new_page(viewport={'width':vp[0],'height':vp[1]}); hits=[]; err=[]
    pg.on('pageerror',lambda e:err.append(str(e))); pg.route('**/api/contact',lambda r:(hits.append(1),r.abort()))
    pg.route('https://formsubmit.co/**',lambda r:(hits.append(1),r.abort()))
    pg.goto(B+'lien-he.html',wait_until='domcontentloaded'); pg.wait_for_timeout(300); return pg,hits,err
  def state(pg): return pg.evaluate("""()=>{const f=document.querySelector('form[data-contact]'),e=f.querySelector('.form-err');
    return {shown:!e.hidden,text:e.innerText,role:e.getAttribute('role'),inv:[...f.elements].filter(x=>x.getAttribute('aria-invalid')=='true').map(x=>x.name),
      red:[...f.querySelectorAll('.inv')].length,focus:document.activeElement&&document.activeElement.name,below:e.getBoundingClientRect().top>=f.querySelector('button[type=submit]').getBoundingClientRect().bottom,
      nv:f.noValidate}}""")
  CASES=[('ho-ten-trong',dict(V,name=''),True,['name'],'họ và tên'),('sdt-sai',dict(V,phone='abc'),True,['phone'],'Số điện thoại chưa đúng'),
         ('email-thieu-@',dict(V,email='khachvidu.vn'),True,['email'],'thiếu ký tự "@"'),('chua-tick',V,False,['consent'],'tick ô đồng ý'),
         ('nhieu-loi',{'name':'','phone':'12','email':'abc'},False,['name','phone','email','consent'],'Chưa gửi được')]
  for case,vals,tick,want,txt in CASES:
    for vp,tag in [((1280,900),''),((390,844),'@390')]:
      pg,hits,err=vpage(vp)
      for k,v in vals.items(): pg.fill(f'form[data-contact] [name={k}]',v)
      if tick: pg.check('form[data-contact] [name=consent]')
      pg.click('form[data-contact] button[type=submit]'); pg.wait_for_timeout(400); s=state(pg); c=case+tag
      chk(s['shown'] and s['role']=='alert' and s['below'],f'{c}: không hiện dòng lỗi role=alert dưới nút gửi')
      chk(sorted(s['inv'])==sorted(want),f'{c}: aria-invalid {s["inv"]} != {want}'); chk(s['red']==len(want),f'{c}: viền đỏ {s["red"]}')
      chk(txt in s['text'],f'{c}: thiếu thông báo "{txt}"'); chk(s['focus']==want[0],f'{c}: focus {s["focus"]} != {want[0]}')
      chk(s['nv'],f'{c}: form chưa novalidate (tooltip gốc)'); chk(not hits,f'{c}: vẫn gửi request khi dữ liệu sai'); chk(not err,f'{c}: lỗi JS {err}')
      chk(pg.evaluate("()=>{const i=document.querySelector('form[data-contact] [name=email]');let p=null;i.addEventListener('invalid',e=>p=e.defaultPrevented);i.value='x';i.reportValidity();return p}"),f'{c}: tooltip gốc chưa bị chặn')
      if case=='nhieu-loi' and SHOT: shot({'pg':pg},'form-validation-'+('mobile' if tag else 'desktop')+'.png')
      pg.unroute_all(behavior='ignoreErrors'); pg.close()
  # sửa ô thì lỗi tắt dần
  pg,hits,err=vpage(); pg.fill('form[data-contact] [name=name]',''); pg.fill('form[data-contact] [name=phone]','12'); pg.fill('form[data-contact] [name=email]','abc')
  pg.click('form[data-contact] button[type=submit]'); pg.wait_for_timeout(300)
  pg.wait_for_timeout(3000); chk(state(pg)['shown'],'lỗi biến mất sớm (sau 3s)')
  pg.fill('form[data-contact] [name=name]','Nguyễn Văn Test'); s=state(pg); chk('name' not in s['inv'] and s['shown'] and 'họ và tên' not in s['text'],'sửa họ tên: lỗi họ tên chưa tắt')
  pg.fill('form[data-contact] [name=phone]','1234'); s=state(pg); chk('phone' in s['inv'],'SĐT vẫn sai mà lỗi đã tắt')
  pg.fill('form[data-contact] [name=phone]','0328 439 972'); pg.fill('form[data-contact] [name=email]','khach@vidu.vn'); pg.check('form[data-contact] [name=consent]')
  s=state(pg); chk(not s['shown'] and not s['inv'] and s['red']==0,f'sửa hết: lỗi chưa tắt {s}')
  pg.unroute_all(behavior='ignoreErrors'); pg.close()
  b.close()
fail=[x for x in fail if x]
for f in fail: print('FAIL:',f)
print('OK: test_contact_form đạt (13 trường hợp gửi + 11 trường hợp kiểm tra dữ liệu)' if not fail else f'{len(fail)} lỗi'); sys.exit(1 if fail else 0)
