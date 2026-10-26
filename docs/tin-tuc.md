# Mục Tin tức công nghệ

Trang: `tin-tuc.html`, còn trang chủ có khối "Tin công nghệ mới nhất" hiện 3 tin mới nhất. Dữ liệu nằm trong `data/news.json`.

## Thêm một tin
Thêm một mục vào `items` trong `data/news.json`:
```json
{"id":"slug-khong-dau","date":"2026-10-27","topic":"ai","title":"Tiêu đề tiếng Việt do mình đặt",
 "summary":"2–3 câu, tự viết lại bằng lời của mình.","insight":"Một câu Góc nhìn My Agent: tin này có ý nghĩa gì với doanh nghiệp nhỏ.",
 "source":"Tên nguồn","url":"https://link-bai-goc"}
```
- `topic` phải là một trong: `ai`, `bao-mat`, `web-seo`, `du-lieu`, `nen-tang`. Chủ đề nào không có tin thì nút lọc tự ẩn.
- `date` là ngày đăng bài gốc, viết theo dạng YYYY-MM-DD. Nhớ sửa cả `updated` ở đầu file.

## Dựng lại trang
```
python3 scripts/news_build.py --check-urls   # kiểm tra trường bắt buộc + link nguồn
python3 scripts/tech_pass.py                 # menu, SEO, sitemap, cache-busting
python3 scripts/ci_check.py
```
Lệnh `--check-urls` báo `CHẶN BOT?` khi gặp mã 401/403/429. Khi đó hãy tự mở link bằng trình duyệt để kiểm tra; link có mã lỗi khác thì phải bỏ.

## Quy tắc
- Chỉ đưa tin có thật và đã mở đọc bài gốc. Không bịa số liệu, trích dẫn hay ngày đăng; chi tiết nào chưa chắc thì bỏ.
- Tóm tắt phải tự viết bằng lời của mình, không chép câu của nguồn. Không lấy ảnh của nguồn, trang chỉ dùng icon theo chủ đề.
- Tin nào cũng phải có link nguồn gốc và ngày thật. Nên chọn tin trong khoảng 30 ngày gần nhất và giữ khoảng 8–12 tin; tin cũ thì xoá bớt.
