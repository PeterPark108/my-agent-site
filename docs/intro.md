# Màn intro trang chủ

Khi khách mở trang chủ lần đầu trong phiên, web hiện màn intro chỉ có **logo My Agent** (~3,3 giây): tia sáng hội tụ vào tâm → chớp sáng + vòng sóng xung kích → logo phóng to/nhòe rồi hiện rõ, nhiễu glitch tách màu vài khung hình, hạt sáng bung ra, viền sáng neon đỏ/xanh, vệt sáng quét ngang logo → trang phóng nhẹ và tan vào trang chủ. Không có chữ nào khác ngoài nút **Bỏ qua** (hoặc phím Esc).

- **Tắt/bật:** sửa `introEnabled` trong `js/config.js` (`true` = bật, `false` = tắt), rồi đẩy lên như bình thường.
- **Xem thử:** mở `https://myagentvn.com/?intro=1` (luôn hiện). `?intro=0` = không hiện.
- Mỗi phiên trình duyệt chỉ hiện 1 lần (khóa `myagent_intro_seen` trong sessionStorage). Máy bật "giảm chuyển động" sẽ không thấy intro.
- Nội dung trang chủ vẫn nằm nguyên trong HTML (không ảnh hưởng SEO); intro là lớp phủ do `js/intro.js` thêm vào, tự gỡ sau tối đa 6,5 giây. Hiệu ứng nền vẽ bằng canvas (DPR tối đa 1,5, dừng khi tab ẩn, dọn sạch khi xong); phần logo dùng CSS.
- File: `js/intro.js`, CSS ở cuối `css/style.css`, đoạn script nhỏ trong `<head>` do `scripts/tech_pass.py` thêm vào `index.html`.

## v0.1.8
- Nút "Bỏ qua" chỉ còn icon × (góc trên phải, mờ cho tới khi hover/focus; aria-label "Bỏ qua intro", 44×44px, Esc vẫn dùng được). Intro không còn chữ nào ngoài logo (logo-dark.svg có wordmark "MyAgent" — là một phần logo).
- Cache-busting: `css/style.min.css?v=VERSION` và `js/intro.js?v=VERSION` (tech_pass.py tự cập nhật theo VERSION) vì server cache 7 ngày, khách cũ có thể còn bản intro v0.1.6 có chữ terminal.
