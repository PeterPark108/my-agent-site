# Mục Tin tức công nghệ – hướng dẫn đăng bài

Dành cho người/agent viết bài (SEO My Agent). Mỗi bài = **1 file Markdown** trong `data/news/`, rồi chạy **1 lệnh**.
Đặc tả máy đọc được: `docs/tin-tuc-format.json`. File mẫu: `data/news/_template.md.example`.

## Cấu trúc URL
- `tin-tuc.html` – danh sách (12 tin/trang), các trang sau: `tin-tuc/trang-2.html`, `tin-tuc/trang-3.html`…
- `tin-tuc/chu-de/<chủ-đề>.html` – lọc theo chủ đề (chạy cả khi tắt JS), trang sau: `…/<chủ-đề>-trang-2.html`
- `tin-tuc/<slug>.html` – trang bài viết; `tin-tuc/feed.xml` – RSS 20 tin mới nhất; `tin-tuc/` chuyển về `tin-tuc.html`
- Trang chủ tự hiện 3 tin mới nhất. Sitemap, menu, chân trang, trợ lý MJ tự cập nhật.

## Các bước đăng 1 bài
```bash
cd my-agent-site                       # repo PeterPark108/my-agent-site, cần quyền push + gh đã đăng nhập
git fetch origin
git switch -c news/2026-10-28 origin/production
cp data/news/_template.md.example data/news/2026-10-28-ten-bai-khong-dau.md
# ... viết bài ...
scripts/news_publish.sh --check-urls  # phải ra "=> PASS"
git add -A
git commit -m "news: Tiêu đề bài"
git push -u origin news/2026-10-28
gh pr create --base production --head news/2026-10-28 --title "news: 2026-10-28" --body "Bài: ... Nguồn: ..."
```
Người duyệt (không tự merge nếu chưa được giao quyền duyệt):
```bash
gh pr merge <số-PR> --merge
git fetch origin && git push origin origin/production:main   # VPS tự kéo nhánh main khoảng 5 phút một lần
```
`production` được bảo vệ: bắt buộc qua PR. Nhiều bài trong ngày thì cho chung một nhánh/PR.

## Ví dụ file `data/news/2026-10-28-google-cap-nhat-tai-lieu-seo.md`
```markdown
---
title: "Google cập nhật tài liệu về dữ liệu có cấu trúc cho bài viết"
date: 2026-10-28
topic: web-seo
summary: "Google bổ sung hướng dẫn về dữ liệu có cấu trúc cho bài viết, làm rõ các trường nên khai báo. Bài tóm tắt điểm mới và việc chủ website nên kiểm tra."
insight: "Website có mục tin tức nên rà lại schema bài viết; sai trường thường không gây phạt nhưng làm mất cơ hội hiển thị đẹp."
tags: [google, schema]
sources:
  - name: Google Search Central
    url: https://developers.google.com/search/docs/appearance/structured-data/article
---
## Có gì mới
Nội dung tự viết, ≥ 250 từ...
```

## Quy tắc (script kiểm tra tự động, báo lỗi tiếng Việt)
| Trường | Bắt buộc | Quy tắc |
|---|---|---|
| tên file | ✓ | `YYYY-MM-DD-slug.md`, slug a-z 0-9 `-`, không trùng; ngày = `date` |
| `title` | ✓ | 20–70 ký tự, không trùng bài khác |
| `date` / `updated` | ✓ / – | `YYYY-MM-DD`, không ở tương lai; `updated` ≥ `date` |
| `topic` | ✓ | `ai`, `bao-mat`, `web-seo`, `du-lieu`, `nen-tang` |
| `summary` | ✓ | 120–200 ký tự, tự viết |
| `insight` | ✓ | 1–3 câu (40–400 ký tự) – khối "Góc nhìn My Agent" |
| `sources` | ✓ | ≥ 1 nguồn `name` + `url` https, không link affiliate/utm |
| `tags`, `image`+`image_alt`, `draft` | – | ảnh phải nằm trong `assets/news/` (png/jpg/webp); `draft: true` = không đăng |
| nội dung | ✓ | ≥ 250 từ, chỉ dùng `##`/`###` (không `#`), Markdown cơ bản; HTML bị hiển thị thành chữ, link `javascript:` bị chặn |

Cụm từ bị cấm ở mọi trường: "24/7", "FPT Polytechnic", "cam kết/đảm bảo/100% lên top", "top 1/trang 1" kiểu cam kết.

## Checklist trước khi mở PR
- [ ] Tin có thật, đã mở đọc nguồn gốc; ngày đúng; số liệu không bịa.
- [ ] Viết bằng lời của mình (không chép câu của nguồn); trích ngắn thì ghi nguồn.
- [ ] Có ít nhất 1 link nguồn gốc; `--check-urls` không báo `LỖI` (`CHẶN BOT?` thì mở tay bằng trình duyệt).
- [ ] Không hứa thứ hạng, không giá, không "24/7".
- [ ] `scripts/news_publish.sh` ra `=> PASS`.

## Ghi chú kỹ thuật
- `scripts/news_build.py`: kiểm tra + dựng mọi trang tin, RSS, khối trang chủ, chạy `chatbot_build.py`. Tuỳ chọn: `--validate-only`, `--check-urls`, `-v` (hiện cảnh báo của thẻ link cũ).
- `scripts/news_publish.sh` = news_build → tech_pass (2 lần, phải không đổi) → test_news → ci_check → seo_audit → kiểm tra feed.
- 10 tin cũ (trước v0.7.0) là `type: link`: chỉ có thẻ trỏ ra bài gốc, không có trang riêng. Bài mới mặc định `type: article`.
- Xoá file `.md` thì lần dựng sau tự xoá trang tương ứng. Không sửa tay các file HTML trong `tin-tuc/`.
