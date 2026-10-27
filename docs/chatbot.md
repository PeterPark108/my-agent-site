# Trợ lý MJ trên website (chatbot)

## Cách hoạt động
- Nút avatar MJ (bông hoa đỏ) ở góc dưới **bên trái** mọi trang (trừ 404 và trang chuyển hướng). Nút gọi/Zalo vẫn ở góc phải.
- MJ **không dùng AI trên máy chủ, không gửi dữ liệu đi đâu**: khi khách mở khung chat lần đầu, trình duyệt tải `data/chatbot-kb.json` (nội dung lấy từ chính các trang của web) rồi tìm đoạn phù hợp nhất (bỏ dấu, từ đồng nghĩa, chấm điểm kiểu BM25).
- Có sẵn các ý: chào, cảm ơn, "bạn là ai / có phải người thật", danh sách dịch vụ, giá, thời gian làm, liên hệ, tra cứu tiến độ.
- Câu hỏi về giá: chỉ trích đúng bảng giá tham khảo có trên trang (hiện có: Thiết kế website, Chăm sóc website); còn lại trả lời "giá tùy phạm vi" + nút liên hệ.
- Không chắc thì trả lời "Mình chưa chắc..." kèm nút Gọi 0328 439 972, Chat Zalo, Gửi form liên hệ.
- Cuộc trò chuyện chỉ lưu trong `sessionStorage` (đóng tab là mất). Không có ô nhập thông tin cá nhân.

## Cập nhật kiến thức
1. Sửa nội dung trang (hoặc `scripts/svc_data.py` rồi chạy lại script tạo trang như mọi khi).
2. `python3 scripts/tech_pass.py`
3. `python3 scripts/chatbot_build.py` → tạo lại `data/chatbot-kb.json`
4. `python3 scripts/chatbot_eval.py` → chạy bộ câu hỏi thử trong `scripts/chatbot_eval.txt` (thêm câu mới theo mẫu `câu hỏi | trang hoặc intent:...`).
- Sửa giao diện/logic: sửa `js/chat.src.js` rồi `npx terser js/chat.src.js -c -m -o js/chat.js`. CSS nằm cuối `css/style.css` (mục "trợ lý MJ").

## Bật / tắt
- Tắt hẳn: `chatbotEnabled: false` trong `js/config.js`.
- Tắt riêng một lần xem: thêm `?chat=0` vào link.

## Nâng cấp sau này
Muốn MJ trả lời bằng mô hình ngôn ngữ (LLM) thật thì cần một máy chủ/proxy nhỏ giữ API key (không được để key trong JS công khai), giới hạn lượt gọi, và vẫn nên "mớm" nội dung từ `chatbot-kb.json` để không bịa. Hiện **chưa làm**.
