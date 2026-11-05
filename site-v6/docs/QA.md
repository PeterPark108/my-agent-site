> **Hiện hành: v6.** Đọc [REDESIGN-V6.md](REDESIGN-V6.md) và [SELF-REVIEW-V6.md](SELF-REVIEW-V6.md) trước. Nội dung dưới đây là hồ sơ lịch sử khi khác với v6.

# Hướng dẫn QA

## Tái lập

Node 22 LTS khuyến nghị. npm ci → npm run lint → npm run build → npm run typecheck. Chạy E2E bằng npx playwright install chromium rồi npm run test:e2e; cấu hình tự khởi động production server. Nếu port 3000 đang dùng, dừng server của bạn hoặc sửa đồng bộ baseURL/webServer; tránh kiểm tra nhầm ứng dụng.

## Ma trận thủ công

Chrome/Edge desktop, Safari iOS và Chrome Android. Viewport 320, 390, 768, 1024, 1440. Kiểm tra portrait/landscape và zoom 200%. Capture ảnh hero, dịch vụ, contact. Ghi browser/version/date/viewport, expected, actual, severity và ảnh cho lỗi.

1. Reload đầu trang và tại #lien-he, font không vỡ, logo không lỗi. Xem Network 404 và Console hydration/runtime.
2. Cuộn hết trang, scroll ngược, resize desktop/mobile 5 lần. Không giật hoặc mất section, không trigger lặp bất thường.
3. Mobile: mở menu, tab từng link, Escape đóng, mở lại rồi chọn link. Desktop nav luôn hiển thị.
4. Tab từ skip link đến cuối, Enter/Space mở FAQ. Focus rõ và không bị header che. Mailto phải mở trình soạn, tel phải có số đúng; test không cần gửi thư/gọi thật.
5. Emulate prefers-reduced-motion: reduce trước load và đổi khi đang mở trang. Không tween/parallax, vẫn đủ nội dung. Tắt JavaScript và reload; nội dung/FAQ/link liên hệ vẫn hoạt động, nav mobile cần JS nên dùng CTA trong nội dung.
6. Kiểm tra ảnh SVG ở độ phân giải cao, chữ Việt dấu tổ hợp, 200% zoom, contrast bằng axe/DevTools; không dựa vào nhìn bằng mắt cho AA.
7. Kiểm tra link external dịch vụ/dự án trên site thật có nội dung phù hợp tại ngày release. Concept không bị trình bày như case study thật.

## Performance

Production build, Lighthouse mobile 3 lần (cửa sổ sạch); ghi median và JSON report. Mục tiêu: Performance >=90, Accessibility >=95, Best Practices >=95; SEO chỉ nghiệm thu sau cấu hình index production. Lab LCP <=2.5s, CLS <=0.1, TBT <=200ms. Field INP <=200ms cần dữ liệu thực sau release, không khẳng định đạt từ build hoặc lab. Nếu không đạt: đo font/JS/image/animation trước khi tối ưu; không tăng motion chỉ để gây ấn tượng.

## Phạm vi test tự động hiện tại

Playwright: asset logo, h1, menu/hash, FAQ, CTA mailto, overflow, pageerror, reduced-motion visibility. Chưa thay thế kiểm tra Safari thật, axe, độ đúng hình ảnh hoặc audit hiệu năng. CI cài Chromium và chạy hai project desktop/mobile.

## Release gate

P0/P1 còn mở chặn public. Build qua không chứng minh đã đạt UI/UX. Lưu logs/ảnh, duyệt nội dung, xác nhận quyền asset, deploy preview rồi kiểm tra production headers/SEO. Không đưa snapshot HTML nguồn có script vào public/. Có thể rollback bằng deployment trước và DNS cũ đã lưu.

## QA bổ sung v3

- Cuộn tự nhiên từ hero vào 01: chữ gõ đúng thứ tự, sau khi hoàn tất opacity chữ thường .8 và chữ nhấn 1; dòng hai đỏ logo. Icon không đè chữ ở 320/390/768/1440.
- Ba service glass xuất hiện theo thứ tự, click vẫn dẫn đúng site thật.
- 02: cuộn để bật LED, lần lượt Aurora → Orbit → Forma, dự án sau phủ từ dưới lên; electric ở viền sau mỗi lần vào vị trí. Cuộn ngược và resize khi đang pin, rồi tiếp tục xuống 03, không bị kẹt.
- Reduced motion và JS tắt: ba concept đều đọc được dạng stack tĩnh; không pin hoặc giấu card. Các tên là dự án ảo, không đổi thành client thật.
- 03: chạm đầu tiên pulse theo chu kỳ .5s; reduced motion giữ opacity 1.
- Header glass và nền sao xuyên trang, menu mobile/focus và các CTA vẫn hoạt động.

