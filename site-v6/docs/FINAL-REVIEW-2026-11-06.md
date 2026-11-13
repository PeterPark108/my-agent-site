# Tự rà soát trước khi bàn giao ZIP lên VPS

## Đã sửa trong lượt cuối

- Giữ chunk của trang Điều khoản nằm trong thư mục `_next/.../dieu-khoan-dich-vu.html/`. Quy tắc đóng gói cũ đã nhầm thư mục asset này với thư mục route trùng tên file HTML.
- Giữ các tệp payload `.html.txt` của bản xuất Next.js, chỉ bỏ thư mục route gây xung đột với file HTML đã chuẩn hóa.
- Sửa liên kết ở trang Combo sang bài “Thiết kế web trọn gói gồm những gì”; thêm đích `main` cho liên kết bỏ qua nội dung trên trang Điều khoản.
- Thêm trang 404 tiếng Việt với nền vũ trụ, logo và các lối quay lại trang chủ/dịch vụ. Trang 404 có noindex.
- Làm thanh cuộn popup mảnh và cùng màu với kính, giữ nguyên bố cục 3D.

## Kết quả

- Lint, typecheck, build đạt; 61 trang HTML.
- Rà offline 257 tệp và 4.891 tham chiếu nội bộ: không thiếu file, không sai anchor, không trùng ID; ảnh có thuộc tính alt, mỗi trang có một h1 và một title.
- Đã kiểm tra 5 nhóm / 18 thẻ dịch vụ ở 1440/390px và thêm nhóm Dữ liệu ở 320px. Giữ bản sửa sơ đồ 18 dịch vụ và tiêu đề Blog/Tin 19px.
- Lượt cuối trên trình duyệt kiểm tra trang chủ, ba popup, Dịch vụ, Blog, Tin, Dự án, Combo, Liên hệ, Tra cứu, Điều khoản và 404; thêm các trang nội dung ở 390px. Không ghi nhận tràn ngang trang hoặc ảnh lỗi trong các lượt này.
- Popup: modal, backdrop blur, khóa cuộn, Escape, nút đóng, trả focus và bấm ngoài để đóng đều hoạt động. Menu điện thoại mở/đóng được.
- Tính giá Landing page cho kết quả 2–3,6 triệu, PDF tải xuống thành công. Đây là kiểm tra một cấu hình, không phải kiểm thử toàn bộ phép tính giá.
- Nền sao/nhịp sao băng đã kiểm tra ở lượt trước, xem COSMIC-FLIGHT. Giao diện sáng/tối và popup responsive đã kiểm tra ở các lượt trước và lượt sửa dịch vụ.

## Giới hạn còn lại

Chưa kiểm tra Safari/thiết bị thật, Lighthouse/axe hoặc full E2E. Không gửi form liên hệ, không tra mã khách hàng và không xác nhận API trên VPS. ZIP là frontend tĩnh; `/api/contact` và `/api/tracking` cần backend trên VPS. Tra cứu trước đó đã được ghi nhận là cần cấu hình backend riêng. Không có dữ liệu đơn hàng, biến môi trường hay mã backend trong ZIP triển khai.

## Hướng nâng cấp tiếp theo

1. Tìm dịch vụ nhanh theo nhu cầu, giữ các thẻ kính và nhóm hiện tại.
2. Cho người xem chọn mức chuyển động “Đầy đủ / Nhẹ” ngay trên giao diện; tiếp tục tôn trọng cài đặt giảm chuyển động của thiết bị.
3. Bổ sung điều hướng vuốt cho ảnh dự án trong popup trên điện thoại.

Ba mục này là đề xuất, chưa thêm vào bản bàn giao. Bản hiện tại được giữ ở PR nháp; chủ site tự tải ZIP lên VPS.
