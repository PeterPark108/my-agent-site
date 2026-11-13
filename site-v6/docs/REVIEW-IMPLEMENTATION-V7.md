# My Agent v7 — Review và kết quả triển khai

Ngày: 05/11/2026. Nguồn: ZIP v6.1 và MASTER-PLAN v2.0 do chủ website cung cấp. Trạng thái: mã nguồn nâng cấp để duyệt; chưa phát hành domain.

## Kết luận review lần cuối

Kế hoạch phù hợp khi triển khai theo thứ tự demo → báo giá/hỗ trợ → đồ họa nâng cao. Không nên coi bản đồ hoặc WebGL là điều kiện bắt buộc trước khi kiểm chứng khả năng sử dụng. Bổ sung bốn yêu cầu kỹ thuật:

1. Demo đang bị che phải bị loại khỏi cây truy cập và tương tác; giảm thời gian ghim, bỏ ghim trên mobile/màn hình thấp/reduced motion.
2. Đóng API danh sách đơn ngay; không tiếp tục proxy tệp đơn từ backend cũ. Luồng mới chỉ nhận mã bằng POST và chỉ trả một projection được duyệt.
3. Rate limit trong bộ nhớ không đủ cho nhiều máy chủ. Production yêu cầu kho giới hạn dùng chung; chưa cấu hình thì từ chối API thay vì âm thầm bỏ bảo vệ.
4. Phân biệt mã đã hoàn thành, dịch vụ ngoài chưa nối và nghiệm thu thiết bị chưa chạy. Không đánh dấu toàn bộ master plan là hoàn tất vì build qua.

## Đã triển khai trong mã

| Phạm vi | Kết quả |
|---|---|
| Demo P0 | Giữ thứ tự NhàĐất Việt → Nhà Gió → NHỊP; ảnh contain, kích thước khai báo, lazy load; không có nút mobile giả. Desktop từ 1100×760 trở lên mới pin; quãng cuộn giảm từ 2,8 xuống 1,6 chiều cao viewport. Nút chọn cập nhật ảnh/tên/link; inactive có aria-hidden và inert. |
| Báo giá P1 | Thẻ lựa chọn có nút bỏ, tổng và chi tiết một lần/định kỳ sau điều chỉnh, kỳ thanh toán, VAT, khoản thương lượng; mobile có thanh tóm tắt, native dialog đóng bằng Escape và trả focus. Không sửa giá hoặc pricing engine. |
| PDF | Giữ tính lại phía server, font tiếng Việt, khoản thương lượng; trạng thái chờ/thành công/lỗi và giữ lựa chọn. Bổ sung kiểm tra MIME phản hồi. |
| Hỗ trợ P1 | Kết nối gồm Gọi, Zalo, MJ và nút đóng; mobile ẩn launcher MJ độc lập, dành khoảng trống cho báo giá và safe area. Giữ nội dung đang gõ khi thu gọn MJ. Gợi ý theo trang, không thêm LLM. |
| Hệ sinh thái P2 | Giữ tab/danh sách và đường dẫn; thêm đường liên kết phụ trợ trên desktop, nút dọc trên mobile. Không thay bằng bản đồ tương tác khi chưa có thử nghiệm nhiệm vụ. |
| Hero P3 | Giữ lõi CSS và nhận diện; thêm nghiêng biên độ nhỏ chỉ với con trỏ chính xác. Không thêm WebGL. Dừng nhịp hero khi ẩn tab; nền sao giảm trên mobile và vùng đọc dài. |
| Điều hướng | Giữ sửa hash v6.1; sửa thêm liên kết footer về section trang chủ từ trang con. |
| Tra cứu S0 | GET /data/orders.json trả 410. POST /api/tracking nhận mã riêng, gọi backend bằng token server, chỉ trả percent/status/updated/note/steps; không trả history/PII/ghi chú nội bộ. Không tự đọc mã từ query, không uppercase token, không tải danh sách. |
| API S0 | Giới hạn stream trước khi parse, timeout đọc, loại trường lạ, validate kiểu/độ dài/consent; chống prototype-key trong lựa chọn báo giá. Giới hạn đồng thời theo tiến trình và giới hạn tần suất Redis atomic dùng chung; form chống gửi trùng 60 giây. Lỗi chung không lộ stack/upstream. |
| HTML/chatbot S0 | sanitize-html với allowlist cho nội dung đã kiểm soát; bỏ inline onclick công cụ và gắn listener an toàn. Kiểm tra giao thức link MJ; trạng thái tra cứu chỉ dùng class theo allowlist. |
| Headers S1 | nosniff, no-referrer, DENY/frame-ancestors, hạn chế object/base, Permissions-Policy. CSP script ở report-only để tiếp tục quan sát; chưa bật HSTS khi chưa biết phạm vi domain. |

## Bằng chứng kiểm tra vòng này

- `npm ci`: thành công từ lockfile v6.1. Baseline build trước thay đổi thành công, có log riêng.
- Build production, ESLint, TypeScript: đã qua; log trong `docs/qa-v7/`.
- `npm run test:security`: 19 kiểm tra với route handler thật, fetch giả lập; không gửi contact hoặc tra mã khách thật. Bao gồm đồng ý, origin/host qua proxy, kích thước stream, khóa nguyên mẫu, PDF thật, giá tổ hợp, gửi trùng, retry, projection, rate limit, concurrency, Redis atomic, HTML và chống self-proxy.
- `npm audit --omit=dev`: không có cảnh báo đã biết trong báo cáo tại thời điểm chạy; không đồng nghĩa không có lỗ hổng. Dữ liệu giá, pricing engine, PDF renderer và logo đối chiếu byte không đổi; danh mục 55 route nội dung giữ nguyên.
- PDF mẫu một trang được tạo, mở bằng pdf-lib, render và kiểm tra thị giác: tiếng Việt hiển thị, không chồng chữ. Tệp mẫu và ảnh render ở `docs/qa-v7/`.
- Browser Chromium cloud, viewport quan sát 1363×936: chọn NHỊP cập nhật đúng ảnh/tên/link; Kết nối mở và focus tới Gọi; MJ mở từ Kết nối; Escape và mở lại giữ nội dung đang nhập; nhóm Dữ liệu & phần mềm hiển thị đúng link; từ bảng giá về Hệ dịch vụ có top 116px và opacity 1; không tràn ngang ở trang chủ khi đo.
- Browser báo giá: website + SEO + hosting, kỳ 6 tháng có tổng 17.800.000–30.700.000đ + khoản thương lượng, thẻ bỏ hoạt động; sau khi bỏ hosting tổng thay đổi theo chính sách combo cũ. Đã xác nhận UI tạo PDF thành công sau sửa kiểm tra origin qua proxy. Chưa xác nhận lưu/mở PDF xuống đĩa bằng trình duyệt người dùng.
- Lỗi chọn demo bằng smooth scroll và lỗi kiểm tra origin qua proxy phát hiện khi QA đã được sửa. Chọn demo trực tiếp cũng kết thúc sau xung viền; đã xác nhận opacity viền bằng 0 ở trạng thái dừng. HMR có thể giữ script công cụ cũ trong phiên dev; dùng reload đầy đủ khi sửa HTML công cụ.

## Chưa được nghiệm thu / điều kiện chặn phát hành

| Mục | Trạng thái / yêu cầu |
|---|---|
| Backend contact/tracking thật | Chưa cấu hình, chưa thử. Đọc SECURITY-RUNBOOK-V7.md. Tra cứu mới cần backend có API riêng và mã ngẫu nhiên có thể thu hồi; không tương thích mã ngắn/băm của tệp cũ. |
| Redis và trusted edge | Adapter đã có test giả lập; chưa kiểm thử Redis thật/nhiều instance. Không bật MYAGENT_LOCAL_QA ở production. |
| Mobile 390/768 và desktop 1440 | CSS và hành vi đã lập trình, nhưng vòng này chưa có bằng chứng browser đúng các kích thước này. Không có ảnh mobile giả. |
| Safari/iOS, bàn phím đầy đủ, reduced motion, light theme | Cần chạy ma trận nghiệm thu lại. Chỉ một số thao tác desktop đã kiểm tra. |
| Bộ Playwright E2E cũ | Đã cập nhật mock cho tracking mới và lối mở MJ; chưa chạy lại toàn bộ. Không tái sử dụng con số pass của v6/v6.1. |
| Hiệu năng / axe | Chưa đo LCP/INP/CLS/Lighthouse/axe trước sau. Không tuyên bố đạt ngân sách. |
| CSP | Script report-only, chưa có collector; vi phạm xem ở browser console. Cần khảo sát và thêm nonce/hash trước enforce script. |
| Tài khoản, backup, quyền dữ liệu | Chủ hệ thống cần xác minh 2FA, quyền, chính sách lưu/xóa, bản sao và diễn tập phục hồi. |
| Giới hạn PDF | Có input bounds, rate limit toàn hệ thống và semaphore theo tiến trình. Chưa có worker/queue với hard timeout hủy tác vụ PDF hoặc semaphore dùng chung giữa các instance. |
| P2/P3 nâng cao | Bản đồ tương tác và WebGL tiếp tục hoãn cho tới khi có baseline hiệu năng và quan sát nhiệm vụ. |

Bàn giao này là một bước triển khai có kiểm tra, không phải nghiệm thu toàn bộ master plan hoặc chứng nhận an toàn. Không cấu hình hosting, đổi domain, gửi dữ liệu khách hoặc tự bật analytics.

## Khôi phục

ZIP v6.1 giữ nguyên để so sánh/khôi phục giao diện. Không bật lại endpoint bulk orders khi rollback; giữ bản vá tra cứu và cấu hình an toàn, hoặc tắt tra cứu cho tới khi backend sẵn sàng.
