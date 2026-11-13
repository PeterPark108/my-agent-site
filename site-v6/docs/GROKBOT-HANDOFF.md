> **Hiện hành: v6.** Đọc [REDESIGN-V6.md](REDESIGN-V6.md) và [SELF-REVIEW-V6.md](SELF-REVIEW-V6.md) trước. Nội dung dưới đây là hồ sơ lịch sử khi khác với v6.

> **Bản hiện hành v5 — bảo toàn trang con và chức năng cũ.** Đọc [RESTORE-V5.md](RESTORE-V5.md) và FEATURE-PARITY.md trước. Các ghi chú v1–v4 bên dưới là lịch sử.

> **Bản hiện hành: v4.** Đọc [UPGRADE-V4.md](UPGRADE-V4.md) trước. Những mục v1–v3 bên dưới được giữ làm lịch sử; portfolio hiện dùng sản phẩm mẫu thật được liệt kê trên myagentvn.com, không còn Aurora/Orbit/Forma.

# Bàn giao cho Grokbot

## Prompt khởi đầu

Bạn tiếp tục repository My Agent hiện có. Đọc README.md, docs/BRAND-AUDIT.md, DESIGN-SYSTEM.md, BRIEF.md, QA.md và REVIEW.md trước khi thay đổi. Chạy npm ci rồi build để có baseline. Giữ logo gốc và các token đã xác minh từ myagentvn.com; đừng đổi thương hiệu thành AI agent hoặc tự tạo số liệu/dự án. Hoàn thiện theo các nhiệm vụ bên dưới và ghi kết quả kiểm tra thực tế. Mọi mục chưa kiểm tra phải ghi chưa kiểm tra. Không công bố website hay thay domain khi chưa có quyền.

## Công việc theo ưu tiên

| ID | Ưu tiên | Nhiệm vụ | File / đầu ra | Điều kiện hoàn tất |
|---|---|---|---|---|
| G01 | P0 | Đọc review, tái lập môi trường | lockfile, REVIEW.md | npm ci/build/lint/typecheck qua |
| G02 | P0 | QA desktop/mobile thật | QA log + ảnh 390/768/1440 | không tràn, lỗi console, chặn CTA |
| G03 | P0 | Duyệt copy và liên hệ với chủ sở hữu | content.ts, content approval | không còn claim chưa duyệt |
| G04 | P0 | Kiểm tra accessiblity | báo cáo axe + keyboard | contrast AA, focus rõ, reduced motion đủ nội dung |
| G05 | P1 | Portfolio thật nếu có dữ liệu | Showcase + asset manifest | mỗi ảnh có quyền dùng, alt, size; nếu chưa có giữ nhãn concept |
| G06 | P1 | Form thật nếu có yêu cầu | component + API route + env example | validate server, rate limit, chống spam, error/success thực; không đưa secret ra client |
| G07 | P1 | Trang dịch vụ nếu mở rộng | app/dich-vu/... | route thật, title/meta, breadcrumbs, link nội bộ qua QA |
| G08 | P1 | Hiệu năng | Lighthouse report | đạt mục tiêu QA hoặc ghi lý do/biện pháp |
| G09 | P0 trước public | SEO và phát hành | metadata, robots, sitemap, OG | URL/canonical đúng, index chỉ bật trên production đã duyệt |
| G10 | P0 trước public | Handover vận hành | runbook + rollback | preview được duyệt, backup site/DNS, rollback thử được |

## Quy tắc sửa code

Giữ Server Component mặc định; client chỉ khi cần state/motion. Thêm animation trong scope hiện có hoặc useGSAP riêng có cleanup, không kill toàn bộ trigger toàn ứng dụng. Không thêm thư viện smooth scroll khi chưa có lý do đo được. Không hide nội dung bằng CSS chờ JS. SVG logo không sửa; nếu cần bản outline xin file gốc.

## Định nghĩa hoàn thành

Hoàn tất checklist acceptance, gửi diff và bảng kết quả PASS/FAIL/NOT RUN, kèm ảnh và command logs. Không đánh dấu xong chỉ vì build qua. Khi làm tính năng ngoài scope, ghi quyết định và cách rollback. Không gửi dữ liệu khách tới dịch vụ ngoài trước khi xác định backend và chính sách.
