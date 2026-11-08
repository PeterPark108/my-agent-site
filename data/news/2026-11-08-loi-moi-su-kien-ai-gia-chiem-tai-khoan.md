---
title: "Lời mời sự kiện AI giả chiếm tài khoản Microsoft, Google"
date: 2026-11-08
topic: bao-mat
summary: "Ngày 5/11/2026, Push Security cảnh báo chiến dịch giả lời mời sự kiện OpenAI, SpaceX và Anthropic để chiếm tài khoản Microsoft và Google của nhân viên, dùng Kali365 và VoidProxy."
insight: "Nhân viên doanh nghiệp nhỏ thường tò mò sự kiện AI và phần thưởng như ChatGPT Pro. Chỉ cần đăng nhập tài khoản công việc trên trang lạ, kể cả khi có xác thực hai lớp, bên kia vẫn có thể lấy phiên Microsoft 365 hoặc Google Workspace. Nên kiểm tra người gửi trước khi bấm đăng nhập."
tags: [phishing, microsoft, google, ai, bao-mat]
sources:
  - name: Push Security – Analyzing a fake event campaign combining AiTM and device code phishing payloads
    url: https://pushsecurity.com/blog/ai-themed-fake-event-campaign-analysis
    date: 2026-11-05
  - name: BleepingComputer – Fake OpenAI, SpaceX events used to steal Microsoft and Google accounts
    url: https://www.bleepingcomputer.com/news/security/fake-openai-spacex-events-used-to-steal-microsoft-google-accounts/
    date: 2026-11-05
---
## Có gì mới

Ngày 5/11/2026, công ty bảo mật Push Security công bố phân tích một chiến dịch dùng trang đăng ký sự kiện giả mạo OpenAI, SpaceX và Anthropic. Các trang này mời người xem tham gia livestream hoặc buổi giới thiệu về AI, rồi yêu cầu đăng nhập bằng tài khoản công việc để nhận phần thưởng.

Push cho biết họ đã phát hiện và chặn các lượt truy cập tới trang giả trên trình duyệt của khách hàng vào cuối tháng 10/2026. Một trang bắt chước giao diện OpenAI Academy, quảng bá livestream ngày 4/11 với chủ đề về ChatGPT dành cho nhóm marketing số và hứa tặng ba tháng ChatGPT Pro. Trang khác giả sự kiện riêng của SpaceX vào ngày 12/11 về AI cho marketing, cho người xem chọn phần thưởng ba tháng Grok Heavy hoặc một “cổ phần SpaceX”. Một biến thể giả sự kiện Anthropic tại hội nghị AWS re:Invent đã không còn hoạt động khi nhóm nghiên cứu kiểm tra.

Cả hai nút “Continue with Microsoft” và “Continue with Google” đều dẫn tới dịch vụ lừa đảo cho thuê (phishing-as-a-service). Theo Push, hai nền tảng này được thiết kế để vượt hoặc làm mất tác dụng lớp xác thực nhiều yếu tố (MFA):

- Với Microsoft: trang giả nhờ nền tảng Kali365 tạo mã đăng nhập thiết bị (device code) rồi hiện hộp thoại bảo người dùng sao chép mã và mở đúng trang đăng nhập thiết bị của Microsoft. Khi nạn nhân dán mã, đăng nhập và chấp thuận, Microsoft cấp token cho phiên Kali365 của bên tấn công — họ không cần gõ mật khẩu trên trang giả. Sau đó nạn nhân bị chuyển tiếp sang trang đăng nhập Microsoft do nền tảng VoidProxy đóng vai, để lấy thêm mật khẩu và cookie phiên.
- Với Google: trang giả mở cửa sổ bật lên là máy chủ proxy đứng giữa (adversary-in-the-middle) của VoidProxy. Proxy này chuyển tiếp đúng quy trình đăng nhập Google nên trông quen thuộc, đồng thời ghi lại mật khẩu, phản hồi MFA và cookie phiên.

Push nhận định Kali365 và VoidProxy là hai nền tảng riêng, bán dịch vụ cho nhiều chiến dịch không liên quan; nhóm điều hành chiến dịch này rất có thể chỉ là khách hàng của cả hai. BleepingComputer, khi tường thuật lại báo cáo vào cùng ngày 5/11/2026, cũng nêu rõ cùng một trang giả có thể kết hợp cả hai nền tảng tùy nút người dùng chọn.

Đường dẫn tới trang giả thường đi qua liên kết rút gọn của Google hoặc của Zapier. Các đợt trước còn từng gửi thư qua hệ thống thư sự kiện trực tuyến hoặc trang sự kiện Zoom thật. Trước khi hiện form đăng ký, miền giả hiện thử thách “xác nhận bạn không phải robot” của Cloudflare, nên nhiều công cụ quét công khai dừng lại ở bước này. Push ghi nhận miền họ kiểm tra vào ngày 2/11/2026 mới chỉ được tạo khoảng ba ngày, và bên điều hành đổi miền vài tuần một lần.

## Vì sao doanh nghiệp nhỏ cần chú ý

Phần thưởng kiểu gói AI trả phí hoặc “sự kiện nội bộ” rất dễ hấp dẫn nhân viên ở mọi ngành, không riêng đội kỹ thuật. Trang giả còn tự dịch theo ngôn ngữ trình duyệt, nên người xem tiếng Việt cũng có thể thấy giao diện quen. Yêu cầu “đăng nhập tài khoản công việc để nhận quà” nghe hợp lý với sự kiện miễn phí, nhưng đó chính là bước trao quyền truy cập hộp thư, tệp và các ứng dụng đã liên kết.

Điều dễ gây nhầm là nạn nhân có thể đang thao tác trên trang Microsoft thật khi nhập mã thiết bị. Xác thực hai lớp thông thường không chặn được kiểu này: với device code, token được cấp sau khi người dùng đã xác nhận trên trang chính thức; với proxy đứng giữa, bên tấn công lấy luôn phiên đã đăng nhập. BleepingComputer lưu ý token Microsoft lấy được có thể dùng để vào Microsoft 365 và các ứng dụng đăng nhập một lần (SSO) đã kết nối với tài khoản đó.

Việc này liên quan trực tiếp tới thói quen hằng ngày hơn là “vá một lỗ hổng phần mềm”. Website và email doanh nghiệp vẫn cần được [bảo mật ở lớp cơ bản](../blog/bao-mat-website-co-ban-cho-doanh-nghiep-nho.html), nhưng lần này cửa vào là lời mời sự kiện trông có vẻ hữu ích.

## Việc nên làm ngay

1. Không nhập mã đăng nhập thiết bị Microsoft do một website lạ đưa ra. Không đăng nhập tài khoản công việc chỉ để nhận quà hay giữ chỗ sự kiện AI khi chưa kiểm tra người gửi qua một kênh khác đã biết (điện thoại nội bộ, email công ty đã xác nhận).
2. Nhắc cả nhóm: lời mời sự kiện gắn thương hiệu công cụ AI kèm phần thưởng, nhất là khi bắt buộc dùng email công ty, cần được xác minh trước khi bấm đăng nhập.
3. Nếu ai đó đã nhập mã hoặc đã đăng nhập trên trang nghi ngờ: coi tài khoản đã bị chiếm. Đổi mật khẩu, thu hồi phiên đăng nhập và token, kiểm tra quy tắc chuyển tiếp hộp thư, các ứng dụng OAuth đã cấp quyền và nhật ký đăng nhập lạ.
4. Ở cấp độ quản trị: tắt hoặc hạn chế đăng nhập bằng device code nếu doanh nghiệp không dùng tới; ưu tiên hình thức xác thực kháng lừa đảo như khóa bảo mật FIDO2 khi nhà cung cấp hỗ trợ.
5. Không chỉ dựa vào danh sách miền độc hại. Push cho biết bên điều hành xoay miền thường xuyên và núp sau liên kết của dịch vụ lớn, nên các dấu hiệu kỹ thuật chủ yếu hữu ích để rà nhật ký cũ hơn là để chặn các đợt sau.

Tin này không đòi doanh nghiệp nhỏ mua thêm phần mềm ngay. Việc thực tế nhất là dừng lại trước khi “đăng nhập để nhận quà sự kiện AI”, và nhớ rằng nhìn thấy trang đăng nhập Microsoft hoặc Google quen thuộc vẫn chưa đủ để kết luận đường dẫn đó an toàn.
