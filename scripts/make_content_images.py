#!/usr/bin/env python3
"""Sinh ảnh đại diện và ảnh trong bài cho blog/tin tức My Agent.

Phong cách: nền tối #05070F, lưới, icon kính teal (cùng glyph với scripts/glass_icons.py).
Không dùng ảnh người, khách giả, giao diện sản phẩm có bản quyền, hay ảnh tin/người nổi tiếng.

Dùng (từ thư mục gốc repo):
  python3 scripts/make_content_images.py --batch1
  python3 scripts/make_content_images.py --spec scripts/content-images-batch1.json
  python3 scripts/make_content_images.py --contact-sheet /tmp/contact-sheet.webp

Mỗi ảnh: WebP, bề ngang 1200px; cover 1200×630; thân bài 1200×675; ≤ 150 KB.
"""
from __future__ import annotations
import argparse, html, io, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path("/usr/share/fonts/truetype/sand-box/google/Be Vietnam Pro")
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
MAX_KB = 150
COVER = (1200, 630)
BODY = (1200, 675)

# Glyph 48×48 cùng bộ với scripts/glass_icons.py (thân kính .b, nét teal .c, khối .f)
ICONS = {
  "website": '<rect class="b" x="6" y="9" width="36" height="28" rx="5"/><path class="c" d="M6 16h36"/><circle class="f" cx="11" cy="12.5" r="1.3"/><rect class="c" x="11" y="21" width="15" height="10" rx="2"/><path class="c" d="M30 22h7M30 27h5"/>',
  "hosting": '<rect class="b" x="8" y="8" width="32" height="13" rx="4"/><rect class="b" x="8" y="26" width="32" height="13" rx="4"/><circle class="f" cx="14" cy="14.5" r="2"/><circle class="f" cx="14" cy="32.5" r="2"/><path class="c" d="M21 14.5h13M21 32.5h9"/>',
  "domain": '<circle class="b" cx="24" cy="24" r="16"/><path class="b" d="M24 8c-6 5-6 27 0 32M24 8c6 5 6 27 0 32"/><path class="c" d="M8.5 24h31M11 16h26M11 32h26"/>',
  "care": '<path class="b" d="M24 6l15 6v10c0 10-6.5 17-15 20-8.5-3-15-10-15-20V12z"/><path class="c" d="M17 24l5 5 9-10"/>',
  "seo": '<circle class="b" cx="21" cy="21" r="13"/><path class="b" d="M31 31l9 9" stroke-width="4"/><path class="c" d="M15 26v-4M21 26v-9M27 26v-6"/>',
  "data": '<rect class="b" x="6" y="7" width="36" height="34" rx="5"/><path class="c" d="M13 34V25M20 34V18M27 34v-7M34 34V14"/><path class="c" d="M12 19l8-6 7 5 8-7" opacity=".6"/>',
  "app": '<rect class="b" x="12" y="4" width="24" height="40" rx="6"/><path class="b" d="M20 8h8"/><rect class="c" x="16.5" y="13" width="15" height="9" rx="2"/><circle class="f" cx="19" cy="29" r="2.4"/><circle class="f" cx="29" cy="29" r="2.4"/><path class="b" d="M21 39h6"/>',
  "network": '<circle class="b" cx="12" cy="24" r="6"/><circle class="b" cx="35" cy="11" r="6"/><circle class="b" cx="35" cy="37" r="6"/><path class="c" d="M17.5 21l12-7M17.5 27l12 7"/><circle class="f" cx="12" cy="24" r="2"/>',
  "growth": '<path class="b" d="M6 40h36"/><rect class="b" x="9" y="28" width="7" height="12" rx="1.5"/><rect class="b" x="20.5" y="21" width="7" height="19" rx="1.5"/><rect class="b" x="32" y="13" width="7" height="27" rx="1.5"/><path class="c" d="M8 22L22 11l6 5L40 6M33 6h7v7"/>',
  "legal": '<path class="b" d="M24 7v34M14 41h20M9 11h30"/><path class="c" d="M9 11l-5 12h10zM39 11l-5 12h10z"/>',
  "combo": '<rect class="b" x="6" y="6" width="16" height="16" rx="4"/><rect class="b" x="6" y="26" width="16" height="16" rx="4"/><rect class="b" x="26" y="6" width="16" height="16" rx="4"/><rect class="c" x="26" y="26" width="16" height="16" rx="4"/><path class="c" d="M34 30v8M30 34h8"/>',
  "hex": '<path class="b" d="M24 5l17 9v20l-17 9-17-9V14z"/><path class="b" d="M7 14l17 9 17-9M24 23v20"/><path class="c" d="M15.5 9.5l17 9v7"/>',
  "mail": '<rect class="b" x="6" y="11" width="36" height="26" rx="5"/><path class="c" d="M8 14l16 12 16-12"/>',
  "profile": '<path class="b" d="M12 5h17l9 9v29H12z"/><path class="b" d="M29 5v9h9"/><circle class="f" cx="21" cy="21" r="3.5"/><path class="c" d="M16 32h16M16 37h11M26 21h6"/>',
  "db": '<ellipse class="b" cx="20" cy="11" rx="12" ry="4.5"/><path class="b" d="M8 11v24c0 2.5 5.4 4.5 12 4.5S32 37.5 32 35V11"/><path class="c" d="M8 19.5c0 2.5 5.4 4.5 12 4.5s12-2 12-4.5"/>',
  "software": '<rect class="b" x="5" y="8" width="38" height="30" rx="5"/><path class="b" d="M15 8v30"/><path class="c" d="M8.5 15h3M8.5 20h3M8.5 25h3"/><rect class="c" x="20" y="14" width="9" height="7" rx="1.5"/>',
  "search": '<circle class="b" cx="21" cy="21" r="13"/><path class="b" d="M31 31l9 9" stroke-width="4"/>',
  "shield": '<path class="b" d="M24 6l15 6v10c0 10-6.5 17-15 20-8.5-3-15-10-15-20V12z"/>',
  "check": '<path class="b" d="M24 6l15 6v10c0 10-6.5 17-15 20-8.5-3-15-10-15-20V12z"/><path class="c" d="M17 24l5 5 9-10"/>',
  "phone": '<rect class="b" x="13" y="5" width="22" height="38" rx="5"/><path class="b" d="M21 38h6"/>',
  "chat": '<path class="b" d="M8 10h32a3 3 0 013 3v18a3 3 0 01-3 3H22l-8 7v-7H8a3 3 0 01-3-3V13a3 3 0 013-3z"/>',
  "key": '<circle class="b" cx="16" cy="24" r="8"/><path class="c" d="M23 24h17M34 24v6M39 24v4"/><circle class="f" cx="16" cy="24" r="2.4"/>',
  "lock": '<rect class="b" x="10" y="20" width="28" height="20" rx="4"/><path class="c" d="M16 20v-5a8 8 0 0116 0v5"/><circle class="f" cx="24" cy="30" r="2.2"/>',
  "calendar": '<rect class="b" x="6" y="10" width="36" height="32" rx="5"/><path class="c" d="M6 18h36M16 6v8M32 6v8"/><path class="c" d="M14 26h6M22 26h6M30 26h6M14 33h6M22 33h6"/>',
  "warning": '<path class="b" d="M24 6l20 34H4z"/><path class="c" d="M24 18v12"/><circle class="f" cx="24" cy="35" r="1.8"/>',
  "backup": '<ellipse class="b" cx="24" cy="14" rx="14" ry="6"/><path class="b" d="M10 14v16c0 3.4 6.3 6 14 6s14-2.6 14-6V14"/><path class="c" d="M24 20v12M19 28l5 5 5-5"/>',
  "cloud": '<path class="b" d="M16 34h18a8 8 0 000-16 11 11 0 00-21-3A8 8 0 0016 34z"/>',
  "robot": '<rect class="b" x="10" y="14" width="28" height="22" rx="6"/><circle class="f" cx="19" cy="25" r="2.4"/><circle class="f" cx="29" cy="25" r="2.4"/><path class="c" d="M24 8v6M16 10h16M18 32h12"/>',
  "link": '<path class="b" d="M20 28a7 7 0 010-10l6-6a7 7 0 1110 10l-3 3"/><path class="c" d="M28 20a7 7 0 010 10l-6 6a7 7 0 11-10-10l3-3"/>',
  "doc": '<path class="b" d="M12 5h17l9 9v29H12z"/><path class="b" d="M29 5v9h9"/><path class="c" d="M16 24h16M16 30h16M16 36h10"/>',
  "image": '<rect class="b" x="6" y="10" width="36" height="28" rx="5"/><circle class="f" cx="16" cy="20" r="3"/><path class="c" d="M8 32l10-9 7 6 5-4 10 7"/>',
  "pencil": '<path class="b" d="M30 8l10 10-22 22H8V30z"/><path class="c" d="M26 12l10 10"/>',
  "refresh": '<path class="b" d="M12 12a16 16 0 0116-6 16 16 0 0114 22"/><path class="c" d="M38 8v12H26"/><path class="b" d="M36 36a16 16 0 01-16 6A16 16 0 016 20"/><path class="c" d="M10 40V28h12"/>',
  "clock": '<circle class="b" cx="24" cy="24" r="16"/><path class="c" d="M24 14v11l7 5"/>',
  "home": '<path class="b" d="M6 22L24 8l18 14v18H6z"/><path class="c" d="M18 40V26h12v14"/>',
  "form": '<rect class="b" x="8" y="6" width="32" height="36" rx="5"/><path class="c" d="M14 16h20M14 24h20M14 32h12"/>',
  "devices": '<rect class="b" x="4" y="12" width="28" height="20" rx="3"/><path class="b" d="M12 32h12"/><rect class="c" x="30" y="16" width="14" height="22" rx="3"/>',
  "nas": '<rect class="b" x="7" y="8" width="34" height="32" rx="5"/><path class="c" d="M12 16h24M12 24h24M12 32h24"/><circle class="f" cx="16" cy="16" r="1.5"/><circle class="f" cx="16" cy="24" r="1.5"/><circle class="f" cx="16" cy="32" r="1.5"/>',
  "revoke": '<circle class="b" cx="24" cy="24" r="16"/><path class="c" d="M16 16l16 16M32 16L16 32"/>',
}

def _font(name):
    return (FONT_DIR / name).as_uri()

def css():
    return f"""
@font-face{{font-family:"Be Vietnam Pro";src:url("{_font('BeVietnamPro-Regular.ttf')}") format("truetype");font-weight:400;}}
@font-face{{font-family:"Be Vietnam Pro";src:url("{_font('BeVietnamPro-Medium.ttf')}") format("truetype");font-weight:500;}}
@font-face{{font-family:"Be Vietnam Pro";src:url("{_font('BeVietnamPro-SemiBold.ttf')}") format("truetype");font-weight:600;}}
@font-face{{font-family:"Be Vietnam Pro";src:url("{_font('BeVietnamPro-Bold.ttf')}") format("truetype");font-weight:700;}}
@font-face{{font-family:"Be Vietnam Pro";src:url("{_font('BeVietnamPro-ExtraBold.ttf')}") format("truetype");font-weight:800;}}
:root{{--bg:#05070F;--bg2:#0A0F22;--tx:#E9ECF5;--mu:#A3ABC2;--teal:#2EE6D6;--teal2:#0B6F67;--line:rgba(255,255,255,.09);--red:#FF2D3D;--blue:#3D7BFF;}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--bg);color:var(--tx);font-family:"Be Vietnam Pro",system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}}
.stage{{position:relative;width:var(--w);height:var(--h)}}
.bg{{position:absolute;inset:0;background:
  radial-gradient(42% 55% at 8% 12%, rgba(46,230,214,.20), transparent 68%),
  radial-gradient(40% 50% at 92% 88%, rgba(61,123,255,.16), transparent 70%),
  radial-gradient(30% 40% at 80% 10%, rgba(255,45,61,.07), transparent 70%),
  var(--bg)}}
.grid{{position:absolute;inset:0;background-image:
  linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),
  linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);
  background-size:48px 48px;
  -webkit-mask-image:radial-gradient(ellipse at 50% 42%, #000 18%, transparent 78%);
  mask-image:radial-gradient(ellipse at 50% 42%, #000 18%, transparent 78%);
  opacity:.42}}
.ic{{--s:180px;width:var(--s);height:var(--s);flex:none;border-radius:28%;
  display:grid;place-items:center;position:relative;isolation:isolate;
  color:var(--teal);
  background:linear-gradient(145deg,rgba(255,255,255,.20),rgba(255,255,255,.04) 55%,rgba(46,230,214,.12));
  border:1px solid rgba(255,255,255,.22);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.42), inset 0 -10px 18px -10px rgba(46,230,214,.40), 0 18px 40px -16px rgba(46,230,214,.48)}}
.ic:before{{content:"";position:absolute;inset:0;border-radius:inherit;background:radial-gradient(60% 50% at 30% 18%,rgba(255,255,255,.32),transparent 70%);pointer-events:none}}
.ic svg{{width:72%;height:72%;overflow:visible;position:relative;z-index:1;filter:drop-shadow(0 0 4px rgba(46,230,214,.55))}}
.ic .b{{fill:rgba(255,255,255,.13);stroke:rgba(255,255,255,.88);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}
.ic .c{{fill:none;stroke:var(--teal);stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round}}
.ic .f{{fill:var(--teal);stroke:none}}
.k{{font-size:15px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin-bottom:18px}}
h1{{font-weight:800;letter-spacing:-.03em;line-height:1.18;text-wrap:balance;color:#F7F9FF;text-shadow:0 1px 12px rgba(0,0,0,.6),0 0 1px rgba(0,0,0,.85)}}
.sub{{color:#C5E8E4;font-weight:500;line-height:1.45;text-shadow:0 1px 10px rgba(0,0,0,.55)}}
.brand{{position:absolute;right:36px;bottom:24px;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:rgba(233,236,245,.45)}}
.brand b{{color:var(--teal);font-weight:700}}
.panel{{background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.12);border-radius:22px;backdrop-filter:blur(10px)}}
"""

def icon_html(key, size=None, cls="ic"):
    if key not in ICONS:
        raise SystemExit(f"icon không có: {key}")
    style = f' style="--s:{size}px"' if size else ""
    return f'<div class="{cls}"{style} aria-hidden="true"><svg viewBox="0 0 48 48" fill="none">{ICONS[key]}</svg></div>'

def page(w, h, body):
    return f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><style>
{css()}
body,.stage{{width:{w}px;height:{h}px}}
</style></head><body>
<div class="stage" style="--w:{w}px;--h:{h}px">
  <div class="bg"></div><div class="grid"></div>
  {body}
  <div class="brand">My <b>Agent</b></div>
</div></body></html>"""

def cover_html(kicker, title, subtitle, icon, size=COVER):
    w, h = size
    # Long titles get a slightly smaller type size
    fs = 52 if len(title) < 42 else 44 if len(title) < 58 else 38
    return page(w, h, f"""
    <div style="position:relative;z-index:1;display:flex;align-items:center;justify-content:space-between;gap:48px;height:100%;padding:56px 72px 64px;">
      <div style="max-width:720px;min-width:0">
        <div class="k">{html.escape(kicker)}</div>
        <h1 style="font-size:{fs}px;margin:0 0 18px;color:#F7F9FF">{html.escape(title)}</h1>
        <p class="sub" style="font-size:22px;max-width:28ch;color:#C5E8E4">{html.escape(subtitle)}</p>
      </div>
      {icon_html(icon, 200)}
    </div>""")

def cards_html(kicker, title, items, size=BODY):
    """items: list of (icon, label, note?)"""
    w, h = size
    n = len(items)
    cols = n if n <= 4 else (3 if n == 6 else 4)
    cells = []
    for it in items:
        icon, label, *rest = it
        note = rest[0] if rest else ""
        cells.append(f"""<div class="panel" style="padding:22px 20px 20px;display:flex;flex-direction:column;align-items:flex-start;gap:14px;min-width:0">
          {icon_html(icon, 72)}
          <div style="font-weight:700;font-size:20px;letter-spacing:-.02em;line-height:1.3">{html.escape(label)}</div>
          {f'<div class="sub" style="font-size:15px;line-height:1.45">{html.escape(note)}</div>' if note else ''}
        </div>""")
    return page(w, h, f"""
    <div style="position:relative;z-index:1;height:100%;padding:40px 56px 52px;display:flex;flex-direction:column">
      <div class="k">{html.escape(kicker)}</div>
      <h1 style="font-size:32px;margin:0 0 28px">{html.escape(title)}</h1>
      <div style="flex:1;display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:18px;align-items:stretch">{''.join(cells)}</div>
    </div>""")

def steps_html(kicker, title, steps, size=BODY):
    w, h = size
    n = len(steps)
    cells = []
    for i, label in enumerate(steps, 1):
        cells.append(f"""<div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px;min-width:0;position:relative">
          <div style="width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-weight:800;font-size:20px;color:#05070F;background:linear-gradient(145deg,#2EE6D6,#0B6F67);box-shadow:0 0 22px rgba(46,230,214,.4)">{i:02d}</div>
          <div style="font-weight:600;font-size:{15 if n>6 else 17}px;line-height:1.35;color:var(--tx)">{html.escape(label)}</div>
        </div>""")
    return page(w, h, f"""
    <div style="position:relative;z-index:1;height:100%;padding:40px 48px 52px;display:flex;flex-direction:column">
      <div class="k">{html.escape(kicker)}</div>
      <h1 style="font-size:32px;margin:0 0 36px">{html.escape(title)}</h1>
      <div style="flex:1;display:grid;grid-template-columns:repeat({n},minmax(0,1fr));gap:10px;align-items:center;position:relative">
        <div style="position:absolute;top:50%;left:8%;right:8%;height:2px;margin-top:-28px;background:linear-gradient(90deg,transparent,rgba(46,230,214,.55),transparent)"></div>
        {''.join(cells)}
      </div>
    </div>""")

def checklist_html(kicker, title, items, icon="check", size=BODY):
    w, h = size
    mid = (len(items) + 1) // 2
    def col(chunk):
        rows = []
        for t in chunk:
            rows.append(f"""<div style="display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-top:1px solid rgba(255,255,255,.08)">
              <div style="width:28px;height:28px;border-radius:9px;flex:none;display:grid;place-items:center;background:rgba(46,230,214,.14);border:1px solid rgba(46,230,214,.45);color:var(--teal);font-weight:800;font-size:16px;margin-top:1px">✓</div>
              <div style="font-size:20px;font-weight:600;line-height:1.35">{html.escape(t)}</div>
            </div>""")
        return "<div>" + "".join(rows) + "</div>"
    return page(w, h, f"""
    <div style="position:relative;z-index:1;height:100%;padding:40px 56px 52px;display:flex;gap:40px;align-items:center">
      {icon_html(icon, 160)}
      <div style="flex:1;min-width:0">
        <div class="k">{html.escape(kicker)}</div>
        <h1 style="font-size:32px;margin:0 0 22px">{html.escape(title)}</h1>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px 36px">
          {col(items[:mid])}{col(items[mid:])}
        </div>
      </div>
    </div>""")

def wireframe_html(kicker, title, size=BODY):
    w, h = size
    return page(w, h, f"""
    <div style="position:relative;z-index:1;height:100%;padding:36px 56px 48px;display:flex;flex-direction:column">
      <div class="k">{html.escape(kicker)}</div>
      <h1 style="font-size:30px;margin:0 0 22px">{html.escape(title)}</h1>
      <div class="panel" style="flex:1;padding:0;overflow:hidden;display:flex;flex-direction:column;min-height:0">
        <div style="height:36px;display:flex;align-items:center;gap:8px;padding:0 16px;border-bottom:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03)">
          <span style="width:10px;height:10px;border-radius:50%;background:#FF5F57"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#FEBC2E"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#28C840"></span>
          <div style="margin-left:12px;flex:1;height:18px;border-radius:8px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08)"></div>
        </div>
        <div style="padding:28px 28px 32px;flex:1;display:grid;grid-template-columns:1.15fr .85fr;gap:22px;align-items:stretch">
          <div>
            <div style="height:14px;width:28%;border-radius:6px;background:rgba(46,230,214,.7);margin-bottom:14px"></div>
            <div style="height:22px;width:80%;border-radius:8px;background:rgba(255,255,255,.86);margin-bottom:8px"></div>
            <div style="height:22px;width:62%;border-radius:8px;background:rgba(255,255,255,.4);margin-bottom:16px"></div>
            <div style="height:10px;width:90%;border-radius:5px;background:rgba(255,255,255,.16);margin-bottom:6px"></div>
            <div style="height:10px;width:70%;border-radius:5px;background:rgba(255,255,255,.12);margin-bottom:18px"></div>
            <div style="display:flex;gap:10px">
              <div style="height:32px;width:120px;border-radius:10px;background:linear-gradient(135deg,#E2253C,#B81F2C)"></div>
              <div style="height:32px;width:100px;border-radius:10px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06)"></div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;align-content:start">
            <div class="panel" style="padding:14px;height:88px"><div style="width:28px;height:28px;border-radius:8px;background:rgba(46,230,214,.25);margin-bottom:10px"></div><div style="height:8px;width:70%;background:rgba(255,255,255,.3);border-radius:4px"></div></div>
            <div class="panel" style="padding:14px;height:88px"><div style="width:28px;height:28px;border-radius:8px;background:rgba(61,123,255,.25);margin-bottom:10px"></div><div style="height:8px;width:70%;background:rgba(255,255,255,.3);border-radius:4px"></div></div>
            <div class="panel" style="padding:14px;height:88px"><div style="width:28px;height:28px;border-radius:8px;background:rgba(46,230,214,.25);margin-bottom:10px"></div><div style="height:8px;width:70%;background:rgba(255,255,255,.3);border-radius:4px"></div></div>
            <div class="panel" style="padding:14px;height:88px"><div style="width:28px;height:28px;border-radius:8px;background:rgba(61,123,255,.25);margin-bottom:10px"></div><div style="height:8px;width:70%;background:rgba(255,255,255,.3);border-radius:4px"></div></div>
          </div>
        </div>
      </div>
    </div>""")

def compare_html(kicker, title, cols, size=BODY):
    """cols: list of {icon, title, points:[]}"""
    w, h = size
    cells = []
    for c in cols:
        pts = "".join(f'<div style="display:flex;gap:8px;align-items:flex-start;padding:6px 0;color:var(--mu);font-size:16px"><span style="color:var(--teal)">·</span><span>{html.escape(p)}</span></div>' for p in c["points"])
        cells.append(f"""<div class="panel" style="padding:24px;display:flex;flex-direction:column;gap:10px;min-width:0">
          {icon_html(c["icon"], 72)}
          <div style="font-weight:800;font-size:24px;letter-spacing:-.02em;margin-top:6px">{html.escape(c["title"])}</div>
          {pts}
        </div>""")
    return page(w, h, f"""
    <div style="position:relative;z-index:1;height:100%;padding:40px 56px 52px;display:flex;flex-direction:column">
      <div class="k">{html.escape(kicker)}</div>
      <h1 style="font-size:32px;margin:0 0 24px">{html.escape(title)}</h1>
      <div style="flex:1;display:grid;grid-template-columns:repeat({len(cols)},minmax(0,1fr));gap:18px">{''.join(cells)}</div>
    </div>""")

def flow_html(kicker, title, nodes, size=BODY):
    """nodes: list of (icon, label)"""
    w, h = size
    parts = []
    for i, (icon, label) in enumerate(nodes):
        if i:
            parts.append('<div style="width:36px;flex:none;height:3px;background:linear-gradient(90deg,rgba(46,230,214,.2),rgba(46,230,214,.7),rgba(46,230,214,.2));border-radius:2px"></div>')
        parts.append(f"""<div class="panel" style="padding:22px 18px;display:flex;flex-direction:column;align-items:center;gap:12px;min-width:0;flex:1">
          {icon_html(icon, 80)}
          <div style="font-weight:700;font-size:18px;text-align:center;line-height:1.35">{html.escape(label)}</div>
        </div>""")
    return page(w, h, f"""
    <div style="position:relative;z-index:1;height:100%;padding:40px 48px 52px;display:flex;flex-direction:column">
      <div class="k">{html.escape(kicker)}</div>
      <h1 style="font-size:32px;margin:0 0 28px">{html.escape(title)}</h1>
      <div style="flex:1;display:flex;align-items:center;gap:12px">{''.join(parts)}</div>
    </div>""")

def build_html(spec):
    kind = spec["kind"]
    if kind == "cover":
        return cover_html(spec["kicker"], spec["title"], spec["subtitle"], spec["icon"], tuple(spec.get("size") or COVER))
    if kind == "cards":
        return cards_html(spec["kicker"], spec["title"], [tuple(x) for x in spec["items"]], tuple(spec.get("size") or BODY))
    if kind == "steps":
        return steps_html(spec["kicker"], spec["title"], spec["steps"], tuple(spec.get("size") or BODY))
    if kind == "checklist":
        return checklist_html(spec["kicker"], spec["title"], spec["items"], spec.get("icon") or "check", tuple(spec.get("size") or BODY))
    if kind == "wireframe":
        return wireframe_html(spec["kicker"], spec["title"], tuple(spec.get("size") or BODY))
    if kind == "compare":
        return compare_html(spec["kicker"], spec["title"], spec["cols"], tuple(spec.get("size") or BODY))
    if kind == "flow":
        return flow_html(spec["kicker"], spec["title"], [tuple(x) for x in spec["nodes"]], tuple(spec.get("size") or BODY))
    raise SystemExit(f"kind không hỗ trợ: {kind}")

def save_webp(im, dest: Path, max_kb=MAX_KB):
    from PIL import Image
    dest.parent.mkdir(parents=True, exist_ok=True)
    lo, hi = 40, 90
    best = None
    best_q = None
    # binary search highest quality that fits
    while lo <= hi:
        q = (lo + hi) // 2
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=q, method=6)
        if buf.tell() <= max_kb * 1024:
            best, best_q = buf.getvalue(), q
            lo = q + 1
        else:
            hi = q - 1
    if best is None:
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=40, method=6)
        if buf.tell() > max_kb * 1024:
            # last resort: shrink
            ratio = (max_kb * 1024 / buf.tell()) ** 0.5
            im2 = im.resize((int(im.width * ratio * 0.95), int(im.height * ratio * 0.95)), Image.Resampling.LANCZOS)
            # then scale back? no, keep smaller? we must keep 1200 width. Try lower quality 30.
            buf = io.BytesIO()
            im.save(buf, "WEBP", quality=30, method=6)
        best, best_q = buf.getvalue(), 30
        if len(best) > max_kb * 1024:
            raise SystemExit(f"{dest} vẫn lớn hơn {max_kb}KB ({len(best)} bytes)")
    dest.write_bytes(best)
    return dest.stat().st_size, best_q

def render_spec(spec, dest: Path, fmt="webp"):
    from PIL import Image
    if not CHROME:
        raise SystemExit("Không tìm thấy google-chrome / chromium")
    w, h = tuple(spec.get("size") or (COVER if spec["kind"] == "cover" else BODY))
    html_doc = build_html(spec)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "page.html"
        png = Path(td) / "shot.png"
        src.write_text(html_doc, encoding="utf-8")
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               "--force-device-scale-factor=2", f"--window-size={w},{h}",
               f"--screenshot={png}", src.as_uri()]
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if r.returncode != 0 or not png.is_file():
            raise SystemExit(f"Chrome screenshot lỗi ({r.returncode}): {r.stderr[-400:]}")
        im = Image.open(png).convert("RGB")
        if im.size != (w * 2, h * 2) and im.size != (w, h):
            # crop/resize if chrome added chrome
            im = im.resize((w * 2, h * 2), Image.Resampling.LANCZOS) if im.size[0] > w else im
        if im.size != (w, h):
            im = im.resize((w, h), Image.Resampling.LANCZOS)
        dest = Path(dest)
        if fmt == "png":
            dest.parent.mkdir(parents=True, exist_ok=True)
            im.save(dest, "PNG", optimize=True)
            return dest.stat().st_size, "png"
        return save_webp(im, dest)

# ---------- Batch 1 specs ----------
def batch1_specs():
    C, B = list(COVER), list(BODY)
    return [
        # homepage / listing fallback OG
        {"id": "og-home", "out": "assets/og-image.png", "fmt": "png", "size": C, "kind": "cover",
         "kicker": "My Agent", "title": "Thiết kế website cho doanh nghiệp nhỏ",
         "subtitle": "SEO · Dữ liệu · AI · TP.HCM · Toàn quốc", "icon": "hex"},

        # blog 1
        {"id": "b1-cover", "out": "assets/blog/website-dung-de-lam-gi-cho-doanh-nghiep-nho-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Website dùng để làm gì cho doanh nghiệp nhỏ",
         "subtitle": "Khách tìm thấy, tin được, xem dịch vụ rồi liên hệ.", "icon": "website"},
        {"id": "b1-roles", "out": "assets/blog/website-dung-de-lam-gi-cho-doanh-nghiep-nho-vai-tro.webp", "size": B, "kind": "cards",
         "kicker": "Vai trò của website", "title": "Sáu việc website làm cho doanh nghiệp nhỏ",
         "items": [
            ("search", "Tìm thấy", "Đúng chữ khách đang gõ"),
            ("check", "Tin được", "Thông tin kiểm chứng được"),
            ("doc", "Mô tả ổn định", "Trên tên miền của mình"),
            ("form", "Nhận liên hệ", "Gọi, Zalo, form ngắn"),
            ("profile", "Tự chủ nội dung", "Sửa khi việc thay đổi"),
            ("data", "Theo dõi", "Biết trang đang chạy"),
         ]},
        {"id": "b1-contact", "out": "assets/blog/website-dung-de-lam-gi-cho-doanh-nghiep-nho-lien-he.webp", "size": B, "kind": "cards",
         "kicker": "Nhận yêu cầu", "title": "Nút liên hệ cần dễ thấy trên điện thoại",
         "items": [
            ("phone", "Gọi điện", "Mở đúng số"),
            ("chat", "Zalo", "Đúng tài khoản"),
            ("form", "Form ngắn", "Tên, liên hệ, nhu cầu"),
         ]},
        {"id": "b1-measure", "out": "assets/blog/website-dung-de-lam-gi-cho-doanh-nghiep-nho-do-luong.webp", "size": B, "kind": "cards",
         "kicker": "Theo dõi", "title": "Đo những gì liên quan đến khách",
         "items": [
            ("growth", "Nguồn truy cập", "Khách đến từ đâu"),
            ("form", "Liên hệ", "Form, gọi, Zalo"),
            ("data", "Trang xem nhiều", "Việc nào đang hút khách"),
         ]},

        # blog 2
        {"id": "b2-cover", "out": "assets/blog/chon-ten-mien-va-hosting-cho-doanh-nghiep-nho-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Chọn tên miền và hosting cho doanh nghiệp nhỏ",
         "subtitle": "Tên dễ nhớ, đúng chủ sở hữu, gia hạn, sao lưu và HTTPS.", "icon": "domain"},
        {"id": "b2-domain", "out": "assets/blog/chon-ten-mien-va-hosting-cho-doanh-nghiep-nho-ten-mien.webp", "size": B, "kind": "compare",
         "kicker": "Tên miền", "title": "Tên ngắn, dễ đọc; đuôi .vn hay .com",
         "cols": [
            {"icon": "domain", "title": "ten-cong-ty.vn", "points": ["Ngắn, dễ đọc, dễ nhớ", "Đứng tên đúng chủ sở hữu", "Tự giữ tài khoản và gia hạn"]},
            {"icon": "link", "title": ".vn hoặc .com", "points": ["Chọn đuôi khách dễ gõ", "Không cần ôm nhiều đuôi cùng lúc", "Giữ liên kết ổn định lâu dài"]},
         ]},
        {"id": "b2-hosting", "out": "assets/blog/chon-ten-mien-va-hosting-cho-doanh-nghiep-nho-hosting.webp", "size": B, "kind": "cards",
         "kicker": "Hosting", "title": "Ba nhóm hosting ở mức cơ bản",
         "items": [
            ("hosting", "Shared", "Chia sẻ máy, phù hợp web nhỏ"),
            ("software", "VPS", "Máy ảo, kiểm soát nhiều hơn"),
            ("cloud", "Cloud", "Nâng dần khi nhu cầu tăng"),
         ]},
        {"id": "b2-ops", "out": "assets/blog/chon-ten-mien-va-hosting-cho-doanh-nghiep-nho-https-sao-luu.webp", "size": B, "kind": "checklist",
         "kicker": "Vận hành", "title": "Cần có sẵn khi chọn hosting",
         "icon": "care",
         "items": ["HTTPS / chứng chỉ SSL", "Sao lưu và cách phục hồi", "Vị trí máy chủ rõ ràng", "Hỗ trợ khi website gặp sự cố", "Đường nâng cấp khi web lớn hơn", "Không bị khóa dữ liệu khi chuyển"]},

        # blog 3
        {"id": "b3-cover", "out": "assets/blog/noi-dung-tren-website-moi-trang-nen-viet-gi-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Nội dung trên website: mỗi trang nên viết gì",
         "subtitle": "Trang chủ, dịch vụ, giới thiệu, liên hệ, FAQ và hình ảnh.", "icon": "doc"},
        {"id": "b3-home", "out": "assets/blog/noi-dung-tren-website-moi-trang-nen-viet-gi-trang-chu.webp", "size": B, "kind": "wireframe",
         "kicker": "Trang chủ", "title": "Nói đúng việc chính trong vài giây đầu"},
        {"id": "b3-pages", "out": "assets/blog/noi-dung-tren-website-moi-trang-nen-viet-gi-cac-trang.webp", "size": B, "kind": "cards",
         "kicker": "Cấu trúc trang", "title": "Mỗi loại trang một nhiệm vụ rõ",
         "items": [
            ("home", "Trang chủ", "Việc chính và bước tiếp theo"),
            ("doc", "Dịch vụ", "Mỗi dịch vụ một trang đủ quyết định"),
            ("profile", "Giới thiệu", "Kể thật, kiểm chứng được"),
            ("form", "Liên hệ", "Đủ thông tin, rõ bước sau"),
         ]},
        {"id": "b3-photo", "out": "assets/blog/noi-dung-tren-website-moi-trang-nen-viet-gi-hinh-anh.webp", "size": B, "kind": "checklist",
         "kicker": "Hình ảnh", "title": "Cho thấy việc thật, đúng ngữ cảnh",
         "icon": "image",
         "items": ["Ảnh đúng việc mình đang làm", "Không dùng ảnh người không có thật", "Ghi chú (alt) mô tả đúng ảnh", "Nén ảnh để trang mở nhanh", "Khớp với chữ trên cùng trang", "Cập nhật khi dịch vụ thay đổi"]},

        # blog 4
        {"id": "b4-cover", "out": "assets/blog/quy-trinh-lam-website-cho-doanh-nghiep-nho-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Quy trình làm website: từ trao đổi đến bàn giao",
         "subtitle": "Bảy chặng rõ việc, để chủ doanh nghiệp theo dõi được.", "icon": "combo"},
        {"id": "b4-steps", "out": "assets/blog/quy-trinh-lam-website-cho-doanh-nghiep-nho-7-chang.webp", "size": B, "kind": "steps",
         "kicker": "Quy trình", "title": "Bảy chặng từ trao đổi đến bàn giao",
         "steps": ["Trao đổi", "Báo giá", "Cấu trúc", "Dựng trang", "Rà soát", "Ra mắt", "Bàn giao"]},
        {"id": "b4-structure", "out": "assets/blog/quy-trinh-lam-website-cho-doanh-nghiep-nho-cau-truc-giao-dien.webp", "size": B, "kind": "flow",
         "kicker": "Duyệt theo thứ tự", "title": "Chốt cấu trúc, rồi mới duyệt giao diện",
         "nodes": [("doc", "Cấu trúc trang"), ("website", "Giao diện"), ("devices", "Dựng nội dung thật")]},
        {"id": "b4-handoff", "out": "assets/blog/quy-trinh-lam-website-cho-doanh-nghiep-nho-ban-giao.webp", "size": B, "kind": "checklist",
         "kicker": "Bàn giao", "title": "Bàn giao quyền, không chỉ gửi một link",
         "icon": "legal",
         "items": ["Tài khoản tên miền", "Tài khoản hosting", "Quyền quản trị website", "Chứng chỉ HTTPS", "Hướng dẫn cập nhật nội dung", "Kênh hỗ trợ sau bàn giao"]},

        # blog 5
        {"id": "b5-cover", "out": "assets/blog/cham-soc-website-sau-ban-giao-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Chăm sóc website sau khi bàn giao",
         "subtitle": "Cập nhật, sao lưu, gia hạn, form, tốc độ và bảo mật.", "icon": "care"},
        {"id": "b5-tasks", "out": "assets/blog/cham-soc-website-sau-ban-giao-7-viec.webp", "size": B, "kind": "cards",
         "kicker": "Việc định kỳ", "title": "Bảy việc nên làm sau khi bàn giao",
         "items": [
            ("pencil", "Cập nhật nội dung", "Cho đúng thực tế"),
            ("backup", "Sao lưu", "Và kiểm tra phục hồi"),
            ("calendar", "Gia hạn", "Tên miền, hosting, SSL"),
            ("form", "Kiểm tra liên hệ", "Form, gọi, Zalo"),
            ("devices", "Tốc độ và ảnh", "Trang mở được trên điện thoại"),
            ("lock", "Bảo mật cơ bản", "Cập nhật, mật khẩu, sao lưu"),
            ("data", "Analytics", "Xem số liệu vừa đủ"),
         ]},
        {"id": "b5-renew", "out": "assets/blog/cham-soc-website-sau-ban-giao-gia-han.webp", "size": B, "kind": "cards",
         "kicker": "Gia hạn", "title": "Theo dõi ngày hết hạn cho ba thứ",
         "items": [
            ("domain", "Tên miền", "Mất tên miền là mất địa chỉ"),
            ("hosting", "Hosting", "Hết hạn thì trang ngưng chạy"),
            ("lock", "Chứng chỉ SSL", "Để kết nối vẫn an toàn"),
         ]},
        {"id": "b5-cadence", "out": "assets/blog/cham-soc-website-sau-ban-giao-nhip-goi-y.webp", "size": B, "kind": "compare",
         "kicker": "Nhịp gợi ý", "title": "Chia việc theo tuần, tháng và năm",
         "cols": [
            {"icon": "clock", "title": "Hàng tuần", "points": ["Xem form và tin nhắn", "Kiểm tra trang còn mở", "Sửa thông tin vừa đổi"]},
            {"icon": "calendar", "title": "Hàng tháng", "points": ["Xem số liệu vừa đủ", "Rà ảnh và tốc độ", "Sao lưu và thử phục hồi"]},
            {"icon": "refresh", "title": "Hàng năm", "points": ["Gia hạn tên miền", "Gia hạn hosting, SSL", "Rà quyền truy cập"]},
         ]},

        # news 1 microsoft
        {"id": "n1-cover", "out": "assets/news/microsoft-ai-quet-secret-github-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "AI agent quét kho mã tìm khóa bị lộ",
         "subtitle": "Chỉ xoá dòng trên GitHub là chưa đủ — phải thu hồi và đổi khóa.", "icon": "key"},
        {"id": "n1-risk", "out": "assets/news/microsoft-ai-quet-secret-github-rui-ro.webp", "size": B, "kind": "flow",
         "kicker": "Rủi ro", "title": "Khóa nằm trong kho mã công khai có thể bị lấy rất nhanh",
         "nodes": [("doc", "Khóa trong file"), ("robot", "Công cụ quét tự động"), ("warning", "Vào hệ thống khác")]},
        {"id": "n1-todo", "out": "assets/news/microsoft-ai-quet-secret-github-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Việc nên làm ngay", "title": "Xoá dòng chưa đủ, phải thu hồi khóa",
         "icon": "revoke",
         "items": ["Tìm khóa, token trong kho mã", "Thu hồi và đổi khóa ngay", "Xoá khỏi lịch sử và bản sao", "Dùng kho bí mật, không dán vào file", "Giới hạn quyền của từng khóa", "Rà tài khoản đã cấp quyền"]},

        # news 2 zero wire
        {"id": "n2-cover", "out": "assets/news/cloudflare-zero-wire-lo-hong-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "Theo dõi lỗ hổng Internet dễ hiểu hơn",
         "subtitle": "Bản tin nêu việc nên làm, kèm nguồn — hữu ích khi hỏi hosting.", "icon": "warning"},
        {"id": "n2-bulletin", "out": "assets/news/cloudflare-zero-wire-lo-hong-ban-tin.webp", "size": B, "kind": "cards",
         "kicker": "Bản tin lỗ hổng", "title": "Mỗi bản tin cần những gì để dùng được",
         "items": [
            ("doc", "Tóm tắt dễ hiểu", "Chuyện gì đang xảy ra"),
            ("check", "Việc nên làm", "Bước kiểm tra cụ thể"),
            ("link", "Link nguồn", "Đọc thêm khi cần"),
         ]},
        {"id": "n2-todo", "out": "assets/news/cloudflare-zero-wire-lo-hong-hoi-hosting.webp", "size": B, "kind": "checklist",
         "kicker": "Doanh nghiệp nhỏ", "title": "Hỏi đúng câu với bên vận hành máy chủ",
         "icon": "hosting",
         "items": ["Lỗ hổng này có liên quan phần mềm đang dùng?", "Đã có bản vá trên máy chủ chưa?", "Cần tắt tính năng nào tạm thời?", "Sao lưu còn dùng được không?", "Ai là người cập nhật hộ?", "Khi nào nhận được xác nhận đã vá?"]},

        # news 3 AI agents
        {"id": "n3-cover", "out": "assets/news/cloudflare-kiem-soat-tro-ly-ai-ca-nhan-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Nền tảng", "title": "Xem và kiểm soát trợ lý AI vào website",
         "subtitle": "Chặn hết nghe an toàn nhưng có thể làm mất khách.", "icon": "robot"},
        {"id": "n3-stats", "out": "assets/news/cloudflare-kiem-soat-tro-ly-ai-ca-nhan-thong-ke.webp", "size": B, "kind": "compare",
         "kicker": "Số liệu", "title": "Xem đã có bao nhiêu lượt từ trợ lý AI",
         "cols": [
            {"icon": "devices", "title": "Trình duyệt", "points": ["Khách tự mở trang", "Vẫn là nguồn quen thuộc", "Giữ nội dung rõ ràng"]},
            {"icon": "robot", "title": "Trợ lý AI", "points": ["Khách nhờ máy xem hộ", "Có thể tìm và đặt giúp", "Xem số liệu rồi mới chặn hay cho phép"]},
         ]},
        {"id": "n3-decide", "out": "assets/news/cloudflare-kiem-soat-tro-ly-ai-ca-nhan-quyet-dinh.webp", "size": B, "kind": "flow",
         "kicker": "Góc nhìn", "title": "Xem số liệu thực tế, rồi mới quyết định",
         "nodes": [("data", "Xem thống kê"), ("legal", "Chọn cho phép hoặc hạn chế"), ("refresh", "Rà lại sau một thời gian")]},

        # news 4 siri
        {"id": "n4-cover", "out": "assets/news/apple-siri-ai-mo-cho-nha-phat-trien-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · AI", "title": "Trợ lý AI trên điện thoại mở cho ứng dụng",
         "subtitle": "Doanh nghiệp chưa cần vội, nhưng nên giữ thông tin có cấu trúc.", "icon": "app"},
        {"id": "n4-connect", "out": "assets/news/apple-siri-ai-mo-cho-nha-phat-trien-ket-noi.webp", "size": B, "kind": "flow",
         "kicker": "Có gì mới", "title": "Trợ lý có thể gọi tới ứng dụng và dịch vụ",
         "nodes": [("chat", "Khách hỏi trợ lý"), ("app", "Ứng dụng nhận yêu cầu"), ("check", "Thông tin phải rõ, đúng")]},
        {"id": "n4-info", "out": "assets/news/apple-siri-ai-mo-cho-nha-phat-trien-thong-tin-ro.webp", "size": B, "kind": "checklist",
         "kicker": "Góc nhìn", "title": "Giữ thông tin trên website có cấu trúc",
         "icon": "profile",
         "items": ["Tên dịch vụ rõ ràng", "Giờ mở cửa / giờ làm việc", "Khu vực phục vụ", "Cách liên hệ và đặt lịch", "Mô tả sản phẩm, dịch vụ ổn định", "Cập nhật khi thông tin thay đổi"]},

        # news 5 synology
        {"id": "n5-cover", "out": "assets/news/synology-nas-c3rb3r-ransomware-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "Mã độc tống tiền nhắm vào NAS chưa cập nhật",
         "subtitle": "Cập nhật hệ thống, đừng mở trang quản trị ra Internet, giữ bản sao rời.", "icon": "nas"},
        {"id": "n5-risk", "out": "assets/news/synology-nas-c3rb3r-ransomware-rui-ro.webp", "size": B, "kind": "cards",
         "kicker": "Rủi ro", "title": "NAS thường giữ dữ liệu quan trọng của cả công ty",
         "items": [
            ("doc", "Hợp đồng, hoá đơn", "Mất là mất hồ sơ làm việc"),
            ("image", "Ảnh sản phẩm", "Tài nguyên bán hàng"),
            ("backup", "Bản sao lưu", "Nếu chỉ nằm trên chính NAS đó"),
         ]},
        {"id": "n5-todo", "out": "assets/news/synology-nas-c3rb3r-ransomware-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Việc nên làm", "title": "Cập nhật, đóng cổng quản trị, sao lưu rời",
         "icon": "lock",
         "items": ["Cập nhật hệ thống lưu trữ mạng", "Bật cập nhật tự động nếu có", "Không mở trang quản trị ra Internet", "Giữ thêm bản sao lưu tách rời", "Kiểm tra tài khoản được cấp quyền", "Thử phục hồi bản sao một lần"]},
    ]


def batch2_specs():
    """Đợt 2: 9 blog còn lại + 7 tin article + 9 ảnh bìa cho thẻ type:link. Không gồm og-image.png."""
    C, B = list(COVER), list(BODY)
    return [
        # ----- blog 6: tốc độ -----
        {"id": "b6-cover", "out": "assets/blog/toc-do-website-co-ban-cho-doanh-nghiep-nho-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Tốc độ website cơ bản cho doanh nghiệp nhỏ",
         "subtitle": "Tự kiểm tra, nén ảnh, bớt plugin, bật cache, ưu tiên điện thoại.", "icon": "clock"},
        {"id": "b6-viec", "out": "assets/blog/toc-do-website-co-ban-cho-doanh-nghiep-nho-7-viec.webp", "size": B, "kind": "checklist",
         "kicker": "Bảy việc cơ bản", "title": "Làm lần lượt, không cần sửa sâu ngay",
         "icon": "clock",
         "items": ["Tự đo tốc độ trước khi sửa", "Giảm dung lượng ảnh và media", "Chọn hosting phù hợp", "Bớt plugin và mã nhúng thừa", "Bật bộ nhớ đệm hợp lý", "Ưu tiên trải nghiệm trên điện thoại", "Hỏi rõ khi thuê làm web"]},
        {"id": "b6-anh", "out": "assets/blog/toc-do-website-co-ban-cho-doanh-nghiep-nho-anh.webp", "size": B, "kind": "cards",
         "kicker": "Việc 2", "title": "Ảnh lớn thường làm trang chậm",
         "items": [
            ("image", "Nén ảnh", "Ưu tiên WebP khi hệ thống hỗ trợ"),
            ("devices", "Đúng kích thước", "Không tải ảnh rộng hơn chỗ hiện"),
            ("growth", "Ít media thừa", "Bỏ video và slider không cần"),
         ]},
        {"id": "b6-mobile", "out": "assets/blog/toc-do-website-co-ban-cho-doanh-nghiep-nho-dien-thoai.webp", "size": B, "kind": "checklist",
         "kicker": "Việc 6", "title": "Ưu tiên bản điện thoại khi tối ưu",
         "icon": "phone",
         "items": ["Chữ đọc được ngay, không chờ ảnh lớn", "Nút gọi, Zalo, form hiện sớm", "Trang không bị kéo ngang", "Đo bằng mạng di động, tắt Wi-Fi thử", "Xem gợi ý bản mobile trên PageSpeed", "Thử bấm liên hệ bằng chính điện thoại mình"]},

        # ----- blog 7: GA -----
        {"id": "b7-cover", "out": "assets/blog/do-luong-website-bang-google-analytics-co-ban-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Đo lường website bằng Google Analytics cơ bản",
         "subtitle": "Cài đúng, tự giữ quyền, xem nguồn truy cập và sự kiện quan trọng.", "icon": "data"},
        {"id": "b7-muc-tieu", "out": "assets/blog/do-luong-website-bang-google-analytics-co-ban-muc-tieu.webp", "size": B, "kind": "cards",
         "kicker": "Việc 1", "title": "Xác định trước điều mình muốn biết",
         "items": [
            ("search", "Website để làm gì", "Giới thiệu, nhận liên hệ hay đặt lịch"),
            ("form", "Hành động quan trọng", "Gọi điện, Zalo, form, đặt mua"),
            ("calendar", "Số liệu theo tháng", "Chỉ theo dõi vài con số thật sự cần"),
         ]},
        {"id": "b7-su-kien", "out": "assets/blog/do-luong-website-bang-google-analytics-co-ban-su-kien.webp", "size": B, "kind": "cards",
         "kicker": "Việc 5", "title": "Đánh dấu hành động có giá trị",
         "items": [
            ("form", "Gửi form", "Yêu cầu liên hệ"),
            ("phone", "Bấm gọi điện", "Mở đúng số"),
            ("chat", "Bấm Zalo", "Đúng tài khoản"),
            ("calendar", "Đặt lịch", "Khi website có lịch"),
         ]},
        {"id": "b7-nhip", "out": "assets/blog/do-luong-website-bang-google-analytics-co-ban-nhip-thang.webp", "size": B, "kind": "checklist",
         "kicker": "Việc 6", "title": "Đọc số liệu định kỳ, rồi mới hành động",
         "icon": "calendar",
         "items": ["Xem hằng tháng, không cần mỗi ngày", "Người dùng và trang xem nhiều", "Nguồn truy cập chính", "Số sự kiện quan trọng", "So sánh với tháng trước", "Ghi vài dòng nhận xét rồi chỉnh trang"]},

        # ----- blog 8: bảo mật -----
        {"id": "b8-cover", "out": "assets/blog/bao-mat-website-co-ban-cho-doanh-nghiep-nho-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Bảo mật website cơ bản cho doanh nghiệp nhỏ",
         "subtitle": "HTTPS, cập nhật, mật khẩu mạnh, 2FA, sao lưu và phân quyền.", "icon": "lock"},
        {"id": "b8-7viec", "out": "assets/blog/bao-mat-website-co-ban-cho-doanh-nghiep-nho-7-viec.webp", "size": B, "kind": "checklist",
         "kicker": "Bảy việc nên làm", "title": "Không an toàn tuyệt đối, nhưng giảm rủi ro rõ",
         "icon": "shield",
         "items": ["Bật HTTPS cho toàn bộ website", "Cập nhật phần mềm, giao diện, plugin", "Mật khẩu mạnh và xác thực hai bước", "Sao lưu định kỳ và thử khôi phục", "Phân quyền tài khoản rõ ràng", "Bảo vệ form liên hệ khỏi spam", "Biết ai xử lý khi có sự cố"]},
        {"id": "b8-taikhoan", "out": "assets/blog/bao-mat-website-co-ban-cho-doanh-nghiep-nho-tai-khoan.webp", "size": B, "kind": "cards",
         "kicker": "Việc 3", "title": "Tài khoản quản trị là chìa khóa",
         "items": [
            ("key", "Mật khẩu riêng", "Dài, không dùng chung, lưu ở trình quản lý"),
            ("lock", "Xác thực hai bước", "Bật ở web, hosting, tên miền, email"),
            ("profile", "Không dùng chung tài khoản", "Mỗi người một tài khoản"),
         ]},
        {"id": "b8-saoluu", "out": "assets/blog/bao-mat-website-co-ban-cho-doanh-nghiep-nho-sao-luu.webp", "size": B, "kind": "flow",
         "kicker": "Việc 4", "title": "Sao lưu chỉ có ích khi phục hồi được",
         "nodes": [("backup", "Sao lưu mã và dữ liệu"), ("cloud", "Giữ thêm bản tách khỏi hosting"), ("refresh", "Thử khôi phục một lần")]},

        # ----- blog 9: Facebook / Zalo / sàn -----
        {"id": "b9-cover", "out": "assets/blog/da-co-facebook-zalo-san-tmdt-co-can-website-rieng-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Đã có Facebook, Zalo, sàn TMĐT, có cần website riêng?",
         "subtitle": "Không bắt buộc, nhưng website làm được vài việc nền tảng không làm thay.", "icon": "website"},
        {"id": "b9-gioi-han", "out": "assets/blog/da-co-facebook-zalo-san-tmdt-co-can-website-rieng-gioi-han.webp", "size": B, "kind": "cards",
         "kicker": "Ý 2", "title": "Giới hạn khi chỉ dựa vào nền tảng",
         "items": [
            ("legal", "Phí và hoa hồng", "Tùy nền tảng và gói đang dùng"),
            ("profile", "Khó giữ dữ liệu khách", "Lịch sử nằm trên nền tảng"),
            ("warning", "Phụ thuộc một kênh", "Thay đổi chính sách là bị ảnh hưởng"),
         ]},
        {"id": "b9-loi-ich", "out": "assets/blog/da-co-facebook-zalo-san-tmdt-co-can-website-rieng-loi-ich.webp", "size": B, "kind": "cards",
         "kicker": "Ý 3", "title": "Website riêng giúp được gì",
         "items": [
            ("phone", "Liên hệ trực tiếp", "Khách tìm tên doanh nghiệp rồi gọi"),
            ("check", "Tăng độ tin cậy", "Thông tin, địa chỉ, chính sách rõ"),
            ("doc", "Tự chủ nội dung", "Sửa khi việc thay đổi, không chờ nền tảng"),
         ]},
        {"id": "b9-toi-thieu", "out": "assets/blog/da-co-facebook-zalo-san-tmdt-co-can-website-rieng-toi-thieu.webp", "size": B, "kind": "checklist",
         "kicker": "Ý 5", "title": "Website tối thiểu cần những gì",
         "icon": "home",
         "items": ["Trang chủ: làm gì, cho ai", "Trang dịch vụ hoặc sản phẩm", "Form liên hệ hoặc nút Zalo", "Chính sách đổi trả / bảo hành", "Bản đồ và thông tin liên hệ", "Tên miền riêng có HTTPS"]},

        # ----- blog 10: GBP -----
        {"id": "b10-cover", "out": "assets/blog/google-business-profile-dich-vu-tai-tphcm-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Google Business Profile cho dịch vụ tại TP.HCM",
         "subtitle": "Tên đúng, danh mục sát, khu vực phục vụ rõ, ảnh thật, đánh giá thật.", "icon": "search"},
        {"id": "b10-loai", "out": "assets/blog/google-business-profile-dich-vu-tai-tphcm-loai-ho-so.webp", "size": B, "kind": "compare",
         "kicker": "Chọn đúng loại hồ sơ", "title": "Có chỗ khách đến, hay phục vụ tận nơi",
         "cols": [
            {"icon": "home", "title": "Có địa điểm đón khách", "points": ["Cửa hàng, phòng khám, văn phòng", "Hiện địa chỉ trên Maps", "Khách có thể chỉ đường tới"]},
            {"icon": "network", "title": "Phục vụ tận nơi", "points": ["Gặp khách tại nhà hoặc công trình", "Ẩn địa chỉ, khai khu vực phục vụ", "Ví dụ một hoặc vài quận ở TP.HCM"]},
         ]},
        {"id": "b10-thong-tin", "out": "assets/blog/google-business-profile-dich-vu-tai-tphcm-thong-tin.webp", "size": B, "kind": "checklist",
         "kicker": "Điền đúng quy định", "title": "Tên, danh mục và thông tin phải thật",
         "icon": "profile",
         "items": ["Tên đúng thương hiệu, không nhồi từ khóa", "Một danh mục chính sát việc đang làm", "Giờ mở cửa và cách liên hệ khớp thực tế", "Khu vực phục vụ khai đúng", "Ảnh thật về công việc, không lấy trên mạng", "Không mua hoặc tạo đánh giá giả"]},
        {"id": "b10-song", "out": "assets/blog/google-business-profile-dich-vu-tai-tphcm-giu-ho-so.webp", "size": B, "kind": "cards",
         "kicker": "Giữ hồ sơ luôn sống", "title": "Cập nhật đều, thông tin khớp với website",
         "items": [
            ("image", "Ảnh thật", "Công việc và đội ngũ"),
            ("chat", "Trả lời đánh giá", "Lịch sự, cả đánh giá chưa tốt"),
            ("link", "Khớp với website", "Tên, điện thoại, khu vực phục vụ"),
         ]},

        # ----- blog 11: checklist SEO -----
        {"id": "b11-cover", "out": "assets/blog/checklist-seo-co-ban-cho-website-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Checklist SEO cơ bản cho website doanh nghiệp nhỏ",
         "subtitle": "Mỗi trang một chủ đề, title riêng, liên kết nội bộ, sitemap, Search Console.", "icon": "seo"},
        {"id": "b11-noidung", "out": "assets/blog/checklist-seo-co-ban-cho-website-noi-dung.webp", "size": B, "kind": "checklist",
         "kicker": "Phần nội dung", "title": "Mỗi trang một chủ đề, title và mô tả riêng",
         "icon": "doc",
         "items": ["Ghi trang nào phục vụ cụm từ nào", "Không để hai trang cùng tranh một cụm", "Title riêng, nói đúng việc của trang", "Mô tả riêng, đủ để khách hiểu", "Tiêu đề trên trang khớp nội dung", "Chữ dễ đọc, trả lời đúng câu khách hỏi"]},
        {"id": "b11-kythuat", "out": "assets/blog/checklist-seo-co-ban-cho-website-ky-thuat.webp", "size": B, "kind": "checklist",
         "kicker": "Phần kỹ thuật", "title": "Nền tảng kỹ thuật tự kiểm được",
         "icon": "software",
         "items": ["Website chạy HTTPS, không báo lỗi", "Hiển thị tốt, bấm dễ trên điện thoại", "Ảnh được nén, có mô tả alt đúng", "Có sitemap và robots.txt", "Không chặn nhầm trang quan trọng", "Không có link hỏng dẫn tới trang lỗi"]},
        {"id": "b11-theodoi", "out": "assets/blog/checklist-seo-co-ban-cho-website-theo-doi.webp", "size": B, "kind": "flow",
         "kicker": "Liên kết và theo dõi", "title": "Dẫn nội bộ hợp lý, rồi rà bằng Search Console",
         "nodes": [("link", "Liên kết bài và trang dịch vụ"), ("search", "Kết nối Search Console"), ("refresh", "Rà lại khi thêm trang")]},

        # ----- blog 12: website chuyên nghiệp -----
        {"id": "b12-cover", "out": "assets/blog/website-chuyen-nghiep-can-gi-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Website chuyên nghiệp cần những gì?",
         "subtitle": "Mười tiêu chí tự kiểm được: rõ việc, dễ bấm, liên hệ được, nền tảng vững.", "icon": "check"},
        {"id": "b12-10tieu-chi", "out": "assets/blog/website-chuyen-nghiep-can-gi-10-tieu-chi.webp", "size": B, "kind": "checklist",
         "kicker": "Mười tiêu chí", "title": "Tự kiểm được, kể cả khi không rành kỹ thuật",
         "icon": "check",
         "items": ["Khách hiểu mình làm gì ngay khi mở trang", "Đẹp và dễ bấm trên điện thoại", "Nội dung rõ, thông tin kiểm chứng được", "Nút liên hệ hiện sớm, bấm được", "HTTPS, tốc độ chấp nhận được", "SEO nền tảng, sitemap, Search Console", "Form và chính sách rõ", "Ảnh thật, đúng việc", "Dễ cập nhật khi thông tin đổi", "Tên miền và tài khoản đứng đúng tên mình"]},
        {"id": "b12-tukiem", "out": "assets/blog/website-chuyen-nghiep-can-gi-tu-kiem.webp", "size": B, "kind": "cards",
         "kicker": "Tự kiểm thế nào", "title": "Ba việc làm được ngay trên điện thoại",
         "items": [
            ("phone", "Tự mở và bấm thử", "Gọi, Zalo, gửi form"),
            ("clock", "Đo tốc độ", "PageSpeed Insights của Google"),
            ("search", "Xem chỉ mục", "Google Search Console"),
         ]},

        # ----- blog 13: trọn gói -----
        {"id": "b13-cover", "out": "assets/blog/thiet-ke-web-tron-goi-gom-nhung-gi-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Thiết kế web trọn gói gồm những gì?",
         "subtitle": "Từ tư vấn, giao diện, bàn giao đến tên miền, hosting và chăm sóc.", "icon": "combo"},
        {"id": "b13-buoc", "out": "assets/blog/thiet-ke-web-tron-goi-gom-nhung-gi-cac-buoc.webp", "size": B, "kind": "steps",
         "kicker": "Các bước", "title": "Một dự án thiết kế web trọn gói đi thế nào",
         "steps": ["Tư vấn và xác định mục tiêu", "Sơ đồ trang và wireframe", "Giao diện máy tính và điện thoại", "Lập trình, form, SEO cơ bản", "Bàn giao trên tên miền của mình"]},
        {"id": "b13-ban-giao", "out": "assets/blog/thiet-ke-web-tron-goi-gom-nhung-gi-ban-giao.webp", "size": B, "kind": "checklist",
         "kicker": "Khi bàn giao", "title": "Anh/chị nên nhận được những gì",
         "icon": "care",
         "items": ["Website chạy trên tên miền của mình, có HTTPS", "Giao diện cho máy tính và điện thoại", "Sitemap, robots.txt và thẻ SEO từng trang", "Form liên hệ gửi về email của mình", "Tài liệu hoặc buổi hướng dẫn cập nhật", "Quyền quản trị và mã nguồn sau khi thanh toán đủ"]},
        {"id": "b13-kem", "out": "assets/blog/thiet-ke-web-tron-goi-gom-nhung-gi-phan-kem.webp", "size": B, "kind": "cards",
         "kicker": "Phần đi kèm nên hỏi rõ", "title": "Nền móng không phải lúc nào cũng nằm trong gói thiết kế",
         "items": [
            ("domain", "Tên miền", "Đăng ký đứng tên mình"),
            ("hosting", "Hosting", "Cấu hình và sao lưu rõ"),
            ("mail", "Email theo tên miền", "Hỏi trước khi chốt gói"),
         ]},

        # ----- blog 14: chi phí -----
        {"id": "b14-cover", "out": "assets/blog/chi-phi-lam-website-phu-thuoc-yeu-to-nao-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Blog", "title": "Chi phí làm website phụ thuộc vào yếu tố nào?",
         "subtitle": "Loại web, số trang, tính năng, nội dung, tên miền, hosting và chăm sóc.", "icon": "growth"},
        {"id": "b14-yeu-to", "out": "assets/blog/chi-phi-lam-website-phu-thuoc-yeu-to-nao-yeu-to.webp", "size": B, "kind": "cards",
         "kicker": "Các yếu tố chính", "title": "Không có một con số chung cho mọi website",
         "items": [
            ("website", "Loại website", "Landing, giới thiệu hay bán hàng"),
            ("doc", "Số trang, nội dung", "Ai chuẩn bị chữ và hình"),
            ("software", "Tính năng", "Form cơ bản hay quản lý đơn"),
            ("refresh", "Phạm vi chỉnh sửa", "Hỏi rõ số lần sửa trong gói"),
         ]},
        {"id": "b14-kem", "out": "assets/blog/chi-phi-lam-website-phu-thuoc-yeu-to-nao-chi-phi-kem.webp", "size": B, "kind": "cards",
         "kicker": "Chi phí hay bị quên", "title": "Các khoản tính riêng, cần hỏi trước",
         "items": [
            ("domain", "Tên miền", "Thường tính theo năm, đứng tên mình"),
            ("hosting", "Hosting / VPS", "Gia hạn và sao lưu"),
            ("care", "Chăm sóc sau bàn giao", "Cập nhật, bảo hành, hỗ trợ"),
         ]},
        {"id": "b14-hoi", "out": "assets/blog/chi-phi-lam-website-phu-thuoc-yeu-to-nao-nen-hoi.webp", "size": B, "kind": "checklist",
         "kicker": "Khi xem báo giá", "title": "Giá thấp không xấu, nếu biết mình nhận gì",
         "icon": "legal",
         "items": ["Có giao diện điện thoại không?", "Có HTTPS không?", "Có thẻ SEO và sitemap không?", "Ai sở hữu mã nguồn và tên miền?", "Bảo hành bao lâu?", "Giá đã gồm tên miền, hosting chưa? (My Agent: chưa, chưa bao gồm VAT)"]},

        # ----- news articles -----
        {"id": "n6-cover", "out": "assets/news/wordpress-7-1-4-ban-va-bao-mat-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "WordPress 7.1.4 vá nhiều lỗi bảo mật",
         "subtitle": "Nên kiểm tra phiên bản và cập nhật, rồi rà lại tài khoản có quyền viết bài.", "icon": "software"},
        {"id": "n6-loi", "out": "assets/news/wordpress-7-1-4-ban-va-bao-mat-loi-dang-chu-y.webp", "size": B, "kind": "cards",
         "kicker": "Những lỗi đáng chú ý", "title": "Bản 7.1.4 sửa một loạt lỗ hổng, gồm lỗi lúc cập nhật lõi",
         "items": [
            ("warning", "Cập nhật lõi", "Thư mục giải nén có thể bị truy cập"),
            ("lock", "Vá bảo mật", "Khuyến nghị cập nhật ngay"),
            ("refresh", "Nhánh cũ", "Bản vá được đưa ngược về nhánh còn hỗ trợ"),
         ]},
        {"id": "n6-viec", "out": "assets/news/wordpress-7-1-4-ban-va-bao-mat-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Góc nhìn cho doanh nghiệp nhỏ", "title": "Việc nên làm trong tuần này",
         "icon": "check",
         "items": ["Xem phiên bản WordPress hiện tại", "Cập nhật lên 7.1.4 hoặc bản vá tương ứng", "Sao lưu trước khi cập nhật", "Rà tài khoản có quyền viết bài", "Gỡ plugin và giao diện không dùng", "Xác nhận site đã nhận bản mới"]},

        {"id": "n7-cover", "out": "assets/news/gitlab-cve-2026-97229-cisa-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "Lỗ hổng GitLab điểm 10 đang bị khai thác",
         "subtitle": "CISA đưa vào danh mục KEV. Máy tự cài cần nâng cấp bản đã vá.", "icon": "warning"},
        {"id": "n7-rui-ro", "out": "assets/news/gitlab-cve-2026-97229-cisa-rui-ro.webp", "size": B, "kind": "cards",
         "kicker": "Lỗ hổng nguy hiểm ở đâu", "title": "Không cần đăng nhập vẫn có thể chạy mã",
         "items": [
            ("software", "CI/CD", "Lỗi khi biên dịch biểu thức chính quy"),
            ("revoke", "Không cần đăng nhập", "Kẻ tấn công có thể chạy mã trên máy"),
            ("legal", "CISA KEV", "Đã có bằng chứng khai thác thực tế"),
         ]},
        {"id": "n7-viec", "out": "assets/news/gitlab-cve-2026-97229-cisa-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Doanh nghiệp nhỏ nên làm gì", "title": "Xác định mình có dùng GitLab tự cài không",
         "icon": "lock",
         "items": ["Hỏi đơn vị quản lý mã nguồn đã vá chưa", "Nếu tự cài: kiểm tra phiên bản", "Nâng lên 19.4.2, 19.3.5 hoặc 19.2.8", "Ưu tiên máy chủ mở ra Internet", "GitLab.com đã được hãng vá sẵn", "Rà nhật ký theo hướng dẫn của GitLab"]},

        {"id": "n8-cover", "out": "assets/news/google-robots-txt-ai-training-control-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Web & SEO", "title": "Google sẽ hỗ trợ lệnh chung chặn AI huấn luyện",
         "subtitle": "Vẫn là đề xuất nháp, mục tiêu 2027. Chưa cần sửa robots.txt vội.", "icon": "robot"},
        {"id": "n8-co-che", "out": "assets/news/google-robots-txt-ai-training-control-co-che.webp", "size": B, "kind": "compare",
         "kicker": "Cơ chế dự kiến", "title": "Một mã chính sách dùng chung, thay vì lệnh riêng từng hãng",
         "cols": [
            {"icon": "doc", "title": "Hiện nay", "points": ["Phải viết lệnh riêng cho từng công ty AI", "Google-Extended là cách của Google từ 2023", "Dễ sót nếu chỉ chặn một vài bot"]},
            {"icon": "robot", "title": "Đề xuất mới", "points": ["Một policy token trong robots.txt", "Từ chối huấn luyện AI dùng chung", "Chưa áp dụng; mục tiêu trong năm 2027"]},
         ]},
        {"id": "n8-viec", "out": "assets/news/google-robots-txt-ai-training-control-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Doanh nghiệp nhỏ nên làm gì", "title": "Chưa cần thay đổi gì ngay",
         "icon": "search",
         "items": ["Chưa thêm mã mới vào robots.txt vội", "Kiểm tra robots.txt hiện tại đang cho phép gì", "Tránh một dòng chặn sai làm mất trang trên Google", "Theo dõi khi Google và các hãng chính thức hỗ trợ", "Quyết định sau: cho phép hay hạn chế huấn luyện"]},

        {"id": "n9-cover", "out": "assets/news/canva-brush-ai-chinh-sua-thiet-ke-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · AI", "title": "Canva ra mắt Brush, AI chuyên chỉnh sửa thiết kế",
         "subtitle": "Giữ bố cục, màu và chữ khi sửa. Đang có trên gói Pro, vẫn nên tự đọc lại.", "icon": "pencil"},
        {"id": "n9-vi-sao", "out": "assets/news/canva-brush-ai-chinh-sua-thiet-ke-vi-sao.webp", "size": B, "kind": "cards",
         "kicker": "Vì sao đáng chú ý", "title": "Tạo thiết kế đã khó, sửa mà không lệch bố cục còn khó hơn",
         "items": [
            ("image", "Hiểu cái cần đổi", "Không làm hỏng phần còn lại"),
            ("pencil", "Giữ màu và chữ", "Sửa đúng chỗ, đúng nhận diện"),
            ("refresh", "Làm việc lặp lại", "Đổi kích thước, thay tiêu đề hàng loạt"),
         ]},
        {"id": "n9-viec", "out": "assets/news/canva-brush-ai-chinh-sua-thiet-ke-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Doanh nghiệp nhỏ nên làm gì", "title": "Thử với việc lặp lại nhiều nhất, rồi tự kiểm",
         "icon": "check",
         "items": ["Nếu đang dùng gói Pro, thử với banner và bài đăng", "Chuẩn bị logo, mã màu, font thống nhất", "Luôn tự đọc lại chữ và hình trước khi đăng", "Không đưa thông tin khách hay nội bộ vào lệnh", "Chỉnh tay phần AI làm chưa đúng"]},

        {"id": "n10-cover", "out": "assets/news/node2shell-nodejs-brotli-cisa-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "Lỗ hổng Node2Shell trong Node.js đang bị khai thác",
         "subtitle": "CISA xác nhận khai thác thực tế. Nâng lên bản đã vá, đừng mở cổng lạ.", "icon": "warning"},
        {"id": "n10-anh-huong", "out": "assets/news/node2shell-nodejs-brotli-cisa-anh-huong.webp", "size": B, "kind": "cards",
         "kicker": "Ai bị ảnh hưởng", "title": "Lỗi nằm ở bộ giải nén Brotli đi kèm Node.js",
         "items": [
            ("software", "Node.js", "Vá: 22.23.4, 24.22.1, 26.12.1"),
            ("network", "Phần mềm khác", "Nhiều sản phẩm dùng Brotli cũng đã vá"),
            ("revoke", "Dòng hết hỗ trợ", "Không nhận bản vá, cần chuyển dòng còn hỗ trợ"),
         ]},
        {"id": "n10-viec", "out": "assets/news/node2shell-nodejs-brotli-cisa-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Doanh nghiệp nhỏ nên làm gì", "title": "Hỏi đơn vị làm web hoặc tự kiểm tra máy chủ",
         "icon": "lock",
         "items": ["Xem website, API, công cụ nội bộ có chạy Node.js không", "Nâng cấp lên bản vá tương ứng", "Sao lưu và thử trên bản thử trước", "Dòng đã hết hỗ trợ thì chuyển sang dòng còn hỗ trợ", "Không mở cổng quản trị ra Internet nếu không cần", "Theo dõi thông báo của đơn vị vận hành"]},

        {"id": "n11-cover", "out": "assets/news/magento-cve-2026-48356-cisa-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "Lỗ hổng tải tệp trên Magento đang bị khai thác",
         "subtitle": "CISA đưa vào KEV. Cập nhật bản -2026-jul, rồi rà thư mục tải lên.", "icon": "lock"},
        {"id": "n11-phien-ban", "out": "assets/news/magento-cve-2026-48356-cisa-phien-ban.webp", "size": B, "kind": "cards",
         "kicker": "Phiên bản bị ảnh hưởng", "title": "Adobe Commerce và Magento Open Source cần bản vá tháng 7/2026",
         "items": [
            ("software", "Nhiều dòng 2.4.x", "Kể cả các bản p-patch cũ hơn"),
            ("refresh", "Bản sửa -2026-jul", "Ví dụ 2.4.8-2026-jul"),
            ("legal", "CISA KEV", "Đã có bằng chứng khai thác thực tế"),
         ]},
        {"id": "n11-viec", "out": "assets/news/magento-cve-2026-48356-cisa-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Nên làm gì", "title": "Xác định có chạy Magento không, rồi cập nhật có sao lưu",
         "icon": "check",
         "items": ["Hỏi đơn vị làm web phiên bản hiện tại", "Cập nhật lên bản -2026-jul tương ứng", "Làm trên bản thử, sao lưu trước", "Rà thư mục tải lên tìm tệp lạ", "Kiểm tra tài khoản quản trị", "Theo dõi cảnh báo sau khi vá"]},

        {"id": "n12-cover", "out": "assets/news/google-ai-mode-links-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Web & SEO", "title": "Google AI Mode dẫn nhiều liên kết về website hơn",
         "subtitle": "AI tóm tắt vẫn dẫn sang trang gốc, nếu trang đó rõ và đáng tin.", "icon": "link"},
        {"id": "n12-thay-doi", "out": "assets/news/google-ai-mode-links-thay-doi.webp", "size": B, "kind": "cards",
         "kicker": "Chuyện gì đã xảy ra", "title": "AI Mode và AI Overviews dễ bấm sang website gốc hơn",
         "items": [
            ("search", "Dẫn ra trang gốc", "Không chỉ đọc câu trả lời tóm tắt"),
            ("check", "Nguồn đáng tin", "Trang rõ ràng, kiểm chứng được"),
            ("form", "Việc cụ thể", "Đặt lịch, xem dịch vụ, liên hệ"),
         ]},
        {"id": "n12-viec", "out": "assets/news/google-ai-mode-links-viec-nen-lam.webp", "size": B, "kind": "checklist",
         "kicker": "Doanh nghiệp nhỏ nên làm gì", "title": "Giữ thông tin trên website rõ, thống nhất, dễ hiểu",
         "icon": "doc",
         "items": ["Rà trang dịch vụ: làm gì, cho ai, ở đâu", "Cập nhật trang liên hệ cho đủ và đúng", "Khớp thông tin với Google Business Profile", "Viết câu trả lời đúng câu khách hay hỏi", "Dùng chữ đơn giản, dễ trích dẫn"]},

        # ----- 9 link-only covers (listing thumbs only) -----
        {"id": "l1-cover", "out": "assets/news/google-spam-update-09-2026-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Web & SEO", "title": "Google hoàn tất đợt cập nhật spam tháng 9/2026",
         "subtitle": "Kéo dài gần 14 ngày. Nên xem Search Console nếu lưu lượng thay đổi lạ.", "icon": "search"},
        {"id": "l2-cover", "out": "assets/news/zbs-khung-gio-gui-tin-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Nền tảng", "title": "Tin nhắn mẫu ZBS chỉ gửi chăm sóc từ 7h đến 22h",
         "subtitle": "Tin giao dịch vẫn gửi mọi lúc. Đặt lịch gửi trong khung giờ cho phép.", "icon": "clock"},
        {"id": "l3-cover", "out": "assets/news/power-bi-10-2026-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Dữ liệu", "title": "Power BI tháng 10/2026: Gantt gốc và Copilot",
         "subtitle": "Biểu đồ Gantt có sẵn và Copilot hỗ trợ dựng báo cáo.", "icon": "data"},
        {"id": "l4-cover", "out": "assets/news/beyondtrust-cve-2026-102764-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "Lỗ hổng vượt xác thực trên BeyondTrust đang bị khai thác",
         "subtitle": "Remote Support bị lỗi xác thực. Cần vá nếu doanh nghiệp đang dùng.", "icon": "warning"},
        {"id": "l5-cover", "out": "assets/news/google-search-control-docs-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Web & SEO", "title": "Google cập nhật tài liệu kiểm soát nội dung Search",
         "subtitle": "Rà lại cách website cho phép hoặc hạn chế nội dung chia sẻ với Search.", "icon": "doc"},
        {"id": "l6-cover", "out": "assets/news/php2shell-cisa-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Bảo mật", "title": "Lỗ hổng PHP php2shell: CISA yêu cầu vá ngay",
         "subtitle": "Lỗi nghiêm trọng, đã có trong danh mục khai thác thực tế.", "icon": "lock"},
        {"id": "l7-cover", "out": "assets/news/zalo-oa-the-tuong-tac-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Nền tảng", "title": "Zalo OA thêm Thẻ tương tác cho bài viết",
         "subtitle": "Bộ sưu tập, biểu mẫu và quà tặng ngay trong bài viết OA.", "icon": "chat"},
        {"id": "l8-cover", "out": "assets/news/zbs-quy-dinh-kiem-duyet-10-2026-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · Nền tảng", "title": "Zalo siết từ ngữ tuyệt đối khi duyệt mẫu tin ZBS",
         "subtitle": "Rà lại nội dung mẫu tin chăm sóc, tránh chữ quá tuyệt đối.", "icon": "legal"},
        {"id": "l9-cover", "out": "assets/news/openai-gpt-6-1-terra-cover.webp", "size": C, "kind": "cover",
         "kicker": "My Agent · Tin tức · AI", "title": "OpenAI ra mắt GPT-6.1 Terra",
         "subtitle": "Nhanh, rẻ hơn và giỏi thao tác máy tính hơn bản trước.", "icon": "robot"},
    ]

def contact_sheet(paths, dest: Path, cols=5):
    from PIL import Image, ImageDraw, ImageFont
    ims = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        ims.append((p, im))
    if not ims:
        raise SystemExit("Không có ảnh để ghép contact sheet")
    thumb_w = 360
    thumbs = []
    for p, im in ims:
        ratio = thumb_w / im.width
        th = max(1, int(im.height * ratio))
        thumbs.append((p, im.resize((thumb_w, th), Image.Resampling.LANCZOS)))
    rows = (len(thumbs) + cols - 1) // cols
    pad, gap, cap_h = 24, 16, 36
    # use max thumb height in a row roughly 360*675/1200=202 for body, 189 for cover
    cell_h = max(t.size[1] for _, t in thumbs) + cap_h
    W = pad * 2 + cols * thumb_w + (cols - 1) * gap
    H = pad * 2 + rows * cell_h + (rows - 1) * gap + 40
    sheet = Image.new("RGB", (W, H), (5, 7, 15))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(str(FONT_DIR / "BeVietnamPro-Regular.ttf"), 14)
        font_b = ImageFont.truetype(str(FONT_DIR / "BeVietnamPro-SemiBold.ttf"), 18)
    except Exception:
        font = font_b = ImageFont.load_default()
    draw.text((pad, 12), "My Agent — ảnh bài viết (batch 2)", fill=(46, 230, 214), font=font_b)
    for i, (p, t) in enumerate(thumbs):
        r, c = divmod(i, cols)
        x = pad + c * (thumb_w + gap)
        y = 48 + r * (cell_h + gap)
        sheet.paste(t, (x, y))
        label = Path(p).name
        if len(label) > 42:
            label = label[:40] + "…"
        draw.text((x, y + t.size[1] + 6), label, fill=(163, 171, 194), font=font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() == ".png":
        sheet.save(dest, "PNG", optimize=True)
        return dest.stat().st_size, "png"
    return save_webp(sheet, dest, max_kb=400)

def main(argv=None):
    ap = argparse.ArgumentParser(description="Sinh ảnh blog/tin tức My Agent")
    ap.add_argument("--batch1", action="store_true", help="Sinh toàn bộ ảnh đợt 1 (và og-image.png)")
    ap.add_argument("--batch2", action="store_true", help="Sinh ảnh đợt 2 (9 blog + 7 tin article + 9 ảnh bìa thẻ link; không đụng og-image.png)")
    ap.add_argument("--spec", help="File JSON danh sách ảnh (cùng schema với batch 1)")
    ap.add_argument("--only", help="Chỉ sinh id này (cách nhau bởi dấu phẩy)")
    ap.add_argument("--contact-sheet", help="Ghép contact sheet từ ảnh vừa sinh hoặc từ thư mục")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    specs = []
    if args.batch1:
        specs = batch1_specs()
    if args.batch2:
        specs = batch2_specs()
    if args.spec:
        specs = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    if args.only:
        want = {x.strip() for x in args.only.split(",") if x.strip()}
        specs = [s for s in specs if s.get("id") in want]
    if not specs and not args.contact_sheet:
        ap.print_help(); return 2
    written = []
    for s in specs:
        dest = ROOT / s["out"]
        if args.dry_run:
            print(f"DRY {s.get('id','')} -> {dest}")
            continue
        size, meta = render_spec(s, dest, s.get("fmt") or "webp")
        print(f"OK {s.get('id','')}  {dest.relative_to(ROOT)}  {size} bytes  q={meta}")
        if dest.stat().st_size > MAX_KB * 1024 and dest.suffix.lower() != ".png":
            raise SystemExit(f"Vượt {MAX_KB}KB: {dest} ({dest.stat().st_size} bytes)")
        written.append(dest)
    if args.contact_sheet:
        paths = written or sorted((ROOT / "assets/blog").glob("*.webp")) + sorted((ROOT / "assets/news").glob("*.webp"))
        sz, meta = contact_sheet(paths, Path(args.contact_sheet))
        print(f"OK contact-sheet {args.contact_sheet}  {sz} bytes  {meta}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
