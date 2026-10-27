#!/usr/bin/env python3
"""Kiểm tra bố cục bằng Chromium: python3 scripts/test_layout.py http://127.0.0.1:8947/"""
import sys,re,pathlib
from playwright.sync_api import sync_playwright
B=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8947/').rstrip('/')+'/'
fail=[]
css=pathlib.Path(__file__).resolve().parent.parent.joinpath('css/style.css').read_text()
if len(re.findall(r'(?:^|[}\s,])\.bg-grid\s*[{,]',css))!=1: fail.append('style.css: .bg-grid chỉ được định nghĩa một lần (lớp nền cố định)')
PAGES=['bang-gia.html','combo.html','dich-vu/thiet-ke-website.html','dich-vu/cham-soc-website.html']
with sync_playwright() as p:
  b=p.chromium.launch()
  for w,h in [(1440,900),(1280,800),(1024,640),(768,1024),(390,844)]:
    for u in PAGES:
      pg=b.new_page(viewport={'width':w,'height':h}); err=[]; pg.on('pageerror',lambda e:err.append(str(e)))
      pg.goto(B+u,wait_until='networkidle'); pg.wait_for_timeout(400)
      r=pg.evaluate('''()=>{const hero=document.querySelector('.hero');const hb=hero?hero.getBoundingClientRect().bottom+scrollY:0;
        const bad=[...document.querySelectorAll('main *, section *')].filter(e=>e.querySelector('table,.plans,.bg-card')&&getComputedStyle(e).position==='fixed').map(e=>e.className);
        const g=[...document.querySelectorAll('.bg-card,.plans,table')].map(e=>e.getBoundingClientRect().top+scrollY);
        const fx=[...document.querySelectorAll('main *')].filter(e=>getComputedStyle(e).position==='fixed'&&e.getBoundingClientRect().height>0).map(e=>e.tagName+'.'+e.className);
        return {fx,hs:document.documentElement.scrollWidth-innerWidth,bad,over:g.filter(t=>t<hb-1).length}}''')
      if r['hs']>0: fail.append(f'{u}@{w}: cuộn ngang {r["hs"]}px')
      if r['bad']: fail.append(f'{u}@{w}: khối nội dung position:fixed {r["bad"]}')
      if r['over']: fail.append(f'{u}@{w}: {r["over"]} khối giá nằm chồng lên hero')
      if r['fx']: fail.append(f'{u}@{w}: phần tử trong <main> hiển thị position:fixed {r["fx"]}')
      if err: fail.append(f'{u}@{w}: lỗi JS {err}')
      pg.close()
  b.close()
for f in fail: print('FAIL:',f)
print('OK: test_layout đạt' if not fail else f'{len(fail)} lỗi'); sys.exit(1 if fail else 0)
