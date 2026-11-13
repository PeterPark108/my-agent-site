> **Hiện hành: v6.** Đọc [REDESIGN-V6.md](REDESIGN-V6.md) và [SELF-REVIEW-V6.md](SELF-REVIEW-V6.md) trước. Nội dung dưới đây là hồ sơ lịch sử khi khác với v6.

# Đối chiếu chức năng v5

| Nhóm | Route / thành phần | Trạng thái |
|---|---|---|
| Trang chủ GSAP | / | Next.js, giữ bản nâng cấp |
| Dịch vụ và 18 trang chi tiết | /dich-vu.html, /dich-vu/*.html | HTML nội dung gốc, shell glass |
| Combo và tự chọn | /combo.html | Script he-thong.js gốc |
| Bảng giá và tính giá | /bang-gia.html | pricing.json + script gốc, đã mở kiểm tra |
| Tra cứu tiến độ | /tra-cuu-tien-do.html | Script gốc; dữ liệu live qua route no-store, chưa tra mã thật |
| Form trang chủ | BriefForm + /api/contact | Consent bắt buộc cả client/server, mock test qua |
| Form trang liên hệ | /lien-he.html | Payload/API gốc được giữ |
| MJ | js/chat.js + data/chatbot-kb.json | Trả lời đã quan sát, không cần LLM key |
| Gọi/Zalo | Widget cố định | tel và zalo.me gốc |
| Chính sách | /chinh-sach-bao-mat.html | Nội dung gốc |
| Mục điều khoản | /dieu-khoan-dich-vu.html | Mục lục chính sách/phạm vi/điều kiện công khai, không phải hợp đồng mới |
| Blog/tin/tài nguyên/công cụ/giới thiệu | Các route trong inventory | Nội dung và script source được giữ |
| Analytics | config.js | Tắt gaId trong preview; cấu hình/duyệt lại khi release |
| Backend/VPS | MYAGENT_BACKEND_ORIGIN | Phụ thuộc hạ tầng gốc, chưa chuyển máy chủ |
