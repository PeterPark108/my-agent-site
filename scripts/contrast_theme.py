#!/usr/bin/env python3
"""Đo tương phản WCAG của token theme trong css/style.css và css/intro3d.css.
Không phụ thuộc ngoài thư viện. Thoát 1 nếu cặp chữ thường < 4.5 hoặc nền nút chữ trắng < 4.5.
"""
import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent

def lin(c):
    c = c/255
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4

def parse_hex(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(x*2 for x in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def Lrgb(rgb):
    r, g, b = rgb
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)

def contrast(a, b):
    la, lb = Lrgb(a), Lrgb(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi+0.05)/(lo+0.05)

def block_vars(css, selector_marker):
    i = css.find(selector_marker)
    if i < 0:
        return {}
    j = css.find("{", i)
    k = css.find("}", j)
    body = css[j+1:k]
    out = {}
    for name, val in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+)", body):
        val = val.strip()
        m = re.fullmatch(r"#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})", val)
        if m:
            out[name] = parse_hex(m.group(0))
    return out

css = (ROOT/"css/style.css").read_text(encoding="utf-8")
dark = block_vars(css, ":root{")
light = dict(dark)
light.update(block_vars(css, "html[data-theme=light]{"))

def need(theme, name):
    if name not in theme:
        raise SystemExit("thiếu token " + name)
    return theme[name]

pairs = []
def add(theme_name, theme, fg, bg, minimum, note):
    pairs.append((theme_name, note, fg, bg, contrast(need(theme, fg), need(theme, bg)), minimum))

for label, th in (("tối", dark), ("sáng", light)):
    bg = "--bg"
    surface = "--bg2"
    add(label, th, "--text", bg, 4.5, "chữ chính / nền")
    add(label, th, "--text", surface, 4.5, "chữ chính / bề mặt")
    add(label, th, "--text-strong", bg, 4.5, "chữ đậm / nền")
    add(label, th, "--text-muted", bg, 4.5, "chữ phụ / nền")
    add(label, th, "--text-muted", surface, 4.5, "chữ phụ / bề mặt")
    add(label, th, "--text-subtle", bg, 4.5, "chữ mờ / nền")
    add(label, th, "--text-subtle", surface, 4.5, "chữ mờ / bề mặt")
    add(label, th, "--text-soft", bg, 4.5, "chữ mềm / nền")
    add(label, th, "--link", bg, 4.5, "liên kết / nền")
    add(label, th, "--link", surface, 4.5, "liên kết / bề mặt")
    add(label, th, "--info", bg, 4.5, "nhấn teal-info / nền")
    add(label, th, "--info", surface, 4.5, "nhấn teal-info / bề mặt")
    add(label, th, "--teal", bg, 4.5, "teal / nền")
    add(label, th, "--danger", bg, 4.5, "trạng thái lỗi / nền")
    add(label, th, "--danger-text", surface, 4.5, "chữ lỗi / bề mặt")
    add(label, th, "--ok", bg, 4.5, "trạng thái đạt / nền")
    add(label, th, "--warn", surface, 4.5, "trạng thái chờ / bề mặt")
    add(label, th, "--accent", surface, 4.5, "nhấn / bề mặt")
    add(label, th, "--on-accent", "--btn-from", 4.5, "chữ trắng / nền nút đầu")
    add(label, th, "--on-accent", "--btn-mid", 4.5, "chữ trắng / nền nút giữa")
    add(label, th, "--on-accent", "--accent-deep", 4.5, "chữ trắng / nền nút cuối")
    add(label, th, "--on-accent", "--blue", 4.5, "chữ trắng / xanh nút")
    add(label, th, "--on-accent", "--navy", 4.5, "chữ trắng / navy")
    add(label, th, "--on-accent", "--teal-deep", 4.5, "chữ trắng / teal nút")

# intro sáng: teal #0B6F67 trên nền #eef5fb, chữ trắng trên nút teal
intro = [
    ("sáng intro", "chữ teal / nền intro", "#0B6F67", "#eef5fb", 4.5),
    ("sáng intro", "chữ phụ intro", "#3d4d66", "#eef5fb", 4.5),
    ("sáng intro", "chữ chính intro", "#0b1a33", "#eef5fb", 4.5),
    ("sáng intro", "chữ trắng / nút teal", "#ffffff", "#0B6F67", 4.5),
    ("tối intro", "chữ chính intro", "#f4f8ff", "#050b1a", 4.5),
    ("tối intro", "chữ phụ intro", "#b4c2d8", "#050b1a", 4.5),
    ("tối intro", "teal sáng / nền intro", "#2ee6d6", "#050b1a", 4.5),
    ("tối intro", "chữ đậm / nút teal sáng", "#04121a", "#2ee6d6", 4.5),
]
fail = 0
rows = []
for theme, note, fg, bg, ratio, minimum in pairs:
    ok = ratio + 1e-9 >= minimum
    if not ok:
        fail += 1
    rows.append((ok, theme, note, ratio, minimum))
for theme, note, fg, bg, minimum in intro:
    ratio = contrast(parse_hex(fg), parse_hex(bg))
    ok = ratio + 1e-9 >= minimum
    if not ok:
        fail += 1
    rows.append((ok, theme, note, ratio, minimum))

print("| Đạt | Theme | Cặp | Tỷ lệ | Ngưỡng |")
print("|---|---|---|---:|---:|")
for ok, theme, note, ratio, minimum in rows:
    print(f"| {'đạt' if ok else 'TRƯỢT'} | {theme} | {note} | {ratio:.2f} | {minimum:.1f} |")
print()
print(f"{'OK' if not fail else 'FAIL'}: {len(rows)-fail}/{len(rows)} cặp đạt, {fail} trượt")
sys.exit(1 if fail else 0)
