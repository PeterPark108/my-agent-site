# Blog / Kiến thức – cách thêm bài

Mục Blog (`blog.html`, `blog/<slug>.html`) là bài **hướng dẫn / kiến thức do My Agent tự viết**. Khác Tin tức (`tin-tuc/`): không bắt buộc nguồn ngoài, không có "Góc nhìn". Mỗi bài = **1 file Markdown**; bộ dựng sinh ra mọi thứ còn lại.

## URL & những gì được sinh tự động
| Thứ | Ở đâu |
|---|---|
| Danh sách | `blog.html` (mới nhất trước; `blog/` tự chuyển về đây) |
| Bài viết | `blog/<slug>.html` (slug = tên file) |
| RSS | `blog/feed.xml` (20 bài mới nhất) |
| Menu/footer | mục "Blog" trên menu, "Blog / Kiến thức" ở footer |
| SEO | canonical, OG (og:type article), breadcrumb hiển thị + BreadcrumbList, Article JSON-LD, sitemap (lastmod = updated/date) |
| Trong bài | mục lục (khi có ≥2 tiêu đề `##`), Dịch vụ liên quan + nút Liên hệ, bài mới hơn/cũ hơn, Bài liên quan (cùng chuyên mục/tag) |
| Trợ lý MJ | bài được đưa vào `data/chatbot-kb.json` |

**Khi chưa có bài nào:** `blog.html` hiện "Bài viết đầu tiên sắp ra mắt" và được đặt **`noindex, follow` + không có trong sitemap** (tránh Google index trang mỏng). Khi có ≥1 bài, `noindex` tự gỡ và trang vào sitemap. Sitemap chỉ chứa bài có file thật (ci_check kiểm tra).

## Các bước (SEO My Agent)
```bash
git checkout dev && git pull --ff-only
cp data/blog/_template.md.example data/blog/<slug>.md   # rồi sửa nội dung
scripts/blog_publish.sh                                  # phải in "=> PASS"
git add -A && git -c user.name="My Agent Bot" -c user.email="bot@users.noreply.github.com" commit -m "blog: <tiêu đề>"
git push origin dev
gh pr create --base production --head dev --title "blog: <tiêu đề>" --body "Bài mới: blog/<slug>.html"
```
Không tự merge: người duyệt (Peter) merge PR, rồi `git push origin origin/production:main` để lên site.
Ảnh (tuỳ chọn): đặt file png/jpg/webp vào `assets/blog/` (nên ≤ 200 KB, ngang 1200px), khai báo `image` + `image_alt`.

## Front-matter
Nằm giữa hai dòng `---` ở đầu file. Chuỗi có dấu `:` hoặc `#` thì đặt trong ngoặc kép. Danh sách dạng `[a, b]`.

| Trường | Bắt buộc | Quy tắc |
|---|---|---|
| `title` | có | 20–70 ký tự, không trùng bài khác; là H1 + tiêu đề trang |
| `date` | có | `YYYY-MM-DD`, ngày có thật, không ở tương lai |
| `updated` | không | `YYYY-MM-DD`, không trước `date` |
| `description` | có | 110–155 ký tự, không trùng; là meta description + lead |
| `category` | có | `website` · `seo` · `marketing` · `du-lieu` · `ai` |
| `services` | có | 1–4 slug trang `dich-vu/<slug>.html` có thật, vd `[thiet-ke-website, seo-tong-the]` |
| `tags` | không | danh sách từ khóa |
| `slug` | không | nếu ghi thì phải trùng tên file |
| `image`, `image_alt` | không | ảnh trong `assets/blog/`; có `image` thì bắt buộc `image_alt` |
| `draft` | không | `true` = bỏ qua, chưa đăng |

Trường khác = lỗi. Tên file: `data/blog/<slug>.md`, slug chỉ `a-z 0-9 -`, không dấu, không trùng (`index`, `feed` bị cấm).

Slug dịch vụ hợp lệ: thiet-ke-website, hosting-seo, ten-mien, email-doanh-nghiep, cham-soc-website, seo-tong-the, quang-cao-google-facebook, traffic-user, google-maps, video-ai, cham-soc-fanpage, zalo-oa-mini-app, profile-doanh-nghiep, phan-tich-du-lieu, ky-thuat-du-lieu, phan-mem-noi-bo, thiet-ke-app, bo-cong-thuong.

## Markdown được phép
`##` / `###` (không dùng `#` – H1 là title), đoạn văn, `**đậm**`, `*nghiêng*`, `` `code` ``, danh sách `-` / `1.`, `> trích dẫn`, khối ```` ``` ````, bảng `| a | b |`, `---`, link `[chữ](https://...)` hoặc link nội bộ `../dich-vu/x.html`, ảnh `![mô tả](../assets/blog/x.webp)` (bắt buộc mô tả). HTML thô bị escape; `javascript:`, `data:`, `//` bị chặn. Tối thiểu **300 từ**.

## Quy tắc viết (validator chặn tự động)
- Tiếng Việt có dấu, lời của My Agent, hướng dẫn thực tế.
- **Không** "24/7", "24/24", "24h"; **không** cam kết/đảm bảo top, thứ hạng, "top 1", "lên trang 1"; **không** "FPT Polytechnic".
- **Không bịa giá, khách hàng, số liệu.** Mọi đoạn có số đi kèm `%`, `triệu`, `tỷ`, `nghìn`, `đ/đồng/VNĐ/USD`, `khách hàng`, `doanh nghiệp`, `dự án` phải ghi rõ "ví dụ"/"giả định"/"minh hoạ" **hoặc** có link nguồn `https://` trong cùng đoạn. (Số thường như "3 bước", "10 phút" không sao.)
- Không trùng title/description với bài khác.

## Kiểm tra
`scripts/blog_publish.sh` chạy: blog_build → tech_pass → chạy lại (phải không đổi) → test_blog → test_news → ci_check → seo_audit → kiểm tra RSS, in bảng PASS/FAIL. Lỗi in bằng tiếng Việt kèm tên file. Chạy lẻ: `python3 scripts/blog_build.py --validate-only`.
Nếu sửa trợ lý MJ: `python3 scripts/chatbot_eval.py` (cần Chromium/Playwright).

## Checklist trước khi mở PR
- [ ] `scripts/blog_publish.sh` in PASS
- [ ] Mở `blog/<slug>.html` xem thử (máy tính + điện thoại)
- [ ] Không có số liệu/giá chưa đánh dấu, không hứa hẹn thứ hạng
- [ ] PR vào `production`, không tự merge
