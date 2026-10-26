# Gắn tên miền riêng cho website My Agent (GitHub Pages)

1. **Mua tên miền** (vd `myagent.vn`) ở nhà đăng ký bất kỳ (Mắt Bão, PA Việt Nam, Tenten, Namecheap…).
2. **Vào trang quản lý DNS** của tên miền, thêm các bản ghi:

   | Loại | Tên (Host) | Giá trị |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | peterpark108.github.io |
   | AAAA (tùy chọn) | @ | 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153 |

   Xoá các bản ghi A/CNAME cũ trùng tên `@` hoặc `www` (nếu có).
3. **Báo cho mình (hoặc người kỹ thuật) tên miền**, sẽ chạy `scripts/set-domain.sh myagent.vn` để cập nhật canonical, sitemap, robots, ảnh chia sẻ và tạo file `CNAME`, rồi đẩy lên GitHub.
4. **Bật tên miền trong GitHub**: repo `PeterPark108/my-agent-site` → Settings → Pages → Custom domain → nhập `myagent.vn` → Save
   (hoặc `gh api -X PUT repos/PeterPark108/my-agent-site/pages -f cname=myagent.vn`).
5. Chờ DNS cập nhật (vài phút đến 24 giờ), rồi tích **Enforce HTTPS** trong Settings → Pages.

Lưu ý: KHÔNG tạo file `CNAME` trước khi DNS trỏ đúng, nếu không web có thể bị lỗi tạm thời.
