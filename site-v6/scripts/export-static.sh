#!/usr/bin/env bash
# Build Next.js v6 thành web tĩnh và chép ra thư mục gốc repo (nơi VPS phục vụ bằng git pull).
# Dùng: (cd site-v6 && npm ci && bash scripts/export-static.sh)
set -euo pipefail
cd "$(dirname "$0")/.."
npm run build
OUT=.next-v5
# Next xuất route "x.html" thành file "x.html.html" + thư mục "x.html/" (RSC). Đổi lại đúng URL cũ.
find "$OUT" -name '*.html.html' | while read -r f; do d="${f%.html}"; rm -rf "$d"; mv "$f" "$d"; done
# Keep fresh RSC payloads next to HTML. Deleting them leaves stale metadata
# from the previous export in the repository root.
ROOT=..
# Retain prior content-addressed assets so cached HTML can still hydrate.
# Old live bundles may contain owner edits; the new build uses new hashes.
cp -a "$OUT"/. "$ROOT"/

echo "Đã xuất web tĩnh v6 ra thư mục gốc repo."
