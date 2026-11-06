# Quả cầu ba quỹ đạo — bản thử 06/11/2026

Theo yêu cầu chủ site, thêm tương tác vào quả cầu hiện tại và giữ phong cách Cosmic Glass 3D. Không dùng `design-taste-frontend`.

## Hành vi

- Ba nút Dịch vụ, Dự án, Kết nối nằm quanh quả cầu. Quỹ đạo đang chọn sáng lên; lớp xoay riêng chuyển hướng nhẹ mà không ghi đè chuyển động nổi và nghiêng theo chuột có sẵn.
- Dịch vụ: ba lối tắt theo nhu cầu và đường dẫn đến toàn bộ 18 dịch vụ.
- Dự án: ảnh xem trước, nút trước/sau, tên và đường dẫn đến bốn demo hiện có. Dùng chung danh mục với ProjectShowcase, không thêm dự án hoặc claim mới.
- Kết nối: các đường dẫn Zalo, gọi điện, email và trang tư vấn hiện có; không tự gửi thông tin.
- Nút đang chọn hoặc nút đóng thu bảng lại. Escape đóng bảng và trả focus; phím mũi tên/Home/End di chuyển giữa ba nút. Dùng aria-expanded, aria-controls và thông báo tên dự án khi chuyển mẫu.
- Desktop lớn: bảng kính nằm cạnh phần dưới của quả cầu. Màn hình đến 1375px: bảng nằm dưới quả cầu, cuộn tới vùng đọc sau khi refresh layout và chừa khoảng cho nút liên hệ nổi.
- Hoạt động ở cả sáng/tối. Reduced motion bỏ xoay và chuyển cảnh; nội dung vẫn mở trực tiếp. GSAP có scope, cleanup và chỉ animate transform/opacity. Không thêm thư viện hay vòng lặp trang trí mới.

Các sửa lỗi sơ đồ/icon/tiêu đề từ bản trước giữ nguyên. Những phần ngoài hero giữ giao diện 3D cũ.

## Kiểm tra thực tế

- Lint, TypeScript và production build đạt; 61 trang tĩnh.
- Browser desktop 1440px và mobile 390px; thêm cả ba bảng ở 320/768/1024/1376px: không tràn ngang, chỉ một bảng mở, nút quỹ đạo bấm được.
- Bốn dự án chuyển tiến/lùi và quay vòng đúng ảnh, tên, đường dẫn; ảnh mẫu tải được.
- Kiểm tra Escape, trả focus, phím mũi tên/Enter, đóng bằng nút và hai giao diện sáng/tối.
- Bấm lối tắt Website doanh nghiệp mở đúng trang dịch vụ; sơ đồ trên trang đó vẫn tồn tại. Chỉ đọc URL liên hệ, không gọi/gửi email/Zalo hay submit form.
- Lượt đầu ghi nhận GSAP không hỗ trợ reset `rotationZ`; đã chuyển sang alias `rotation`. Bản cuối xoay được cả hai trục, không ghi nhận cảnh báo mới trong các lượt sau. Nhật ký cũ giữ trong hồ sơ QA với ghi chú đã sửa.
- Chưa chạy full E2E, Lighthouse/axe, Safari/thiết bị thật hoặc giả lập tùy chọn reduced motion của hệ điều hành. Reduced motion được kiểm tra trong mã.

Source và bản xuất tĩnh cập nhật vào dev / PR nháp; chưa merge hoặc triển khai website chính thức.
