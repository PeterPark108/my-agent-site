#!/usr/bin/env bash
# Quy trình SEO cho web v6. Chạy từ thư mục gốc repo:
#   scripts/seo_v6.sh blog                  (sau khi thêm/sửa data/blog/*.md)
#   scripts/seo_v6.sh news [--check-urls]   (sau khi thêm/sửa data/news/*.md)
# 1) Dựng site cũ trong thư mục tạm (bản gốc LEGACY_BASE + scripts/data/docs hiện tại), chạy blog_publish.sh / news_publish.sh như trước.
# 2) Nhập blog/tin tức vừa dựng vào site-v6 (giao diện v6 + og/JSON-LD), build tĩnh, chép ra thư mục gốc.
# Xem docs/QUY-TRINH-SEO-V6.md.
set -euo pipefail
cd "$(dirname "$0")/.."; ROOT=$PWD
MODE=${1:-}; shift || true
case "$MODE" in blog|news) ;; *) echo "Dùng: scripts/seo_v6.sh blog|news [tham số news_publish]"; exit 2;; esac
BASE=${LEGACY_BASE:-64d947c80f02e206a647f796718a84d39eeca533}
command -v node >/dev/null || { echo "Thiếu Node.js >= 22"; exit 1; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
echo "== Dựng site cũ trong $T (gốc $BASE)"
git archive "$BASE" | tar -x -C "$T"
rm -rf "$T/scripts" "$T/data" "$T/docs"; cp -a scripts data docs VERSION "$T"/
mkdir -p "$T/assets"
cp -a assets/. "$T/assets/"
(cd "$T" && python3 scripts/news_build.py | tail -2 && python3 scripts/blog_build.py | tail -2 && python3 scripts/tech_pass.py >/dev/null \
  && git init -q && git add -A && git -c user.name=seo -c user.email=seo@localhost commit -qm base)
(cd "$T" && bash "scripts/${MODE}_publish.sh" "$@")
echo "== Chép dữ liệu/feed/sitemap về repo"
cp -a "$T/data/." data/
for f in blog/feed.xml tin-tuc/feed.xml sitemap.xml; do cp "$T/$f" "$f"; done
grep -q 'dieu-khoan-dich-vu.html' sitemap.xml || sed -i 's#</urlset>#  <url><loc>https://myagentvn.com/dieu-khoan-dich-vu.html</loc></url>\n</urlset>#' sitemap.xml
echo "== Đồng bộ feed vào site-v6/public (tránh export ghi đè feed cũ)"
mkdir -p site-v6/public/tin-tuc site-v6/public/blog
cp tin-tuc/feed.xml site-v6/public/tin-tuc/feed.xml
cp blog/feed.xml site-v6/public/blog/feed.xml
echo "== Nhập vào v6 và build tĩnh"
cd site-v6
[ -d node_modules ] || npm ci
node scripts/import-legacy.cjs "$T"
npm run lint >/dev/null
bash scripts/export-static.sh >/dev/null
cd "$ROOT"
echo "== Chép lại feed sau export (export có thể ghi đè từ public)"
cp "$T/tin-tuc/feed.xml" tin-tuc/feed.xml
cp "$T/blog/feed.xml" blog/feed.xml
cp tin-tuc/feed.xml site-v6/public/tin-tuc/feed.xml
cp blog/feed.xml site-v6/public/blog/feed.xml
echo "== Kiểm tra 200 các URL trong sitemap (máy chủ tạm)"
PORT=$((20000+RANDOM%20000)); python3 -m http.server $PORT >/dev/null 2>&1 & SP=$!; sleep 1; bad=0
for u in $(grep -o '<loc>[^<]*' sitemap.xml | sed 's#<loc>https://myagentvn.com##'); do c=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT$u"); [ "$c" = 200 ] || { echo "LỖI $c $u"; bad=1; }; done
for f in $(grep -o '<loc>[^<]*' sitemap.xml | sed 's#<loc>https://myagentvn.com/##' | grep -E '^(blog|tin-tuc)'); do grep -q '/_next/static' "$f" && grep -q 'application/ld+json' "$f" && grep -q 'og:title' "$f" || { echo "LỖI thiếu v6/og/JSON-LD: $f"; bad=1; }; done
kill $SP
[ $bad = 0 ] && echo "=> PASS: commit (git add -A) rồi mở PR như trước" || { echo "=> FAIL"; exit 1; }
