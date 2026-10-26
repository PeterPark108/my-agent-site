# Việc Peter tự làm cho SEO (agent không làm thay)

1. **Google Search Console** (search.google.com/search-console): Thêm thuộc tính → chọn **Miền** → nhập `myagentvn.com` → chép bản ghi TXT → thêm vào DNS nơi quản lý tên miền (loại TXT, tên `@`) → bấm Xác minh (có thể chờ vài phút đến vài giờ). Vào **Sơ đồ trang web** → gửi `https://myagentvn.com/sitemap.xml`.
2. **Yêu cầu lập chỉ mục:** trong Search Console, dán từng URL vào ô kiểm tra trên cùng → **Yêu cầu lập chỉ mục**: trang chủ, `/dich-vu.html`, `/dich-vu/thiet-ke-website.html`, `/lien-he.html`, rồi các trang dịch vụ chính.
3. **Bing Webmaster Tools** (bing.com/webmasters): đăng nhập → **Nhập từ Google Search Console** (tự lấy site và sitemap).
4. **Google Business Profile** (business.google.com): cần tên doanh nghiệp đúng giấy phép, **địa chỉ thật** (hoặc chọn "doanh nghiệp khu vực dịch vụ" để ẩn địa chỉ, phục vụ TP.HCM), số điện thoại 0328439972, danh mục (vd "Nhà thiết kế trang web"), giờ làm việc, website `https://myagentvn.com`, logo và vài ảnh thật. Google sẽ xác minh bằng video/điện thoại/thư — chỉ Peter làm được.
5. **Trang mạng xã hội:** khi có Zalo OA, Facebook Page, LinkedIn, Google Business Profile → gửi link cho agent để thêm vào `sameAs` (schema) và chân trang.
6. **Google Analytics 4:** tạo luồng dữ liệu web cho `https://myagentvn.com` → chép Measurement ID dạng `G-XXXXXXX` → gửi agent điền vào `js/config.js` (trường `gaId`). Nên thêm banner đồng ý cookie nếu cần tuân thủ NĐ 13/2023.
7. Sau 1–2 tuần, xem báo cáo **Trang** và **Hiệu quả** trong Search Console, gửi agent nếu có lỗi.
