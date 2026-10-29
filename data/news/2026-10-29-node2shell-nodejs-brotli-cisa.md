---
title: "Lỗ hổng Node2Shell trong Node.js bị CISA xác nhận đang bị khai thác"
date: 2026-10-29
topic: bao-mat
summary: "Lỗ hổng Node2Shell (CVE-2026-111497) trong bộ giải nén Brotli của Node.js vừa được CISA đưa vào danh mục bị khai thác. Node.js đã có bản vá từ 21/10, máy chủ nên cập nhật sớm."
insight: "Website hoặc ứng dụng chạy Node.js nên kiểm tra phiên bản và nâng cấp lên bản vá ngay, kể cả khi code không tự gọi tới Brotli. Nếu thuê đơn vị khác vận hành máy chủ, hãy hỏi họ đã cập nhật chưa."
tags: [nodejs, brotli, bao-mat, cisa]
sources:
  - name: Node.js – October 2026 Security Releases
    url: https://nodejs.org/en/blog/vulnerability/october-2026-security-releases
    date: 2026-10-21
  - name: CISA
    url: https://www.cisa.gov/news-events/alerts/2026/10/27/cisa-adds-two-known-exploited-vulnerabilities-catalog
    date: 2026-10-27
  - name: SecurityWeek
    url: https://www.securityweek.com/cisa-warns-of-node2shell-exploitation-as-honeypots-log-attack-attempts/
    date: 2026-10-28
  - name: Akamai Security Research
    url: https://www.akamai.com/blog/security-research/inside-node2shell-closer-look-cve-2026-111497
    date: 2026-10-26
---
## Chuyện gì đã xảy ra

Ngày 21/10/2026, dự án Node.js phát hành bản cập nhật bảo mật cho cả ba dòng đang được hỗ trợ là 22.x, 24.x và 26.x. Lỗi đáng chú ý nhất trong đợt này mang mã **CVE-2026-111497**, được giới bảo mật gọi là **Node2Shell**. Lỗi nằm trong bộ giải nén Brotli mà Node.js đóng gói sẵn. Brotli là định dạng nén do Google phát triển, được dùng rộng rãi để nén dữ liệu truyền qua HTTP.

Theo thông báo của Node.js, khi gặp một luồng dữ liệu nén bị làm sai cấu trúc, bộ giải nén không coi đó là lỗi định dạng mà tưởng mình chỉ đang thiếu dữ liệu, nên tiếp tục ghi thêm vào một vùng đệm nội bộ rất nhỏ và tràn ra ngoài. Nếu kẻ tấn công gửi được dữ liệu Brotli độc hại để ứng dụng giải nén qua module `node:zlib`, tiến trình có thể bị sập, lộ nội dung bộ nhớ, thậm chí bị chạy mã từ xa. Node.js xếp lỗi ở mức cao; lỗi được nhóm bảo mật của OpenAI phát hiện và báo cáo.

Ngày 27/10/2026, CISA đưa lỗ hổng vào danh mục KEV – nơi liệt kê các lỗ hổng đã có bằng chứng bị khai thác thực tế. SecurityWeek dẫn lời hai đơn vị vận hành hệ thống bẫy (honeypot) cho biết đã ghi nhận các lần thử tấn công. Một đơn vị nhận định bản khai thác mà kẻ tấn công dùng còn lỗi, chưa chiếm được máy chủ, nhưng cảnh báo rằng ngay cả lần tấn công thất bại cũng có thể làm sập tiến trình Node.js.

## Ai bị ảnh hưởng

Thư viện Brotli gốc từ bản 1.0.3 đến 1.2.0 đều có lỗi, nên ngoài Node.js, nhiều sản phẩm khác như Bun, Envoy, Istio cũng đã phát hành bản sửa. Với Node.js, các bản đã vá là **22.23.4**, **24.22.1** và **26.12.1**. Các dòng đã ngừng hỗ trợ không nhận bản vá; Node.js lưu ý phiên bản hết hạn luôn được coi là bị ảnh hưởng.

Theo phân tích của Akamai, ứng dụng vẫn có thể bị lộ ngay cả khi lập trình viên không trực tiếp gọi hàm giải nén Brotli, ví dụ khi nhận phản hồi qua `fetch()` có sẵn hoặc khi Express 5 đọc nội dung yêu cầu được nén.

Cùng đợt cập nhật này, Node.js còn sửa thêm một số lỗi khác liên quan tới kiểm tra chứng chỉ TLS và phân giải DNS, nên nâng cấp đủ bản mới là cách gọn nhất.

## Doanh nghiệp nhỏ nên làm gì

1. Hỏi đơn vị làm web hoặc tự kiểm tra xem website, API, công cụ nội bộ có chạy Node.js không (lệnh `node -v` trên máy chủ).
2. Nâng cấp lên bản vá tương ứng; nếu đang dùng dòng đã hết hỗ trợ thì chuyển sang dòng còn được hỗ trợ. Nên thử trên bản thử và sao lưu trước.
3. Đừng quên các ảnh Docker, máy chủ phụ hay công cụ tự động hoá cũng có thể chứa Node.js cũ.
4. Nếu ứng dụng không cần nhận dữ liệu nén từ người dùng, có thể tắt tính năng này để giảm rủi ro trong lúc chờ cập nhật.
5. Theo dõi nhật ký máy chủ: tiến trình Node.js tự khởi động lại nhiều lần bất thường là dấu hiệu cần kiểm tra.
