> **Hiện hành: v6.** Đọc [REDESIGN-V6.md](REDESIGN-V6.md) và [SELF-REVIEW-V6.md](SELF-REVIEW-V6.md) trước. Nội dung dưới đây là hồ sơ lịch sử khi khác với v6.

# Design system

## Hướng thị giác

Digital editorial: nền tối sâu, chữ Việt lớn, dòng dịch vụ thoáng, đỏ làm điểm quyết định và xanh tạo chiều sâu. Không thay logo hoặc suy diễn palette từ screenshot. Toàn bộ token thương hiệu trong globals.css trùng CSS thật, xem BRAND-AUDIT.md. Các layout, orbit, disc và typography composition là thiết kế đề xuất.

## Typography / spacing

Be Vietnam Pro 400/600/800; font latin + Vietnamese được bundle local. H1 44–76px desktop, 40–64px mobile; H2 32–56px; body 14–15px, line-height 1.7. Body phụ dùng --mu, tránh dùng accent cho đoạn dài. Spacing: 8/12/16/24/32/48/72/96/110px; container max 1280px, gutter 48 desktop, 32 tablet, 20 mobile. Breakpoint 1050 và 700px. Không cố định chiều cao cho đoạn văn.

## Thành phần và trạng thái

Header sticky có backdrop, menu mobile dạng disclosure không phải modal; aria-expanded + aria-controls, Escape đóng. Focus order đi theo DOM; nav chỉ xuất hiện khi mở ở mobile. CTA đỏ --red với chữ --bg (contrast tính theo sRGB khoảng 4.61:1; hover --neon khoảng 5.46:1), focus viền --el; link nội dung gạch chân. Service row viền mảnh, mũi tên đổi màu; FAQ native details/summary có trạng thái mở. Không dùng màu một mình để truyền thông tin. Reduced motion bỏ GSAP và smooth scrolling.

## Motion specification

| Thành phần | Trigger | Thông số | Fallback |
|---|---|---|---|
| Hero copy | mount | y 24 → 0, opacity 0 → 1, 0.8s power3.out, stagger .09s | SSR hiển thị toàn bộ |
| Section / row | top 92% viewport | y 32 → 0, opacity 0 → 1, .7s power2.out, once | nội dung tự nhiên |
| Hero orbit | hero qua viewport | rotation đến 150°, scrub 1 | orbit tĩnh |
| Concept artwork | section qua viewport | yPercent -8, scrub .8 | artwork tĩnh |

Chỉ chạy khi prefers-reduced-motion: no-preference. useGSAP scope root, matchMedia.revert cleanup cả tween và ScrollTrigger. Không scroll hijack, không pin dài hoặc animation vô hạn. Không đặt opacity:0 trong CSS để trang vẫn đọc được khi JS tắt. Chỉ animate transform/opacity. Nếu thêm ảnh sau này: khai báo kích thước và refresh ScrollTrigger sau load có thay đổi layout.

## Khả năng tiếp cận

lang=vi, một h1, landmark, nhãn nav, skip link, focus-visible, FAQ dùng keyboard, đồ họa thuần trang trí aria-hidden. Điện thoại và email là link thực. Kiểm tra contrast tự động trước phát hành: đặc biệt chữ nhỏ và trạng thái hover, chữ nhỏ và accent. Không dùng --ln làm màu chữ. Thiết kế chưa được chứng nhận WCAG; QA.md nêu kiểm tra bắt buộc.

## Hero v2 — yêu cầu cập nhật

Hero desktop dùng grid 1fr / 2fr (text / quả cầu). WEBSITE ĐẸP viết hoa, cùng màu --tx; dòng Trải nghiệm khác biệt in nghiêng, chiều dài chữ xấp xỉ 2/3 tiêu đề. Hai nút nằm ngay sau heading. Bỏ highlight đỏ riêng ở hero. Mobile xếp dọc để giữ khả năng đọc.

Nền gồm 90 ngôi sao có opacity/scale tween GSAP và lớp sao drift. Quả cầu glass có phản xạ, lưới, vĩ tuyến và kinh tuyến; đúng hai vòng ngoài trôi x/y/rotation độc lập, chu kỳ 4.6s/5.7s yoyo. Quả cầu float 5s. M giảm sáng rồi bật lên trong 0.5s, nghỉ 2.5s: mỗi chu kỳ 3s. Reduced motion giữ cảnh tĩnh. Animation liên tục pause khi hero ra khỏi viewport, cleanup theo matchMedia.

## V3 — cấu hình hiện hành, thay thế các mô tả chuyển động cũ

Cosmos là lớp sao fixed xuyên trang (130 điểm sao CSS twinkle), mọi section có nền trong suốt. Header dạng floating glass có backdrop blur. Services, process, FAQ, contact và footer dùng glass-panel chung.

Services: eyebrow và heading typewriter bằng GSAP, stagger .035s/character khi top heading đạt 78% viewport; các chữ luôn có sẵn trong SSR, aria-label giữ câu đầy đủ cho trình đọc màn hình. Một mục tiêu / Một website có opacity .8; rõ ràng / phù hợp có opacity 1. Toàn dòng Một website phù hợp dùng --red (#E23636). Ba lựa chọn GSAP y+rotationX stagger .16s. Icon chip và workflow tự dựng SVG, glass plate float và orbit.

Projects: ba concept hư cấu Aurora/Orbit/Forma; GSAP pin khung tại top 110px trong quãng cuộn 2.8 viewport, scrub .65. LED scaleY .015 → 1, dự án sau yPercent 105 → 0 trực tiếp đè lớp trước; mỗi lần hạ vào vị trí có một xung electric viền. Không thay native scroll. Cuộn ngược đảo chuyển động. Khi reduced motion hoặc không có JS, ba dự án hiển thị dạng stack tĩnh, không pin/ẩn nội dung.

Process: chạm đầu tiên pulsing opacity 1 → .45 → 1, chu kỳ .5s, không nhấp nháy tắt hoàn toàn. Reduced motion bỏ tất cả GSAP/pulse/twinkle. GSAP matchMedia cleanup giữ khả năng đổi chế độ khi đang mở trang.


## V4 — hệ nội dung hiện hành

Dùng UPGRADE-V4.md làm tham chiếu cuối. Thêm service console 5 tab, portfolio ảnh sản phẩm mẫu thật, navigation trong màn hình LED, form phác thảo và footer 4 cột. Glass được tiết chế; sao giữ toàn trang. Font form mobile 16px để tránh zoom tự động iOS. Các project mẫu là nội dung nguồn, không dùng tên khách hàng hoặc số liệu hiệu quả chưa xác minh.

