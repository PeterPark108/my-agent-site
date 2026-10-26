#!/usr/bin/env python3
"""Quản lý đơn cho trang Tra cứu tiến độ (python3 stdlib).
data/orders.json (public, commit): chỉ hash mã đơn + tiến độ. KHÔNG có thông tin cá nhân.
data/private/orders-map.json (private, gitignore): hash -> nhãn khách. KHÔNG commit.
  add    [--label NHÃN] [--code MÃ]        tạo đơn, in mã MỘT lần
  update MÃ|--label NHÃN [--step 1-5] [--percent N] [--status "..."] [--note "..."] [--date YYYY-MM-DD]
  list
  remove MÃ|--label NHÃN
"""
import argparse,hashlib,json,secrets,sys,datetime,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
PUB=R/'data/orders.json'; PRIV=R/'data/private/orders-map.json'
STEPS=['Tiếp nhận','Lên kế hoạch – thiết kế','Thực hiện','Duyệt','Bàn giao']
ALPHA='23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
HIST_MAX=8
def norm(c): return ''.join(c.split()).upper()
def load(p,d):
  return json.loads(p.read_text()) if p.exists() else d
def save(p,o):
  p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=1)+'\n')
def db():
  d=load(PUB,None)
  if d is None: d={'v':1,'salt':secrets.token_hex(16),'orders':{}}
  return d
def h(d,code): return hashlib.sha256((d['salt']+norm(code)).encode()).hexdigest()
def today(): return datetime.date.today().isoformat()
def steps_for(cur,done=False): return ['done' if i<cur or done else 'current' if i==cur else 'pending' for i in range(1,6)]
def find(d,m,a):
  if a.code: k=h(d,a.code)
  elif a.label:
    ks=[k for k,v in m.items() if v.get('label')==a.label]
    if len(ks)!=1: sys.exit(f'Nhãn "{a.label}": tìm thấy {len(ks)} đơn (cần đúng 1).')
    k=ks[0]
  else: sys.exit('Cần MÃ hoặc --label')
  if k not in d['orders']: sys.exit('Không tìm thấy đơn.')
  return k
def main():
  ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
  sp=ap.add_subparsers(dest='cmd',required=True)
  x=sp.add_parser('add'); x.add_argument('--label',default=''); x.add_argument('--code',help='tự đặt mã (vd đơn demo)')
  x.add_argument('--status',default='Đã tiếp nhận yêu cầu'); x.add_argument('--note',default='Đã tiếp nhận đơn hàng.')
  for n in ('update','remove'):
    x=sp.add_parser(n); x.add_argument('code',nargs='?'); x.add_argument('--label')
    if n=='update':
      x.add_argument('--step',type=int,choices=range(1,6)); x.add_argument('--percent',type=int)
      x.add_argument('--status'); x.add_argument('--note'); x.add_argument('--date'); x.add_argument('--done',action='store_true',help='đánh dấu hoàn tất (100%)')
  sp.add_parser('list')
  a=ap.parse_args(); d=db(); m=load(PRIV,{})
  if a.cmd=='add':
    ym=datetime.date.today().strftime('%y%m')
    code=norm(a.code) if a.code else f'MA-{ym}-'+''.join(secrets.choice(ALPHA) for _ in range(8))
    k=h(d,code)
    if k in d['orders']: sys.exit('Mã đã tồn tại.')
    t=today()
    d['orders'][k]={'step':1,'steps':steps_for(1),'percent':5,'status':a.status,'updated':t,'note':a.note,'history':[{'d':t,'n':a.note}]}
    m[k]={'label':a.label,'created':t}
    save(PUB,d); save(PRIV,m)
    print(code); print(f'Link: https://myagentvn.com/tra-cuu-tien-do.html?ma={code}',file=sys.stderr)
    print('Lưu mã này ngay: script không lưu mã gốc.',file=sys.stderr)
  elif a.cmd=='update':
    k=find(d,m,a); o=d['orders'][k]; t=a.date or today()
    if a.done: a.step=5; a.percent=100
    if a.step: o['step']=a.step
    o['steps']=steps_for(o['step'],a.done or o.get('percent')==100 and not a.step)
    if a.percent is not None: o['percent']=max(0,min(100,a.percent))
    if o['percent']==100: o['steps']=steps_for(5,True)
    if a.status: o['status']=a.status
    o['updated']=t
    if a.note:
      o['note']=a.note; o['history'].insert(0,{'d':t,'n':a.note}); o['history']=o['history'][:HIST_MAX]
    save(PUB,d); print('Đã cập nhật', k[:10], f"bước {o['step']} · {o['percent']}%")
  elif a.cmd=='remove':
    k=find(d,m,a); d['orders'].pop(k); m.pop(k,None); save(PUB,d); save(PRIV,m); print('Đã xoá',k[:10])
  else:
    print(f"{'HASH':12} {'NHÃN':24} {'BƯỚC':26} {'%':>4}  CẬP NHẬT")
    for k,o in d['orders'].items():
      print(f"{k[:10]:12} {m.get(k,{}).get('label','?')[:24]:24} {o['step']}. {STEPS[o['step']-1][:22]:23} {o['percent']:>4}  {o['updated']}")
if __name__=='__main__': main()
