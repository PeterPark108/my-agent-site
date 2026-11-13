# MY AGENT — Hồ sơ tổng hợp giao diện, trải nghiệm và bảo mật

**Phiên bản tài liệu:** 2.0 — Tổng hợp  
**Ngày:** 05/11/2026  
**Mốc hiện tại:** repository v6.1  
**Trạng thái:** Tổng hợp kết quả v6/v6.1 và kế hoạch nâng cấp đã tự review; các đề xuất mới chưa triển khai  
**Dành cho:** Chủ website, người thiết kế và Grokbot/người tiếp tục phát triển

## 0. Phạm vi và trạng thái thực tế

Tài liệu này hợp nhất các kết luận đã trao đổi: kết quả website v6/v6.1, đề xuất giao diện công nghệ, phần tự review, lộ trình thực hiện và bảo mật. Khi có khác biệt với ý tưởng ban đầu, quyết định sau review trong tài liệu này được ưu tiên. Đây là tài liệu bàn giao, không phải chứng nhận bảo mật hoặc thông báo website đã phát hành.

### Đã hoàn thành trong repository

- Nền tảng Next.js/React/TypeScript, GSAP/ScrollTrigger; logo, font và màu lấy từ thương hiệu thật.
- Trang chủ và 55 đường dẫn nội dung dùng giao diện chung, menu glass, nền sao; trang con có bố cục mới theo loại nội dung.
- Bảo toàn các công cụ chính, combo, tính giá, MJ, gọi/Zalo, chính sách và form có consent.
- Xuất PDF báo giá tiếng Việt, kiểm tra lựa chọn và tính giá lại phía máy chủ.
- v6.1 đổi thứ tự demo thành NhàĐất Việt → Nhà Gió → NHỊP; đưa demo xưởng xuống danh sách bổ sung, hiển thị đủ ảnh nguồn thay vì cắt ảnh.
- Menu Hệ dịch vụ được sửa để tới đúng HỆ SINH THÁI MY AGENT từ cả trang chủ và trang con.

### Bằng chứng kiểm tra đã ghi nhận

- v6: build, lint, TypeScript qua; 23 bài E2E đạt, 1 kiểm tra inventory trùng lặp trên mobile được bỏ qua. Chạy với QA_RESTRICTED_DOWNLOADS=1, xác minh Blob PDF và sự kiện tải thay cho lưu tệp xuống đĩa.
- v6.1: build, lint, TypeScript qua; 8 kiểm tra homepage desktop/mobile đạt, gồm vị trí menu, thứ tự demo và selector. Đây là bộ kiểm tra tập trung riêng, không cộng thành một lần chạy 31 bài.
- PDF mẫu một trang và ba trang đã được render để kiểm tra tiếng Việt, bố cục và phân trang.
- Form và tra cứu được thử bằng dữ liệu giả lập, không gửi yêu cầu khách thật.

### Những việc chưa xác minh hoặc chưa hoàn thành

- Lưu/mở PDF bằng trình duyệt thật bên ngoài môi trường Windows hạn chế; môi trường kiểm thử hủy cả download TXT đơn giản.
- Safari/iOS thật, Lighthouse, axe, đo hiệu năng thực địa và kiểm tra xâm nhập có phạm vi.
- Backend thật sau khi chuyển domain; dữ liệu riêng tư và quy trình vận hành production.
- Các ý tưởng nâng cấp mới trong phần 5 và kiểm soát bảo mật trong phần 12–14.
- Website chưa được triển khai lên domain chính. File ZIP v6.1 là bản mã nguồn đã bàn giao; tài liệu này không tự cập nhật mã nguồn hoặc ZIP đó.

### Mục lục

1. Kết luận tự review
2. Mục tiêu và giới hạn
3. Đánh giá bảy đề xuất
4. Hướng mỹ thuật
5. Đặc tả cải tiến
6. Quy tắc chuyển động
7. Lộ trình
8. Ngân sách chất lượng
9. QA trải nghiệm
10. Bàn giao Grokbot
11. Điều kiện hoàn thành giao diện
12. Đánh giá và ưu tiên bảo mật
13. Đặc tả bảo mật
14. Acceptance bảo mật và cổng phát hành
15. Quyết định tổng hợp và nguồn tham khảo

## 1. Kết luận sau khi tự review

Bảy ý tưởng ban đầu có hướng đi phù hợp với My Agent, nhưng chưa đủ chặt để triển khai trực tiếp. Chúng đặt quá nhiều trọng tâm vào hiệu ứng, chưa quy định rõ điều kiện sử dụng, hành vi trên điện thoại, phương án dự phòng và cách đánh giá kết quả.

Hướng cải tiến nên là: **một điểm nhấn công nghệ mạnh, sản phẩm được trình diễn rõ, công cụ phản hồi tức thì và nội dung dễ tiếp cận.** Cảm giác tương lai cần đến từ sự nhất quán và khả năng tương tác hữu ích.

Điều chỉnh quan trọng nhất: chưa ưu tiên bản đồ dịch vụ hoặc quả cầu 3D trước khi hoàn thiện trình diễn dự án và chất lượng sử dụng hiện tại. Thứ tự mới là **nền tảng trải nghiệm → sản phẩm mẫu → báo giá và hỗ trợ → hệ sinh thái → quả cầu nâng cao**.

Tài liệu này dựa trên thiết kế và lịch sử kiểm tra của repository v6.1. Đây là review đề xuất, không phải một vòng đo hiệu năng hay nghiên cứu người dùng mới.

## 2. Mục tiêu và giới hạn

### Mục tiêu

- Khi vào website, khách nhận ra My Agent làm gì và có thể xem sản phẩm thật ngay.
- Phong cách công nghệ có dấu ấn riêng qua logo, màu sắc, cách chuyển động và hình khối.
- Khách tìm được dịch vụ phù hợp, hiểu phạm vi, tính giá và liên hệ thuận tiện.
- Desktop và mobile đều có bố cục chủ động, không chỉ thu nhỏ cùng một giao diện.
- Chuyển động không cản đọc, bấm nút, điều hướng hoặc gửi thông tin.

### Những yêu cầu hiện tại phải được bảo toàn

- Logo và hệ màu đã trích từ website thật; không tự thay thương hiệu.
- Nền sao xuyên suốt, menu glass dùng chung trang chủ và trang con.
- Hero có WEBSITE ĐẸP, dòng trải nghiệm khác biệt in nghiêng, hai CTA và quả cầu công nghệ.
- Sản phẩm mẫu chính theo thứ tự: **NhàĐất Việt → Nhà Gió → NHỊP**.
- Banner hero demo hiển thị đủ, không cắt mất chữ hoặc bố cục.
- “Hệ dịch vụ” dẫn tới HỆ SINH THÁI MY AGENT trên trang chủ, kể cả khi đi từ trang con.
- Các đường dẫn nội dung, công cụ, chính sách, chatbot, gọi/Zalo, consent và PDF báo giá hiện có.
- Dự án mẫu phải tiếp tục được ghi rõ là demo; không biến thành tuyên bố khách hàng hay thành tích chưa xác minh.

## 3. Tự đánh giá từng đề xuất ban đầu

| Đề xuất | Giá trị | Điểm chưa hợp lý trong ý kiến cũ | Quyết định sau review |
|---|---|---|---|
| Lõi công nghệ tương tác | Dấu ấn đầu trang, thể hiện năng lực | 3D nhiều lớp có thể tốn tài nguyên; thêm tương tác dịch vụ ở hero dễ trùng hệ sinh thái | Giữ, triển khai sau; làm bản CSS/SVG trước, thử WebGL có điều kiện |
| Bản đồ hệ sinh thái | Thể hiện quan hệ giữa các nhóm dịch vụ | Bản đồ có thể khiến khách khó tìm dịch vụ hơn danh sách hiện tại | Thử nghiệm ở desktop; danh sách và đường dẫn rõ vẫn là nền tảng |
| Trình diễn sản phẩm thật | Chứng minh năng lực trực tiếp | Chưa phân biệt ảnh mobile thật và ảnh desktop bị thu nhỏ; ghim cuộn quá dài gây mệt | Ưu tiên cao; ảnh đúng thiết bị, chuyển dự án có kiểm soát |
| Chiều sâu có phân cấp | Tăng độ tinh tế và khả năng tập trung | “Nhiều lớp” dễ trở thành nhiều blur, nhiều sáng, ít tương phản | Giữ; hạn chế số lớp động và bề mặt blur cùng lúc |
| Ngôn ngữ chuyển động | Làm trải nghiệm nhất quán | Dễ bị hiểu là mọi nút/thẻ đều cần hiệu ứng riêng | Giữ; dùng bộ quy tắc chung, phần lớn tương tác rất nhẹ |
| Báo giá trực quan | Hữu ích và hỗ trợ quyết định mua | Chưa giải quyết tổng giá trên màn hình nhỏ và các khoản thương lượng | Ưu tiên cao; bố cục rõ, không thay đổi business rule gốc |
| Gom hỗ trợ nổi | Giảm che nội dung | Giấu toàn bộ hỗ trợ sau một nút có thể làm khách khó tìm cách liên hệ | Mobile gom; desktop lựa chọn cách hiển thị sau khi kiểm tra khả năng tìm thấy |

Không nên tự chấm điểm “9/10” hoặc gọi trải nghiệm là “đỉnh cao” trước khi quan sát trên thiết bị thật. Chất lượng cần được chứng minh bằng hành vi và kết quả kiểm tra.

## 4. Hướng mỹ thuật: Cosmic Precision

Tên nội bộ của hướng thiết kế: **Cosmic Precision — Vũ trụ có trật tự**.

### Màu và vật liệu

Giữ các token đã xác minh của thương hiệu:

- Nền chính: `#05070F`; nền phụ: `#0A0F22`.
- Navy: `#0B1E4A`; blue: `#1B3A8C`; electric: `#3D7BFF`.
- Red: `#E23636`; neon: `#FF2D3D`.
- Chữ chính: `#E9ECF5`; chữ phụ: `#A3ABC2`.
- Font: Be Vietnam Pro, đóng gói local.

Đỏ dùng cho thương hiệu và hành động chính. Xanh dùng cho cấu trúc, trạng thái chọn và dấu hiệu công nghệ. Nội dung dài ưu tiên màu chữ trung tính. Không rải gradient lên mọi tiêu đề.

Glass cần có nền đủ đậm để chữ luôn dễ đọc khi ngôi sao hoặc nội dung đi qua phía sau. Dùng viền mảnh và ánh sáng cạnh để tạo chiều sâu; tránh tăng blur vô hạn.

### Phân cấp ba lớp

1. Lớp xa: ngôi sao thưa, tương phản thấp, chuyển động rất chậm.
2. Lớp giữa: quầng sáng lớn, khu vực hóa theo từng section.
3. Lớp gần: chữ, công cụ, thẻ và CTA có độ sắc nét cao.

Vùng đọc bài viết và điều khoản giảm chuyển động nền. Theme sáng cần được thiết kế tương ứng, không đơn thuần đảo màu.

## 5. Đặc tả cải tiến

### 5.1. Sản phẩm mẫu — ưu tiên P0

**Desktop:** giữ khung trình duyệt công nghệ, hiện đầy đủ ảnh hero. Khi cuộn, dự án sau phủ lên dự án trước; electric viền chỉ xuất hiện ngắn khi dự án ổn định. Luôn có nút chọn dự án, mở demo và bỏ qua phần cuộn.

**Desktop/Mobile preview:** chỉ hiện nút đổi thiết bị khi có ảnh thật tương ứng. Không lấy ảnh desktop ép thành hình điện thoại. Mỗi ảnh có kích thước khai báo trước để tránh thay đổi chiều cao khi tải.

**Mobile:** ưu tiên một dự án mỗi lần, điều khiển bằng nút dễ chạm. Không bắt khách cuộn một quãng dài trong vùng ghim mới tới nội dung tiếp theo. Có thể bỏ ghim ở màn hình thấp hoặc khi bật reduced motion.

**Nội dung:** tên, loại sản phẩm, một câu mô tả giá trị và CTA. NhàĐất Việt tập trung khám phá/lọc bất động sản; Nhà Gió tập trung trải nghiệm không gian/đặt phòng; NHỊP tập trung khám phá và mua sản phẩm.

**Nghiệm thu:** đúng thứ tự; không cắt hero; đổi dự án cập nhật đúng tên/ảnh/link; bàn phím sử dụng được; không tự chuyển khi người dùng đang thao tác; cuộn thoát dễ dàng.

### 5.2. Bảng cấu hình báo giá — ưu tiên P1

Desktop chia khu vực chọn dịch vụ và tóm tắt chi phí. Lựa chọn hiện dưới dạng thẻ có nút bỏ; thay đổi tổng được nhấn sáng nhẹ, không dùng số nhảy liên tục gây khó đọc.

Mobile có thanh tóm tắt gọn ở đáy, mở chi tiết khi chạm. Cần dành khoảng trống trong trang và tính safe-area để thanh này không che ô nhập, nút gửi hoặc hỗ trợ.

Hiện rõ giá một lần, giá định kỳ, kỳ thanh toán, phụ phí, chiết khấu, VAT và khoản cần thương lượng. Không hiển thị khoản chưa có giá như bằng 0. Trạng thái tạo PDF phải có đang xử lý, thành công và lỗi có thể thử lại.

**Nghiệm thu:** lựa chọn và tổng trên giao diện khớp PDF; giữ dữ liệu khi lỗi; gói không hợp lệ bị từ chối; kiểm tra tải/mở PDF thật trên desktop và điện thoại trước khi phát hành.

### 5.3. Hệ sinh thái — ưu tiên P2, cần kiểm chứng

Giữ các nhóm dịch vụ và đường dẫn hiện có. Bổ sung sơ đồ kết nối trên desktop như một cách khám phá trực quan: chọn nhóm làm sáng một nhánh và cập nhật bảng nội dung cạnh bên.

Mỗi bảng trả lời ba câu hỏi: dịch vụ giải quyết việc gì, khách nhận được gì, bước tiếp theo là gì. Không nối các dịch vụ bằng đường sáng nếu quan hệ đó không mang ý nghĩa thực tế.

Mobile dùng tab/thẻ theo chiều dọc. Không yêu cầu kéo, zoom hoặc rê chuột để thấy thông tin. Bàn phím có thể chọn mọi nhóm.

**Điều kiện giữ bản đồ:** khách tìm một dịch vụ và đi tới trang chi tiết dễ ít nhất như giao diện danh sách hiện tại. Nếu sơ đồ làm nhiệm vụ khó hơn, quay về danh sách và chỉ giữ đồ họa phụ trợ.

### 5.4. Lõi công nghệ đầu trang — ưu tiên P3

Phiên bản đầu dùng CSS/SVG với lõi M, lớp kính, vòng quỹ đạo và các điểm sáng có trật tự. Chuyển động nghiêng theo chuột chỉ bật ở thiết bị có con trỏ chính xác. Biên độ nhỏ để logo dễ nhận diện.

Chỉ thử WebGL sau khi có baseline đo hiệu năng. Nếu dùng, tải phần nâng cao sau nội dung quan trọng, có ảnh/SVG dự phòng khi không hỗ trợ hoặc lỗi. Dừng render khi ra ngoài viewport hoặc tab bị ẩn.

Không thêm thao tác chọn dịch vụ vào quả cầu ngay ở vòng đầu: hero cần ưu tiên thông điệp và hai CTA. Tương tác này có thể thử sau nếu chứng minh được giá trị.

**Nghiệm thu:** tiêu đề/CTA xuất hiện độc lập với đồ họa; không phụ thuộc hover; lỗi đồ họa không làm mất nội dung; mobile không bị giật rõ khi cuộn qua hero.

### 5.5. Hỗ trợ và chatbot — ưu tiên P1

Mobile gom cụm hỗ trợ thành một nút Kết nối có tên rõ. Khi mở, hiện Gọi, Zalo và MJ cùng nút đóng. Khi đã có thanh báo giá, bố trí lại hỗ trợ để hai thành phần không chồng nhau.

Desktop có thể giữ lối vào MJ và một nút kết nối gọn. Quyết định dựa trên khả năng nhìn thấy và khoảng trống thực tế, không chỉ tính thẩm mỹ.

MJ có thể nhận ngữ cảnh trang để hiện câu hỏi gợi ý. Đây là mở rộng giao diện của chatbot hiện có; không mặc định bổ sung LLM hay gửi dữ liệu ra dịch vụ mới. Câu trả lời về giá/phạm vi phải dựa trên nguồn dữ liệu đang dùng.

**Nghiệm thu:** mở/đóng bằng bàn phím; focus đúng khi mở và trả về nút gọi khi đóng; không che CTA; gọi/Zalo vẫn mở đúng đích; nội dung người dùng đã nhập không mất khi thu gọn.

## 6. Quy tắc chuyển động

Các con số dưới đây là thông số khởi đầu để tinh chỉnh, không phải kết quả đã đo:

| Loại tương tác | Hướng thực hiện |
|---|---|
| Hover/focus nút | 120–180 ms; thay viền/ánh sáng hoặc nâng 1–2 px |
| Chọn tab/thẻ | 180–280 ms; không làm đổi vị trí nút đang bấm |
| Hiện cụm nội dung | 400–650 ms; dịch chuyển khoảng 12–24 px |
| Chuyển dự án | Theo tiến độ cuộn, giới hạn vùng ghim; luôn có điều khiển trực tiếp |
| Điện ở viền | Một xung ngắn, cường độ thấp, không chớp toàn màn hình |
| Nền sao/quỹ đạo | Nhịp dài; không cạnh tranh với nội dung |

Ưu tiên transform/opacity, tránh hoạt ảnh liên tục làm thay đổi bố cục. GSAP phải có scope và cleanup; cập nhật ScrollTrigger sau khi font/ảnh làm đổi kích thước. Kiểm tra anchor sau khi dựng pin.

Nhịp M mỗi 3 giây và chữ “chạm đầu tiên” mỗi 0,5 giây là yêu cầu hiện có của chủ site. Khuyến nghị thay đổi opacity nhẹ thay vì bật/tắt hoàn toàn; nếu muốn đổi nhịp thì trình chủ site duyệt. Reduced motion dừng các nhịp trang trí, bỏ pin và giữ toàn bộ nội dung ở trạng thái đọc được.

## 7. Lộ trình thực hiện

| Giai đoạn | Công việc | Điều kiện chuyển tiếp |
|---|---|---|
| A — Baseline | Chụp các trang chính; kiểm tra menu/hash, lớp che, bàn phím, mobile; ghi số đo hiệu năng | Có bằng chứng hiện trạng và danh sách lỗi |
| B — P0 | Hoàn thiện sản phẩm mẫu, ảnh hai thiết bị nếu có; điều chỉnh vùng ghim, khoảng cách và chiều sâu | Hero đủ; chọn/mở demo đúng; không giữ người dùng trong cuộn |
| C — P1 | Bảng báo giá, PDF, hỗ trợ nổi và ngôn ngữ chuyển động chung | Luồng chọn → hiểu giá → xuất PDF/liên hệ hoàn tất |
| D — P2 | Prototype sơ đồ hệ sinh thái, so sánh nhiệm vụ với danh sách | Chỉ giữ khi dễ tìm và dễ hiểu |
| E — P3 | Prototype lõi công nghệ nâng cao | Có dự phòng; không làm suy giảm đáng kể trải nghiệm đo được |
| F — Phát hành | QA toàn bộ, cấu hình backend, kiểm tra nội dung/SEO và rollback | Chủ site duyệt preview; các lỗi chặn đã xử lý |

Không nâng nhiều thành phần lớn cùng lúc: mỗi giai đoạn cần một bản preview có thể so sánh và quay lại.

## 8. Ngân sách chất lượng đề xuất

- Mục tiêu ban đầu: LCP ≤ 2,5 giây; INP ≤ 200 ms; CLS ≤ 0,1. Đây là mục tiêu dự án, chưa phải số đo của website.
- Ghi rõ thiết bị, mạng, công cụ và điều kiện khi báo cáo. Phân biệt phép thử phòng lab và dữ liệu sử dụng thực tế; không dùng một điểm Lighthouse để kết luận mọi thiết bị đều nhanh.
- Chuyển động nên giữ nhịp khung hình ổn định trên thiết bị thử; hạ mật độ sao và chất lượng đồ họa trước khi hy sinh phản hồi thao tác.
- Không tự tải iframe demo nặng ngay khi mở trang; dùng ảnh tối ưu và nút mở website.
- Chữ phụ vẫn phải đọc được, focus rõ; kiểm tra contrast thực tế trên nền glass và cả hai theme.
- Không để hình thức “công nghệ” làm giảm cỡ chữ hoặc vùng chạm.

## 9. Kịch bản QA và acceptance tổng

Kiểm tra ở 390, 768 và 1440 px; bổ sung điện thoại thật, màn hình thấp và Safari trước phát hành.

- [ ] Trang chủ cho biết dịch vụ chính và có CTA rõ mà không cần đợi animation.
- [ ] Menu giống nhau ở mọi trang; Hệ dịch vụ cuộn đúng từ trang chủ, trang con và khi mở URL hash trực tiếp.
- [ ] Nhấn Back/Forward không làm mất vị trí hoặc mắc trong vùng pin.
- [ ] Ba demo đúng thứ tự, đủ banner, link tương ứng; ảnh mobile là ảnh đúng bố cục mobile.
- [ ] Không có nội dung đứng ở opacity 0 sau khi cuộn hoặc đổi kích thước.
- [ ] Không tràn ngang; header, hỗ trợ, chatbot và thanh báo giá không che nhau.
- [ ] Có thể dùng tab, Enter, Escape; focus không mất sau khi đóng bảng nổi.
- [ ] Reduced motion vẫn hoàn thành mọi nhiệm vụ.
- [ ] Thay lựa chọn báo giá cập nhật đúng; PDF khớp giá, giữ tiếng Việt và phân trang tốt.
- [ ] Form bắt buộc consent; lỗi giữ dữ liệu; chỉ báo thành công khi API xác nhận.
- [ ] Các route và công cụ cũ vẫn hoạt động; kiểm tra tra cứu bằng dữ liệu được phép.
- [ ] Đo trước/sau theo cùng điều kiện; ghi rõ giới hạn chưa xác minh.
- [ ] Build, lint và typecheck qua; chỉ thêm regression test cho hành vi có rủi ro thực tế.

### Nhiệm vụ quan sát với người dùng

Yêu cầu người thử tìm dịch vụ website, mở demo bất động sản, chọn một cấu hình báo giá và tìm cách liên hệ. Quan sát vị trí họ dừng lại, thao tác nhầm và câu hỏi phát sinh. Không hướng dẫn trước vị trí nút. Sửa các điểm gây vướng trước khi tăng thêm hiệu ứng.

## 10. Hướng dẫn bàn giao cho Grokbot

1. Đọc README, UPDATE-V6.1, REDESIGN-V6 và SELF-REVIEW-V6 để hiểu nguồn dữ liệu và giới hạn đã biết.
2. Tái lập bản hiện tại; xác định component liên quan trước khi sửa. Ưu tiên Header, ProjectShowcase, Ecosystem, Motion, QuoteExport và SupportWidgets.
3. Bắt đầu giai đoạn A/B, giữ logo, token, route và business rule. Không thay pricing engine chỉ để phục vụ layout.
4. Các ảnh thiết bị còn thiếu phải được thu thập từ demo được phép hoặc ghi rõ chưa có; không giả lập bằng cách cắt ảnh.
5. Với mỗi giai đoạn, bàn giao code, ảnh desktop/mobile, ghi chú thay đổi, kết quả kiểm tra và phần chưa xác minh.
6. Kiểm tra lại cách nối backend trước phát hành. Không gửi form thật, xem đơn hàng riêng tư hoặc triển khai domain ngoài phạm vi được chủ site cho phép.
7. Chỉ đưa WebGL, thư viện lớn hoặc API mới vào sau khi nêu rõ lợi ích, chi phí và phương án dự phòng.

## 11. Điều kiện hoàn thành định hướng giao diện

Website đạt mục tiêu khi khách cảm nhận được chất công nghệ, đồng thời dễ hiểu dịch vụ, xem được sản phẩm và thực hiện bước tiếp theo. Một nâng cấp chỉ được coi là thành công nếu cải thiện hình thức mà không làm suy giảm các nhiệm vụ đó.

Các checkbox là tiêu chí cho vòng triển khai tiếp theo, không phải xác nhận đã thực hiện các tính năng mới. Điều kiện bảo mật và phát hành được bổ sung bên dưới.


## 12. Đánh giá và ưu tiên bảo mật

Bảo mật là một luồng công việc song song với cải tiến trải nghiệm và là điều kiện trước phát hành. Các kết quả build/E2E hiện có không thay thế một đợt rà soát bảo mật. Các rủi ro dưới đây được suy ra từ kiến trúc đã trao đổi, chưa phải kết quả kiểm tra xâm nhập trên website production.

### Rủi ro cần xử lý đầu tiên: tra cứu tiến độ

Kiến trúc hiện tại lấy dữ liệu qua /data/orders.json và tìm đơn ở trình duyệt. Nếu phản hồi chứa nhiều đơn, phần dữ liệu đó đã tới máy người xem dù giao diện chỉ hiện một đơn. Việc băm mã tra cứu không bảo vệ được nội dung đã gửi xuống client. no-store chỉ hạn chế lưu cache, không phải kiểm soát truy cập.

**Đề xuất:** chuyển tra cứu sang máy chủ, chỉ trả các trường cần thiết của đúng đơn được phép xem. Dùng mã truy cập ngẫu nhiên đủ mạnh, có thể thu hồi; giới hạn lượt thử. Với thông tin nhạy cảm hơn tiến độ cơ bản, cần xác thực bổ sung như tài khoản hoặc xác minh qua kênh đã đăng ký. Không chỉ đổi tên URL hoặc giấu nút trên giao diện.

### Thứ tự xử lý

| Ưu tiên | Hạng mục | Kết quả cần đạt |
|---|---|---|
| S0 — Trước phát hành | Tra cứu tiến độ | Không trả danh sách đơn riêng tư cho client; kiểm tra quyền ở server |
| S0 — Trước phát hành | Form và PDF | Chống lạm dụng, giới hạn tài nguyên, validate phía server |
| S0 — Trước phát hành | Nội dung HTML/chatbot | Dữ liệu không tin cậy không thể chạy thành mã trong trang |
| S0 — Trước phát hành | Tài khoản, secrets, backend | Quyền tối thiểu, xác thực hai bước, cấu hình đúng nơi lưu bí mật |
| S1 — Trước phát hành | Dữ liệu và vận hành | Quy tắc lưu/xóa, logging tối thiểu, HTTPS, headers, backup |
| S2 — Duy trì | Thư viện và giám sát | Rà phiên bản, xử lý cảnh báo, thử khôi phục định kỳ |

S0/S1/S2 là ưu tiên bảo mật của tài liệu này, độc lập với P0/P1/P2/P3 của thiết kế.

## 13. Đặc tả bảo mật theo chức năng

### 13.1. API và tra cứu

- Xác minh quyền truy cập trên mỗi yêu cầu có dữ liệu riêng tư.
- Chỉ trả dữ liệu tối thiểu: trạng thái, phần trăm và ghi chú đã được duyệt cho khách xem. Không mặc định trả ghi chú nội bộ hoặc dữ liệu khách khác.
- Dữ liệu đơn hàng và bí mật không nằm trong public, bundle frontend, source map công khai hoặc ZIP bàn giao.
- Giới hạn lượt tra cứu, theo dõi hành vi bất thường và phản hồi lỗi không làm lộ thêm dữ liệu.
- Nếu mã tra cứu đóng vai trò khóa truy cập, tránh đưa mã vào URL/log/analytics; hỗ trợ thay hoặc thu hồi mã.
- Khi triển khai nhiều máy chủ, giới hạn tần suất cần có hiệu lực trên toàn hệ thống, không chỉ bộ nhớ của một tiến trình.

### 13.2. Form liên hệ

- Kiểm tra độ dài, kiểu dữ liệu, các trường được chấp nhận và consent phía server.
- Giới hạn tần suất, kích thước yêu cầu và số yêu cầu đồng thời; chống gửi trùng và đặt timeout cho backend.
- Honeypot là lớp hỗ trợ; chỉ yêu cầu thử thách chống bot khi cần để hạn chế ảnh hưởng khách thật.
- Kiểm tra Origin hiện có không phải xác thực hoặc chống spam. Nếu sau này dùng phiên đăng nhập/cookie cho thao tác thay đổi dữ liệu, bổ sung biện pháp chống CSRF phù hợp.
- Không đưa lỗi nội bộ, stack trace hoặc bí mật upstream vào thông báo trả cho khách.
- Consent ghi nhận lựa chọn của khách, không tự mã hóa hay bảo vệ dữ liệu. Nội dung đồng ý cần diễn đạt cụ thể mục đích sử dụng.

### 13.3. Tạo PDF báo giá

- Tiếp tục tính giá ở server từ dữ liệu giá được quản lý; không chấp nhận tổng giá do client gửi như nguồn tin cậy.
- Giới hạn hạng mục, số lượng, độ dài ghi chú, kích thước đầu vào, thời gian xử lý và mức đồng thời.
- Thêm giới hạn tần suất để một người dùng hoặc bot không chiếm toàn bộ tài nguyên tạo PDF.
- Chỉ dùng font/logo/tài nguyên đã kiểm soát. Không cho người dùng truyền URL hoặc đường dẫn tệp tùy ý để máy chủ đọc.
- Nếu có dữ liệu cá nhân trong PDF về sau, không để tải qua URL công khai có thể đoán được; xác định quyền truy cập và thời gian lưu rõ ràng.
- Không tự lưu lịch sử tải hoặc thông tin khách nếu tính năng không cần đến.

### 13.4. HTML, nội dung chuyển đổi và chatbot

- Rà các điểm dùng dangerouslySetInnerHTML, innerHTML và chèn nội dung từ tham số URL, API hoặc tin nhắn.
- Nội dung tĩnh lấy từ nguồn của chủ site vẫn cần quy trình kiểm tra khi cập nhật. Không mở rộng đường chèn HTML đó cho nội dung người dùng chưa được xử lý.
- Ưu tiên hiển thị dữ liệu như văn bản. Khi cần hỗ trợ HTML, dùng thư viện làm sạch phù hợp với danh sách thẻ/thuộc tính cho phép; không tự lọc bằng một vài biểu thức chính quy.
- Link do chatbot hoặc nội dung động tạo ra cần kiểm tra giao thức và đích đến phù hợp.
- Chatbot chỉ dùng nguồn kiến thức công khai/được phép; không cấp quyền đọc đơn hàng hoặc secrets để phục vụ tư vấn chung.
- Nếu sau này thêm LLM, cần review riêng dữ liệu gửi nhà cung cấp và quyền gọi công cụ. Chỉ dẫn do người dùng hoặc nội dung truy xuất cung cấp không được tự trở thành quyền truy cập dữ liệu hay quyền thực thi hành động.

### 13.5. Hạ tầng và tài khoản vận hành

- HTTPS trên production; kiểm tra cấu hình chuyển hướng và chứng chỉ. Chỉ bật chính sách HSTS sau khi xác nhận phạm vi domain/subdomain phù hợp.
- Thiết lập Content Security Policy phù hợp Next.js/GSAP; bắt đầu ở chế độ báo cáo, xử lý vi phạm rồi mới thực thi. Không mở rộng chính sách tùy tiện chỉ để bỏ lỗi.
- Bổ sung chính sách chống nhúng trái phép, nosniff và referrer policy phù hợp. CSP là lớp bổ sung, không thay xử lý XSS ở nguồn.
- Bật xác thực hai bước cho domain, hosting, repo và email nhận liên hệ. Dùng quyền tối thiểu, tránh tài khoản dùng chung.
- Secrets đặt phía máy chủ; không dùng biến công khai cho API key riêng tư. Kiểm tra repo/ZIP trước bàn giao; nếu từng lộ khóa, thu hồi và thay khóa, không chỉ xóa khỏi file hiện tại.
- Backend proxy dùng đích được cấu hình và kiểm soát. Trước cutover domain, tránh trỏ proxy trở lại chính ứng dụng gây vòng lặp.
- Cập nhật dependency theo quy trình có kiểm tra tương thích; xem xét từng cảnh báo thay vì tự động nâng tất cả lên phiên bản mới nhất.

### 13.6. Quyền riêng tư và vận hành

- Chỉ thu dữ liệu phục vụ yêu cầu cụ thể; định nghĩa người được truy cập, thời hạn lưu và cách xử lý yêu cầu xóa.
- Không ghi nguyên nội dung liên hệ, số điện thoại, mã tra cứu hoặc dữ liệu PDF vào log không cần thiết.
- Analytics không thu các trường biểu mẫu nhạy cảm hoặc mã truy cập. Không mặc định bật trong preview.
- Sao lưu có kiểm tra khôi phục; giới hạn quyền truy cập và thời gian giữ bản sao.
- Có người chịu trách nhiệm khi xảy ra sự cố: hạn chế truy cập, thu hồi khóa, giữ bằng chứng cần thiết, phục hồi và đánh giá ảnh hưởng.
- Các nội dung chính sách/đồng ý cuối cùng cần được chủ site duyệt; tài liệu này là đề xuất kỹ thuật, không thay thế đánh giá nghĩa vụ pháp lý cụ thể.

## 14. Acceptance bảo mật và cổng phát hành

Các mục dưới đây chưa được đánh dấu hoàn tất trong lần tổng hợp tài liệu này.

- [ ] Trình duyệt không tải được danh sách đơn hàng riêng tư qua API/public asset.
- [ ] Yêu cầu thiếu hoặc sai quyền không trả thông tin của đơn khác.
- [ ] Mã tra cứu và thông tin khách không xuất hiện ngoài ý muốn trong URL, log, analytics hoặc ZIP.
- [ ] Form từ chối đầu vào sai/thiếu consent; xử lý được gửi lặp và vượt giới hạn.
- [ ] PDF từ chối lựa chọn không hợp lệ; xử lý được quá tải mà không làm mất khả năng phục vụ toàn website.
- [ ] Nội dung nhập vào form/chatbot hoặc tham số URL không được thực thi thành HTML/script ngoài ý muốn.
- [ ] CSP và headers được kiểm tra trên các trang/công cụ chính; không làm hỏng GSAP, font, chatbot hoặc tải PDF.
- [ ] Secrets không xuất hiện trong client; tài khoản vận hành bật xác thực hai bước và có quyền phù hợp.
- [ ] Có quy tắc lưu/xóa dữ liệu, logging tối thiểu và backup đã thử khôi phục.
- [ ] Các hạn chế kiểm thử được ghi rõ; không suy từ build/E2E đạt thành website an toàn tuyệt đối.

**Cổng phát hành:** chỉ đề xuất đưa lên domain khi hoàn thành các mục S0/S1 áp dụng, các luồng chính hoạt động trên thiết bị thật, backend được cấu hình đúng và chủ site duyệt. Kiểm tra bằng dữ liệu giả trong môi trường kiểm thử; kiểm thử gây tải hoặc tác động production cần phạm vi được cho phép riêng.

## 15. Quyết định tổng hợp và nguồn tham khảo

### Quyết định thực hiện

1. Bắt đầu từ baseline v6.1, giữ các sửa lỗi menu, ảnh demo và business rule hiện tại.
2. Ưu tiên xử lý kiến trúc tra cứu, chống lạm dụng form/PDF và rà chèn HTML song song với hoàn thiện trình diễn dự án.
3. Sau đó cải tiến báo giá, hỗ trợ và hệ sinh thái dựa trên khả năng hoàn thành nhiệm vụ.
4. Quả cầu nâng cao/WebGL chỉ triển khai khi có lợi ích thị giác rõ, dự phòng đầy đủ và không làm xấu trải nghiệm đo được.
5. Mỗi đợt bàn giao phải có danh sách thay đổi, ảnh desktop/mobile, kết quả kiểm tra và các hạn chế thực tế. Không tự tuyên bố đạt chuẩn bảo mật, khả năng truy cập hay hiệu năng khi chưa có bằng chứng.

### Nguồn tham khảo bảo mật

Các hướng dẫn sau đã được tham khảo trong cuộc trao đổi; chúng hỗ trợ nguyên tắc phòng vệ, không xác nhận website My Agent đã áp dụng đầy đủ:

- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html): kiểm soát truy cập API, kiểm tra đầu vào và giới hạn tần suất.
- [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet): hiển thị an toàn dữ liệu không tin cậy, xử lý HTML và các lớp phòng vệ XSS.
- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html): sử dụng CSP như lớp phòng vệ bổ sung.

### Hồ sơ dự án dùng để tổng hợp

- README và hồ sơ REDESIGN-V6/SELF-REVIEW-V6 của repository.
- UPDATE-V6.1: thứ tự demo, hiển thị đủ hero và sửa điều hướng hệ sinh thái.
- MY-AGENT-UI-UX-UPGRADE-PLAN.md: đề xuất giao diện và tự review ban đầu.
- Phần trao đổi bảo mật: được tích hợp thành các phần 12–14, không coi là bản vá đã triển khai.

**Đầu ra của lần làm việc này:** một tài liệu Markdown tổng hợp. Không thay đổi mã website, cấu hình production hoặc nội dung ZIP đã bàn giao.
