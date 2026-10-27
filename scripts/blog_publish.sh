#!/usr/bin/env bash
# Dựng + kiểm tra mục Blog / Kiến thức trong 1 lệnh. Chạy từ thư mục gốc repo:
#   scripts/blog_publish.sh
# In bảng PASS/FAIL; mã thoát 0 = sẵn sàng commit và mở PR.
cd "$(dirname "$0")/.." || exit 1
declare -a NAMES RES; fail=0
step(){ local n="$1"; shift; echo "== $n"; if "$@"; then NAMES+=("$n"); RES+=(PASS); else NAMES+=("$n"); RES+=(FAIL); fail=1; fi; }
step "blog_build (kiểm tra bài + dựng trang)" python3 scripts/blog_build.py
if [ $fail = 0 ]; then
  step "tech_pass (SEO head, menu, sitemap)" python3 scripts/tech_pass.py
  snap=$(git status --porcelain=v1 -uall | md5sum; git diff | md5sum)
  python3 scripts/blog_build.py >/dev/null && python3 scripts/tech_pass.py >/dev/null
  step "chạy lại không đổi gì (idempotent)" test "$snap" = "$(git status --porcelain=v1 -uall | md5sum; git diff | md5sum)"
  step "test_blog (validator + dựng thử)" python3 scripts/test_blog.py
  step "test_news" python3 scripts/test_news.py
  step "ci_check (link nội bộ, dữ liệu, sitemap)" bash -c 'python3 scripts/ci_check.py 2>/dev/null | tail -3; exit ${PIPESTATUS[0]}'
  step "seo_audit" python3 scripts/seo_audit.py
  step "blog/feed.xml hợp lệ" python3 -c "import xml.etree.ElementTree as E;r=E.parse('blog/feed.xml').getroot();assert r.tag=='rss' and r.find('channel') is not None"
fi
echo; echo "===== KẾT QUẢ ====="
for i in "${!NAMES[@]}"; do printf '%-5s %s\n' "${RES[$i]}" "${NAMES[$i]}"; done
if [ $fail = 0 ]; then echo "=> PASS: có thể commit và mở PR"; else echo "=> FAIL: sửa lỗi ở trên rồi chạy lại"; fi
exit $fail
