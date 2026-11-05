# Tự review v6 — 05/11/2026

## Đánh giá và cải tiến sau review

Giao diện đã có ngôn ngữ công nghệ chung từ trang chủ sang trang con: nền sao, menu kính, sơ đồ công nghệ, typography và nhịp chuyển động. Mỗi nhóm trang có bố cục riêng, không còn chỉ phủ glass lên stylesheet cũ. Mức hoàn thiện phù hợp bàn giao preview; chưa tuyên bố đạt hiệu năng hay khả năng truy cập chuẩn hóa khi chưa đo.

Các lỗi đã tìm và sửa: listener glow-cursor cũ tham chiếu phần tử đã bỏ; menu tablet cần thu gọn; kiểm tra origin từ localhost gây từ chối preview 127.0.0.1; PDF cần nhóm tổng/ghi chú để không rơi thành trang lẻ; combo cần nối sang công cụ xuất PDF. Nhãn kỹ thuật nội bộ đã đổi sang tiếng Việt, metadata và CTA gốc được đưa về hero mới. Tăng thời gian giữ Blob để tránh thu hồi sớm khi tải.

## Bằng chứng

- Build production, lint và TypeScript: qua trên máy hiện tại. Windows có lỗi quyền tạo thư mục output của Next; tạo sẵn thư mục output tương ứng rồi build lại thành công.
- E2E Chromium desktop/mobile: 23 passed, 1 skipped (inventory HTTP chỉ chạy một lần). Chế độ QA_RESTRICTED_DOWNLOADS=1; kiểm tra PDF Blob, định dạng, số trang và sự kiện tải, không xác nhận saveAs xuống đĩa.
- Đã đối chiếu 55 route cùng shell v6; kiểm tra sáu nhóm trang qua screenshot và lỗi trình duyệt/tràn ngang.
- PDF mẫu 1 trang và trường hợp nhiều dịch vụ 3 trang được render kiểm tra tiếng Việt, phân trang và khoảng cách.
- Form gửi dùng mock; tra cứu dùng đơn hàng giả. Không gửi thông tin thử nghiệm tới chủ site, không tra mã khách thật.

## Giới hạn thực tế

Chromium trong môi trường Windows hạn chế hủy lưu download, tái hiện với TXT không liên quan PDF. Nút tạo đúng Blob PDF nhưng lưu tệp trên trình duyệt thật vẫn là mục QA chưa hoàn tất. CUA preview không khởi tạo được; ảnh kiểm tra được chụp bằng Playwright và xem trực tiếp. Chưa chạy Safari thật, Lighthouse hoặc axe. Chưa phát hành; proxy API cần backend riêng trước cutover domain. Nội dung dài gốc được giữ để tránh mất thông tin, có thể biên tập thêm sau khi chủ site duyệt.
Bổ sung review cuối: cập nhật vị trí ScrollTrigger sau khi script và font sẵn sàng, kiểm tra opacity nội dung sau cuộn; sửa dấu phân cách metadata bài viết để ngày/thời lượng/tác giả không dính nhau.
