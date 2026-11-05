# Third-party assets

- public/brand/logo-dark.svg: https://myagentvn.com/assets/logo-dark.svg; tải 05/11/2026, giữ nguyên. Chủ thương hiệu giữ quyền. Không có giấy phép tái phân phối nhãn hiệu được xác minh; chỉ dùng cho dự án My Agent được ủy quyền.
- public/brand/favicon.svg: https://myagentvn.com/assets/favicon.svg; cùng điều kiện.
- docs/evidence/*: snapshot HTML/CSS từ site, chỉ để review nguồn, không nhập vào bundle hoặc xuất bản như trang mới.
- @fontsource/be-vietnam-pro: font Be Vietnam Pro, SIL OFL 1.1; xem LICENSE trong dependency sau npm ci. Mã nguồn repo không ghi đè giấy phép dependency.
- Next.js, React, GSAP, @gsap/react, TypeScript, ESLint, Playwright: dùng theo giấy phép đi kèm bản cài; kiểm tra điều khoản GSAP tại https://gsap.com/community/standard-license/ trước khi tái phân phối sản phẩm hoặc dịch vụ.
- Orb/disc và layout: CSS được tạo cho bản concept này, không cần ảnh stock.

Repository chưa áp dụng giấy phép OSS cho toàn bộ dự án vì quyền thương hiệu và ý định phân phối cần chủ sở hữu quyết định.

## Ảnh dự án v4

Các ảnh public/projects/{nhagio,xnlinhkien,nhip,nhadat,huongnghiep}.webp tải nguyên bản từ https://myagentvn.com/assets/projects/{tên}-960.webp ngày 05/11/2026 để làm bản nâng cấp cùng thương hiệu. Trang du-an.html xác định đây là demo cá nhân của Peter. Chủ sở hữu cần xác nhận quyền tái phân phối screenshot và các ảnh bên trong trước public. Xem docs/ASSET-MANIFEST.json và snapshot portfolio; không dùng screenshot để tuyên bố khách hàng thật.


## Snapshot hệ thống v5

55 trang HTML và tài nguyên CSS/JS/font/ảnh từ myagentvn.com được giữ cho cùng dự án thương hiệu, theo danh mục docs/LEGACY-INVENTORY.json. Giữ trang ghi-nguon.html và các ghi chú nguồn trong bài gốc. Không cấp lại giấy phép cho ảnh hoặc nội dung bên thứ ba. Chủ sở hữu cần duyệt trước phát hành. Không có dữ liệu orders.json trong gói.
## Thư viện/asset bổ sung v6

- pdf-lib 1.17.1 (MIT), @pdf-lib/fontkit 1.1.1 (MIT); xem giấy phép các dependency sau npm ci.
- cheerio 1.2.0 (MIT), dùng chuyển đổi nội dung tại thời điểm chuẩn bị repository.
- public/fonts/BeVietnamPro-Regular.ttf và BeVietnamPro-SemiBold.ttf: Google Fonts github.com/google/fonts/tree/main/ofl/bevietnampro, SIL OFL; bản giấy phép tại public/fonts/OFL.txt. Font nhúng PDF, không tải từ bên thứ ba khi chạy.
- pricing engine và nội dung/tool source được giữ từ website My Agent để phục vụ dự án được chủ site yêu cầu, không cấp lại quyền cho thương hiệu/nội dung gốc.
