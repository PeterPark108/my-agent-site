# Thiết kế và bàn giao v6

## Hệ thống giao diện

Giữ token thương hiệu đã xác minh: nền #05070F, navy #0B1E4A, blue #1B3A8C, electric #3D7BFF, red #E23636, neon #FF2D3D, text #E9ECF5, muted #A3ABC2; Be Vietnam Pro local. Nền sao phủ toàn trang, bề mặt kính có viền mỏng, khoảng trắng và phân cấp chữ rõ. Đỏ dành cho thương hiệu/điểm nhấn, xanh dành cho tọa độ/cấu trúc công nghệ.

Header/Footer là component chung cho mọi trang, không sao chép từng route. Homepage giữ quả cầu kính/công nghệ, vòng trôi, pulse M, heading gõ chữ, dự án màn hình LED và chuyển lớp GSAP. Trang con có hero riêng, icon glass chuyển động và reveal nội dung có cleanup/reduced-motion; bố cục bài viết, danh mục, dịch vụ và công cụ khác nhau theo nhu cầu đọc.

55 đường dẫn từ inventory dùng renderer Next chung và dữ liệu cấu trúc; HTML gốc chỉ lưu trong content/source. Không phục vụ public HTML hay tải CSS cũ. Logic công cụ được giữ qua ID/data attribute và script chọn lọc. Nội dung cũ là nguồn tin cậy của chủ site, không phải HTML từ người dùng.

## PDF báo giá

Từ /bang-gia.html chọn dịch vụ, gói, độ phức tạp, số lượng, kỳ thanh toán và tiến độ; bấm Tải PDF báo giá. Combo có đường dẫn mang lựa chọn sang bảng giá. API POST /api/quote xác minh ID, gói, số lượng và tính lại bằng pricing engine gốc, không tin giá client. PDF A4 có tiếng Việt/font nhúng, logo, chi tiết/chiết khấu/phụ phí, tổng tham khảo, VAT và ghi chú thương lượng. Không lưu thông tin khách hoặc lịch sử tải.

## Acceptance và QA v6

- [x] 55 route cũ trả thành công qua shell v6, không CSS/header cũ.
- [x] Header/Footer chung, theme và menu responsive; không tràn ngang ở viewport desktop/mobile đã kiểm tra.
- [x] GSAP/reduced motion, nguồn logo local, FAQ, danh mục và demo dự án còn hoạt động.
- [x] Consent bắt buộc, API từ chối thiếu consent; thành công chỉ sau phản hồi API (QA dùng mock).
- [x] Combo → tính giá → PDF; prefill liên hệ; công cụ mật khẩu; MJ và liên kết tel/Zalo.
- [x] Tra cứu với dữ liệu giả lập; không đóng gói đơn hàng thật.
- [x] PDF tiếng Việt đọc được, bản 1 và 3 trang không chồng chữ qua kiểm tra render.
- [ ] Tải và mở PDF trên Chrome/Safari thật bên ngoài môi trường Windows hạn chế.
- [ ] Form/backend và mã tiến độ thật sau cấu hình môi trường phát hành.
- [ ] Lighthouse, axe, Safari/iOS thật và kiểm tra tải trên thiết bị yếu.

Chạy E2E mặc định sẽ yêu cầu lưu tệp PDF thực sự. Chỉ trong môi trường Windows hạn chế đã tái hiện lỗi hủy cả download TXT, có thể đặt QA_RESTRICTED_DOWNLOADS=1: kiểm tra byte của chính Blob do nút tạo ra và sự kiện download thay cho saveAs. Đây là phạm vi kiểm tra thu hẹp, không được báo là đã xác minh lưu tệp trên thiết bị thật.

## Nhiệm vụ Grokbot còn lại

1. Tái lập lint/typecheck/build/E2E; đọc SELF-REVIEW-V6. Giữ các nguồn gốc và business rule đã bảo toàn.
2. Kiểm tra PDF tải xuống trên Chrome, Safari và điện thoại thật; đối chiếu tổng với lựa chọn, cả giá thương lượng và nhiều trang.
3. Kiểm tra 390/768/1440px, bàn phím, theme sáng/tối, reduced motion; đo Lighthouse/axe rồi sửa theo bằng chứng.
4. Cấu hình backend riêng cho contact/orders; kiểm tra bằng yêu cầu được chủ site cho phép. Không đưa đơn hàng riêng tư vào repo.
5. Trước phát hành: kiểm tra SEO/canonical/sitemap cho toàn bộ route, rate limit backend, CSP, preview và rollback. Chỉ triển khai khi chủ site cho phép.

Không tự bịa dự án khách hàng, số liệu thành tích hoặc điều khoản ràng buộc. Trang điều khoản hiện là mục lục dẫn đến chính sách/phạm vi công khai; cần chủ site duyệt hợp đồng riêng nếu có.
