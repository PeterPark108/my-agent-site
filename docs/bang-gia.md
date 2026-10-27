# Bảng giá & công cụ tính giá (`/bang-gia.html`)

Nguồn dữ liệu: thư mục ngoài repo (`/workspace/bang-gia/pricing.json`). **Không** copy file `.xlsx` hay sheet "Nội bộ" vào repo.

## Cập nhật giá
```
python3 scripts/pricing_publish.py /workspace/bang-gia   # lọc whitelist -> data/pricing.json, js/combo-calculator.js
python3 scripts/bang_gia_build.py                         # dựng bang-gia.html
python3 scripts/svc_pricing.py                            # bảng giá trên 17 trang dịch vụ
python3 scripts/tech_pass.py                              # menu, footer, head, sitemap, ?v=
python3 scripts/chatbot_build.py                          # KB chatbot
python3 scripts/test_pricing.py                           # kiểm tra loại trừ + đối chiếu máy tính
```

## Không bao giờ công khai
- Giá Traffic User; sheet Nội bộ, nguồn tham khảo, định vị giá so với thị trường, chi phí/biên lợi nhuận; file .xlsx.
- Cam kết "24/7", "24h", hứa thứ hạng; nhắc FPT Polytechnic.

`test_pricing.py` (chạy trong `ci_check.py`) tự động chặn các mục trên.

## Hosting/VPS & quảng cáo
Là "Thương lượng": không cộng vào tổng, hiển thị dòng riêng. Giá quảng cáo chưa gồm tiền quảng cáo trả cho nền tảng.

## Gửi sang liên hệ
Nút gửi mở `lien-he.html?tam-tinh=…&ngan-sach=…&dich-vu=…#form`; `js/lien-he-prefill.js` điền vào ô tin nhắn (không đổi form/endpoint), nếu không có ô thì hiện bản tóm tắt để copy.

## Trang dịch vụ
Khối "Bảng giá tham khảo" trên `dich-vu/*.html` được sinh từ `data/pricing.json` bằng `scripts/svc_pricing.py` — không sửa tay. `test_pricing.py` báo lỗi nếu giá trang lệch pricing.json, còn mức giá cũ (web app 20–48 triệu, 1,5–4 / 4–10 / 8–20 triệu/gói, 300/600 nghìn, 1 triệu/tháng) hoặc cam kết 24 giờ/24h/24/7.

## Điều khoản thanh toán
Sinh theo `billing` trong pricing.json: `monthly`/`yearly` → thanh toán 100% trước theo kỳ đã chọn (tháng/6/12/24 tháng; tên miền theo năm), không đặt cọc; `one-time` → đặt cọc 30–50%, 2 lần chỉnh sửa, bảo hành 60 ngày.

## Web app (v0.9.8, Peter chốt phương án B 28/10/2026)
Không còn gói "Web app theo yêu cầu" trong Thiết kế website. Web app có đăng nhập, phân quyền, dashboard báo giá theo bảng Phần mềm nội bộ (`phan-mem-noi-bo`: 9,6–20 / 24–48 / 48–96 triệu, đã gồm VAT). Link cũ `?goi-dv=thiet-ke-website&goi=web-app` (hoặc `?goi=web-app`) được `js/lien-he-prefill.js` chuyển sang `phan-mem-noi-bo` / `tieu-chuan`. Báo giá đã gửi trước ngày đổi giữ nguyên.
