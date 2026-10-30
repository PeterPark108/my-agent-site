#!/usr/bin/env python3
"""Kiểm tra CI (stdlib): link nội bộ, không lộ dữ liệu cá nhân, JSON hợp lệ, sitemap."""
import json, re, subprocess, sys, os, threading, http.server, functools, socketserver
fail = []
files = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True).stdout.split()
if any(f.startswith('data/private/') for f in files):
    fail.append('data/private/** đang bị git theo dõi')
if not os.path.isfile('sitemap.xml'):
    fail.append('thiếu sitemap.xml')
try:
    d = json.load(open('data/orders.json', encoding='utf-8'))
    raw = open('data/orders.json', encoding='utf-8').read()
    if re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', raw): fail.append('orders.json chứa email')
    if re.search(r'(\+?84|0)[\s.-]?\d{2,3}[\s.-]?\d{3}[\s.-]?\d{3,4}', raw): fail.append('orders.json chứa số điện thoại')
    if not re.fullmatch(r'[0-9a-f]{16,}', str(d.get('salt', ''))): fail.append('salt không hợp lệ')
    for k, v in d.get('orders', {}).items():
        if not re.fullmatch(r'[0-9a-f]{64}', k): fail.append('khóa đơn không phải SHA-256: ' + k[:12])
        bad = set(v) - {'step', 'steps', 'percent', 'status', 'updated', 'note', 'history'}
        if bad: fail.append(f'trường lạ trong đơn {k[:8]}: {sorted(bad)}')
except Exception as e:
    fail.append(f'orders.json lỗi: {e}')
# nội dung Tin tức + Blog hợp lệ (từ cấm, độ dài, ngày, slug trùng, dịch vụ liên quan...)
for sc in ('news_build.py', 'blog_build.py'):
    r = subprocess.run([sys.executable, 'scripts/' + sc, '--validate-only'], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else sc)
    if r.returncode: fail.append(f'{sc} --validate-only lỗi:\n' + r.stdout.strip())
# Bảng giá: chặn dữ liệu không công khai, bắt buộc câu VAT/tham khảo/quảng cáo
r = subprocess.run([sys.executable, 'scripts/test_pricing.py'], capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'test_pricing')
if r.returncode: fail.append('test_pricing.py lỗi:\n' + r.stdout.strip())
# v0.9.23: Peter chốt giá CHƯA bao gồm VAT; chặn "đã (bao) gồm VAT" quay lại (trừ câu hỏi "... đã gồm VAT chưa?")
_VAT = re.compile(r'đã\s+(bao\s+)?gồm\s+(VAT|thuế\s*GTGT)(?!\s+chưa)', re.I)
for _f in subprocess.run(['git', 'ls-files', '*.html', '*.js', '*.json', '*.md', '*.py', '*.xml', '*.txt'], capture_output=True, text=True).stdout.split():
    if _f in ('CHANGELOG.md', 'scripts/ci_check.py') or _f.startswith('data/private/'): continue
    try: _s = open(_f, encoding='utf-8').read()
    except Exception: continue
    _m = _VAT.search(_s)
    if _m: fail.append(f'{_f}: còn "{_m.group(0)}" (giá phải là chưa bao gồm VAT)')
# js/css đổi so với tag phát hành gần nhất mà VERSION chưa bump -> trình duyệt dùng bản cache cũ (?v= trùng)
_tag = subprocess.run(['git', 'describe', '--tags', '--abbrev=0', '--match', 'v*'], capture_output=True, text=True).stdout.strip()
if _tag:
    _ver = open('VERSION').read().strip()
    _chg = subprocess.run(['git', 'diff', '--name-only', _tag, '--', 'js', 'css'], capture_output=True, text=True).stdout.split()
    if _chg and _ver == _tag.lstrip('v'):
        fail.append(f'js/css đổi so với {_tag} ({", ".join(_chg[:5])}) nhưng VERSION vẫn {_ver}: bump VERSION rồi chạy tech_pass.py (cache-busting ?v=)')
r = subprocess.run([sys.executable, 'server/contact-api/test_contact_api.py'], capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'test_contact_api')
if r.returncode: fail.append('test_contact_api.py lỗi:\n' + r.stdout.strip() + r.stderr[-500:])
# v0.9.7: Peter chốt chỉ dùng tên "My Agent"; chặn tên pháp nhân cũ quay lại (html, js, json, generator, nội dung)
_BAN = re.compile(r'TNHH|Thương mại và Dịch vụ My Agent', re.I)
for _root, _dirs, _files in os.walk('.'):
    _dirs[:] = [d for d in _dirs if d not in ('.git', 'node_modules')]
    for _f in _files:
        if _f.endswith(('.html', '.js', '.json', '.xml', '.md', '.py', '.txt')) and _f != 'CHANGELOG.md' and _f != 'ci_check.py':
            _p = os.path.join(_root, _f)
            try: _s = open(_p, encoding='utf-8').read()
            except Exception: continue
            if _BAN.search(_s): fail.append('còn tên pháp nhân cũ (TNHH) trong ' + _p)
# v0.9.10: GA4 bật với ID thật, chặn placeholder quay lại; mọi trang có head tải config.js (một nguồn GA duy nhất)
_cfg = open('js/config.js', encoding='utf-8').read()
_m = re.search(r"gaId:\s*'([^']*)'", _cfg)
if not _m or not re.fullmatch(r'G-[A-Z0-9]{6,}', _m.group(1)) or _m.group(1) == 'G-XXXXXXXXXX':
    fail.append('js/config.js: gaId phải là Measurement ID thật (không để placeholder G-XXXXXXXXXX)')
for _f in files:
    if not _f.endswith('.html'): continue
    _s = open(_f, encoding='utf-8').read()
    if 'http-equiv="refresh"' in _s: continue  # trang chuyển hướng noindex: bỏ qua
    if _s.count('js/config.js') != 1: fail.append(f'{_f}: cần đúng 1 lần tải js/config.js (GA), có {_s.count("js/config.js")}')
    if 'googletagmanager.com/gtag' in _s: fail.append(f'{_f}: gtag chèn trực tiếp, chỉ tải qua js/config.js')
    for _ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', _s, re.S):
        for _o in json.loads(_ld).get('@graph', []):
            if _o.get('@id', '').endswith('#org') and _o.get('sameAs') != ['https://www.facebook.com/myagentvn']:
                fail.append(f'{_f}: #org sameAs phải là ["https://www.facebook.com/myagentvn"], đang {_o.get("sameAs")}')
# sitemap chỉ chứa URL có file thật
for loc in re.findall(r'<loc>https://myagentvn\.com/(.*?)</loc>', open('sitemap.xml', encoding='utf-8').read()):
    if not os.path.isfile(loc or 'index.html'): fail.append('sitemap có URL không tồn tại: ' + loc)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory='.')
H.log_message = lambda *a: None
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(('127.0.0.1', 8899), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
out = subprocess.run([sys.executable, 'scripts/check_links.py', 'http://127.0.0.1:8899/'], capture_output=True, text=True).stdout
srv.shutdown(); print(out.strip())
m = re.search(r'checked (\d+) URLs, (\d+) problems', out)
if not m or m.group(2) != '0' or int(m.group(1)) < 5: fail.append('kiểm tra link thất bại')
print('\n'.join('FAIL: ' + f for f in fail) or 'OK: tất cả kiểm tra đạt')
sys.exit(1 if fail else 0)
