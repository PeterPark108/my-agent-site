# Yêu cầu cấu hình máy chủ (nginx, prod-web-01) cho SEO và tốc độ

Agent web KHÔNG tự sửa máy chủ. Danh sách này để agent VPS thực hiện. Sau khi đổi: `nginx -t && systemctl reload nginx`.

1. **HTTPS và tên miền chuẩn:** `http://` → `https://` và `www.myagentvn.com` → `https://myagentvn.com` bằng **301** (giữ nguyên đường dẫn và query).
2. **HTTP/2** (và HTTP/3 nếu có): `listen 443 ssl http2;`.
3. **Nén:** bật `gzip on; gzip_types text/css application/javascript application/json image/svg+xml application/manifest+json text/xml application/xml text/plain;` (brotli nếu có module).
4. **Cache:**
   - `/assets/fonts/*.woff2`: `Cache-Control: public, max-age=31536000, immutable` (tên file font cố định theo phiên bản).
   - `/assets/` (ảnh, logo), `/css/`, `/js/`: `Cache-Control: public, max-age=604800` (7 ngày; chưa có fingerprint nên không để immutable).
   - `*.html`, `/sitemap.xml`, `/robots.txt`, `/data/orders.json`, `/js/config.js`: `Cache-Control: no-cache` (luôn kiểm tra lại, dùng ETag/Last-Modified).
5. **Trang 404:** `error_page 404 /404.html;` và `location = /404.html { internal; }` — phải trả mã **404** thật (không 200).
6. **MIME:** `.webmanifest` → `application/manifest+json`; `.woff2` → `font/woff2`; `.svg` → `image/svg+xml`; `.webp` → `image/webp`; `.xml` → `application/xml`.
7. **Header bảo mật:** `Strict-Transport-Security: max-age=31536000; includeSubDomains` (chỉ thêm `preload` khi chắc chắn), `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()`, `X-Frame-Options: SAMEORIGIN`.
8. **Không đặt `X-Robots-Tag`** cho toàn site (noindex chỉ nằm trong thẻ meta của trang tra cứu tiến độ và 404).
9. **Chặn file nội bộ:** trả 404 cho `/.git`, `/data/private/`, `/scripts/`, `/docs/`, `*.md`, `*.py`, `*.sh` (repo có các file này nhưng không cần public).
10. **Đường dẫn không đuôi (tuỳ chọn):** giữ URL `.html` như sitemap; nếu bật `try_files $uri $uri.html $uri/ =404;` thì canonical vẫn là bản `.html`.
11. Sau khi đổi, kiểm tra: `curl -sI https://myagentvn.com/` (thấy `content-encoding`, HSTS), `curl -sI https://myagentvn.com/khong-co` (mã 404), `curl -sI http://www.myagentvn.com/` (301 về apex).
