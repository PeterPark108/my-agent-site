# Nền vũ trụ chuyển động — 06/11/2026

Theo yêu cầu chủ site, nền chung tạo cảm giác lơ lửng giữa vũ trụ. Các vì sao trôi cùng hướng từ phải sang trái, hơi chéo xuống; ba độ sâu dùng tốc độ/kích thước khác nhau. Giữ quả cầu và toàn bộ phong cách 3D hiện tại.

- Một canvas trong Cosmos dùng chung các route; 155 sao trên desktop, 85 trên điện thoại, vẽ tối đa khoảng 30 lần/giây và giới hạn độ phân giải để giảm tải.
- Sao băng nhỏ: một lượt mỗi 5 giây, bay trong 0,9 giây. Sao băng lớn: một lượt mỗi 10 giây, bay trong 1,6 giây. Hai chu kỳ trùng nhau ở mốc 10 giây nhưng có vị trí xuất phát riêng.
- Vệt sáng đi cùng hướng với nền sao, có đầu sáng và đuôi mờ. Không che hoặc nhận tương tác thay cho nội dung.
- GSAP timeline cho sao băng, ticker cho các lớp sao. Dừng khi tab bị ẩn; tiếp tục khi trở lại. Reduced motion giữ nền sao tĩnh và ẩn sao băng. Cleanup hủy ticker/listener/observer/timeline của component.
- Tương thích sáng/tối; nền các bài dài giảm độ sáng để giữ khả năng đọc.

## Kiểm tra

- Lint, typecheck và build đạt; 61 trang tĩnh.
- Hai ảnh chụp cùng vùng chỉ có nền sao có dữ liệu khác nhau, xác nhận nền đang chuyển động.
- Đo nhiều chu kỳ từ thời điểm bắt đầu mỗi lượt: nhỏ trung bình 5000,46ms, lớn 10001ms. Đã quan sát và chụp một lượt sao băng lớn thực tế.
- Blog, Tin công nghệ, dịch vụ thiết kế website và điều khoản đều có đúng một canvas, hai lớp sao băng, không tràn ngang. Tiêu đề Blog/Tin vẫn 19px.
- Không có cảnh báo mới trong browser log ở bản cuối. Các cảnh báo rotationZ của lượt thử quỹ đạo đầu đã được sửa trước đó và giữ làm lịch sử trong hồ sơ QA.
- Chưa đo Lighthouse/axe, thiết bị thật, Safari hoặc thử chuyển reduced motion ở cấp hệ điều hành. Tính năng dừng khi ẩn tab/reduced motion được rà soát trong mã.

Hồ sơ hiện tại gồm popup kính ba nhóm và nền chuyển động; source cùng bản xuất tĩnh nằm trong dev / PR nháp, chưa triển khai production.
