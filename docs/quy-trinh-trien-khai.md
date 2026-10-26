# Quy trình triển khai (dev → production)

## Nhánh
- `dev`: nhánh làm việc. AI/bot chỉ được push vào đây.
- `production`: GitHub Pages phục vụ myagentvn.com từ nhánh này. Có bảo vệ: chỉ nhận thay đổi qua Pull Request và CI `check` phải đạt; không force push, không xóa nhánh.

## Deploy (do Peter, hoặc MJ khi Peter đồng ý)
1. Làm và push lên `dev` → mở PR `dev → production` (`gh pr create -B production -H dev`).
2. Chờ CI `check` xanh, xem lại thay đổi.
3. Bấm **Merge** PR trên GitHub. Sau 1–2 phút web cập nhật.
4. Gắn phiên bản: `bash scripts/release.sh v0.1.1 "ghi chú"`.

Riêng cập nhật tiến độ đơn (`data/orders.json`) là thay đổi nhỏ, Peter có thể merge nhanh khi CI xanh.

## Tag phiên bản
`vMAJOR.MINOR.PATCH`: PATCH = sửa nhỏ/nội dung, MINOR = thêm trang/tính năng, MAJOR = làm lại lớn.

## Quay lại bản cũ (rollback)
- Cách 1 (khuyên dùng): trên GitHub mở PR đã merge gây lỗi → **Revert** → merge PR revert đó.
- Cách 2 (về đúng một tag cũ, ví dụ v0.1.0):
  ```
  git fetch --tags origin && git checkout -B dev origin/dev
  git checkout v0.1.0 -- . && git commit -m "Rollback về v0.1.0"
  git push origin dev && gh pr create -B production -H dev -t "Rollback về v0.1.0" -b "Rollback"
  ```
  rồi merge PR như bình thường.

## Quy tắc dữ liệu
- Dữ liệu khách (tên, SĐT, email, giá, đơn hàng) không bao giờ đưa vào repo hay dán vào chat AI.
- `data/private/` đã gitignore (chứa file ánh xạ mã đơn ↔ khách), cần sao lưu riêng. `data/orders.json` chỉ chứa salt, mã băm và tiến độ — CI sẽ chặn nếu thấy email/SĐT.
- Không để mật khẩu, khóa, token trên Prod hay trong mã.

## Ghi chú cho thông báo Zalo sau này
Token Zalo OA lưu trong GitHub Secrets hoặc biến môi trường của server, không bao giờ ghi vào mã. Việc gửi tin chạy ở hàm phía server (serverless/VPS), không gọi từ trình duyệt.
