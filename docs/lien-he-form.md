# Form liên hệ (lien-he.html) — cách hoạt động và phương án nhận form

## Tình trạng (27/10/2026)
- Form gửi tới FormSubmit.co (`https://formsubmit.co/ajax/<formEmail>`). Từ máy MJ và từ box của bot: kết nối TLS tới `formsubmit.co` thành công nhưng **không nhận được byte nào** (GET `/`, OPTIONS và POST `/ajax/vantungn044@gmail.com` đều hết thời gian chờ 20–25 giây, 0 byte). Không đọc được phản hồi "cần kích hoạt".
- Peter có nhận thư kích hoạt của FormSubmit nhưng bấm **Activate** thì trang FormSubmit báo **lỗi 500** → lỗi phía FormSubmit. **Không dựa vào FormSubmit làm kênh chính nữa.**
- Trước v0.9.3 code không có thời gian chờ nên nút treo ở "Đang gửi...".

## Luồng mới (Peter quyết 27/10): khách gửi → thẳng về Telegram của Peter
Khách bấm gửi → `POST /api/contact` (JSON) trên myagentvn.com → nginx → service `127.0.0.1:8787` → Telegram Bot API `sendMessage` tới chat của Peter.
Nếu **không gửi được trong 5 giây** hoặc có bất kỳ lỗi nào → báo lỗi + 3 nút dự phòng: **Gửi qua Email** (mailto điền sẵn), **Nhắn Zalo**, **Gọi ngay**.
FormSubmit **tắt hoàn toàn** (`formSubmitEnabled:false`, không có request nào tới formsubmit.co).

> **Cache:** nginx cache js/css 7 ngày theo `?v=VERSION`. Mỗi lần đổi nội dung js/css phải **bump VERSION** rồi chạy `python3 scripts/tech_pass.py` (ci_check báo lỗi nếu js/css khác tag phát hành gần nhất mà VERSION chưa đổi). Không bao giờ để một `?v=` trỏ tới hai nội dung khác nhau (sự cố v0.9.3: trình duyệt giữ main.js cũ).

## Front-end (js/main.js, cấu hình ở js/config.js)
| Khoá | Giá trị | Ý nghĩa |
|---|---|---|
| `formEndpoint` | `'/api/contact'` | Máy chủ nhận form trên VPS. Chỉ coi là gửi thành công khi trả **HTTP 2xx + Content-Type JSON + `{"ok":true}`**. |
| `formSubmitEnabled` | `false` | `true` chỉ có tác dụng khi `formEndpoint` = `''` (dùng lại FormSubmit). |
| `formTimeoutMs` | `5000` | Chờ tối đa 5 giây (AbortController). |
| `formEmail`, `zaloPhone` | | Cho nút Email (mailto), Zalo, Gọi ngay. |

Mọi trường hợp khác (404/405 HTML của nginx, 200 HTML trang tĩnh, JSON `ok:false`, 5xx, lỗi mạng, hết 5 giây) → thông báo lỗi + 3 nút; nút gửi bật lại; **dữ liệu giữ nguyên**; chặn gửi trùng; **không bao giờ hiện "Cảm ơn"**. Mailto gồm họ tên, SĐT, email, dịch vụ, nội dung (kể cả số liệu từ công cụ tính giá). Body JSON gửi thêm `estimate` (giá trị `?tam-tinh=` nếu có).

Hiện tại (27/10, trước khi VPS bật endpoint) `POST https://myagentvn.com/api/contact` trả **HTTP 404, `text/html`** (trang 404 của site, ~1,2 s) → khách thấy ngay 3 nút dự phòng. Sau khi agent VPS bật endpoint, form tự hoạt động, không cần sửa front-end.

Kiểm thử: `python3 scripts/test_contact_form.py` (Chromium, ~30 s, timeout 5 s thật; `SHOT=/thu-muc` để lưu ảnh). Dịch vụ: `python3 server/contact-api/test_contact_api.py` (Telegram giả lập, chạy trong ci_check).

## Máy chủ nhận form trên VPS (chưa triển khai)
Mã mẫu `server/contact-api/` (Python 3.8+ thư viện chuẩn, không cần pip): `contact_api.py`, `test_contact_api.py`, `contact-api.service`, `nginx-api-contact.conf`, `contact-api.env.example`. Không deploy tự động; repo không chứa bí mật.

### Hợp đồng API
`POST /api/contact`, `Content-Type: application/json`, body ≤ 16 KB:
```json
{"name":"Nguyễn Văn A","phone":"0328 439 972","email":"a@b.vn","service":"Thiết kế website","message":"...","consent":"Đồng ý","_honey":"","page":"https://myagentvn.com/lien-he.html","estimate":"7.200.000đ"}
```
| Mã | Body | Khi nào |
|---|---|---|
| 200 | `{"ok":true,"id":"a1b2c3d4"}` | Telegram `sendMessage` trả `ok:true` |
| 200 | `{"ok":true,"id":"-"}` | Honeypot có giá trị (bot) — không gửi gì |
| 400 | `{"ok":false,"error":"invalid","fields":["phone"]}` | Sai dữ liệu |
| 403 | `{"ok":false,"error":"origin"}` | Origin không phải myagentvn.com |
| 413 / 415 | `too_large` / `json_required` | Body quá lớn / không phải JSON |
| 429 | `{"ok":false,"error":"rate_limited"}` | Quá giới hạn |
| 502 | `{"ok":false,"error":"delivery_failed"}` | Telegram lỗi/chưa cấu hình/hết 4 s |
`GET /api/contact/health` → `{"ok":true}` (chỉ 127.0.0.1).

### Tin nhắn Telegram
`parse_mode=HTML`, mọi giá trị được `html.escape`; gồm: Tên, SĐT, Email, Dịch vụ, Tạm tính (nếu có), Trang nguồn, Thời gian (Asia/Ho_Chi_Minh), Nội dung; cắt ≤ 4096 ký tự (cắt trên văn bản gốc, thêm "…"). Gọi Telegram tối đa 4 s (`TELEGRAM_TIMEOUT`) để cả chuỗi < 5 s.

### Kiểm tra dữ liệu / chống spam
- `name` 2–100; `phone` `[0-9 +().-]{8,20}` và ≥ 8 chữ số; `email` tuỳ chọn; `consent` bắt buộc; `message` ≤ 3000; bỏ ký tự điều khiển.
- Honeypot `_honey`; 5 lần/10 phút/IP trong service + nginx `limit_req` 6/phút (burst 3); `client_max_body_size 16k`; chỉ POST/OPTIONS.
- Cùng origin (không cần CORS); service chỉ chấp nhận Origin `https://myagentvn.com`, `https://www.myagentvn.com`.

### Cần gì ở VPS
- Python 3.8+, user `myagent-contact` (nologin), `/opt/myagent-contact-api/contact_api.py`, `/etc/myagent/contact-api.env` (chmod 600: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`).
- systemd `myagent-contact-api.service`, lắng nghe **127.0.0.1:8787** (không mở ra ngoài, **không đụng cổng 80**).
- nginx: `limit_req_zone` trong `http{}` + `location = /api/contact` trong server HTTPS (mẫu `nginx-api-contact.conf`, `proxy_read_timeout 6s`).

### Peter tạo bot Telegram (chỉ hướng dẫn — bot chưa tạo)
1. Trên Telegram mở **@BotFather** → `/newbot` → đặt tên (vd "My Agent Website") và username kết thúc bằng `bot` → BotFather trả **token** dạng `123456:ABC...`.
2. Mở bot vừa tạo và gửi **`/start`** (bắt buộc, nếu không bot không nhắn được cho anh).
3. Lấy **chat id**: mở `https://api.telegram.org/bot<TOKEN>/getUpdates` trong trình duyệt → tìm `"chat":{"id":123456789` (hoặc để agent VPS chạy lệnh này trên VPS).
4. Gửi **token + chat id trực tiếp cho agent VPS** (không dán vào repo, PR hay nhóm chat). Token lộ thì vào @BotFather → `/revoke` để đổi.

### Checklist cho agent VPS (9f628461-e88c-485f-b02f-55a599f871de)
1. Nhận token + chat id từ Peter; `useradd -r -s /usr/sbin/nologin myagent-contact`; copy `contact_api.py` → `/opt/myagent-contact-api/`; tạo `/etc/myagent/contact-api.env` từ `.env.example` (chmod 600).
2. `python3 test_contact_api.py` trên VPS (Telegram giả lập) → OK.
3. Cài unit, `systemctl enable --now myagent-contact-api`; `curl -s 127.0.0.1:8787/api/contact/health` → `{"ok":true}`.
4. **Bật:** thêm khối nginx vào server HTTPS, `nginx -t && systemctl reload nginx`.
5. **Kiểm tra:** `curl -s -X POST https://myagentvn.com/api/contact -H 'Content-Type: application/json' -H 'Origin: https://myagentvn.com' -d '{"name":"TEST My Agent bot - bỏ qua","phone":"0000000000","consent":"1"}'` → `{"ok":true,...}` và Peter nhận 1 tin Telegram; SĐT sai → 400; 7 lần liên tiếp → 429; gửi thử 1 lần trên lien-he.html → "Cảm ơn anh/chị!".
6. **Dự phòng còn chạy:** `systemctl stop myagent-contact-api` → gửi thử trên web → trong ≤ 5 s hiện lỗi + 3 nút (nginx trả 502) → `systemctl start` lại.
### Rollback
- VPS: xoá `location /api/contact`, `nginx -t && reload`; `systemctl disable --now myagent-contact-api`. Front-end không cần sửa: 404 → 3 nút dự phòng.
- Front-end (nếu cần): `formEndpoint: ''` → bấm gửi là hiện ngay 3 nút (FormSubmit vẫn tắt).

## Kênh khác (chỉ đề xuất, không dùng)
- Email (Brevo SMTP / Gmail App Password) có thể thêm sau làm kênh phụ; hiện bỏ để đơn giản.
- FormSubmit: lỗi (treo, 500 khi kích hoạt) — để tắt. Web3Forms/Formspree: cần tài khoản bên ngoài, chưa đăng ký.
