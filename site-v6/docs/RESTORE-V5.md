# Bản hiện hành v5 — khôi phục hệ thống trang và chức năng

## Điều đã sửa

Bản v4 chỉ nâng cấp trang chủ và chưa bảo toàn toàn bộ website. V5 giữ trang chủ Next.js đã nâng cấp, đồng thời khôi phục 55 trang HTML từ sitemap và các liên kết của myagentvn.com. Các trang con nằm trong public/, giữ nội dung và script gốc, thêm css/upgrade-shell.css cho glass và nền sao. Chúng là trang nội dung đầy đủ chạy trên cùng host, không phải iframe hoặc link chuyển hết về site cũ. Chưa chuyển từng trang này thành component React riêng.

Menu Khám phá trên trang chủ dẫn tới dịch vụ, combo, bảng giá, portfolio, tra cứu, tin tức, blog, công cụ, tài nguyên, giới thiệu, liên hệ và chính sách. Các link trong nội dung v4 đã chuyển sang route local. /index.html redirect về / để giữ backlink cũ.

## Form và quyền đồng ý

Trang chủ có Họ tên, điện thoại, email tùy chọn, dịch vụ, nội dung và checkbox đồng ý bắt buộc, mặc định chưa tích. Checkbox dẫn tới chính sách gốc và mục điều khoản/dịch vụ. Validation trình duyệt và server cùng kiểm tra consent. API /api/contact chuyển payload có giới hạn sang backend gốc /api/contact, timeout 5 giây. Chỉ xác nhận thành công nếu upstream trả HTTP thành công và JSON ok:true. Lỗi giữ nguyên dữ liệu và có Email/Zalo/Gọi dự phòng. Form đầy đủ trên /lien-he.html giữ luồng gốc và checkbox gốc.

## Chính sách và điều khoản

/chinh-sach-bao-mat.html giữ chính sách đang công khai. Nguồn không có trang điều khoản hợp đồng độc lập trong sitemap hoặc liên kết đã kiểm tra. Vì vậy /dieu-khoan-dich-vu.html là mục lục dẫn chính sách, phạm vi dịch vụ và ghi chú bảng giá/thanh toán đã công bố; không tự đặt điều khoản hợp đồng mới. Trước production cần chủ sở hữu duyệt nội dung pháp lý hiện hành.

## Chatbot và liên hệ

Giữ script MJ gốc public/js/chat.js và bộ public/data/chatbot-kb.json. MJ tra cứu kiến thức trên trình duyệt, không cần API key LLM. Đã quan sát MJ trả lời câu hỏi thiết kế website và dẫn tới trang local. Home có nút gọi tel:0328439972 và Zalo cố định; các trang HTML giữ widget gốc. Có chế độ sáng/tối gốc trên trang con.

## Dữ liệu chức năng cũ

Giữ data/pricing.json và các script tính giá/combo/prefill. data/orders.json KHÔNG có trong ZIP: route server lấy dữ liệu từ hệ thống gốc theo yêu cầu với no-store, giữ cơ chế tra mã của tracking.js. Không tải hoặc lưu dữ liệu đơn hàng thật vào repository.

## Cấu hình backend trước khi nối domain

.env.example có MYAGENT_BACKEND_ORIGIN=https://myagentvn.com cho local/preview. Khi triển khai lên chính myagentvn.com, bắt buộc đổi sang origin riêng của backend cũ hoặc giữ API/data routes tại reverse proxy VPS. Nếu upstream host trùng host ứng dụng, code trả 503 để tránh vòng lặp. ZIP không chứa backend Telegram, token, dữ liệu đơn hàng hay credentials VPS; không thể tuyên bố đã chuyển các thành phần máy chủ đó chỉ từ mã nguồn công khai.

Giữ API cùng domain bằng reverse proxy là phương án ít thay đổi nhất nếu backend đang chạy trên VPS. Tích hợp endpoint thật phải test trong môi trường được chủ sở hữu duyệt, có rollback. Đã test client bằng mock; chưa gửi form thật hoặc tra mã đơn hàng thật.

## Kiểm tra đã thực hiện

- Production build PASS; lint PASS; typecheck PASS.
- HTTP 55/55 trang con trả thành công: PAGE-CHECK-V5.json.
- Desktop/mobile: form không consent không gửi; mock ok:true mới báo thành công; server reject thiếu consent; nav, FAQ, giảm chuyển động, portfolio và overflow đã kiểm tra.
- MJ mở được, KB và pricing tải 200, bảng tính giá có nội dung. Ban đầu một test mobile chờ mascot đứng yên bị timeout; test được đổi sang click hit target sau khi visible vì mascot có animation liên tục. Rerun nhóm continuity mobile: 3/3 PASS.
- Đã xem thủ công MJ trả lời và trang bảng giá, nút sáng/tối hoạt động.
- Chưa audit axe/Lighthouse/Safari và chưa kiểm chứng mọi công cụ bằng dữ liệu thật. Không đổi domain hoặc deploy production.

## Tệp tham chiếu

LEGACY-INVENTORY.json liệt kê 55 route và ba đường dẫn dữ liệu động được giải quyết lại theo đúng base URL. Các 404 trong trường failures là dấu vết lần crawl JS tương đối; mục resolved ghi cách xử lý đúng. Test continuity.spec.ts kiểm tra consent, API reject, MJ và trang chức năng. Mã JS legacy được giữ nguyên logic và loại khỏi lint ứng dụng mới để tránh sửa hành vi chỉ nhằm thay đổi style code.
