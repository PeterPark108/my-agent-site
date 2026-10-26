# Theo dõi tiến độ đơn

Trang: `tra-cuu-tien-do.html` (hỗ trợ `?ma=MÃ`). Dữ liệu: `data/orders.json` (công khai, chỉ chứa SHA-256 có salt của mã đã chuẩn hoá + tiến độ). Ánh xạ hash ↔ nhãn khách: `data/private/orders-map.json` (gitignore, **không commit**).

Chuẩn hoá mã: bỏ mọi khoảng trắng, viết hoa. Hash = SHA-256(salt + mã).

```bash
python3 scripts/order_admin.py add --label "Tên khách – Website"   # in mã 1 lần: MA-YYMM-XXXXXXXX
python3 scripts/order_admin.py update MÃ --step 3 --percent 60 --status "Đang dựng giao diện" --note "Xong trang chủ"
python3 scripts/order_admin.py update --label "Tên khách – Website" --done --note "Đã bàn giao"
python3 scripts/order_admin.py list
python3 scripts/order_admin.py remove MÃ
git add data/orders.json && git commit -m "Cập nhật tiến độ" && git push
```

`--step` 1–5 (Tiếp nhận / Lên kế hoạch – thiết kế / Thực hiện / Duyệt / Bàn giao) tự suy ra trạng thái các bước; `--date YYYY-MM-DD` để ghi ngày khác hôm nay. Lịch sử giữ 8 mục mới nhất.

Link gửi khách: `https://myagentvn.com/tra-cuu-tien-do.html?ma=MÃ` (tạm thời: `https://peterpark108.github.io/my-agent-site/tra-cuu-tien-do.html?ma=MÃ`). Mã demo: `MA-DEMO-0001`.

Lưu ý: mọi thứ trong `data/orders.json` ai cũng đọc được — không ghi tên, SĐT, email, giá vào ghi chú. Mã sinh tự động có 8 ký tự ngẫu nhiên (32^8 ≈ 1,1 nghìn tỷ tổ hợp) nên không dò ngược được từ hash. Mã demo thì ai cũng biết. Nếu mất file private, đơn vẫn chạy, chỉ mất nhãn khách.
