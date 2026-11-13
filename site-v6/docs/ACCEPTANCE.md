> **Hiện hành: v6.** Đọc [REDESIGN-V6.md](REDESIGN-V6.md) và [SELF-REVIEW-V6.md](SELF-REVIEW-V6.md) trước. Nội dung dưới đây là hồ sơ lịch sử khi khác với v6.

# Acceptance checklist

Đánh dấu theo bằng chứng của lần nghiệm thu cuối. Các ô dưới đây để trống có chủ đích; trạng thái kiểm tra hiện tại nằm ở REVIEW.md.

- [ ] npm ci từ thư mục mới thành công; package-lock.json đồng bộ.
- [ ] npm run build, npm run typecheck, npm run lint thành công.
- [ ] Logo đúng file gốc/hash và không méo; token đúng BRAND-AUDIT.md.
- [ ] Tiếng Việt render đầy đủ dấu, font load local, không 404 asset.
- [ ] 320/390/768/1024/1440px không tràn ngang hoặc đè nội dung.
- [ ] Hero, services, concept, process, FAQ, contact đầy đủ; một h1.
- [ ] Menu mobile mở/đóng, Escape, link đóng menu; tab order hợp lý.
- [ ] ScrollTrigger không nhân bản sau remount/resize; không scroll hijack.
- [ ] Reduced motion và JS tắt vẫn có nội dung, mailto/tel và FAQ dùng được.
- [ ] Các CTA/hash/external link đúng đích; không claim gửi form thành công giả.
- [ ] Không có lỗi console/hydration, asset hỏng hoặc layout shift đáng kể.
- [ ] Keyboard toàn trang, focus visible, axe không có serious/critical; contrast AA.
- [ ] Nội dung, liên hệ và portfolio được chủ sở hữu duyệt.
- [ ] Lighthouse/Core Web Vitals theo mục tiêu QA hoặc có ngoại lệ được duyệt.
- [ ] Trước public: OG/canonical/sitemap/robots đúng, gỡ noindex có chủ đích.
- [ ] Không secret, không dữ liệu cá nhân khách; quyền sử dụng asset đã duyệt.
- [ ] Preview và kế hoạch rollback đã duyệt trước khi nối domain thật.
