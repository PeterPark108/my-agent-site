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
