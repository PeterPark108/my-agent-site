# Trang Tài nguyên AI Agent

Trang: `tai-nguyen-ai-agent.html`. Dữ liệu: `data/ai-agent-resources.json`.

## Thêm hoặc sửa một tài nguyên
1. Mở `data/ai-agent-resources.json`, thêm vào `items` của nhóm phù hợp (`video`, `github`, `huong-dan`, `sach`, `nghien-cuu`, `khoa-hoc`):
   `{"name": "...", "provider": "...", "level": "Nhập môn|Nền tảng|Thực hành|Nâng cao|Nghiên cứu|Tham khảo", "url": "https://...", "description_vi": "1–2 câu tự viết"}`
   Không có link chính thức thì bỏ `url` (thẻ hiện tên, không link).
2. Đổi `updated` thành ngày hôm nay (YYYY-MM-DD).
3. Chạy: `python3 scripts/resources_build.py --check-urls` rồi `python3 scripts/tech_pass.py`.

## Quy tắc link
- KHÔNG dùng link affiliate, link rút gọn hay link có mã theo dõi (`imp.i384100.net`, `bit.ly`, `utm_*`, `ref=`, `irclickid`...). Script sẽ báo lỗi nếu gặp.
- Dùng trang gốc chính thức (Coursera, GitHub, arXiv, trang nhà xuất bản...).
- Mô tả tự viết, đúng với nội dung thật của tài nguyên.
