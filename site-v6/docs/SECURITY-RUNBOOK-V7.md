# Cấu hình và vận hành v7

## Chạy thử an toàn

Node 22+, `npm ci`, `npm run dev`. Dev wrapper chỉ dịch cờ host/port để chạy được cả local và preview quản lý. Không có backend mặc định. Contact và tracking thật không gửi đi khi chưa cấu hình. PDF local dùng giới hạn trong bộ nhớ.

Production: `npm run build`, đặt biến server qua hosting, `npm start`. Không dùng dev wrapper cho production. Đặt MYAGENT_PUBLIC_ORIGIN là origin public chính xác, gồm scheme; không có dấu / cuối. Nếu reverse proxy giữ Host và protocol đúng thì có thể để trống trong local preview.

## Biến server

- MYAGENT_BACKEND_ORIGIN: origin HTTPS của backend riêng được kiểm soát, khác frontend, không chuyển hướng.
- MYAGENT_TRACKING_API_TOKEN: token chỉ ở server; backend phải xác minh token này trước khi truy vấn đơn.
- MYAGENT_REDIS_REST_URL / MYAGENT_REDIS_REST_TOKEN: REST Redis HTTPS hỗ trợ EVAL, SET NX EX, DEL. Dùng quyền tối thiểu cho prefix myagent. Test mã giả lập đã qua, chưa xác minh dịch vụ thật.
- MYAGENT_TRUSTED_IP_HEADER: chỉ đặt khi edge tin cậy ghi đè header này và không cho client đi vòng edge. Để trống dùng một bucket chung toàn khách, an toàn nhưng có thể hạn chế nhầm khách thật.
- MYAGENT_LOCAL_QA=1: chỉ phục vụ kiểm thử local, bỏ yêu cầu Redis. Tuyệt đối không đặt trong production.

Thiếu Redis trong production trả 503; Redis lỗi cũng từ chối thay vì chuyển sang in-memory. Mỗi loại API có bucket tổng và bucket khách; contact 5/phút, tracking 5/phút, quote 8/phút; tổng quote 60/phút, contact/tracking 120/phút. Điều chỉnh dựa trên traffic thật. Quote tối đa 2 yêu cầu/tiến trình, contact/tracking 4.

## Hợp đồng tra cứu mới

Frontend → POST /api/tracking, JSON `{ "code": "<mã truy cập ngẫu nhiên>" }`. Không truyền mã bằng URL. Mã dài 24–128 ký tự base64url; độ dài không chứng minh entropy. Backend phải sinh bằng bộ sinh ngẫu nhiên mật mã, tối thiểu 128 bit, gắn một đơn, lưu hash/HMAC có khóa riêng, cho phép thu hồi/thay mã. Không log mã hoặc body.

Ứng dụng → backend POST /api/tracking, Authorization Bearer token server, body chứa code. Backend tra bằng hash của code và chỉ trả bản ghi được phép. Phản hồi thành công:

```json
{"ok":true,"order":{"percent":60,"status":"Đang thực hiện","updated":"2026-11-05","note":"Ghi chú được duyệt cho khách","steps":["done","done","current","pending","pending"]}}
```

Không tìm thấy/không được phép trả 404 với thông báo chung. API gateway tiếp tục bỏ mọi trường ngoài percent/status/updated/note/steps; không tự suy luận field `note` là an toàn nếu backend gửi nhầm ghi chú nội bộ. Backend cần phân biệt customerNote/internalNote trước khi tạo projection.

Không nối /data/orders.json cũ vào luồng mới. Không gói tệp đơn hàng, mã truy cập thật hoặc token vào repo/public/ZIP. Thông tin nhạy cảm hơn tiến độ cơ bản cần xác thực bổ sung và review riêng.

## Contact

Backend /api/contact nhận schema cũ, chỉ xác nhận thành công bằng `{ok:true}`. Có consent bắt buộc, giới hạn đầu vào và khóa chống trùng 60 giây. Nếu upstream timeout sau khi có thể đã nhận, giữ khóa cho tới hết TTL để tránh gửi lặp ngay. Backend vẫn nên áp dụng idempotency, rate limit và transaction riêng trước thao tác gửi thông báo/lưu khách.

Chỉ dùng giả lập trong QA; không bật dịch vụ ngoài để thử bằng dữ liệu giả mà chưa có phạm vi vận hành cho phép. Không log tên/số điện thoại/email/message hay payload PDF. Không tự bật analytics thu query hoặc nội dung form.

## Phát hành

1. Cấu hình và kiểm tra backend bằng dữ liệu được phép, Redis thật và nhiều instance; xác minh proxy không vòng lặp, secrets không ở client.
2. Kiểm thử tải PDF và mở file trên Chrome/Safari/điện thoại; chạy E2E, light/reduced motion, bàn phím, focus và responsive 390/768/1440.
3. Đo hiệu năng trước/sau cùng điều kiện. CSP script hiện report-only; chưa có collector. Đọc vi phạm, thiết kế nonce/hash phù hợp Next trước khi enforce. Headers chống nhúng/object/base đã enforce.
4. Chủ hệ thống xác minh 2FA, phân quyền, HTTPS, backup và khôi phục; quyết định HSTS theo domain/subdomain thực tế.
5. Chủ site duyệt preview và chính sách; ghi phiên bản rollback. Không khôi phục bulk API khi rollback.
