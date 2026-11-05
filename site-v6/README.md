# My Agent — v6 / Cosmic Glass

Website Next.js / React / TypeScript với GSAP và ScrollTrigger, dùng logo, font và màu đã đối chiếu từ myagentvn.com. Bản hiện hành là v6; tài liệu v1–v5 chỉ là lịch sử. Chưa triển khai lên domain thật.

## Chạy

Node.js 22+, npm. Chạy `npm ci`, `npm run dev`, mở http://localhost:3000. Production: `npm run build`, `npm start`. Kiểm tra: `npm run lint`, `npm run typecheck`; cài Chromium bằng `npx playwright install chromium`, rồi `npm run test:e2e`.

## Bản v6

- Trang chủ và 55 đường dẫn nội dung dùng chung Header/Footer, nền sao, menu glass, theme sáng/tối, hệ chữ và giao diện công nghệ.
- Trang con có hero, chuyển động GSAP, sơ đồ glass, bố cục nội dung và công cụ mới; không tải stylesheet trang cũ.
- Giữ bộ giá gốc, combo, công cụ miễn phí, tra cứu tiến độ, MJ, gọi/Zalo, chính sách, form và consent.
- Tải báo giá PDF tiếng Việt từ lựa chọn hiện tại, tính lại giá ở server, phân biệt giá cố định và khoản thương lượng.

## Cấu trúc

- `src/app/[...slug]/page.tsx`: renderer chung cho danh mục đường dẫn đã xác minh; route lạ trả 404.
- `src/content/pages.json`: nội dung/metadata/nhóm trang và cấu hình công cụ.
- `src/components`: Header, Footer, Cosmos, homepage, PageTools và QuoteExport.
- `src/app/api/contact`, `src/app/data/orders.json`: cầu nối backend gốc.
- `src/app/api/quote`, `src/lib/quote*`: kiểm tra lựa chọn và tạo PDF.
- `public/js`, `public/data`: logic và dữ liệu công cụ gốc; không chứa dữ liệu đơn hàng riêng tư.
- `content/source`: HTML gốc để đối chiếu, không được phục vụ như trang public.
- `public/brand`, `public/fonts`: thương hiệu và font local, kèm giấy phép.

## Bàn giao và review

Đọc [REDESIGN-V6](docs/REDESIGN-V6.md), [SELF-REVIEW-V6](docs/SELF-REVIEW-V6.md), [GROKBOT-HANDOFF](docs/GROKBOT-HANDOFF.md), [BRAND-AUDIT](docs/BRAND-AUDIT.md). Các yêu cầu acceptance/QA v6 trong REDESIGN-V6 có ưu tiên cao hơn ghi chú lịch sử.

Trước khi chuyển domain, cấu hình `MYAGENT_BACKEND_ORIGIN` tới backend riêng còn hoạt động hoặc nối lại API hiện hữu. Không trỏ proxy về chính ứng dụng trên cùng domain. Không bật analytics hay gửi form thật trong QA nếu chưa được cho phép.
