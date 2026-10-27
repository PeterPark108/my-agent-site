# Nhật ký thay đổi

## 0.7.0 - 2026-10-27
- Tin tức công nghệ thành hệ thống đăng bài: mỗi bài là 1 file Markdown `data/news/YYYY-MM-DD-slug.md` (front-matter + nội dung), dựng bằng `scripts/news_build.py`, kiểm tra bằng `scripts/news_publish.sh`.
- Trang bài viết `tin-tuc/<slug>.html`: breadcrumb, ngày đăng/cập nhật, chủ đề, thời gian đọc, mục lục (bài dài), Nguồn tham khảo, Góc nhìn My Agent, dịch vụ liên quan, bài trước/sau, bài liên quan; NewsArticle + BreadcrumbList JSON-LD, og:type article.
- Danh sách phân trang 12 tin (`tin-tuc/trang-N.html`, rel prev/next), lọc chủ đề bằng trang riêng `tin-tuc/chu-de/<chủ-đề>.html` (chạy cả khi tắt JS), RSS `tin-tuc/feed.xml`, `tin-tuc/` chuyển về `tin-tuc.html`.
- Bộ Markdown an toàn tự viết (`scripts/news_md.py`, escape HTML, chặn link javascript:), validator tiếng Việt, kiểm thử `scripts/test_news.py`. 10 tin cũ chuyển sang `data/news/` dạng thẻ link, nội dung giữ nguyên; bỏ `data/news.json`.
- tech_pass/seo_audit/chatbot_build hỗ trợ trang trong `tin-tuc/`; tài liệu `docs/tin-tuc.md`, `docs/tin-tuc-format.json`, mẫu `data/news/_template.md.example`.

## 0.6.0 - 2026-10-27
- Thêm trợ lý MJ (chatbot chạy trong trình duyệt, avatar bông hoa đỏ) góc dưới trái mọi trang: trả lời từ nội dung web (`data/chatbot-kb.json`), câu hỏi nhanh, gợi ý liên hệ khi chưa chắc.
- Thêm `scripts/chatbot_build.py`, `scripts/chatbot_eval.py` (+ `chatbot_eval.txt`), `docs/chatbot.md`, `assets/mj-avatar.*`; cấu hình `chatbotEnabled` / `?chat=0`.

## 0.5.0 – 2026-10-27
- Trang mới **Lộ trình học AI Agent** (`tai-nguyen-ai-agent.html`): 49 tài nguyên công khai chia 6 nhóm (Video, GitHub, Tài liệu hướng dẫn, Sách, Bài nghiên cứu, Khóa học), tab theo nhóm, ô tìm kiếm, mô tả tiếng Việt, link gốc.
- Dữ liệu ở `data/ai-agent-resources.json`, dựng bằng `scripts/resources_build.py` (có `--check-urls`, chặn link affiliate/theo dõi); hướng dẫn ở `docs/tai-nguyen-ai-agent.md`.
- Link khóa học dùng trang Coursera chính thức, đã bỏ link affiliate và mã theo dõi. Có trong chân trang và sitemap; CollectionPage/ItemList + BreadcrumbList JSON-LD.

## 0.4.0 – 2026-10-27
- Mục mới **Tin tức công nghệ** (`tin-tuc.html`): 10 tin có thật kèm nguồn, bộ lọc theo chủ đề và Góc nhìn My Agent; trang chủ có khối "Tin công nghệ mới nhất".
- Dữ liệu tin nằm ở `data/news.json`, dựng bằng `scripts/news_build.py` (có `--check-urls`); hướng dẫn ở `docs/tin-tuc.md`.
- SEO: CollectionPage/ItemList + BreadcrumbList JSON-LD, có trong sitemap. Menu và chân trang có thêm mục Tin tức.
- Menu desktop: nhãn không còn xuống dòng; mega menu luôn nằm gọn trong màn hình ở 961–1440px.

## 0.3.0 — 2026-10-27
- 18 trang dịch vụ: thêm khối "Góc nhìn chuyên môn" (sơ đồ SVG inline riêng từng dịch vụ + checklist chuyên môn), quy trình có mô tả từng bước, "Bạn nhận được gì", "Công nghệ & công cụ", "Phù hợp với ai", dịch vụ liên quan, FAQ chuyên sâu (FAQPage JSON-LD tự khớp nội dung hiển thị).
- Sinh bằng scripts/svc_deep.py từ scripts/svc_data.py (idempotent, giữa marker svc-deep); CSS thành phần dùng chung trong css/style.css.
- SEO on-page: rà title/description/H1/heading/canonical/og cho 18 trang; meta description Google Maps chứa từ khoá chính.

## 0.2.1 — 2026-10-27
- Trang Về chúng tôi: thay khối console bằng ảnh người sáng lập Nguyễn Văn Tùng (PeterPark) mặc vest, cắt từ ngực trở lên (webp + jpg, 800/480px), khung viền neon, chú thích tên.

## 0.2.0 — 2026-10-27
- Mới: lớp animation toàn site (`js/motion.js` + CSS): thanh tiến trình cuộn, hero hiện lần lượt + parallax, vạch neon tiêu đề, thẻ nghiêng 3D, nút quét sáng/gợn sóng, vạch chỉ báo menu, menu mobile động, chuyển trang mượt, viền gradient CTA/footer.
- Công tắc `motionEnabled` (js/config.js) và `?motion=0`; tôn trọng prefers-reduced-motion. Tài liệu: docs/animation.md.
- Sửa CLS: glow chuột dùng transform; console gõ chữ giữ chiều cao cố định trên mobile.
- Cache-busting `?v=` thêm cho main.js và motion.js.

## 0.1.8 - 2026-10-27
- Intro: nút Bỏ qua chỉ còn icon ×, không còn chữ trong intro.
- Cache-busting ?v=VERSION cho style.min.css và intro.js trên mọi trang.

## v0.1.7 — 27/10/2026
- Làm lại intro trang chủ theo yêu cầu: chỉ còn logo My Agent, xuất hiện hoành tráng (~3,3 giây): tia sáng hội tụ, chớp sáng + vòng sóng xung kích, logo phóng/nhòe vào, glitch tách màu, hạt bung, glow neon, vệt sáng quét, rồi phóng-tan vào trang. Bỏ dòng terminal, thanh tiến trình, phần trăm. Giữ nguyên Bỏ qua/Esc, sessionStorage, reduced-motion, introEnabled, ?intro=1/0.

## v0.1.6 — 27/10/2026
- Màn intro "khởi động hệ thống" ở trang chủ (~3,6 giây): dòng lệnh gõ chữ, thanh tiến trình, ký tự mã rơi + lưới + scan-line, logo My Agent hiện dần rồi mờ vào trang. Nút "Bỏ qua" / phím Esc.
- Chỉ hiện lần đầu mỗi phiên, bỏ qua khi giảm chuyển động; bật/tắt bằng introEnabled trong js/config.js, ?intro=1 / ?intro=0 (docs/intro.md).

## v0.1.5 — 27/10/2026
- Nút gọi nổi (.fab) gọi thẳng tel:0328439972 (aria-label "Gọi 0328 439 972"); trên máy tính bấm vào hiện hộp số điện thoại với Sao chép số / Gọi / Chat Zalo (Esc hoặc bấm ngoài để đóng).
- Thêm nút Zalo nổi (https://zalo.me/0328439972) phía trên nút gọi trên mọi trang.
- Thêm dòng "Điện thoại / Zalo: 0328 439 972" ở chân trang và khối thông tin trang Liên hệ; link Zalo dưới form có href mặc định thật.

## v0.1.4 — 27/10/2026
- Dự án Hướng Nghiệp 360: nút "Xem bản chạy" (trang chủ, du-an.html) đổi sang https://huongnghiep.myagentvn.com.
- Thêm địa chỉ ngắn /tra-cuu-tien-do/ (trang chuyển hướng noindex, giữ ?ma= và #) tới tra-cuu-tien-do.html.

## v0.1.3 — 27/10/2026
- Đổi cam kết: "lên trang đầu Google" → "tối ưu để tăng thứ hạng trên Google" (SEO tổng thể).
- Đổi cam kết: "hỗ trợ kỹ thuật 24/7" / "Hỗ trợ ưu tiên 24/7" → "... trong giờ làm việc, phản hồi trong 24 giờ" (Hosting SEO, gói Chuyên nghiệp các trang dịch vụ).

## v0.1.2 — 27/10/2026
- SEO toàn diện: title/description riêng từng trang theo bộ từ khóa đã chốt (scripts/seo_pages.py), canonical + hreflang vi/x-default về https://myagentvn.com, Open Graph/Twitter đầy đủ.
- JSON-LD: ProfessionalService + WebSite (trang chủ), Service + BreadcrumbList + FAQPage (trang dịch vụ), BreadcrumbList các trang khác; areaServed TP.HCM + Việt Nam.
- Trang tra cứu tiến độ: noindex, follow và loại khỏi sitemap; sitemap có lastmod.
- Trang 404.html (noindex). CSS rút gọn css/style.min.css (bản nguồn css/style.css giữ nguyên).
- Thêm scripts/seo_audit.py, docs/seo-tu-khoa.md, docs/seo-viec-cua-peter.md, docs/seo-yeu-cau-may-chu.md.
- Đổi chữ tối thiểu: H1 trang Thiết kế website, câu mở đầu trang chủ và trang Thiết kế website (xem báo cáo cho MJ duyệt).

## v0.1.0 — 27/10/2026
- Bản phát hành đầu tiên trên myagentvn.com: trang chủ, giới thiệu, 18 trang dịch vụ, combo, dự án, công cụ, liên hệ (form gửi về lienhe@myagentvn.com), tra cứu tiến độ đơn, ghi nguồn & giấy phép, chính sách bảo mật.
- SEO cơ bản (title, meta, ảnh chia sẻ, sitemap, robots), chỗ gắn Google Analytics.
- Quy trình triển khai an toàn: nhánh dev / production, CI kiểm tra, tag phiên bản.
