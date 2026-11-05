# Quy trình SEO My Agent trên web v6

Từ bản 0.10.0, web chính thức là bản v6 (Next.js, mã nguồn ở `site-v6/`, xuất tĩnh ra thư mục gốc). SEO vẫn viết bài bằng Markdown như cũ. Chỉ khác ở **lệnh dựng**: dùng `scripts/seo_v6.sh` thay cho `blog_publish.sh` / `news_publish.sh`.

## Môi trường cần có (máy chạy cron/SEO)
- Python 3 (như trước), git, curl.
- **Node.js ≥ 22 và npm** (mới). Lần đầu chạy, script tự gọi `npm ci` trong `site-v6/` (cần mạng). Sau đó dùng lại `site-v6/node_modules`; không commit thư mục này.
- Cổng 8899 trên máy phải trống (bước `ci_check` cũ dùng cổng này).
- Lịch sử git phải có commit gốc `64d947c` (biến `LEGACY_BASE`). Clone bình thường là có; clone `--depth 1` thì không có, phải `git fetch --unshallow`.

## Bài blog mới (PR cần Peter gõ "Duyệt PR #xx")
```
git checkout production && git pull --ff-only
git checkout -b blog/YYYY-MM-DD-<slug>
# viết data/blog/<slug>.md (mẫu data/blog/_template.md.example)
scripts/seo_v6.sh blog
git add -A && git commit -m "Blog: <tiêu đề>"
git push -u origin HEAD   # mở PR nháp như trước, chờ Duyệt
```

## Tin tức mới (data/news, SEO tự merge như trước)
```
git checkout production && git pull --ff-only
git checkout -b news/YYYY-MM-DD-<slug>
# viết data/news/YYYY-MM-DD-<slug>.md (mẫu data/news/_template.md.example)
scripts/seo_v6.sh news --check-urls
git add -A && git commit -m "Tin: <tiêu đề>"
git push -u origin HEAD   # mở PR, tự merge như trước
```

## Script làm gì (theo thứ tự)
1. Dựng site cũ trong thư mục tạm: bản gốc `64d947c` + `scripts/`, `data/`, `docs/` hiện tại, rồi chạy `news_build.py`, `blog_build.py`, `tech_pass.py`.
2. Chạy `blog_publish.sh` hoặc `news_publish.sh` cũ (validator, idempotent, test, ci_check, seo_audit, feed). Bước nào FAIL thì dừng, repo không bị sửa.
3. Chép về repo: `data/`, `blog/feed.xml`, `tin-tuc/feed.xml`, `sitemap.xml` (tự giữ `dieu-khoan-dich-vu.html`).
4. `site-v6/scripts/import-legacy.cjs`: chép HTML blog/tin tức vào `site-v6/content/source`, thêm route vào `site-v6/docs/LEGACY-INVENTORY.json`, chuyển sang khung v6 bằng `migrate-pages.cjs` (chỉ các route blog/tin tức), gộp vào `src/content/pages.json` và lấy og/twitter/JSON-LD vào `src/content/seo.json`.
5. `npm run lint`, rồi `site-v6/scripts/export-static.sh` (build và chép ra thư mục gốc).
6. Mở máy chủ tạm, kiểm tra mọi URL trong sitemap trả 200, và mỗi trang blog/tin tức có giao diện v6, og:title và JSON-LD. In `=> PASS` hoặc `=> FAIL`.

Lưu ý: không sửa tay file HTML ở thư mục gốc. Mọi thay đổi đi qua Markdown, sau đó chạy lại script. Chạy lại khi không có gì mới thì không ra thay đổi nào.

## Kiểm tra thêm trước khi mở PR
```
git status --short          # chỉ thấy bài mới, blog.html/tin-tuc.html, trang liên quan, sitemap, feed, site-v6/content, _next
python3 -m http.server 8811 # mở http://localhost:8811/blog/<slug>.html xem giao diện
```

## Rollback
- Bài chưa merge: đóng PR, xoá nhánh.
- Bài đã merge: `git revert <merge-sha>` trên nhánh mới rồi mở PR (blog cần Duyệt). Đường dẫn bài cũ vẫn có trong `content/source` nên không 404 sau khi dựng lại.
- Quay hẳn về web cũ: production trước v6 là `64d947c80f02e206a647f796718a84d39eeca533`. Việc này phải để VPS làm theo quy trình rollback, sau khi Peter đồng ý.

## Phần không đổi
`blog_build.py`, `news_build.py`, `tech_pass.py`, `*_publish.sh`, định dạng Markdown, cách đặt tên nhánh/PR, quy tắc merge (tin tự merge, blog chờ "Duyệt PR #xx").
