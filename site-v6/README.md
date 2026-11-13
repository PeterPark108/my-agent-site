# My Agent — v7 / Cosmic Precision

Bản nâng cấp từ ZIP v6.1 theo MASTER-PLAN v2.0: demo, báo giá, hỗ trợ và lớp bảo vệ API. Giữ thương hiệu, dữ liệu giá, công cụ và danh mục đường dẫn. Chưa phát hành domain.

## Bắt đầu

Node.js 22+, npm. `npm ci` → `npm run dev` → http://localhost:3000.

Kiểm tra: `npm run lint`, `npm run build`, `npm run typecheck`, `npm run test:security`.

E2E khi có môi trường Playwright phù hợp: `npm run test:e2e`. Vòng này chưa chạy lại toàn bộ bộ E2E; xem review thay vì suy từ kết quả v6.

Production: đặt biến server theo `.env.example`, `npm run build`, `npm start`. Không dùng MYAGENT_LOCAL_QA=1 ở production. Thiếu Redis/thiếu backend: các API liên quan từ chối an toàn, không tự proxy sang domain cũ.

## Đọc trước bàn giao

- [Review và trạng thái v7](docs/REVIEW-IMPLEMENTATION-V7.md).
- [Cấu hình backend và bảo mật](docs/SECURITY-RUNBOOK-V7.md).
- [Master plan do chủ site cung cấp](docs/MASTER-PLAN.md).
- `docs/qa-v7/`: log, PDF mẫu và ảnh kiểm tra. Các hồ sơ v1–v6.1 giữ làm lịch sử.

## Cấu trúc

- `src/app/[...slug]/page.tsx`, `src/content/pages.json`: các route nội dung, HTML qua allowlist.
- `src/components`: Header/Footer dùng chung, Cosmos, Motion, Hero, ProjectShowcase, Ecosystem, PageTools, QuoteExport, SupportWidgets.
- `src/app/api/contact`, `api/quote`, `api/tracking`: schema/rate limit/server-only proxy hoặc tạo PDF.
- `src/app/data/orders.json`: endpoint cũ đóng bằng HTTP 410.
- `src/lib/api-security.ts`, `safe-content.ts`: giới hạn tài nguyên, Redis adapter và xử lý HTML.
- `public/js`, `public/data`: logic công cụ và dữ liệu công khai; không đặt đơn hàng ở đây.
- `public/brand`, `public/fonts`: thương hiệu và font local; giữ giấy phép.

Không bật analytics, thay domain hoặc gửi dữ liệu thật như một phần của local QA. Backend tra cứu mới cần mã ngẫu nhiên có thể thu hồi và quyền ở server; không dùng lại tệp danh sách đơn.
