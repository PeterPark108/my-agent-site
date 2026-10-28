#!/usr/bin/env python3
"""Kiểm tra nút "Đăng ký" gói trên trang dịch vụ/combo -> lien-he.html điền sẵn (js/lien-he-prefill.js).
  python3 scripts/test_package_prefill.py   (tự chạy máy chủ tĩnh; /api/contact giả lập, không gửi tin thật)
Ca: mọi gói của mọi dịch vụ (bấm nút thật), gói/dịch vụ không tồn tại, tham số HTML/độc hại, quá dài, dịch vụ thương lượng,
chu kỳ tháng/năm (+ky), combo, ưu tiên luồng tam-tinh, gửi đúng field page+message, giá chỉ từ pricing.json, không từ ngữ cấm.
Tuỳ chọn: SHOT=/thu-muc -> pkg-prefill-desktop.png, pkg-prefill-mobile.png"""
import sys,os,json,re,threading,functools,http.server,socketserver,pathlib,urllib.parse
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent; sys.path.insert(0,str(ROOT/'scripts'))
from svc_pricing import rng
P=json.loads((ROOT/'data/pricing.json').read_text())
class Q(http.server.SimpleHTTPRequestHandler):
  def log_message(self,*a): pass
srv=socketserver.ThreadingTCPServer(('127.0.0.1',0),functools.partial(Q,directory=str(ROOT))); srv.daemon_threads=True
threading.Thread(target=srv.serve_forever,daemon=True).start(); B=f'http://127.0.0.1:{srv.server_address[1]}/'
fail=[]; SHOT=os.environ.get('SHOT'); N=[0]
def chk(c,m):
  N[0]+=1
  if not c: fail.append(m)
BAN=re.compile(r'24/7|24h|24 giờ|cam kết',re.I)
def page(b,vp=(1280,900)):
  pg=b.new_page(viewport={'width':vp[0],'height':vp[1]}); pg.route(__import__('re').compile(r'https://([a-z0-9-]+\.)*(googletagmanager|google-analytics)\.com/'),lambda r:r.abort()); pg._err=[]; pg._post=[]; pg._dlg=[]
  pg.on('pageerror',lambda e:pg._err.append(str(e))); pg.on('dialog',lambda d:(pg._dlg.append(d.message),d.dismiss()))
  pg.route('**/api/contact',lambda r:(pg._post.append(r.request.post_data),r.fulfill(status=200,content_type='application/json',body='{"ok":true}')))
  pg.route('https://**',lambda r:r.abort())
  return pg
def st(pg):
  pg.wait_for_timeout(250)
  return pg.evaluate("()=>{const f=document.querySelector('form[data-contact]');return{svc:f.service.value,msg:f.message.value,pre:f.getAttribute('data-prefill'),inj:document.querySelectorAll('img[src=x],script[data-x],#pwn').length}}")
def go(pg,qs): pg.goto(B+'lien-he.html'+qs,wait_until='domcontentloaded'); return st(pg)
with sync_playwright() as p:
  b=p.chromium.launch(); DEF=None
  # 1) mọi gói: bấm nút Đăng ký thật trên trang dịch vụ
  pg=page(b)
  for s in P['services']:
    for i,t in enumerate(s['tiers']):
      pg.goto(B+f'dich-vu/{s["id"]}.html',wait_until='domcontentloaded')
      a=pg.locator('.plans[data-src=pricing] .plan a',has_text='Đăng ký').nth(i)
      chk(a.count()==1,f'{s["id"]}: thiếu nút Đăng ký gói {i}')
      a.click(); pg.wait_for_url('**/lien-he.html?*'); x=st(pg); c=f'{s["id"]}/{t["id"]}'
      chk(x['pre']==s['id'],f'{c}: không điền sẵn'); chk(x['svc'] and x['svc']!='Thiết kế website' or s['id']=='thiet-ke-website',f'{c}: chưa chọn đúng dịch vụ ({x["svc"]})')
      chk(f'Tôi muốn đăng ký gói {t["name"]} của dịch vụ {s["name"]}.' in x['msg'],f'{c}: nội dung thiếu tên gói/dịch vụ')
      want='Thương lượng' if s.get('negotiable') else rng(t['min'],t['max'])+' / '+s['unit']+' (đã gồm VAT, tham khảo)'
      chk('Giá tham khảo: '+want+'.' in x['msg'],f'{c}: giá sai, cần "{want}" -> {x["msg"]!r}')
      if s.get('billing')=='monthly': chk('Chu kỳ: theo tháng' in x['msg'],f'{c}: thiếu chu kỳ tháng')
      elif s.get('billing')=='yearly': chk('Chu kỳ: theo năm' in x['msg'],f'{c}: thiếu chu kỳ năm')
      else: chk('Chu kỳ' not in x['msg'],f'{c}: dịch vụ một lần không được có chu kỳ')
      chk(x['msg'].rstrip().endswith('Nhu cầu cụ thể:'),f'{c}: thiếu "Nhu cầu cụ thể:"'); chk(not BAN.search(x['msg']),f'{c}: có từ ngữ bị cấm')
      chk(pg.evaluate("()=>{const r=document.getElementById('form').getBoundingClientRect();return r.top<innerHeight&&r.bottom>0}"),f'{c}: chưa cuộn tới form')
  # chọn đúng option cho từng dịch vụ
  EXP={'hosting-seo':'Hosting SEO','quang-cao-google-facebook':'ADS Google, Facebook','phan-tich-du-lieu':'Data Analyst','ky-thuat-du-lieu':'Data Engineer','phan-mem-noi-bo':'Phần mềm nội bộ Agency','thiet-ke-app':'Thiết kế App','video-ai':'Edit Video - Video AI','bo-cong-thuong':'Đăng ký Bộ Công Thương'}
  for s in P['services']:
    x=go(pg,f'?goi-dv={s["id"]}&goi={s["tiers"][0]["id"]}'); chk(x['svc']==EXP.get(s['id'],s['name']),f'{s["id"]}: option {x["svc"]!r}')
  # v0.9.8: link cũ goi=web-app -> Phần mềm nội bộ gói tiêu chuẩn
  _s=[s for s in P['services'] if s['id']=='phan-mem-noi-bo'][0]; _t=[t for t in _s['tiers'] if t['id']=='tieu-chuan'][0]
  for qs in ('?goi-dv=thiet-ke-website&goi=web-app#form','?goi=web-app'):
    x=go(pg,qs); chk(x['pre']=='phan-mem-noi-bo' and x['svc']=='Phần mềm nội bộ Agency',f'web-app cũ {qs}: không chuyển sang phần mềm nội bộ ({x})')
    chk(f'gói {_t["name"]} của dịch vụ {_s["name"]}' in x['msg'] and rng(_t['min'],_t['max']) in x['msg'] and '20–48' not in x['msg'],f'web-app cũ {qs}: nội dung sai {x["msg"]!r}')
  base=go(pg,'')
  # 2) tham số xấu -> bỏ qua
  BAD={'gói không tồn tại':'?goi-dv=thiet-ke-website&goi=khong-co','dịch vụ không tồn tại':'?goi-dv=khong-co&goi=landing',
       'HTML trong goi':'?goi-dv=thiet-ke-website&goi='+urllib.parse.quote('<img src=x onerror=alert(1)>'),
       'HTML trong goi-dv':'?goi-dv='+urllib.parse.quote('"><script data-x>alert(1)</script>')+'&goi=landing',
       'quá dài':'?goi-dv=thiet-ke-website&goi='+'a'*41,'path traversal':'?goi-dv=..%2F..%2Fetc&goi=landing',
       'combo không tồn tại':'?combo='+urllib.parse.quote('<b id=pwn>x</b>'),'chỉ có goi':'?goi=landing'}
  for c,qs in BAD.items():
    x=go(pg,qs); chk(x['pre'] is None and x['msg']=='' and x['svc']==base['svc'] and x['inj']==0,f'{c}: không được điền ({x})')
  # 3) chu kỳ ky, combo, ưu tiên tam-tinh
  x=go(pg,'?goi-dv=seo-tong-the&goi=tieu-chuan&ky=12'); chk('đăng ký 12 tháng' in x['msg'],'ky=12 tháng')
  x=go(pg,'?goi-dv=seo-tong-the&goi=tieu-chuan&ky=7'); chk('đăng ký' not in x['msg'].split('Chu kỳ')[1].split('\n')[0],'ky=7 phải bỏ qua')
  x=go(pg,'?goi-dv=ten-mien&goi=vn&ky=2'); chk('đăng ký 2 năm' in x['msg'],'ky=2 năm')
  x=go(pg,'?goi-dv=hosting-seo&goi=nang-cao'); chk('Giá tham khảo: Thương lượng.' in x['msg'] and 'triệu' not in x['msg'],'hosting thương lượng')
  x=go(pg,'?combo=tang-truong'); chk(x['svc']=='Combo Tăng trưởng' and 'Combo Tăng trưởng' in x['msg'],f'combo: {x}')
  x=go(pg,'?tam-tinh=12.000.000%C4%91&dich-vu=SEO&goi-dv=thiet-ke-website&goi=landing'); chk('công cụ tính giá' in x['msg'] and 'Landing' not in x['msg'],'tam-tinh phải được ưu tiên')
  chk(not pg._err and not pg._dlg,f'lỗi JS/dialog: {pg._err} {pg._dlg}'); pg.close()
  # 4) gửi: field page + message đúng (giả lập /api/contact), ảnh desktop/mobile
  for vp,tag in [((1280,900),'desktop'),((390,844),'mobile')]:
    pg=page(b,vp); pg.goto(B+'dich-vu/cham-soc-fanpage.html',wait_until='domcontentloaded')
    pg.locator('.plans[data-src=pricing] .plan a',has_text='Đăng ký').nth(1).click(); pg.wait_for_url('**/lien-he.html?*'); st(pg)
    if SHOT: pg.locator('#form').scroll_into_view_if_needed(); pg.wait_for_timeout(600); pg.screenshot(path=os.path.join(SHOT,f'pkg-prefill-{tag}.png'))
    pg.fill('#form [name=name]','Nguyễn Văn Test'); pg.fill('#form [name=phone]','0328 439 972'); pg.fill('#form [name=email]','khach@vidu.vn'); pg.check('#form [name=consent]')
    pg.locator('#form textarea[name=message]').press('End'); pg.keyboard.type(' 3 bài/tuần')
    pg.click('#form button[type=submit]'); pg.wait_for_timeout(1200)
    chk(len(pg._post)==1,f'{tag}: số request {len(pg._post)}')
    if pg._post:
      d=pg._post[0]; 
      try: d=json.loads(d)
      except Exception: d=dict(urllib.parse.parse_qsl(d))
      chk('goi-dv=cham-soc-fanpage' in d.get('page','') and 'Chăm sóc Fanpage' in d.get('message','') and '3 bài/tuần' in d.get('message',''),f'{tag}: field gửi sai {d}')
    chk(not pg._err,f'{tag}: lỗi JS {pg._err}'); pg.close()
  b.close()
# 5) giá không hard-code trong JS
js=(ROOT/'js/lien-he-prefill.js').read_text(); chk(not re.search(r'\d{6,}|triệu đồng',js),'js có giá hard-code'); chk(not BAN.search(js),'js có từ ngữ cấm')
if fail: print('FAIL:',len(fail),'lỗi'); [print(' -',x) for x in fail]; sys.exit(1)
print(f'OK: test_package_prefill đạt ({N[0]} kiểm tra)')
