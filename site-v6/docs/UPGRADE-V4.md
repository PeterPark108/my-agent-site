# My Agent — bản nâng cấp v4

Tài liệu này mô tả trạng thái hiện hành và thay thế các mô tả cũ về showcase concept Aurora/Orbit/Forma.

## Đối chiếu website thật

Đã xem lại trực tiếp https://myagentvn.com/ và trang https://myagentvn.com/du-an.html vào 05/11/2026 (Asia/Bangkok). Site hiện tại đã có hero glass, hệ thống nhiều nhóm dịch vụ, portfolio, form tư vấn, Zalo, bảng giá, combo và tra cứu tiến độ. Vì thế bản nâng cấp cần thể hiện năng lực và đường đi của khách rõ hơn, không chỉ tăng trang trí.

Trang Dự án nói rõ các sản phẩm là mẫu do Peter tự làm, không phải dự án làm cho khách hàng. Bản v4 giữ nguyên phân biệt này; không chuyển demo thành case study khách hàng và không thêm số liệu doanh thu hoặc hiệu quả giả.

## Thay đổi thực hiện

- Giữ logo, màu thương hiệu, hero chữ/khối cầu theo yêu cầu trước và nền sao xuyên trang; tinh chỉnh mật độ nền và độ tương phản glass.
- Bổ sung nội dung giới thiệu website và dịch vụ số; dùng dải thông điệp ngắn thay cho thống kê không có bằng chứng.
- Giữ ba giải pháp website chính và link vào trang thiết kế website thật.
- Thêm Ecosystem: năm nhóm dịch vụ lấy từ menu site thật, có tab, điều khiển keyboard và link dịch vụ cụ thể.
- Portfolio thay ba concept tự tạo bằng Nhà Gió, XN Linh Kiện Máy In và NHỊP; thêm hai thẻ NhàĐất Việt và Hướng Nghiệp 360. Ảnh tải trực tiếp từ thư mục assets/projects của site.
- Khung LED/GSAP vẫn chuyển lớp khi cuộn, có chọn dự án trực tiếp, link demo tương ứng và bỏ qua cuộn. Controls nằm trong khung pin.
- Contact có Zalo, điện thoại, email và form phác thảo. Form tạo mailto để người dùng xem/gửi trong ứng dụng email; không gửi tới backend, không giả thông báo thành công. Có link tới form đang chạy trên site thật.
- Footer bổ sung combo, bảng giá, tra cứu tiến độ, blog, chính sách và thông tin chủ thương hiệu đã có trên website.

## Những phần chưa đưa sang local

Không sao chép endpoint form, chatbot MJ, hệ thống tra cứu, CMS hoặc tin tức động từ site thật. Các mục này vẫn có đường dẫn về website hiện tại. Nếu muốn thay thế toàn bộ site, Grokbot phải lập danh sách route, redirect, backend và SEO trước khi triển khai. Đây là nâng cấp trang chủ trong repository, không phải chuyển đổi toàn hệ thống.

## Kết quả kiểm tra

- Build production: PASS; Next.js 16.4.5, TypeScript/prerender hoàn tất.
- ESLint: PASS; typecheck: PASS.
- Playwright: 6/6 PASS, exit 0. Desktop/mobile: logo, nav/hash, FAQ, mailto, overflow, pageerror, reduced motion, chọn nhóm dịch vụ, chọn demo và validate form rỗng.
- Visual: đã xem desktop và mobile 390px; ảnh không hỏng; không overflow ngang ở kích thước kiểm tra; tab phần mềm hiển thị đúng; chọn demo thứ hai đồng bộ link xnlinhkien.myagentvn.com.
- Chưa chạy Lighthouse/axe/Safari thật. Chưa gửi email, dữ liệu form hoặc kiểm thử backend. Không deploy lên myagentvn.com.
- Windows từng chặn tạo thư mục build EPERM; sau khi cấp quyền ghi riêng repository, build hoàn tất. Output hiện tại dùng .next-v4; thư mục build không nằm trong ZIP.

## Việc tiếp theo cho Grokbot

1. Dùng v4 làm baseline, không khôi phục concept hư cấu cũ.
2. Duyệt copy và quyền sử dụng ảnh demo trước public. Giữ nhãn sản phẩm mẫu.
3. Nếu cần form gửi trực tiếp: xác định endpoint/CRM được ủy quyền, validation server, chống spam, consent và xử lý lỗi; không đoán endpoint từ HTML.
4. Audit nội dung, contrast, Lighthouse, keyboard, Safari; kiểm tra thay đổi reduced motion khi đang pin và đổi orientation.
5. Chỉ cấu hình indexing/canonical/sitemap và nối domain khi có kế hoạch thay thế site thật, backup và rollback.
