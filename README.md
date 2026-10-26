# My Agent – website tĩnh (GitHub Pages)

Live: https://peterpark108.github.io/my-agent-site/ (deploy từ nhánh `main`, thư mục gốc).

## Cấu hình (một chỗ duy nhất): `js/config.js`
- `siteUrl` – URL gốc; dùng cho canonical / og / sitemap / robots / JSON-LD. Đổi bằng `scripts/set-domain.sh <domain>`.
- `formEmail` – email nhận form liên hệ qua [FormSubmit.co](https://formsubmit.co) (không cần tài khoản). Lần gửi form đầu tiên, FormSubmit gửi mail kích hoạt tới email này → bấm **Activate Form**; sau đó mọi yêu cầu sẽ về hộp thư. Khi còn `PETER_EMAIL_HERE`, form báo "chưa cấu hình".
- `zaloPhone` – số Zalo (link `https://zalo.me/<số>` dưới form). Còn `PHONE_HERE` thì ẩn link.
- `gaId` – GA4 Measurement ID. `G-XXXXXXXXXX` = tắt. Khi bật, cân nhắc thêm banner đồng ý cookie (NĐ 13/2023/NĐ-CP, GDPR nếu có khách EU).

## Scripts
- `python3 scripts/tech_pass.py` – idempotent: chèn thẻ SEO/OG/icon/manifest vào `<head>` (khối `<!-- tech:head -->`), nối form, sinh `sitemap.xml` + `robots.txt`. Chạy lại sau khi thêm/sửa trang (kể cả sau khi chạy lại `gen.py`).
- `python3 scripts/check_links.py http://localhost:8000/` – kiểm tra link/ảnh/anchor hỏng.
- `scripts/set-domain.sh myagent.vn` – chuyển sang tên miền riêng (xem `docs/tro-ten-mien.md`). `CNAME.example` chỉ là mẫu; đừng commit `CNAME` trước khi DNS trỏ đúng.

## Tài nguyên & giấy phép
Phông Be Vietnam Pro, JetBrains Mono (SIL OFL 1.1, tự host trong `assets/fonts`, kèm file giấy phép). Biểu tượng SVG vẽ theo phong cách Lucide (ISC). Chi tiết: `ghi-nguon.html`.
