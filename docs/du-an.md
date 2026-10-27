# Dự án mẫu – cách thêm dự án

Quy tắc của Peter: mọi dự án làm xong đều đưa lên `du-an.html`, có thumbnail.

1. Chụp bản chạy thật 1280x720 (headless Chromium, chờ font/ảnh, ẩn banner cookie). Kiểm tra không có tên thật, email, SĐT, khóa, URL nội bộ.
2. Xuất WebP 16:9 (đúng `aspect-ratio:16/9` của `.thumb`): `assets/projects/<slug>-960.webp` (960x540) và `<slug>-480.webp` (480x270), quality ~80, mỗi file < 120 KB, không EXIF.
3. Copy một thẻ `<div class="card glass post rv">…</div>` trong `du-an.html`, sửa: ảnh (`srcset`, `width="960" height="540"`, `alt` tiếng Việt mô tả màn hình, `loading="lazy"`), tag, tên, mô tả 1–2 câu đúng với bản chạy, dòng ghi chú dữ liệu mẫu, nút "Xem demo" (`target="_blank" rel="noopener noreferrer"`).
4. Giữ câu "sản phẩm mẫu do Peter tự làm… không phải dự án làm cho khách hàng". Không hứa xếp hạng, không "24/7".
5. Chạy `python3 scripts/tech_pass.py`, `python3 scripts/chatbot_build.py`, các kiểm tra (`check_links.py`, `ci_check.py`, `seo_audit.py`), tăng VERSION + CHANGELOG, mở PR.
