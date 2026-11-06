# Sửa danh mục dịch vụ — 06/11/2026

Các thẻ trong `/dich-vu.html` dùng markup `sgrid2` / `scard`, nhưng thiếu CSS tương ứng sau khi nhập giao diện. Thẻ liên kết trở thành phần tử inline, tiêu đề dính mô tả và icon tràn khỏi khung.

- Thêm lưới hai cột trên màn hình rộng, một cột từ 760px trở xuống. Cả 5 nhóm dùng chung bố cục; 18 dịch vụ giữ nguyên nội dung và URL.
- Tiêu đề hiển thị riêng, cỡ 20px (18px ở màn hình nhỏ); mô tả 14px, cách tiêu đề 12px. Icon có cột riêng, co gọn ở điện thoại.
- Giữ bề mặt kính, màu sáng/tối và nền vũ trụ. Có viền focus bàn phím, khoảng cách trước khối combo và phản hồi hover nhẹ.
- Liên kết thẳng đến nhóm từng bị cuộn quá xa do trình duyệt định vị trước khi các nhóm khác được ẩn. Dùng chung hook điều hướng GSAP hiện có để định vị lại sau khi công cụ trang sẵn sàng; cập nhật hash chờ nhóm mới hiện ra. Không đổi hành vi bấm tab.

## Kiểm tra

- Lint, typecheck và build đạt; 61 trang tĩnh.
- Duyệt đủ 5 nhóm / 18 thẻ ở 1440px và 390px: tiêu đề/mô tả tách dòng, icon nằm trong thẻ, không tràn ngang. Kiểm tra thêm nhóm Dữ liệu ở 320px.
- Kiểm tra mở trực tiếp nhóm, đổi tab và điều hướng hash trên bản xuất tĩnh trong trình duyệt.
- Không chạy full E2E, Lighthouse/axe hoặc thiết bị thật cho bản sửa này.

Source và bản tĩnh được cập nhật trong PR nháp vào production; việc merge/triển khai vẫn chờ chủ site duyệt.
