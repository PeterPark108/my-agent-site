# Kế hoạch từ khóa và nội dung SEO – myagentvn.com

Bộ từ khóa chính **đã chốt với Peter**. Mỗi từ khóa chính gắn đúng 1 trang (tránh các trang tự cạnh tranh nhau). Title/description từng trang nằm trong `scripts/seo_pages.py` (sửa ở đó rồi chạy `python3 scripts/tech_pass.py`).

> Không có dữ liệu lượng tìm kiếm: agent không có công cụ đo (Google Keyword Planner cần tài khoản Google Ads của Peter). Không bịa số. Khi có Search Console, dùng báo cáo "Hiệu quả" để chọn lại thứ tự ưu tiên.

Quy tắc: từ khóa dùng tự nhiên trong title (≤60 ký tự), description (≤155), H1/H2 và đoạn mở đầu; không nhồi. "Giá rẻ" diễn đạt là "chi phí hợp lý, báo giá rõ ràng", không ghi giá, không hứa quá mức.

## 1. Bảng từ khóa → trang đích

| Trang đích | Từ khóa chính | Từ khóa phụ / biến thể | Ý định tìm kiếm |
|---|---|---|---|
| `/` (trang chủ) | thiết kế web trọn gói | thiết kế web giá rẻ, thiết kế website HCM, dịch vụ thiết kế web TP.HCM, My Agent | Thương mại – tìm đơn vị làm web |
| `/dich-vu/thiet-ke-website.html` | thiết kế website chuẩn SEO | thiết kế web bán hàng, thiết kế web doanh nghiệp, thiết kế web landing page, thiết kế web cho shop/cá nhân, làm website giá rẻ TPHCM, thiết kế web responsive, web có quản lý đơn hàng | Thương mại – so sánh, hỏi báo giá |
| `/dich-vu.html` | dịch vụ marketing online | dịch vụ marketing online tại HCM, dịch vụ số cho doanh nghiệp | Tìm hiểu tổng quan |
| `/dich-vu/seo-tong-the.html` | dịch vụ SEO tổng thể | dịch vụ SEO tại HCM, SEO website | Thương mại |
| `/dich-vu/quang-cao-google-facebook.html` | quảng cáo Google Ads, Facebook Ads | chạy quảng cáo Facebook tại HCM, dịch vụ Google Ads TP.HCM | Thương mại |
| `/dich-vu/cham-soc-fanpage.html` | dịch vụ chăm sóc fanpage | chăm sóc fanpage tại HCM | Thương mại |
| `/dich-vu/cham-soc-website.html` | dịch vụ chăm sóc website | chăm sóc website tại HCM, bảo trì website | Thương mại |
| `/dich-vu/email-doanh-nghiep.html` | email doanh nghiệp theo tên miền | email doanh nghiệp tại HCM, email tên miền riêng | Thương mại |
| `/dich-vu/google-maps.html` | đăng ký Google Maps doanh nghiệp | đưa doanh nghiệp lên Google Maps tại HCM | Thương mại / hướng dẫn |
| `/dich-vu/hosting-seo.html` | hosting SEO | hosting tốc độ cao tại HCM | Thương mại |
| `/dich-vu/ten-mien.html` | đăng ký tên miền | đăng ký tên miền .vn, .com tại HCM | Thương mại |
| `/dich-vu/thiet-ke-app.html` | thiết kế app di động | thiết kế app iOS Android tại HCM | Thương mại |
| `/dich-vu/phan-mem-noi-bo.html` | phần mềm quản lý nội bộ | phần mềm quản lý theo yêu cầu tại HCM | Thương mại |
| `/dich-vu/phan-tich-du-lieu.html` | dịch vụ Data Analyst | phân tích dữ liệu bán hàng, Data Analyst tại HCM, dashboard báo cáo | Thương mại |
| `/dich-vu/ky-thuat-du-lieu.html` | dịch vụ Data Engineer | kỹ thuật dữ liệu, Data Engineer tại HCM, tự động hoá dữ liệu | Thương mại |
| `/dich-vu/profile-doanh-nghiep.html` | thiết kế profile doanh nghiệp | thiết kế hồ sơ năng lực tại HCM, thiết kế đồ họa doanh nghiệp | Thương mại |
| `/dich-vu/bo-cong-thuong.html` | đăng ký website Bộ Công Thương | thông báo website TMĐT tại HCM | Thông tin + thương mại |
| `/dich-vu/traffic-user.html` | dịch vụ traffic user | traffic website tại HCM | Thương mại |
| `/dich-vu/video-ai.html` | dịch vụ edit video, video AI | dựng video tại HCM | Thương mại |
| `/dich-vu/zalo-oa-mini-app.html` | Zalo OA, Zalo Mini App | làm Zalo Mini App tại HCM | Thương mại |
| `/combo.html` | combo dịch vụ website và marketing | gói website trọn gói kèm marketing | Thương mại |
| `/du-an.html`, `/ve-chung-toi.html`, `/lien-he.html` | thương hiệu "My Agent" | My Agent liên hệ, báo giá | Điều hướng |

Ghi chú: "thiết kế đồ họa" hiện chỉ có dịch vụ gần nhất là Profile doanh nghiệp; nếu Peter muốn từ khóa riêng "thiết kế đồ họa / logo" thì cần một trang dịch vụ mới (MJ viết nội dung).

## 2. Kế hoạch bài viết (blog) cho MJ

Mỗi bài: 1 từ khóa đích riêng (không trùng từ khóa chính của trang dịch vụ), cuối bài dẫn link về trang dịch vụ tương ứng + `/lien-he.html`. Không ghi giá cụ thể.

1. **Thiết kế web trọn gói gồm những gì? Checklist trước khi thuê** – từ khóa: thiết kế web trọn gói gồm những gì – ý: tên miền, hosting, giao diện, nội dung, bàn giao, bảo hành – link: `/`, `/dich-vu/thiet-ke-website.html`.
2. **Chi phí làm website phụ thuộc vào yếu tố nào?** – chi phí làm website – ý: phạm vi trang, tính năng, nội dung, bảo trì; vì sao cần báo giá rõ ràng – link: `/combo.html`.
3. **Website chuẩn SEO là gì? 12 tiêu chí kỹ thuật** – website chuẩn SEO là gì – ý: tốc độ, mobile, cấu trúc URL, schema – link: `/dich-vu/thiet-ke-website.html`, `/dich-vu/seo-tong-the.html`.
4. **Landing page bán hàng: bố cục giúp tăng chuyển đổi** – cách làm landing page – link: `/dich-vu/thiet-ke-website.html`.
5. **Web bán hàng cần những tính năng gì (giỏ hàng, quản lý đơn)** – tính năng web bán hàng – link: `/dich-vu/thiet-ke-website.html`.
6. **Responsive là gì và vì sao web phải đẹp trên điện thoại** – website responsive là gì – link: `/dich-vu/thiet-ke-website.html`.
7. **Chọn tên miền .vn hay .com cho doanh nghiệp** – nên chọn tên miền .vn hay .com – link: `/dich-vu/ten-mien.html`.
8. **Hosting ảnh hưởng tới SEO thế nào** – hosting ảnh hưởng SEO – link: `/dich-vu/hosting-seo.html`.
9. **Email theo tên miền: cách tạo và lợi ích** – cách tạo email theo tên miền – link: `/dich-vu/email-doanh-nghiep.html`.
10. **Hướng dẫn thông báo website với Bộ Công Thương** – thông báo website với Bộ Công Thương – link: `/dich-vu/bo-cong-thuong.html`.
11. **Cách đưa cửa hàng lên Google Maps từng bước** – cách đưa cửa hàng lên Google Maps – link: `/dich-vu/google-maps.html`.
12. **SEO tổng thể khác SEO từ khóa ở điểm nào** – SEO tổng thể là gì – link: `/dich-vu/seo-tong-the.html`.
13. **Google Ads hay Facebook Ads: chọn kênh nào cho doanh nghiệp nhỏ** – nên chạy Google Ads hay Facebook Ads – link: `/dich-vu/quang-cao-google-facebook.html`.
14. **Lịch đăng bài Fanpage 30 ngày cho shop** – lịch đăng bài fanpage – link: `/dich-vu/cham-soc-fanpage.html`.
15. **Bảo trì website hằng tháng gồm những việc gì** – bảo trì website gồm những gì – link: `/dich-vu/cham-soc-website.html`.
16. **Data Analyst giúp chủ shop đọc số liệu bán hàng ra sao** – phân tích dữ liệu bán hàng cho shop – link: `/dich-vu/phan-tich-du-lieu.html`.
17. **Data Engineer là gì? Khi nào doanh nghiệp nhỏ cần** – Data Engineer là gì – link: `/dich-vu/ky-thuat-du-lieu.html`.
18. **Zalo OA và Zalo Mini App: khác nhau và nên làm cái nào** – Zalo Mini App là gì – link: `/dich-vu/zalo-oa-mini-app.html`.
19. **Hồ sơ năng lực doanh nghiệp cần có những mục nào** – hồ sơ năng lực gồm những gì – link: `/dich-vu/profile-doanh-nghiep.html`.
20. **Làm video ngắn bằng AI cho kênh bán hàng** – làm video bằng AI – link: `/dich-vu/video-ai.html`.

Dàn ý chung: mở bài nêu vấn đề (có từ khóa trong 100 chữ đầu) → 3–6 H2 trả lời trực tiếp → ví dụ thực tế (không bịa số liệu khách) → FAQ ngắn 3 câu → kêu gọi liên hệ. Kỹ thuật: cần tạo mục `/blog/` (agent web làm khung trang + đưa vào sitemap khi MJ có bài đầu).

## 3. SEO địa phương (TP.HCM)

- Schema đã khai báo areaServed: Thành phố Hồ Chí Minh + Việt Nam; chưa có địa chỉ đường phố (chỉ thêm khi Peter có địa chỉ kinh doanh công khai).
- Tên – số điện thoại (NAP) phải giống hệt nhau ở web, Google Business Profile, Zalo OA, Facebook: "My Agent", 0328439972.
- Google Business Profile là yếu tố quan trọng nhất cho từ khóa "… tại HCM" (xem `docs/seo-viec-cua-peter.md`). Xin đánh giá thật từ khách sau bàn giao.
- Dùng cụm "tại TP.HCM, nhận khách toàn quốc" tự nhiên, không tạo hàng loạt trang theo từng quận (dễ bị coi là nội dung rác).
