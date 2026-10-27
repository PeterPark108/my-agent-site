# Form liên hệ (lien-he.html) — cách hoạt động và phương án nhận form

## Tình trạng (27/10/2026)
- Form gửi tới FormSubmit.co (`https://formsubmit.co/ajax/<formEmail>`). Từ máy MJ và từ box của bot: kết nối TLS tới `formsubmit.co` thành công nhưng **không nhận được byte nào** (GET `/`, OPTIONS và POST `/ajax/vantungn044@gmail.com` đều hết thời gian chờ 20–25 giây, 0 byte). Không đọc được phản hồi "cần kích hoạt".
- Peter có nhận thư kích hoạt của FormSubmit nhưng bấm **Activate** thì trang FormSubmit báo **lỗi 500** → lỗi phía FormSubmit. **Không dựa vào FormSubmit làm kênh chính nữa.**
- Trước v0.9.3 code không có thời gian chờ nên nút treo ở "Đang gửi...".

## Front-end (js/main.js, cấu hình ở js/config.js)
| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `formEndpoint` | `''` | URL máy chủ nhận form riêng, vd `'/api/contact'` (POST JSON). Có giá trị → dùng nó, không gọi FormSubmit. |
| `formSubmitEnabled` | `true` | Chỉ dùng khi `formEndpoint` trống. `false` = không gọi FormSubmit, bấm gửi là hiện ngay khung dự phòng. |
| `formTimeoutMs` | `15000` | Thời gian chờ tối đa (AbortController). |
| `formEmail`, `zaloPhone` | | Dùng cho nút "Gửi qua Email" (mailto điền sẵn), "Nhắn Zalo", "Gọi ngay". |

Thứ tự: **máy chủ riêng (`formEndpoint`) → khung dự phòng Email/Zalo/Gọi**. Khi chưa bật máy chủ riêng: FormSubmit (tuỳ chọn) → khung dự phòng.
Lỗi (timeout, lỗi mạng, HTTP ≠ 2xx, JSON `success:false`/không có `success:true`/`ok:true`, "chờ kích hoạt") → hiện thông báo tiếng Việt + nút `mailto:` (tiêu đề + nội dung gồm họ tên, SĐT, email, dịch vụ, nội dung — kể cả số liệu điền sẵn từ công cụ tính giá), Zalo và `tel:`; nút gửi bật lại; **dữ liệu trong form giữ nguyên**; chặn gửi trùng khi đang gửi. Thành công vẫn hiện "Cảm ơn anh/chị!" như cũ. Honeypot `_honey` giữ nguyên.

Chuyển sang máy chủ riêng sau khi agent VPS triển khai xong = **sửa 1 dòng** trong js/config.js: `formEndpoint: '/api/contact',` rồi chạy `python3 scripts/tech_pass.py`.

Kiểm thử: `python3 scripts/test_contact_form.py` (Chromium, tự chạy máy chủ tĩnh; giả lập thành công/timeout/lỗi mạng/500/success:false/endpoint riêng; `SHOT=/thu-muc` để lưu ảnh). Dịch vụ mẫu: `python3 server/contact-api/test_contact_api.py`.

## Phương án CHÍNH: endpoint tự chạy trên VPS (chưa triển khai)
Mã mẫu ở `server/contact-api/` (Python 3 thư viện chuẩn, không cần pip): `contact_api.py`, `test_contact_api.py`, `contact-api.service`, `nginx-api-contact.conf`, `contact-api.env.example`. **Không** được deploy tự động (VPS chỉ phục vụ file tĩnh; thư mục `server/` không chứa bí mật).

### Hợp đồng API
`POST /api/contact`, `Content-Type: application/json`, body ≤ 16 KB:
```json
{"name":"Nguyễn Văn A","phone":"0328 439 972","email":"a@b.vn","service":"Thiết kế website","message":"...","consent":"Đồng ý","_honey":"","page":"https://myagentvn.com/lien-he.html"}
```
| Mã | Body | Khi nào |
|---|---|---|
| 200 | `{"ok":true,"id":"a1b2c3d4"}` | Đã gửi mail và/hoặc Telegram (ít nhất 1 kênh thành công) |
| 200 | `{"ok":true,"id":"-"}` | Honeypot có giá trị (bot) — không gửi gì |
| 400 | `{"ok":false,"error":"invalid","fields":["phone"]}` | Sai dữ liệu |
| 403 | `{"ok":false,"error":"origin"}` | Origin không thuộc myagentvn.com |
| 413 / 415 | `too_large` / `json_required` | Body quá lớn / không phải JSON |
| 429 | `{"ok":false,"error":"rate_limited"}` | Quá giới hạn |
| 502 | `{"ok":false,"error":"delivery_failed"}` | Không gửi được kênh nào → front-end hiện dự phòng |
`GET /api/contact/health` → `{"ok":true}` (chỉ cho 127.0.0.1 qua nginx).

### Kiểm tra dữ liệu / chống spam
- `name` 2–100 ký tự; `phone` khớp `[0-9 +().-]{8,20}` và ≥ 8 chữ số; `email` tuỳ chọn, đúng định dạng; `consent` bắt buộc; `service` ≤ 100, `message` ≤ 3000; bỏ ký tự điều khiển.
- Honeypot `_honey`; giới hạn 5 lần/10 phút/IP trong service + `limit_req` 6 lần/phút (burst 3) ở nginx; `client_max_body_size 16k`.
- CORS: cùng origin (form nằm trên myagentvn.com nên không cần CORS); service chỉ trả `Access-Control-Allow-Origin` cho `https://myagentvn.com`, `https://www.myagentvn.com`, từ chối origin khác.

### Cần gì ở VPS
- Python 3.8+ (có sẵn trên Ubuntu/Debian), user hệ thống `myagent-contact` (không shell), thư mục `/opt/myagent-contact-api/` (chỉ `contact_api.py`), file bí mật `/etc/myagent/contact-api.env` (chmod 600).
- systemd unit `myagent-contact-api.service` (mẫu `server/contact-api/contact-api.service`), lắng nghe **127.0.0.1:8787** (không mở ra ngoài, **không đụng cổng 80**).
- nginx: thêm `limit_req_zone` vào `http{}` và `location = /api/contact` vào server HTTPS (mẫu `nginx-api-contact.conf`).

### Gửi thông báo
| Cách | Ưu | Nhược |
|---|---|---|
| Gmail SMTP + App Password | Miễn phí, gửi thẳng tới Gmail của Peter | Cần bật xác minh 2 bước; mật khẩu ứng dụng gắn với tài khoản cá nhân; giới hạn ~500 thư/ngày; Google có thể chặn đăng nhập từ IP VPS |
| **Brevo SMTP (khuyến nghị)** | Gói free 300 thư/ngày, SMTP chuẩn (smtp-relay.brevo.com:587), không dùng mật khẩu Gmail, xác thực tên miền myagentvn.com (SPF/DKIM) → ít vào spam | Cần tạo tài khoản + thêm bản ghi DNS |
| Mailgun / Resend free | API tốt | Mailgun free hạn chế/cần thẻ; Resend free 100 thư/ngày, cần xác thực tên miền |
**Khuyến nghị:** Brevo SMTP (miễn phí đủ dùng, tách khỏi tài khoản Gmail cá nhân, có DKIM cho tên miền) + **Telegram bot** làm kênh thứ hai (BotFather tạo bot → `TELEGRAM_BOT_TOKEN`; Peter nhắn bot rồi lấy `TELEGRAM_CHAT_ID`). Service gửi cả hai; chỉ cần 1 kênh thành công là trả 200. Bí mật chỉ nằm trong `/etc/myagent/contact-api.env` trên VPS, không vào repo.

### Checklist triển khai cho agent VPS (9f628461-e88c-485f-b02f-55a599f871de)
1. Peter tạo tài khoản Brevo (hoặc App Password Gmail) + bot Telegram, đưa bí mật trực tiếp cho agent VPS (không qua repo/chat công khai).
2. `useradd -r -s /usr/sbin/nologin myagent-contact`; copy `contact_api.py` → `/opt/myagent-contact-api/`; tạo `/etc/myagent/contact-api.env` từ `.env.example` (chmod 600).
3. Chạy `python3 test_contact_api.py` trên VPS; cài unit, `systemctl enable --now myagent-contact-api`; `curl -s 127.0.0.1:8787/api/contact/health`.
4. Thêm khối nginx vào server HTTPS, `nginx -t && systemctl reload nginx`.
5. Thử: `curl -s -X POST https://myagentvn.com/api/contact -H 'Content-Type: application/json' -d '{"name":"TEST My Agent bot - bỏ qua","phone":"0000000000","consent":"1"}'` → 200 và Peter nhận 1 thư + 1 tin Telegram; thử sai SĐT → 400; gửi 7 lần liên tiếp → 429.
6. Mở PR đổi `formEndpoint: '/api/contact'` trong js/config.js (chờ Peter duyệt), chạy test_contact_form, deploy, gửi thử 1 lần trên web thật.
### Rollback
- Front-end: đặt lại `formEndpoint: ''` (và `formSubmitEnabled: false` nếu FormSubmit vẫn lỗi) → khách vẫn có khung Email/Zalo/Gọi.
- VPS: xoá `location /api/contact`, `nginx -t && reload`; `systemctl disable --now myagent-contact-api`.

## Phương án khác (chỉ đề xuất, chưa đăng ký)
- Web3Forms (free 250 lần/tháng, cần access key) hoặc Formspree (free 50 lần/tháng): đổi `formEndpoint` + định dạng body; phụ thuộc bên thứ ba như FormSubmit.
