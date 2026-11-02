---
title: "WordPress 7.1.4 vá nhiều lỗi bảo mật, nên cập nhật"
date: 2026-11-02
topic: bao-mat
summary: "WordPress phát hành bản 7.1.4 ngày 28/10/2026, sửa một loạt lỗi bảo mật, trong đó có lỗi ở quá trình cập nhật lõi có thể dẫn tới chạy mã từ xa. Bài tóm tắt điểm chính và việc cần làm."
insight: "Nếu doanh nghiệp đang dùng WordPress, việc đầu tiên là kiểm tra phiên bản và cập nhật lên 7.1.4 hoặc bản vá tương ứng. Sau đó rà lại danh sách tài khoản có quyền viết bài, vì phần lớn lỗi lần này cần một tài khoản trên site mới khai thác được."
tags: [wordpress, bao-mat, cap-nhat]
sources:
  - name: WordPress.org News – WordPress 7.1.4
    url: https://wordpress.org/news/2026/10/wordpress-7-1-4/
    date: 2026-10-28
  - name: GitHub Security Advisory GHSA-4w3m-c66w-69mg (WordPress)
    url: https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-4w3m-c66w-69mg
    date: 2026-10-29
---
## Có gì mới

Ngày 28/10/2026, nhóm phát triển WordPress phát hành phiên bản **7.1.4**, một bản cập nhật chủ yếu để vá lỗi bảo mật. Thông báo chính thức khuyến nghị quản trị viên cập nhật website ngay. Có thể cập nhật trong trang quản trị (mục Bảng tin → Cập nhật) hoặc tải từ WordPress.org; các site đã bật cập nhật nền tự động sẽ tự nhận bản mới.

Đây là bản phát hành chu kỳ ngắn. Theo WordPress, phiên bản lớn tiếp theo là 7.2, đang dự kiến ra mắt ngày 8/12.

## Những lỗi đáng chú ý

Danh sách sửa lỗi trong bản 7.1.4 khá dài. Một số điểm chính:

- **Lỗi trong quá trình cập nhật lõi WordPress.** Theo bản tư vấn bảo mật trên GitHub, khi cập nhật bằng gói đầy đủ, WordPress giải nén tệp mới vào một thư mục có tên dễ đoán nằm trong thư mục upgrade mà web server có thể truy cập. Kẻ tấn công không cần đăng nhập, nếu "chạy đua" thành công đúng lúc giải nén, có thể dẫn tới thực thi mã từ xa. Bản tư vấn này xếp mức độ nghiêm trọng là thấp, vì khoảng thời gian khai thác rất hẹp.
- **Nhiều lỗi XSS lưu trữ (stored XSS)**: liên quan tới mã khối (block) được tạo đặc biệt, yêu cầu xoá dữ liệu cá nhân, Interactivity API, Customizer, khối Categories, khối Playlist và hình ảnh, khối phân trang bình luận, và tên đăng nhập được tạo đặc biệt.
- Một lỗi **từ chối dịch vụ** trong Interactivity API.
- Bản nháp thay đổi giao diện (changeset) của Customizer chưa xuất bản có thể bị người chưa đăng nhập phát hiện.
- Ghi chú (Notes) có thể bị người dùng có quyền cao đọc dù họ không có quyền sửa bài viết gắn với ghi chú đó.
- Cập nhật bộ chứng chỉ gốc đi kèm, do chứng chỉ của eMudhra bị thu hồi.

Đáng chú ý, trong danh sách người báo lỗi có các nhà nghiên cứu từ VietSunshine Cyber Security, một đơn vị bảo mật tại Việt Nam.

## Phiên bản cũ thì sao?

WordPress cho biết các bản vá đã được đưa ngược về mọi nhánh còn nhận bản sửa bảo mật, hiện tính tới nhánh 4.7. Ví dụ, bản tư vấn trên GitHub liệt kê các phiên bản đã vá như 7.0.8, 6.9.11, 6.8.12 và tiếp tục xuống tới 4.7.39. Tuy vậy, WordPress nhắc lại rằng chỉ phiên bản mới nhất mới được hỗ trợ đầy đủ.

## Góc nhìn cho doanh nghiệp nhỏ

Nhiều website bán hàng, giới thiệu công ty hay homestay tại Việt Nam chạy trên WordPress, và thường không có người theo dõi cập nhật thường xuyên. Một vài việc nên làm trong tuần này:

1. Đăng nhập trang quản trị, xem phiên bản WordPress hiện tại. Nếu chưa phải 7.1.4 (hoặc bản vá tương ứng của nhánh đang dùng) thì cập nhật.
2. Sao lưu toàn bộ website và cơ sở dữ liệu trước khi cập nhật, nhất là khi site có nhiều plugin.
3. Rà lại danh sách tài khoản: xoá tài khoản cũ không dùng, chỉ cấp quyền viết bài hoặc quản trị cho người thật sự cần.
4. Nếu thuê đơn vị bên ngoài quản lý web, hãy hỏi họ đã cập nhật chưa và có lịch kiểm tra định kỳ không.

Cập nhật đều đặn là cách rẻ và hiệu quả nhất để giảm rủi ro website bị chèn mã độc hay bị chiếm quyền.
