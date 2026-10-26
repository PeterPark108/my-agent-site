#!/usr/bin/env python3
"""Crawl a site (local or live) and report broken internal links/assets/anchors.
Usage: python3 scripts/check_links.py http://localhost:8811/"""
import sys,re,urllib.request,urllib.parse
from html.parser import HTMLParser
base=sys.argv[1]; seen={}; q=[base]; bad=[]; ids={}; anchors=[]
class P(HTMLParser):
  def __init__(s): super().__init__(); s.l=[]; s.ids=set()
  def handle_starttag(s,t,a):
    a=dict(a)
    if 'id' in a: s.ids.add(a['id'])
    for k in ('href','src'):
      if a.get(k): s.l.append(a[k])
def get(u):
  try:
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'linkcheck'}),timeout=20); return r.status,r.read(),r.headers.get('content-type','')
  except urllib.error.HTTPError as e: return e.code,b'',''
  except Exception as e: return str(e),b'',''
while q:
  u=q.pop(); 
  if u in seen: continue
  st,body,ct=get(u); seen[u]=st
  if st!=200: continue
  if 'html' in ct:
    p=P(); p.feed(body.decode('utf-8','replace')); ids[u]=p.ids
    for h in p.l:
      if h.startswith(('mailto:','tel:','javascript:','data:')) or h=='#': continue
      full=urllib.parse.urljoin(u,h); nu,frag=urllib.parse.urldefrag(full)
      if frag: anchors.append((u,nu,frag))
      if nu.startswith(base):
        if nu not in seen: q.append(nu)
  elif 'css' in ct:
    for h in re.findall(rb'url\(([^)]+)\)',body):
      nu=urllib.parse.urljoin(u,h.decode().strip('\'"'))
      if nu.startswith(base) and nu not in seen: q.append(nu)
for u,st in seen.items():
  if st!=200: bad.append((st,u))
for src,nu,frag in anchors:
  if nu in ids and frag not in ids[nu]: bad.append(('missing #'+frag,src))
print(f'checked {len(seen)} URLs, {len(bad)} problems'); [print(' ',*b) for b in bad]
sys.exit(1 if bad else 0)
