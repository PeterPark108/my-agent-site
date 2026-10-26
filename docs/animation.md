# Hiệu ứng chuyển động (animation) toàn site — v0.2.0

File: `js/motion.js` (~3,6 KB rút gọn, tải `defer` trên mọi trang) + phần `motion layer` cuối `css/style.css`.

## Có gì
- Thanh tiến trình cuộn neon ở mép trên.
- Hero trang chủ: nhãn, tiêu đề, mô tả, nút hiện lần lượt (mờ → rõ, trồi lên); chữ gradient "chạy thật" ánh sáng chạy; parallax nhẹ theo chuột (máy tính).
- Tiêu đề mục: vạch neon tự vẽ dưới dòng `// ...`.
- Thẻ: nghiêng 3D + viền sáng theo chuột (máy tính), nhún nhẹ khi chạm (điện thoại); icon dịch vụ bồng bềnh.
- Nút: vệt sáng quét khi rê chuột, gợn sóng khi bấm.
- Menu: vạch chỉ báo trượt theo mục đang rê (máy tính); menu mobile mở trượt, từng mục hiện lần lượt.
- Chuyển trang mượt (mờ nhanh ~0,17 s) giữa các trang trong site; không ảnh hưởng tab mới, Ctrl/Cmd-click, tel:, mailto:, Zalo, link #.
- Viền gradient chạy ở khối CTA và mép trên chân trang.
- Hiệu ứng có sẵn trước đó vẫn giữ: hiện dần khi cuộn, lưới mạng nhện ở hero, console gõ chữ.

## Tắt / bật
- Tắt hẳn: sửa `motionEnabled: false` trong `js/config.js` (bật lại: `true`).
- Xem thử không hiệu ứng: thêm `?motion=0` vào link, vd `https://myagentvn.com/?motion=0`.
- Máy bật "giảm chuyển động" (prefers-reduced-motion) sẽ tự tắt.
- Không có JS: toàn bộ nội dung hiện bình thường.

Sau khi sửa CSS/JS: chạy `python3 scripts/tech_pass.py` (cập nhật `?v=` và chèn motion.js vào mọi trang).
