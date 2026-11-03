---
title: "Synology cảnh báo mã độc tống tiền tấn công NAS chưa cập nhật"
date: 2026-11-03
topic: bao-mat
summary: "Ngày 29/10/2026, Synology cảnh báo kẻ xấu đang khai thác một lỗ hổng đã vá từ cuối 2024 để mã hoá dữ liệu trên NAS chạy DSM cũ. Bài tóm tắt điểm chính và việc nên làm ngay."
insight: "Ổ lưu trữ mạng (NAS) thường chứa hợp đồng, hoá đơn, ảnh sản phẩm và bản sao lưu của cả công ty, nên mất nó là mất rất nhiều. Hãy cập nhật DSM, bật cập nhật tự động, không mở trang quản trị NAS ra Internet và giữ thêm một bản sao lưu tách rời."
tags: [synology, nas, ransomware, sao-luu]
sources:
  - name: Synology – thông cáo cảnh báo ransomware trên DSM cũ
    url: https://www.synology.com/en-global/company/news/article/C3RB3R/Synology
    date: 2026-10-29
  - name: Synology Security Advisory Synology-SA-24:20
    url: https://www.synology.com/en-global/security/advisory/Synology_SA_24_20
  - name: BleepingComputer
    url: https://www.bleepingcomputer.com/news/security/synology-warns-customers-of-ongoing-c3rb3r-ransomware-attacks/
    date: 2026-11-02
---
## Chuyện gì đang xảy ra

Ngày 29/10/2026, Synology, hãng sản xuất thiết bị lưu trữ mạng (NAS) phổ biến, phát đi thông cáo cảnh báo người dùng. Theo hãng, kẻ tấn công đang lợi dụng một lỗ hổng **đã được vá từ tháng 12/2024** để nhắm vào các thiết bị còn chạy phiên bản hệ điều hành DSM cũ. Mục tiêu là mã hoá dữ liệu rồi đòi tiền chuộc.

Trang tin bảo mật BleepingComputer cho biết đợt tấn công dùng mã độc tống tiền có tên C3RB3R. Người dùng bị hại phản ánh các tệp bị đổi đuôi thành `.L0CK3D`, kèm một tệp ghi chú đòi tiền tên `read-me3.txt`. Cũng theo trang này, đây là lần hiếm hoi Synology chủ động phát cảnh báo về một chiến dịch tấn công đang diễn ra; lần gần nhất là năm 2019.

## Lỗ hổng nào bị khai thác?

Synology chưa nói rõ chính xác lỗ hổng nào đang bị dùng. Thông cáo dẫn tới bản tư vấn bảo mật **Synology-SA-24:20**, công bố tháng 11/2024, gồm ba lỗi trên DSM:

- **CVE-2024-10441**: mức nghiêm trọng, cho phép kẻ tấn công từ xa chạy mã tuỳ ý.
- **CVE-2024-50629**: cho phép đọc một số tệp giới hạn.
- **CVE-2024-10445**: lỗi kiểm tra chứng chỉ ở chức năng cập nhật, cho phép ghi một số tệp giới hạn.

Bản tư vấn liệt kê các bản đã vá, ví dụ DSM 7.2.2-72806-1, 7.2.1-69057-6, 7.2-64570-4, 7.1.1-42962-7 và 6.2.4-25556-8 trở lên. Thiết bị nào thấp hơn các bản này đều nằm trong diện rủi ro.

Synology khuyên người dùng cập nhật DSM ngay và bật cập nhật tự động. BleepingComputer bổ sung lời khuyên chặn truy cập trang quản trị web của NAS từ Internet. Theo trang này, tổ chức giám sát Shadowserver đang ghi nhận hơn 380.000 thiết bị NAS Synology lộ ra Internet, dù chưa rõ bao nhiêu thiết bị đã được vá.

## Góc nhìn cho doanh nghiệp nhỏ

Nhiều văn phòng, cửa hàng và công ty nhỏ mua NAS để lưu tài liệu chung hoặc làm nơi sao lưu, rồi để thiết bị chạy nhiều năm không ai ngó tới. Đợt tấn công này cho thấy một lỗ hổng đã có bản vá gần hai năm vẫn gây hại được, chỉ vì thiết bị không được cập nhật. Một vài việc nên làm trong tuần này:

1. Đăng nhập NAS, xem phiên bản DSM. Nếu thấp hơn các bản đã vá nêu trên, hãy cập nhật lên bản mới nhất mà thiết bị hỗ trợ.
2. Bật cập nhật tự động cho DSM và các gói ứng dụng cài trên NAS.
3. Không mở trang quản trị NAS ra Internet. Nếu cần truy cập từ xa, dùng VPN hoặc giải pháp được hãng khuyến nghị, và bật xác thực hai bước.
4. Giữ thêm ít nhất một bản sao lưu tách rời (ổ cứng ngoài cất riêng hoặc dịch vụ lưu trữ đám mây có lưu nhiều phiên bản), vì NAS bị mã hoá thì bản sao lưu nằm trên chính NAS cũng mất theo.
5. Nếu thiết bị đã quá cũ, không còn nhận bản cập nhật, hãy lên kế hoạch thay thế.

Cập nhật đều đặn và sao lưu đúng cách vẫn là hai lớp bảo vệ đơn giản nhưng hiệu quả nhất trước mã độc tống tiền.
