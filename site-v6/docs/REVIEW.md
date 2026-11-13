# Tự review lần 1 — 05/11/2026 (Asia/Bangkok)

## Kết luận

Repository chạy được và production build thành công. Đủ nền tảng bàn giao Grokbot, chưa phải bản public đã được nghiệm thu. Không deploy hoặc thay đổi domain hiện tại.

## Phạm vi đã đọc và kiểm tra

Đã review source app, component boundaries, dữ liệu nội dung, CSS/responsive, useGSAP lifecycle, link CTA, metadata, asset nguồn và tài liệu. Đã xem hero desktop trong trình duyệt in-app: logo và chữ Việt hiển thị, bố cục không chồng lấn ở viewport quan sát. Không xác nhận đã visual QA toàn bộ mobile hoặc site gốc.

| Kiểm tra | Kết quả | Bằng chứng / giới hạn |
|---|---|---|
| Tải site thật | PASS | Snapshot HTML/CSS, logo SVG và favicon trong docs/evidence và public/brand |
| npm install | PASS | 350 packages; đã tạo package-lock.json |
| npm run build | PASS | Next 16.4.5; compile, TypeScript và prerender thành công; / và /_not-found static |
| npm run lint | PASS | ESLint không lỗi |
| npm run typecheck | PASS | tsc --noEmit không lỗi |
| E2E assertions | PASS 4/4 | Chromium desktop 1280x720 và mobile iPhone 13 emulation 390x664; menu/hash/logo/FAQ/mailto/overflow/pageerror/reduced motion |
| E2E process teardown | LIMITATION | Sau 4 assertions thành công, runner còn chờ dừng webServer trong môi trường Windows; không ghi là exit 0 khi chưa nhận được. Cần xác nhận lại CI Linux. |
| Browser desktop visual | PASS giới hạn | Hero đã quan sát trực tiếp bằng in-app browser; không có visual baseline tự động |
| Contrast CTA | PASS tính toán | --bg trên --red ~4.61:1; hover --neon ~5.46:1, sRGB |
| Axe / Lighthouse / Safari thật | NOT RUN | Cần thực hiện theo QA.md trước public |
| Link ngoài trang | NOT FULLY VERIFIED | URL lấy từ HTML gốc; cần duyệt nội dung đích ở ngày release |
| Quyền asset / copy cuối | PENDING OWNER | Logo gốc được giữ nguyên; copy mới và concept phải duyệt |

Môi trường: Windows, Node v26.13.0, npm 11.20.0. CI chuẩn dùng Node 22; chưa chạy trong phiên này. Browser cài mặc định lần đầu không được tìm thấy do đường dẫn môi trường thay đổi giữa tiến trình; khắc phục bằng PLAYWRIGHT_BROWSERS_PATH trỏ vào thư mục work/browsers. Không ghi đường dẫn máy này vào config dự án.

## Phát hiện và xử lý

1. **Độ tương phản nút**: chữ trắng trên #E23636 khoảng 4.36:1, thấp hơn 4.5:1 cho chữ nhỏ; hover #FF2D3D còn thấp hơn. Đã đổi chữ sang token --bg, giữ màu thương hiệu gốc. Build lại thành công.
2. **Selector test FAQ**: getByText exact không khớp summary vì có dấu + trang trí. Đã đổi sang summary lọc nội dung câu hỏi; chạy lại cho kết quả 4/4 assertions thành công. Không sửa ứng dụng để làm test dễ qua.
3. **Phạm vi claim**: không đưa số liệu, testimonial hoặc dự án tự tạo vào nội dung. Showcase có nhãn concept; quy trình ghi là đề xuất. Liên hệ lấy từ JSON-LD gốc.
4. **Animation cleanup**: useGSAP scope và matchMedia.revert, không kill trigger ngoài phạm vi; SSR vẫn có nội dung và reduced-motion bỏ chuyển động. Chưa stress test bằng profiler/remount lặp.
5. **SEO preview**: noindex/nofollow cố ý; canonical, sitemap và OG phải hoàn thiện khi biết URL phát hành. Không để Grokbot hiểu nhầm là đã SEO production.
6. **Logo chữ SVG**: SVG gốc chứa text với fallback font, giữ nguyên để không làm sai asset; có thể cần xin bản outline từ chủ thương hiệu.

## Việc còn lại trước public

Thực hiện ma trận QA đầy đủ, axe/Lighthouse, duyệt nội dung và quyền asset, thay concept bằng portfolio chỉ khi có dữ liệu được duyệt, cấu hình SEO production, preview và rollback. Form/CRM và trang dịch vụ nội bộ là nhiệm vụ mở rộng có mô tả riêng trong GROKBOT-HANDOFF.md. Build thành công không đồng nghĩa với hoàn tất các gate này.

## Cập nhật hero v2

Đã sửa bố cục 1/3 text, 2/3 glass globe; heading uppercase và subtitle italic cùng màu, hai CTA, sao vũ trụ, hai orbit float độc lập, M light-on chu kỳ 3 giây. Build/lint/typecheck được chạy lại. Kiểm tra browser desktop xác nhận không overflow và GSAP đang cập nhật transform/opacity theo thời gian. Các kiểm tra v1 bên trên là lịch sử, không phải chứng nhận toàn bộ bản v2.

Môi trường Windows khóa cây output .next cũ khi prerender _not-found. Đã dùng distDir .next-preview trong next.config.ts và thêm ignore tương ứng. Không cần xóa output cũ để chạy repository. npm run build và npm start tự dùng cấu hình mới.

Kiểm tra mobile 390px: không overflow ngang, subtitle computed italic và cùng màu rgb(233,236,245). Đã lưu ảnh desktop/mobile v2 bên cạnh ZIP.

## Cập nhật v3 — cosmos và glass toàn trang

Đã kiểm tra trực tiếp desktop và mobile 390px. Service heading computed opacity .8 cho phần chữ mờ, màu dòng hai rgb(226,54,54). Không overflow ngang ở kích thước kiểm tra. Đã cuộn vào LED và quan sát Aurora, Orbit, Forma thay lớp; transform card thứ hai/thứ ba về y=0 theo tiến trình. Khung screen pin top 110px, sau cùng tiếp tục cuộn được. Process mobile có icon bên phải, bốn khung glass và chu kỳ animation .5s. Đã lưu ảnh services, projects desktop/mobile để đối chiếu. Lint và production build v3 thành công. Chưa chạy lại axe/Lighthouse/Safari hoặc toàn bộ CI; kết quả E2E v1 phía trên không đại diện cho regression suite v3.


## Review bản hiện hành v4

Xem UPGRADE-V4.md cho báo cáo đầy đủ. Build/lint/typecheck PASS; 6/6 Playwright PASS exit 0 trên desktop/mobile. Bổ sung test tab dịch vụ, demo selector, validation form. Đã thay portfolio concept bằng ảnh và link demo có trên website thật; nhãn demo giữ rõ ràng. Local không tích hợp backend site thật. Output build .next-v4. Các nhận xét v1–v3 là lịch sử.


## Review hiện hành v5

Xem RESTORE-V5.md và FEATURE-PARITY.md. Đã khôi phục 55 route HTML đầy đủ; 55/55 HTTP checks qua, build/lint/typecheck qua. Kiểm tra consent client/server, form success bằng mock, MJ trả lời và pricing hoạt động. Chưa gửi dữ liệu liên hệ/tra cứu thật. Backend cần cấu hình origin riêng trước đổi domain. Các trang con giữ script/nội dung gốc và shell glass, chưa chuyển toàn bộ sang React.
