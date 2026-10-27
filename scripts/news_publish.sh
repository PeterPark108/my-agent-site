#!/usr/bin/env bash
# Dựng + kiểm tra mục Tin tức trong 1 lệnh. Chạy từ thư mục gốc repo:
#   scripts/news_publish.sh            (thêm --check-urls để kiểm tra link nguồn còn sống)
# In bảng PASS/FAIL; mã thoát 0 = sẵn sàng commit.
cd "$(dirname "$0")/.." || exit 1
declare -a NAMES RES; fail=0
step(){ local n="$1"; shift; echo "== $n"; if "$@"; then NAMES+=("$n"); RES+=(PASS); else NAMES+=("$n"); RES+=(FAIL); fail=1; fi; }
step "news_build (kiểm tra bài + dựng trang)" python3 scripts/news_build.py "$@"
if [ $fail = 0 ]; then
  step "tech_pass (SEO head, menu, sitemap)" python3 scripts/tech_pass.py
  snap=$(git status --porcelain=v1 -uall | md5sum; git diff | md5sum)
  python3 scripts/tech_pass.py >/dev/null
  step "tech_pass chạy lại không đổi gì" test "$snap" = "$(git status --porcelain=v1 -uall | md5sum; git diff | md5sum)"
  step "test_news (Markdown an toàn + validator)" python3 scripts/test_news.py
  step "ci_check (link nội bộ, dữ liệu)" bash -c 'python3 scripts/ci_check.py 2>/dev/null | tail -3; exit ${PIPESTATUS[0]}'
  step "seo_audit" python3 scripts/seo_audit.py
  step "feed.xml hợp lệ" python3 -c "import xml.etree.ElementTree as E;r=E.parse('tin-tuc/feed.xml').getroot();assert r.tag=='rss' and r.find('channel').findall('item')"
fi
echo; echo "===== KẾT QUẢ ====="
for i in "${!NAMES[@]}"; do printf '%-5s %s\n' "${RES[$i]}" "${NAMES[$i]}"; done
if [ $fail = 0 ]; then echo "=> PASS: có thể commit và mở PR"; else echo "=> FAIL: sửa lỗi ở trên rồi chạy lại"; fi
exit $fail
