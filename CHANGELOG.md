# Nhật ký thay đổi

## 0.9.2 - 2026-10-27
- Sửa lỗi giao diện trang Bảng giá: khối bảng giá theo nhóm dùng trùng class `.bg-grid` với lớp lưới nền cố định của toàn site (`position:fixed; inset:0; z-index:-2`), nên các bảng bị ghim chồng lên phần đầu trang. Đổi tên class thành `.bg-groups` trong bang_gia_build.py và style.css.
- Thanh mục lục nhóm dịch vụ (01 · Nền tảng website …) dùng thẻ `<nav>` nên trên màn hình ≤960px bị quy tắc menu di động `nav{position:fixed}` ghim lên đầu trang, chồng lên hero. Đổi thành `<div role="navigation">`.
- Thêm `scripts/test_layout.py` (Chromium/Playwright): kiểm tra khối nhóm giá nằm dưới hero, không có `position:fixed`, không có phần tử position:fixed hiển thị trong <main>, không cuộn ngang ở 1440/1280/1024/768/390, và class bố cục không trùng với lớp nền.

## 0.9.1 - 2026-10-27
- Đồng bộ giá các trang cũ theo `data/pricing.json`: khối "Bảng giá tham khảo" của 17 trang dịch vụ được sinh lại bằng `scripts/svc_pricing.py` (mức và khoảng giá như trang Bảng giá; hosting/VPS và quảng cáo ghi "Thương lượng"; ghi rõ "Giá đã bao gồm VAT" và giá tham khảo theo khoảng). Trang Traffic User vẫn không công khai giá.
- Thiết kế website: 1,5–4 / 4–10 / 8–20 triệu → Landing 2–3,6, Giới thiệu 4–7,2, Bán hàng 7,2–14,4, Web app 20–48 triệu. Chăm sóc website: 300 nghìn / 600 nghìn / 1 triệu mỗi tháng → 0,64–1,2 / 1,4–2,4 / 2,4–4 triệu mỗi tháng.
- Bài blog "Chi phí làm website phụ thuộc vào yếu tố nào?": cập nhật con số và trỏ về Bảng giá (`updated: 2026-10-27`).
- Bỏ các cam kết "phản hồi trong 24 giờ", "Nhận báo giá trong 24h", "24/7" (trang dịch vụ, dich-vu.html, trang chủ, hiệu ứng terminal).
- Chatbot: câu trả lời giá trang dịch vụ đọc đủ khoảng giá, kèm VAT và liên kết Bảng giá.
- `test_pricing.py`: kiểm tra giá trang dịch vụ khớp pricing.json, chặn các mức giá cũ và cam kết 24 giờ/24h/24/7.
- Điều khoản thanh toán theo loại tính phí trong pricing.json (sinh bởi `svc_pricing.py`): dịch vụ tính theo tháng (hosting, email, chăm sóc website, SEO, quảng cáo, Fanpage) và theo năm (tên miền) thanh toán 100% trước theo kỳ đã chọn, không đặt cọc; dịch vụ làm một lần giữ "đặt cọc 30–50%, 2 lần chỉnh sửa, bảo hành 60 ngày". Câu hỏi thường gặp "Được chỉnh sửa mấy lần?" trên trang tính theo kỳ đổi thành "Thanh toán thế nào?".
- Viết lại ghi chú "Giá chưa gồm phí tên miền, hosting… khách thanh toán trực tiếp" (trang dịch vụ, FAQ + JSON-LD, 2 bài blog, chatbot): tên miền có giá riêng; hosting/VPS và quảng cáo: Thương lượng; tiền quảng cáo trả cho nền tảng không nằm trong giá. FAQ Google Workspace/Microsoft 365 khớp bảng giá (tính theo người/tháng, gồm phí bản quyền và hỗ trợ cài đặt).
- Bảng giá: thêm điều khoản thanh toán và 2 câu hỏi thường gặp; chatbot trả lời câu hỏi đặt cọc/thanh toán và "đã gồm tên miền, hosting chưa" theo Bảng giá (3 câu eval mới).
- Chi phí bên thứ ba thanh toán qua My Agent: FAQ Kỹ thuật dữ liệu (máy chủ, cơ sở dữ liệu, phần mềm) và Thiết kế app (tài khoản nhà phát triển Apple/Google) đổi thành "được báo trong báo giá và thanh toán cho My Agent"; nguồn svc_data.py cũng được cập nhật.
- `test_pricing.py`: trang tính theo kỳ không có "đặt cọc 30–50%", trang làm một lần còn đủ điều khoản; chặn ghi chú tên miền/hosting cũ và các câu "thanh toán trực tiếp cho nhà cung cấp".

## 0.9.0 - 2026-10-27
- Trang `/bang-gia.html`: bảng giá 5 nhóm dịch vụ (đã gồm VAT, giá tham khảo theo khoảng), công cụ tính giá combo `#tinh-gia` (trả trước theo tháng/6/12/24 tháng), hosting & quảng cáo "Thương lượng".
- Nút gửi tạm tính sang `lien-he.html` (`?tam-tinh=&ngan-sach=`) + `js/lien-he-prefill.js`.
- Menu "Bảng giá", link footer, nút "Tự tính giá" ở combo và trang dịch vụ; sitemap, schema WebPage + Breadcrumb; chatbot KB + 4 câu eval.
- `scripts/pricing_publish.py`, `scripts/bang_gia_build.py`, `scripts/test_pricing.py` (chạy trong ci_check), `docs/bang-gia.md`.

## 0.8.2 - 2026-10-27
(Số phiên bản 0.8.1 đã dùng cho tag phát hành blog 2 bài đầu, PR #23.)
- Menu chính gọn hơn: bỏ mục "Về chúng tôi" (giữ link "Về chúng tôi" ở footer cột My Agent trên mọi trang) và bỏ mục riêng "Thiết kế website" (vẫn là mục đầu tiên trong dropdown Dịch vụ › 01 · Nền tảng website và trên trang Dịch vụ). Áp dụng cho cả menu mobile.
- "Dịch vụ" được đánh dấu đang xem trên `dich-vu.html` và mọi trang `dich-vu/*` (gồm Thiết kế website).
- Sửa tại nguồn trong `scripts/tech_pass.py` (idempotent) nên các lần dựng Tin tức/Blog sau không sinh lại menu cũ; bỏ CSS ẩn mục thứ 3 của menu ở 961–1200px (không còn cần).

## 0.8.0 - 2026-10-27
- Mục mới **Blog / Kiến thức**: bài hướng dẫn do My Agent tự viết, mỗi bài 1 file `data/blog/<slug>.md`, dựng bằng `scripts/blog_build.py`, kiểm tra bằng `scripts/blog_publish.sh`.
- `blog.html` (danh sách) + `blog/<slug>.html`: breadcrumb hiển thị + BreadcrumbList, Article JSON-LD (author/publisher My Agent), canonical/OG, mục lục, Dịch vụ liên quan + CTA Liên hệ, bài mới hơn/cũ hơn, bài liên quan; RSS `blog/feed.xml`; `blog/` chuyển về `blog.html`.
- Chưa có bài: trạng thái "Bài viết đầu tiên sắp ra mắt", `noindex, follow`, không vào sitemap (tự gỡ khi có bài).
- Menu "Blog" + footer "Blog / Kiến thức" trên mọi trang (tech_pass), sitemap/lastmod cho bài blog.
- Validator: chặn 24/7, 24h, cam kết/đảm bảo top/thứ hạng, top 1, FPT Polytechnic, giá/số liệu chưa đánh dấu "ví dụ"/nguồn, độ dài title/description, thiếu/sai services, slug trùng, ngày sai. `ci_check.py` chạy validator Tin tức + Blog và kiểm tra sitemap không có URL chết; `seo_audit.py` kiểm tra Article/breadcrumb/dịch vụ liên quan/CTA cho bài blog.
- `scripts/test_blog.py` (validator + dựng thử đầu-cuối trên bản sao tạm), trợ lý MJ đọc bài blog, thêm 3 câu eval.
- Tài liệu `docs/blog.md`, `docs/blog-format.json`, mẫu `data/blog/_template.md.example` (không đăng).

## 0.7.3 - 2026-10-27
- (Số phiên bản 0.7.1/0.7.2 đã dùng cho tag của các thay đổi SEO trước đó.)
- Dự án mẫu (`du-an.html`): thêm demo web app XN Linh Kiện Máy In (xnlinhkien.myagentvn.com); thẻ NhàĐất Việt có nút "Xem demo" (nhadat.myagentvn.com).
- Cả 4 thẻ dự án dùng ảnh chụp bản chạy thật (WebP 16:9, 960px + 480px, srcset, width/height, lazy) trong `assets/projects/`, thay hình SVG trang trí.
- Tài liệu `docs/du-an.md`: cách thêm dự án mới kèm thumbnail.

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
