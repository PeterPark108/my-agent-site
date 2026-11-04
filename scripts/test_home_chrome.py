#!/usr/bin/env python3
"""Quả cầu hero phải nhìn thấy, header trang chủ phải dính khi cuộn.

Chạy (server tĩnh đang mở): python3 scripts/test_home_chrome.py [base]
Mặc định http://127.0.0.1:8765/
"""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
if not BASE.endswith('/'):
    BASE += '/'

def box(page, sel):
    return page.evaluate('''(sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const c = getComputedStyle(el);
      return {w:r.width,h:r.height,x:r.x,y:r.y,op:+c.opacity,vis:c.visibility,disp:c.display};
    }''', sel)

def assert_visible(info, name, vw, vh):
    assert info, name + ' missing'
    assert info['w'] > 8 and info['h'] > 8, f'{name} box {info}'
    assert info['op'] > 0.5, f'{name} opacity {info}'
    assert info['vis'] == 'visible' and info['disp'] != 'none', name
    assert info['x'] < vw and info['x'] + info['w'] > 0, name + ' x'
    assert info['y'] < vh and info['y'] + info['h'] > 0, name + ' y'

def painted(page):
    """Cột phải khác nền thuần: quả cầu có pixel không phải màu nền."""
    return page.evaluate('''() => {
      const art = document.querySelector('.hx-art');
      const r = art.getBoundingClientRect();
      const c = document.createElement('canvas');
      const w = Math.max(1, Math.round(r.width)), h = Math.max(1, Math.round(r.height));
      c.width = w; c.height = h;
      const ctx = c.getContext('2d');
      // html2canvas is unavailable; sample via foreignObject is blocked.
      // Use elementFromPoint across the art: the orb must be the hit target somewhere.
      let hits = 0, samples = 0;
      for (let y = 8; y < r.height - 8; y += Math.max(12, r.height / 8)) {
        for (let x = 8; x < r.width - 8; x += Math.max(12, r.width / 8)) {
          samples++;
          const el = document.elementFromPoint(r.x + x, r.y + y);
          if (!el) continue;
          if (el.closest('.orb, .orbit-float, .orb-mark, .tech-orbit')) hits++;
        }
      }
      return {hits, samples, w: Math.round(r.width), h: Math.round(r.height)};
    }''')

def run():
    fails = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome', headless=True, args=['--no-sandbox'])
        views = [(1280, 800), (1536, 864), (390, 844)]
        for w, h in views:
            for theme in ('dark', 'light'):
                for js in (True, False):
                    ctx = b.new_context(viewport={'width': w, 'height': h}, java_script_enabled=js)
                    if js:
                        ctx.add_init_script(f"localStorage.setItem('ma-theme','{theme}')")
                    page = ctx.new_page()
                    errs = []
                    page.on('pageerror', lambda e: errs.append(str(e)))
                    page.goto(BASE + 'index.html', wait_until='domcontentloaded')
                    page.wait_for_timeout(400)
                    if not js and theme == 'light':
                        ctx.close(); continue
                    label = f'{w}x{h} {theme} js={js}'
                    try:
                        for sel, name in (('.hx-art','art'), ('.orb','orb'), ('.tech-orbit','orbit'), ('.orb-mark','M')):
                            assert_visible(box(page, sel), name, w, h)
                        hit = painted(page)
                        assert hit['hits'] >= 3, f'orb not painted {hit}'
                        if errs:
                            raise AssertionError('console ' + errs[0][:180])
                        print('OK', label, 'art', box(page, '.hx-art')['w'], 'hits', hit['hits'])
                    except AssertionError as e:
                        fails.append(label + ': ' + str(e))
                        print('FAIL', label, e)
                    ctx.close()
        # sticky header
        ctx = b.new_context(viewport={'width': 1280, 'height': 800})
        page = ctx.new_page()
        page.goto(BASE + 'index.html', wait_until='networkidle')
        page.evaluate('window.scrollTo(0,1500)')
        page.wait_for_timeout(150)
        top = page.evaluate('''() => {
          const h=document.querySelector('body.home > header');
          const r=h.getBoundingClientRect();
          return {top:r.top, pos:getComputedStyle(h).position, seen:r.height>40 && r.bottom>0};
        }''')
        logo = page.evaluate("document.querySelector('body.home > header .logo').getAttribute('href')")
        print('header', top, 'logo', logo)
        if abs(top['top']) > 2 or top['pos'] != 'sticky' or not top['seen']:
            fails.append('header not sticky ' + str(top))
        if logo != '/':
            fails.append('logo href ' + str(logo))
        # mobile menu
        m = b.new_context(viewport={'width': 390, 'height': 844})
        mp = m.new_page()
        mp.goto(BASE + 'index.html', wait_until='networkidle')
        mp.click('.burger')
        mp.wait_for_timeout(150)
        opened = mp.evaluate('''() => {
          const n=document.querySelector('nav');
          const r=n.getBoundingClientRect();
          return {open:n.classList.contains('open'), h:r.height, exp:document.querySelector('.burger').getAttribute('aria-expanded')};
        }''')
        print('menu', opened)
        if not opened['open'] or opened['h'] < 80:
            fails.append('mobile menu ' + str(opened))
        mp.keyboard.press('Escape')
        mp.wait_for_timeout(100)
        closed = mp.evaluate("document.querySelector('nav').classList.contains('open')")
        if closed:
            fails.append('esc did not close menu')
        # other pages stay sticky and unobstructed
        for path in ('dich-vu.html', 'blog.html', 'lien-he.html'):
            page.goto(BASE + path, wait_until='domcontentloaded')
            page.evaluate('window.scrollTo(0,1200)')
            page.wait_for_timeout(80)
            ht = page.evaluate('''() => {
              const h=document.querySelector('header');
              const r=h.getBoundingClientRect();
              return {top:Math.round(r.top), pos:getComputedStyle(h).position};
            }''')
            print(path, ht)
            if abs(ht['top']) > 2:
                fails.append(path + ' header ' + str(ht))
        b.close()
    if fails:
        print('FAILED')
        for f in fails:
            print(' -', f)
        sys.exit(1)
    print('ALL OK')

if __name__ == '__main__':
    run()
