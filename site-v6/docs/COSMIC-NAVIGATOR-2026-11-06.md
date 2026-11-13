# Quả cầu ba quỹ đạo — bản thử 06/11/2026

Theo yêu cầu chủ site, thêm tương tác vào quả cầu hiện tại và giữ phong cách Cosmic Glass 3D. Không dùng `design-taste-frontend`.

## Hành vi

- Ba nút Dịch vụ, Dự án, Kết nối nằm quanh quả cầu. Quỹ đạo đang chọn sáng lên; lớp xoay riêng chuyển hướng nhẹ mà không ghi đè chuyển động nổi và nghiêng theo chuột có sẵn.
- Dịch vụ: ba lối tắt theo nhu cầu và đường dẫn đến toàn bộ 18 dịch vụ.
- Dự án: ảnh xem trước, nút trước/sau, tên và đường dẫn đến bốn demo hiện có. Dùng chung danh mục với ProjectShowcase, không thêm dự án hoặc claim mới.
- Kết nối: các đường dẫn Zalo, gọi điện, email và trang tư vấn hiện có; không tự gửi thông tin.
- Bấm quỹ đạo mở popup kính giữa màn hình. Native dialog đưa popup lên trên mọi lớp 3D, làm phần còn lại inert; backdrop blur 13px làm mờ website, body khóa cuộn khi mở.
- Popup có ba nút đổi nội dung. Nút ×, Escape hoặc bấm ngoài popup đóng lại và trả focus về quỹ đạo. Tab/Shift+Tab giữ focus trong popup; phím mũi tên/Home/End vẫn dùng cho ba nút ngoài quả cầu khi popup đóng.
- Một bố cục popup dùng cho desktop/mobile, giới hạn trong viewport và cho phép cuộn bên trong trên màn hình thấp. Giữ aria-expanded, aria-controls và thông báo tên dự án khi chuyển mẫu.
- Hoạt động ở cả sáng/tối. Reduced motion bỏ xoay và chuyển cảnh; nội dung vẫn mở trực tiếp. GSAP có scope, cleanup và chỉ animate transform/opacity. Không thêm thư viện hay vòng lặp trang trí mới.

Các sửa lỗi sơ đồ/icon/tiêu đề từ bản trước giữ nguyên. Những phần ngoài hero giữ giao diện 3D cũ.

## Kiểm tra thực tế

- Lint, TypeScript và production build đạt; 61 trang tĩnh.
- Bản popup cuối: cả ba nội dung ở 320/390/768/1440px đều nằm trong viewport, không tràn ngang trang hoặc popup. Native modal hoạt động, nền bị khóa và làm mờ.
- Bốn dự án chuyển tiến/lùi và quay vòng đúng ảnh, tên, đường dẫn; ảnh mẫu tải được.
- Kiểm tra Escape, trả focus, Tab/Shift+Tab quay vòng trong popup, đóng bằng nút, chuyển nhóm và hai giao diện sáng/tối. Handler bấm ngoài popup đã triển khai; không có lượt kiểm tra bằng tọa độ cho thao tác đó.
- Bấm lối tắt Website doanh nghiệp mở đúng trang dịch vụ; sơ đồ trên trang đó vẫn tồn tại. Chỉ đọc URL liên hệ, không gọi/gửi email/Zalo hay submit form.
- Lượt đầu ghi nhận GSAP không hỗ trợ reset `rotationZ`; đã chuyển sang alias `rotation`. Bản cuối xoay được cả hai trục, không ghi nhận cảnh báo mới trong các lượt sau. Nhật ký cũ giữ trong hồ sơ QA với ghi chú đã sửa.
- Chưa chạy full E2E, Lighthouse/axe, Safari/thiết bị thật hoặc giả lập tùy chọn reduced motion của hệ điều hành. Reduced motion được kiểm tra trong mã.

Source và bản xuất tĩnh cập nhật vào dev / PR nháp; chưa merge hoặc triển khai website chính thức.
