# -*- coding: utf-8 -*-
"""Icon glass cho các ô dịch vụ / nhóm / combo (v0.9.30).
Mỗi ô một glyph SVG 48x48 riêng: thân kính (.b), lõi xanh phát sáng (.c nét, .f khối).
Vòng quỹ đạo (.gl-o) + thẻ kính nhỏ (.gl-k) vẽ bằng CSS (css/style.css, mục "icon glass").
Chạy: python3 scripts/glass_icons.py  (idempotent; chèn/thay icon trong các trang tĩnh).
seo_blocks.py import gi() để khối 'tron-goi' (trang chủ) không bị ghi đè mất icon."""
import re,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
G={
# --- 18 dịch vụ ---
'thiet-ke-website':'<rect class="b" x="6" y="9" width="36" height="28" rx="5"/><path class="c" d="M6 16h36"/><circle class="f" cx="11" cy="12.5" r="1.3"/><rect class="c" x="11" y="21" width="15" height="10" rx="2"/><path class="c" d="M30 22h7M30 27h5"/>',
'hosting-seo':'<rect class="b" x="8" y="8" width="32" height="13" rx="4"/><rect class="b" x="8" y="26" width="32" height="13" rx="4"/><circle class="f" cx="14" cy="14.5" r="2"/><circle class="f" cx="14" cy="32.5" r="2"/><path class="c" d="M21 14.5h13M21 32.5h9"/>',
'ten-mien':'<circle class="b" cx="24" cy="24" r="16"/><path class="b" d="M24 8c-6 5-6 27 0 32M24 8c6 5 6 27 0 32"/><path class="c" d="M8.5 24h31M11 16h26M11 32h26"/>',
'email-doanh-nghiep':'<rect class="b" x="6" y="11" width="36" height="26" rx="5"/><path class="c" d="M8 14l16 12 16-12"/><path class="c" d="M8 35l11-10M40 35L29 25" opacity=".55"/>',
'cham-soc-website':'<path class="b" d="M24 6l15 6v10c0 10-6.5 17-15 20-8.5-3-15-10-15-20V12z"/><path class="c" d="M17 24l5 5 9-10"/>',
'seo-tong-the':'<circle class="b" cx="21" cy="21" r="13"/><path class="b" d="M31 31l9 9" stroke-width="4"/><path class="c" d="M15 26v-4M21 26v-9M27 26v-6"/>',
'quang-cao-google-facebook':'<path class="b" d="M8 20v8a3 3 0 003 3h4l12 7V10L15 17h-4a3 3 0 00-3 3z"/><path class="c" d="M33 18c2.5 3 2.5 9 0 12M37.5 14c5 5.5 5 14.5 0 20"/><path class="b" d="M15 31l3 8h4l-2-7"/>',
'traffic-user':'<circle class="b" cx="17" cy="16" r="6"/><path class="b" d="M6 38c0-7 5-11 11-11s11 4 11 11"/><circle class="b" cx="31" cy="14" r="4.5" opacity=".7"/><path class="c" d="M28 36l6-7 4 4 6-8"/><path class="c" d="M40 25h4v4"/>',
'google-maps':'<path class="b" d="M24 43s-13-12-13-23a13 13 0 0126 0c0 11-13 23-13 23z"/><circle class="f" cx="24" cy="20" r="4.5"/><ellipse class="c" cx="24" cy="43" rx="9" ry="2" opacity=".6"/>',
'video-ai':'<rect class="b" x="6" y="10" width="36" height="26" rx="5"/><path class="f" d="M21 17l9 6-9 6z"/><path class="c" d="M37 5v6M34 8h6"/><path class="b" d="M12 41h24"/>',
'cham-soc-fanpage':'<path class="b" d="M8 10h32a3 3 0 013 3v18a3 3 0 01-3 3H22l-8 7v-7H8a3 3 0 01-3-3V13a3 3 0 013-3z"/><path class="f" d="M24 29l-6-6a3.6 3.6 0 015.1-5.1l.9.9.9-.9A3.6 3.6 0 0130 23z"/>',
'zalo-oa-mini-app':'<rect class="b" x="13" y="5" width="22" height="38" rx="5"/><rect class="c" x="17.5" y="13" width="5.5" height="5.5" rx="1.5"/><rect class="c" x="25" y="13" width="5.5" height="5.5" rx="1.5"/><rect class="c" x="17.5" y="20.5" width="5.5" height="5.5" rx="1.5"/><rect class="f" x="25" y="20.5" width="5.5" height="5.5" rx="1.5"/><path class="b" d="M21 38h6"/>',
'profile-doanh-nghiep':'<path class="b" d="M12 5h17l9 9v29H12z"/><path class="b" d="M29 5v9h9"/><circle class="f" cx="21" cy="21" r="3.5"/><path class="c" d="M16 32h16M16 37h11M26 21h6"/>',
'phan-tich-du-lieu':'<rect class="b" x="6" y="7" width="36" height="34" rx="5"/><path class="c" d="M13 34V25M20 34V18M27 34v-7M34 34V14"/><path class="c" d="M12 19l8-6 7 5 8-7" opacity=".6"/>',
'ky-thuat-du-lieu':'<ellipse class="b" cx="20" cy="11" rx="12" ry="4.5"/><path class="b" d="M8 11v24c0 2.5 5.4 4.5 12 4.5S32 37.5 32 35V11"/><path class="c" d="M8 19.5c0 2.5 5.4 4.5 12 4.5s12-2 12-4.5M8 27.5c0 2.5 5.4 4.5 12 4.5s12-2 12-4.5"/><path class="c" d="M36 18h7M40 15l3 3-3 3"/>',
'phan-mem-noi-bo':'<rect class="b" x="5" y="8" width="38" height="30" rx="5"/><path class="b" d="M15 8v30"/><path class="c" d="M8.5 15h3M8.5 20h3M8.5 25h3"/><rect class="c" x="20" y="14" width="9" height="7" rx="1.5"/><rect class="c" x="31" y="14" width="7" height="7" rx="1.5"/><path class="c" d="M20 31l5-5 4 3 9-7"/>',
'thiet-ke-app':'<rect class="b" x="12" y="4" width="24" height="40" rx="6"/><path class="b" d="M20 8h8"/><rect class="c" x="16.5" y="13" width="15" height="9" rx="2"/><circle class="f" cx="19" cy="29" r="2.4"/><circle class="f" cx="29" cy="29" r="2.4"/><path class="b" d="M21 39h6"/>',
'bo-cong-thuong':'<circle class="b" cx="24" cy="19" r="13"/><path class="b" d="M17 30l-4 13 7-3.5 4 4 3-13M31 30l4 13-7-3.5"/><path class="c" d="M18 19l4.5 4.5L31 15"/>',
# --- 5 nhóm (dich-vu.html, trang chủ) ---
'nen-tang-website':'<path class="b" d="M24 6l18 9-18 9L6 15z"/><path class="b" d="M6 24l18 9 18-9" opacity=".75"/><path class="c" d="M6 33l18 9 18-9"/>',
'marketing-tang-truong':'<path class="b" d="M6 40h36"/><rect class="b" x="9" y="28" width="7" height="12" rx="1.5"/><rect class="b" x="20.5" y="21" width="7" height="19" rx="1.5"/><rect class="b" x="32" y="13" width="7" height="27" rx="1.5"/><path class="c" d="M8 22L22 11l6 5L40 6M33 6h7v7"/>',
'mang-xa-hoi-noi-dung':'<circle class="b" cx="12" cy="24" r="6"/><circle class="b" cx="35" cy="11" r="6"/><circle class="b" cx="35" cy="37" r="6"/><path class="c" d="M17.5 21l12-7M17.5 27l12 7"/><circle class="f" cx="12" cy="24" r="2"/>',
'du-lieu-phan-mem':'<rect class="b" x="11" y="11" width="26" height="26" rx="5"/><path class="b" d="M18 5v6M24 5v6M30 5v6M18 37v6M24 37v6M30 37v6M5 18h6M5 24h6M5 30h6M37 18h6M37 24h6M37 30h6"/><rect class="c" x="18" y="18" width="12" height="12" rx="2"/><circle class="f" cx="24" cy="24" r="2"/>',
'phap-ly-thu-tuc':'<path class="b" d="M24 7v34M14 41h20M9 11h30"/><path class="c" d="M9 11l-5 12h10zM39 11l-5 12h10z"/><path class="c" d="M4 23a5 3 0 0010 0M34 23a5 3 0 0010 0"/><circle class="f" cx="24" cy="7" r="2"/>',
'combo':'<rect class="b" x="6" y="6" width="16" height="16" rx="4"/><rect class="b" x="26" y="6" width="16" height="16" rx="4"/><rect class="b" x="6" y="26" width="16" height="16" rx="4"/><rect class="c" x="26" y="26" width="16" height="16" rx="4"/><path class="c" d="M34 30v8M30 34h8"/>',
# --- 6 combo ---
'khoi-nghiep-online':'<path class="b" d="M24 42V22"/><path class="c" d="M24 26c0-8-6-13-15-13 0 8 6 13 15 13zM24 22c0-7 5-12 14-12 0 7-5 12-14 12z"/><path class="b" d="M14 42h20"/>',
'ban-hang-chuyen-doi':'<path class="b" d="M9 16h30l-2.5 25h-25z"/><path class="c" d="M17 20v-6a7 7 0 0114 0v6"/><path class="c" d="M18 31l4 4 8-8"/>',
'thuong-hieu-chuyen-nghiep':'<path class="b" d="M14 6h20l8 11-18 25L6 17z"/><path class="c" d="M6 17h36M18 6l-4 11 10 25M30 6l4 11-10 25"/>',
'tang-truong':'<path class="b" d="M6 42h36M6 42V6"/><path class="b" d="M12 42v-8h8v-8h8v-8h8v24"/><path class="c" d="M10 26l10-9 6 4L38 9M31 9h7v7"/>',
'du-lieu-doanh-nghiep':'<circle class="b" cx="22" cy="26" r="15"/><path class="f" d="M26 6v16h16A16 16 0 0026 6z"/><path class="c" d="M22 11v15l10 10"/>',
'tron-goi-my-agent':'<path class="b" d="M24 5l17 9v20l-17 9-17-9V14z"/><path class="b" d="M7 14l17 9 17-9M24 23v20"/><path class="c" d="M15.5 9.5l17 9v7"/>',
}
def gi(key,tag='span',cls='ic gl'):
  return (f'<{tag} class="{cls}" data-gi="{key}" aria-hidden="true"><i class="gl-o"><i></i></i>'
          f'<svg viewBox="0 0 48 48" focusable="false">{G[key]}</svg><i class="gl-k"></i></{tag}>')
def slug(href):
  m=re.search(r'dich-vu/([a-z0-9-]+)\.html',href) or re.search(r'(combo)\.html',href)
  return m.group(1) if m else None
SVGIC=r'<(?P<t>span|div) class="ic(?: gl)?"(?: data-gi="[^"]*")?(?: aria-hidden="true")?>.*?</(?P=t)>'
def sub_ic(block,key):
  return re.sub(SVGIC,lambda m:gi(key,m.group('t')),block,count=1,flags=re.S)
TAGRE=re.compile(r'<(/?)(div|span|a|article)\b[^>]*>')
def _end(s,i,tag):
  """vị trí ngay sau thẻ đóng khớp với thẻ mở tại i"""
  d=0
  for m in TAGRE.finditer(s,i):
    if m.group(2)!=tag: continue
    d+=-1 if m.group(1) else 1
    if d==0: return m.end()
  raise ValueError('không thấy thẻ đóng')
def _layout(s,open_re,keyf,wrap):
  """v0.9.32: ô 2 cột – chữ trước (cột trái 3/4), icon sau (cột phải 1/4). Idempotent."""
  out=[];pos=0;n=0
  for m in re.finditer(open_re,s,flags=re.S):
    if m.start()<pos: continue
    tag=m.group('tag');st=m.start('o');en=_end(s,st,tag)
    otag=m.group('o');inner=s[m.end('o'):en-len(f'</{tag}>')]
    key=keyf(m,inner)
    t=re.search(SVGIC,inner,flags=re.S);it=t.group('t') if t else ('div' if 'tilt' in otag else 'span')
    inner=re.sub(SVGIC,'',inner,count=1,flags=re.S)
    w=re.fullmatch(r'<div class="glt">(.*)</div>',inner,flags=re.S)
    if w: inner=w.group(1)
    if 'glc' not in otag: otag=re.sub(r'class="([^"]*)"',lambda c:f'class="{c.group(1)} glc"',otag,count=1)
    body=(f'<div class="glt">{inner}</div>' if wrap else inner)+gi(key,it)
    out.append(s[pos:st]+otag+body+f'</{tag}>');pos=en;n+=1
  out.append(s[pos:]);return ''.join(out),n
def apply():
  n=0
  p=R/'dich-vu.html';s=p.read_text()
  # đầu nhóm: key lấy từ id cat-panel ngay trước
  s,k=_layout(s,r'<div class="cat-panel" id="(?P<id>[a-z-]+)"[^>]*>(?P<o><(?P<tag>div) class="cat-head(?: glc)?">)',lambda m,i:m.group('id'),False);n+=k
  s,k=_layout(s,r'(?P<o><(?P<tag>a) class="scard glass(?: glc)?" href="[^"]*?dich-vu/(?P<id>[a-z0-9-]+)\.html">)',lambda m,i:m.group('id'),False);n+=k
  p.write_text(s)
  for p in sorted((R/'dich-vu').glob('*.html')):
    s=p.read_text()
    s,k=_layout(s,r'(?P<o><(?P<tag>a) class="card glass tilt rv(?: glc)?" href="[^"]*?dich-vu/(?P<id>[a-z0-9-]+)\.html">)',lambda m,i:m.group('id'),True);n+=k
    p.write_text(s)
  for f in ['index.html','combo.html']:
    p=R/f;s=p.read_text()
    s,k=_layout(s,r'(?P<o><(?P<tag>article) class="card glass combo rv(?: glc)?" id="(?P<id>[a-z-]+)">)',lambda m,i:m.group('id'),True);n+=k
    s,k=_layout(s,r'(?P<o><(?P<tag>div) class="card glass catc rv(?: glc)?">)',lambda m,i:re.search(r'dich-vu\.html#([a-z-]+)',i).group(1),True);n+=k
    p.write_text(s)
  return n
def tron_goi_key(u):
  return {'combo.html':'combo'}.get(u) or slug(u)
if __name__=='__main__':
  print('icon glass:',apply(),'ô')
