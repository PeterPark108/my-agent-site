---
title: "Google sẽ hỗ trợ lệnh chung chặn AI huấn luyện"
date: 2026-10-31
topic: web-seo
summary: "Google cho biết sẽ hỗ trợ một tín hiệu chung trong robots.txt để website chọn có cho AI dùng nội dung huấn luyện hay không, áp dụng cho nhiều nhà cung cấp AI, dự kiến từ năm 2027."
insight: "Chủ website nhỏ chưa cần sửa robots.txt ngay, vì cơ chế mới dự kiến chạy từ 2027. Việc nên làm bây giờ là quyết định rõ có muốn nội dung của mình được dùng để huấn luyện AI hay không, và nhớ rằng chặn huấn luyện khác với chặn Google Search."
tags: [google, robots-txt, ai]
sources:
  - name: Google Search Central Blog – Supporting a shared AI training control for websites
    url: https://developers.google.com/search/blog/2026/10/ai-training-control
    date: 2026-10-30
---
## Có gì mới

Ngày 30/10/2026, nhóm Google Search Central công bố kế hoạch hỗ trợ một **tín hiệu kiểm soát việc huấn luyện AI dùng chung** đặt trong tệp robots.txt. Ý tưởng là thay vì phải viết hướng dẫn riêng cho từng công ty AI, chủ website chỉ cần dùng một "policy token" (mã chính sách) chung để nói rõ mình có đồng ý cho nội dung được dùng huấn luyện AI hay không, và lựa chọn đó áp dụng cho các nhà cung cấp AI có tham gia.

Đề xuất này dựa trên kết quả của nhóm làm việc AIPREF thuộc IETF, tổ chức xây dựng tiêu chuẩn kỹ thuật cho Internet. Bài viết do John Mueller (Google Search Advocate) đăng tải.

## Cơ chế dự kiến hoạt động ra sao

- Nếu robots.txt dùng mã chung này để **từ chối huấn luyện AI**, và website không khai báo riêng cho **Google-Extended**, Google sẽ hiểu như thể website đã chặn Google-Extended. Google-Extended là cách kiểm soát việc huấn luyện AI mà Google cung cấp từ năm 2023.
- Các cách kiểm soát riêng của từng công ty vẫn tiếp tục hoạt động song song. Nghĩa là có thể đặt một lựa chọn chung cho tất cả, rồi tinh chỉnh riêng cho từng nhà cung cấp.
- Google lưu ý: website **cho phép rõ ràng** Google-Extended thì đủ điều kiện xuất hiện trong câu trả lời và nhận lượt nhấp thông qua cơ chế dẫn nguồn (grounding) trong ứng dụng Gemini.

## Khi nào áp dụng

Đây vẫn là bản đề xuất nháp. Google cho biết đặt mục tiêu hỗ trợ cùng các nhà cung cấp AI khác trong **năm 2027** và sẽ tiếp tục chuẩn hoá qua nhóm làm việc tại IETF. Theo Google, đề xuất phù hợp với Bộ quy tắc thực hành dành cho mô hình AI đa dụng theo Đạo luật AI của EU, vốn coi robots.txt là cách chính để chủ website thể hiện mong muốn theo dạng máy đọc được.

## Doanh nghiệp nhỏ nên làm gì

1. **Chưa cần thay đổi gì ngay.** Mã chính sách chung chưa được áp dụng; thêm vào bây giờ có thể chưa có tác dụng.
2. **Kiểm tra robots.txt hiện tại** để biết website đang cho phép hay chặn những gì. Một dòng chặn sai có thể khiến trang không được thu thập trên Google Search.
3. **Phân biệt hai việc:** chặn AI huấn luyện không giống chặn Google tìm kiếm. Nếu muốn có cơ hội được Gemini dẫn nguồn, đừng vô tình chặn Google-Extended.
4. **Theo dõi cập nhật** từ Google Search Central trong năm 2027 để điều chỉnh khi cơ chế chính thức chạy.
