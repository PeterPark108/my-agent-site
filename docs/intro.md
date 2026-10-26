# Màn intro trang chủ

Khi khách mở trang chủ lần đầu trong phiên, web hiện màn "khởi động hệ thống" khoảng 3,6 giây rồi mờ dần vào trang. Khách bấm **Bỏ qua** hoặc phím Esc để tắt ngay.

- **Tắt/bật:** sửa `introEnabled` trong `js/config.js` (`true` = bật, `false` = tắt), rồi đẩy lên như bình thường.
- **Xem thử:** mở `https://myagentvn.com/?intro=1` (luôn hiện). `?intro=0` = không hiện.
- Mỗi phiên trình duyệt chỉ hiện 1 lần (khóa `myagent_intro_seen` trong sessionStorage). Máy bật "giảm chuyển động" sẽ không thấy intro.
- Nội dung trang chủ vẫn nằm nguyên trong HTML (không ảnh hưởng SEO); intro là lớp phủ do `js/intro.js` thêm vào, tự gỡ sau tối đa 6,5 giây.
- File: `js/intro.js`, CSS ở cuối `css/style.css`, đoạn script nhỏ trong `<head>` do `scripts/tech_pass.py` thêm vào `index.html`.
