# Đối chiếu thương hiệu — 05/11/2026 (Asia/Bangkok)

Đã tải trực tiếp bằng HTTPS từ site thật. Web reader không truy cập được, nhưng tải HTTP trực tiếp thành công. Đây là kiểm tra mã nguồn HTML/CSS/SVG; không khẳng định đã kiểm tra giao diện hiển thị của site gốc.

| Nguồn | Bằng chứng cục bộ | Kết quả |
|---|---|---|
| https://myagentvn.com/ | evidence/source.html | title, meta, header logo, dịch vụ, liên hệ, JSON-LD |
| https://myagentvn.com/css/style.min.css?v=0.9.36 | evidence/style.css | :root và font family |
| https://myagentvn.com/css/fonts.css | evidence/fonts.css | Be Vietnam Pro, self-hosted, OFL |
| https://myagentvn.com/assets/logo-dark.svg | ../public/brand/logo-dark.svg | SVG nguyên bản, viewBox 0 0 260 64 |
| https://myagentvn.com/assets/favicon.svg | ../public/brand/favicon.svg | Favicon nguyên bản |

SHA-256 logo: 1e7bed0fc6d614419adaf44464783b7d22cef3b6bf20319b23ddd5fad9e8d3af

## Token gốc — không phỏng đoán

| Token | Giá trị | Vai trò |
|---|---|---|
| --bg | #05070F | nền chính |
| --bg2 | #0A0F22 | nền phụ |
| --navy | #0B1E4A | navy thương hiệu, có trong logo |
| --blue | #1B3A8C | xanh thương hiệu, có trong logo |
| --el | #3D7BFF | xanh nhấn |
| --red | #E23636 | đỏ thương hiệu, có trong logo |
| --neon | #FF2D3D | đỏ nhấn |
| --tx | #E9ECF5 | chữ chính |
| --mu | #A3ABC2 | chữ phụ |
| --ln | rgba(255,255,255,.09) | đường viền |
| --gl | rgba(255,255,255,.04) | nền kính |
| --r | 18px | bo góc |

Logo SVG sử dụng #E23636, #0B1E4A, #1B3A8C, #fff. Giữ nguyên file, không vẽ lại hoặc đổi màu. Font của logo là SVG text với fallback Arial; hình dáng chữ có thể khác nếu xuất SVG ngoài môi trường đã tải font. Khi cần lockup outline, xin file gốc từ chủ thương hiệu.

HTML gốc xác nhận: My Agent cung cấp website giới thiệu, landing page, web bán hàng; TP.HCM và toàn quốc; +84328439972; vantungn044@gmail.com. Không đổi thông tin này nếu chưa được duyệt. Các câu mô tả mới là copy đề xuất. Quy trình và đồ họa showcase là concept của bản mới, không phải bằng chứng về dự án đã làm.

## Tái kiểm chứng

Mở URL nguồn và tìm :root; tìm class logo trong HTML; so hash asset. Snapshot nguồn chỉ phục vụ đối chiếu, không thực thi script HTML này trên production. Nội dung có thể thay đổi sau ngày kiểm tra.

## Tái đối chiếu v4

Snapshot mới: evidence/source-current.html và evidence/projects-current.html. Trang portfolio nguồn xác nhận các dự án là demo cá nhân, không phải khách hàng. Các URL và ảnh trong v4 lấy từ snapshot này. Không xác nhận quyền của từng ảnh nền bên trong screenshot; cần giữ ghi nguồn tương ứng của dự án nếu tái sử dụng riêng.

