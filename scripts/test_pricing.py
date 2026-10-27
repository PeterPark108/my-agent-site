#!/usr/bin/env python3
"""Kiểm tra Bảng giá công khai (stdlib + node nếu có). Chạy: python3 scripts/test_pricing.py
Chặn: Traffic User, sheet/ghi chú nội bộ, nguồn tham khảo, câu định vị giá so với thị trường, giá vốn, file .xlsx;
bắt buộc có câu VAT + tham khảo + ghi chú quảng cáo; kiểm thử hàm tính (gồm khoản Thương lượng không cộng vào tổng)."""
import json,re,subprocess,pathlib,shutil,sys,os
R=pathlib.Path(__file__).resolve().parent.parent; os.chdir(R)
fail=[]; ok=lambda c,m: c or fail.append(m)
files=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard'],capture_output=True,text=True).stdout.split()
ok(not [f for f in files if f.lower().endswith(('.xlsx','.xls','.ods','.csv')) and 'gia' in f.lower() or f.lower().endswith(('.xlsx','.xls'))],'có file bảng tính (.xlsx/.xls) trong repo')
FORB=re.compile(r'so với thị trường|rẻ hơn thị trường|trung vị thị trường|% trung vị|thị trường \d|giá vốn|biên lợi nhuận|Nội bộ - không công khai|ước tính nội bộ|×\s?0,8',re.I)
SHIP=[f for f in files if f.endswith(('.html','.js','.json','.xml','.txt','.webmanifest')) and not f.startswith(('scripts/','docs/'))]
for f in SHIP:
  t=pathlib.Path(f).read_text(errors='ignore'); m=FORB.search(t)
  ok(not m,f'{f}: chứa nội dung không công khai "{m.group(0) if m else ""}"')
# dữ liệu công khai
P=json.loads(pathlib.Path('data/pricing.json').read_text()); raw=json.dumps(P,ensure_ascii=False)
ok(not re.search(r'traffic',raw,re.I),'data/pricing.json có Traffic User')
for k in ('positioning','sources','formula','cost','margin','internal'): ok(k not in raw,f'data/pricing.json có trường "{k}"')
ok(len(P['services'])==17,'số dịch vụ công khai khác 17')
ok(P.get('vatIncluded') is True,'thiếu vatIncluded')
for s in P['services']:
  ok(set(s)<= {'id','category','name','unit','billing','quantity','complexityApplies','discountable','negotiable','priceLabel','negotiableNote','tiers'},f'{s["id"]}: trường lạ {set(s)}')
  for t in s['tiers']:
    if s.get('negotiable'): ok('min' not in t and 'max' not in t,f'{s["id"]}: thương lượng nhưng có giá')
    else: ok(0<t['min']<=t['max'],f'{s["id"]}/{t["id"]}: khoảng giá sai')
neg={s['id'] for s in P['services'] if s.get('negotiable')}
ok(neg>={'hosting-seo','quang-cao-google-facebook'},'hosting/quảng cáo phải là Thương lượng')
for f in ('js/combo-calculator.js','js/bang-gia.js','js/lien-he-prefill.js'):
  ok(not re.search(r'traffic',pathlib.Path(f).read_text(),re.I),f+' có Traffic')
# trang
s=pathlib.Path('bang-gia.html').read_text(); main=re.search(r'<main\b.*?</main>',s,re.S).group(0)
for need in ('Giá đã bao gồm VAT','Giá chỉ mang tính tham khảo theo khoảng, báo giá chính xác sau khi trao đổi nhu cầu','chưa gồm tiền quảng cáo trả cho nền tảng','Thương lượng','id="tinh-gia"','Gửi số liệu sang liên hệ'):
  ok(need in main,'bang-gia.html thiếu: '+need)
ok(not re.search(r'traffic',main,re.I),'bang-gia.html (main) có Traffic User')
ok(not re.search(r'24/7|24h\b|24 giờ|cam kết (lên )?top|đảm bảo (lên )?top|top 1|fpt poly',main,re.I),'bang-gia.html có từ cấm')
for svc in neg:
  card=re.search(rf'id="gia-{svc}".*?</article>',main,re.S).group(0)
  ok(not re.search(r'\d\s*(triệu|nghìn)',card),f'{svc}: bảng giá phải ghi Thương lượng, không có số')
idx=pathlib.Path('index.html').read_text()
ok('<a href="combo.html">Combo</a></li><li class=""><a href="bang-gia.html">Bảng giá</a></li><li class=""><a href="du-an.html">' in idx,'menu: Bảng giá phải nằm giữa Combo và Dự án')
ok('https://myagentvn.com/bang-gia.html' in pathlib.Path('sitemap.xml').read_text(),'sitemap thiếu bang-gia.html')
ok('bang-gia.html#tinh-gia' in pathlib.Path('combo.html').read_text(),'combo.html thiếu nút Tự tính giá')
ok('js/lien-he-prefill.js' in pathlib.Path('lien-he.html').read_text(),'lien-he.html thiếu script điền sẵn')
# đồng bộ giá các trang cũ (v0.9.1): trang dịch vụ khớp pricing.json, không còn giá cũ / cam kết 24 giờ
sys.path.insert(0,str(R/'scripts')); import svc_pricing as SP
for sv in P['services']:
  pg=pathlib.Path(f'dich-vu/{sv["id"]}.html').read_text()
  blk=re.search(r'<div class="plans" data-src="pricing">.*?</p>',pg,re.S)
  ok(blk,f'dich-vu/{sv["id"]}.html: bảng giá chưa sinh từ pricing.json (chạy scripts/svc_pricing.py)')
  if not blk: continue
  blk=blk.group(0)
  ok('Giá đã bao gồm VAT' in blk,f'dich-vu/{sv["id"]}.html: thiếu "Giá đã bao gồm VAT"')
  for t in sv['tiers']:
    ok(t['name'].replace('&','&amp;') in blk or t['name'] in blk,f'{sv["id"]}: thiếu mức "{t["name"]}"')
    if sv.get('negotiable'): ok('Thương lượng' in blk and not re.search(r'\d\s*(triệu|nghìn)<small>',blk),f'{sv["id"]}: phải ghi Thương lượng')
    else: ok(SP.rng(t['min'],t['max']) in blk,f'{sv["id"]}/{t["id"]}: giá trang khác pricing.json ({SP.rng(t["min"],t["max"])})')
OLD=re.compile(r'1,5\s*[–-]\s*4\s*triệu|(?<![\d,])4\s*[–-]\s*10\s*triệu|8\s*[–-]\s*20\s*triệu\s*(?:<small>)?\s*/\s*gói|Gói Doanh nghiệp\W{0,6}\s*8\s*[–-]\s*20|(?<![\d,])300\s*(?:nghìn|ngàn|k\b)|(?<![\d,])600\s*(?:nghìn|ngàn|k\b)|(?<![\d,–-])1\s*triệu\s*(?:<small>)?\s*/\s*tháng',re.I)
C24=re.compile(r'(?<![\d/])24\s*giờ|(?<![\d/])24h\b|24/7|24/24',re.I)
PUB=[f for f in files if f.endswith(('.html','.js','.json','.xml','.md','.txt')) and not f.startswith(('scripts/','docs/','node_modules/')) and f not in ('CHANGELOG.md','README.md')]
for f in PUB:
  t=pathlib.Path(f).read_text(errors='ignore')
  if f.startswith('js/chat'): t=re.sub(r'/[^/\n]{0,200}24[^/\n]{0,80}/[gimsuy]*','',t)  # bỏ qua regex chặn từ cấm trong mã chatbot
  m=OLD.search(t); ok(not m,f'{f}: còn giá cũ "{m.group(0) if m else ""}" (không khớp data/pricing.json)')
  m=C24.search(t); ok(not m,f'{f}: còn cam kết thời gian "{m.group(0) if m else ""}" (không dùng 24 giờ/24h/24/7)')
# điều khoản thanh toán theo loại tính phí + ghi chú tên miền/hosting mới (v0.9.1)
for sv in P['services']:
  pg=pathlib.Path(f'dich-vu/{sv["id"]}.html').read_text()
  blk=re.search(r'<p class="muted rv" style="margin-top:18px"><small>(.*?)</small>',pg,re.S); blk=blk.group(1) if blk else ''
  if SP.is_recurring(sv):
    ok(not re.search(r'đặt cọc 30|30\s*[–-]\s*50\s*%',pg,re.I),f'{sv["id"]} (tính theo kỳ): không được có đặt cọc 30–50%')
    ok('thanh toán 100% trước' in blk,f'{sv["id"]} (tính theo kỳ): thiếu "thanh toán 100% trước"')
  else:
    for need in ('Đặt cọc 30–50%','60 ngày','2 lần chỉnh sửa'): ok(need in blk,f'{sv["id"]} (làm một lần): thiếu điều khoản "{need}"')
  ok('tên miền có giá riêng' in blk and 'Thương lượng' in blk,f'{sv["id"]}: thiếu ghi chú tên miền/hosting/quảng cáo mới')
OLDNOTE=re.compile(r'chưa gồm phí tên miền, hosting|chưa gồm\*\* phí tên miền, hosting|khách đứng tên và thanh toán trực tiếp cho nhà cung cấp|anh/chị đứng tên và thanh toán trực tiếp|Phí của nhà cung cấp do anh/chị thanh toán trực tiếp',re.I)
for f in PUB:
  t=pathlib.Path(f).read_text(errors='ignore'); m=OLDNOTE.search(t)
  ok(not m,f'{f}: còn ghi chú cũ "{m.group(0) if m else ""}"')
# hàm tính
if shutil.which('node'):
  js=r'''
const fs=require('fs'),a=require('assert');global.window=undefined;
const {calculateCombo:c,setPricing}=require('./js/combo-calculator.js');const P=JSON.parse(fs.readFileSync('data/pricing.json','utf8'));setPricing(P);
const I=(s,t,x={})=>Object.assign({serviceId:s,tierId:t},x);
let r=c({items:[I('thiet-ke-website','gioi-thieu')]});a.strictEqual(r.min,4e6);a.strictEqual(r.max,7.2e6);
r=c({items:[I('thiet-ke-website','gioi-thieu'),I('google-maps','co-ban')]});a.strictEqual(r.discountPercent,5);a.strictEqual(r.min,Math.floor((4e6+0.8e6)*0.95/1e5)*1e5);
r=c({items:[I('hosting-seo','co-ban')]});a.strictEqual(r.min,0);a.strictEqual(r.max,0);a.strictEqual(r.negotiable.length,1);
r=c({items:[I('quang-cao-google-facebook','co-ban',{budgetNote:'20 triệu'})],prepay:'12m'});a.strictEqual(r.max,0);a.strictEqual(r.negotiable[0].budgetNote,'20 triệu');
const w=c({items:[I('seo-tong-the','co-ban')],prepay:'24m'});a.strictEqual(w.prepayPercent,15);a.strictEqual(w.items[0].multiplier,24);
r=c({items:[I('seo-tong-the','co-ban'),I('hosting-seo','co-ban')],prepay:'6m'});a.strictEqual(r.min,w.items[0].min*0+Math.floor(2.8e6*6*0.95/1e5)*1e5);
r=c({items:[I('ten-mien','com')],prepay:'24m'});a.strictEqual(r.items[0].multiplier,2);a.strictEqual(r.items[0].linePercent,15);
r=c({items:[{serviceId:'traffic-user',tierId:'co-ban'}]});a.strictEqual(r.max,0);
// đối chiếu với demo nguồn (nếu có): cùng tổng cho mọi kịch bản ngẫu nhiên
const SRC=process.env.PRICING_SRC;let n=0;
if(SRC&&fs.existsSync(SRC+'/pricing.json')){const S=JSON.parse(fs.readFileSync(SRC+'/pricing.json','utf8'));
 const vm=require('vm'),ctx={window:{}};vm.createContext(ctx);vm.runInContext(fs.readFileSync(SRC+'/combo-calculator.js','utf8'),ctx);
 for(let i=0;i<500;i++){const its=P.services.filter(()=>Math.random()<.35).map(s=>I(s.id,s.tiers[i%s.tiers.length].id,{complexity:['don-gian','tieu-chuan','phuc-tap'][i%3],quantity:i%7}));
  const sel={items:its,rush:['binh-thuong','gap','rat-gap'][i%3],prepay:['monthly','6m','12m','24m'][i%4]};
  const x=c(sel),y=ctx.window.calculateCombo(sel,S);a.strictEqual(x.min,y.min);a.strictEqual(x.max,y.max);a.strictEqual(x.negotiable.length,y.negotiable.length);n++}}
console.log('calc OK, đối chiếu nguồn:',n);'''
  r=subprocess.run(['node','-e',js],capture_output=True,text=True,env=dict(os.environ,PRICING_SRC=os.environ.get('PRICING_SRC','/workspace/bang-gia')))
  print(r.stdout.strip()); ok(r.returncode==0,'hàm tính sai: '+r.stderr.strip()[-600:])
else: print('(bỏ qua kiểm thử JS: không có node)')
print('\n'.join('FAIL: '+f for f in fail) or 'OK: test_pricing đạt')
sys.exit(1 if fail else 0)
