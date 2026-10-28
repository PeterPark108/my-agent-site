# -*- coding: utf-8 -*-
"""Nội dung chuyên sâu cho từng trang dịch vụ (dùng bởi scripts/svc_deep.py).
Nguyên tắc: không bịa số liệu, giá, khách hàng, cam kết thứ hạng hay thời gian cố định."""
S={}
S['thiet-ke-website']=dict(
 vis=('browser',['Header + menu','Hero: lời hứa giá trị','Dịch vụ / sản phẩm','Bằng chứng & CTA','Footer: NAP, liên kết'],'Khung wireframe một trang web: header, hero, dịch vụ, CTA, footer'),
 steps=[('Brief & mục tiêu','Xác định trang cần đạt gì: gọi điện, để lại form hay đặt hàng; ai là khách chính.'),('Sơ đồ trang & wireframe','Lên cấu trúc trang, thứ tự nội dung và đường đi của khách trước khi vẽ giao diện.'),('Thiết kế giao diện','Áp màu, chữ, hình theo nhận diện; duyệt trên cả bản máy tính và điện thoại.'),('Lập trình & nội dung','Dựng mã responsive, gắn nội dung thật, tối ưu ảnh và thẻ SEO cơ bản.'),('Kiểm thử','Kiểm tra trên nhiều trình duyệt, tốc độ tải, form, liên kết hỏng, hiển thị di động.'),('Đưa lên & hướng dẫn','Trỏ tên miền, bật HTTPS, gửi sitemap, hướng dẫn cập nhật nội dung.')],
 exp=('Một website "chuẩn" gồm những gì',[('Tốc độ & Core Web Vitals','Ảnh nén đúng kích thước (WebP), tải chậm ảnh ngoài màn hình, giữ chỗ trước cho ảnh để trang không giật (CLS thấp).'),('Responsive thật sự','Thiết kế từ màn hình điện thoại lên, nút bấm đủ lớn để chạm, chữ đọc được không cần phóng to.'),('SEO kỹ thuật','Mỗi trang một title/description riêng, thẻ H1 rõ ràng, URL dễ đọc, sitemap.xml, robots.txt, dữ liệu cấu trúc (schema).'),('Bảo mật cơ bản','HTTPS, các header bảo mật, form có chống spam, không để lộ file cấu hình hay trang quản trị mặc định.'),('Khả năng tiếp cận','Độ tương phản màu đủ, ảnh có mô tả (alt), dùng được bằng bàn phím: tốt cho người dùng và cho SEO.')]),
 deliv=['Website chạy trên tên miền của bạn, có HTTPS','Giao diện máy tính + điện thoại','Sitemap, robots.txt, thẻ SEO từng trang','Form liên hệ gửi về email của bạn','Tài liệu / buổi hướng dẫn cập nhật nội dung','Quyền quản trị và mã nguồn sau khi thanh toán đủ'],
 tech=['HTML5','CSS3','JavaScript','WordPress','Figma','Nginx','Cloudflare','Google Search Console','GA4'],
 fit=['Doanh nghiệp, cửa hàng cần web giới thiệu hoặc bán hàng quy mô nhỏ – vừa','Bạn muốn sở hữu website và tên miền, không phụ thuộc nền tảng thuê','Cần trang đích (landing page) cho một chiến dịch quảng cáo'],
 nofit=['Cần sàn thương mại điện tử nhiều người bán hoặc hệ thống rất lớn','Chỉ cần một trang bán hàng tạm thời trên sàn có sẵn'],
 faq=[('Nên làm web bằng WordPress hay code tay?','WordPress hợp khi bạn tự đăng bài, sản phẩm thường xuyên. Code tay (HTML/CSS/JS) nhẹ, nhanh và ít lỗ hổng plugin, hợp với web giới thiệu ít thay đổi. Tôi tư vấn dựa trên cách bạn sẽ dùng web.'),('Website mới làm có lên Google ngay không?','Google cần thời gian để thu thập và lập chỉ mục. Tôi gửi sitemap qua Search Console để rút ngắn bước này, nhưng thứ hạng phụ thuộc nội dung và mức cạnh tranh, không ai cam kết được vị trí.')],
 rel=['seo-tong-the','hosting-seo','cham-soc-website'])
S['seo-tong-the']=dict(
 vis=('flow',['Kỹ thuật','Từ khoá','Nội dung','Liên kết','Đo lường'],'Năm trụ cột SEO nối với nhau: kỹ thuật, từ khoá, nội dung, liên kết, đo lường'),
 steps=[('Audit hiện trạng','Thu thập dữ liệu trang, lỗi index, tốc độ, trùng lặp nội dung, trang 404.'),('Nghiên cứu từ khoá','Nhóm từ khoá theo ý định tìm kiếm (tìm hiểu, so sánh, mua) và gán cho từng trang.'),('Sửa kỹ thuật','Title, meta, heading, canonical, sitemap, schema, liên kết nội bộ, tốc độ.'),('Nội dung','Viết mới hoặc nâng cấp bài theo từ khoá; AI hỗ trợ dàn ý nhưng tôi biên tập và kiểm tra lại.'),('Liên kết & uy tín','Hồ sơ doanh nghiệp, Google Maps, đối tác thật; tránh mua liên kết rác.'),('Đo & điều chỉnh','Theo dõi Search Console và GA4, báo cáo định kỳ những gì thay đổi và lý do.')],
 exp=('SEO bền vững làm theo thứ tự nào',[('Index trước, xếp hạng sau','Trang không được lập chỉ mục thì nội dung hay đến mấy cũng không lên. Bước đầu luôn là kiểm tra Search Console.'),('Một trang – một ý định','Mỗi trang nhắm một nhóm từ khoá chính, tránh nhiều trang tự cạnh tranh với nhau (cannibalization).'),('Nội dung trả lời đúng câu hỏi','Bài viết tốt trả lời điều người tìm thực sự cần, có kinh nghiệm thật, dễ đọc trên điện thoại.'),('Không dùng mánh','Không nhồi từ khoá, không mua backlink hàng loạt, không traffic ảo: rủi ro bị Google phạt lớn hơn lợi ích.')]),
 deliv=['Báo cáo audit SEO kèm danh sách lỗi ưu tiên','Bản đồ từ khoá – trang','Các chỉnh sửa kỹ thuật đã thực hiện','Kế hoạch / bài viết nội dung','Báo cáo định kỳ từ Search Console và GA4'],
 tech=['Google Search Console','GA4','PageSpeed Insights','Schema.org','Python','Google Sheets'],
 fit=['Website đã có nhưng ít khách từ Google','Doanh nghiệp sẵn sàng đầu tư nội dung đều đặn vài tháng','Cần hiểu vì sao trang không được index'],
 nofit=['Cần đơn hàng ngay trong tuần tới (nên chạy quảng cáo)','Muốn cam kết vị trí top 1 trong thời gian cố định'],
 faq=[('SEO bao lâu thì thấy kết quả?','Tuỳ độ cạnh tranh của từ khoá, tình trạng website và lượng nội dung. Các lỗi kỹ thuật có thể sửa nhanh, còn thứ hạng thường cần nhiều tháng; tôi không hứa mốc cố định.'),('AI Content SEO có bị Google phạt không?','Google đánh giá chất lượng và tính hữu ích, không phạt chỉ vì dùng AI. Rủi ro nằm ở nội dung sai, chung chung. Vì vậy tôi dùng AI để hỗ trợ và luôn biên tập, kiểm tra lại thông tin.')],
 rel=['thiet-ke-website','google-maps','hosting-seo'])
S['hosting-seo']=dict(
 vis=('flow',['Khách truy cập','CDN / DNS','Nginx + HTTPS','Website','Sao lưu'],'Luồng truy cập từ khách qua DNS, máy chủ Nginx có HTTPS tới website và bản sao lưu'),
 steps=[('Đánh giá nhu cầu','Loại website, lượng truy cập dự kiến, nền tảng (WordPress hay web tĩnh).'),('Chọn & cấu hình máy chủ','Cài máy chủ web, PHP/cơ sở dữ liệu nếu cần, bật nén và bộ nhớ đệm.'),('Bảo mật','HTTPS, tường lửa, tắt dịch vụ thừa, cập nhật hệ thống, phân quyền thư mục.'),('Chuyển dữ liệu','Di chuyển website cũ, kiểm tra lại link, form, email trước khi đổi DNS.'),('Sao lưu & giám sát','Lịch sao lưu tự động, kiểm tra khôi phục được, theo dõi website còn chạy.')],
 exp=('Hosting ảnh hưởng SEO ở đâu',[('Thời gian phản hồi máy chủ','Máy chủ chậm làm tăng TTFB, kéo theo chỉ số LCP xấu đi, ảnh hưởng trải nghiệm và Core Web Vitals.'),('Nén & bộ nhớ đệm','Bật gzip/brotli và cache header đúng giúp trang tải lại nhanh hơn rõ rệt.'),('HTTPS & chuyển hướng','Một phiên bản duy nhất (https, có hoặc không www) để Google không thấy nội dung trùng.'),('Sao lưu có thể khôi phục','Bản sao lưu chỉ có giá trị khi đã thử khôi phục; tôi kiểm tra định kỳ chứ không chỉ bật tính năng.')]),
 deliv=['Máy chủ đã cấu hình và bảo mật cơ bản','Chứng chỉ HTTPS tự gia hạn','Lịch sao lưu tự động','Thông tin truy cập bàn giao cho bạn','Ghi chú cấu hình để kỹ thuật khác tiếp quản được'],
 tech=['Linux','Nginx','Let\'s Encrypt','Cloudflare','MySQL','PHP','WordPress'],
 fit=['Website WordPress hoặc web doanh nghiệp đang chậm, hay lỗi','Muốn chuyển khỏi hosting cũ mà không mất dữ liệu','Cần người hiểu kỹ thuật lo phần máy chủ'],
 nofit=['Ứng dụng cần hạ tầng nhiều máy chủ, tải rất lớn','Chỉ cần trang đơn giản trên nền tảng dựng sẵn có hosting kèm'],
 faq=[('Đổi hosting có làm rớt thứ hạng không?','Nếu giữ nguyên URL, nội dung và chỉ đổi máy chủ thì thường không ảnh hưởng. Tôi kiểm tra kỹ trước khi đổi DNS để tránh thời gian chết và link hỏng.'),('Tôi có giữ quyền quản trị máy chủ không?','Có. Tài khoản nhà cung cấp nên đứng tên bạn; tôi bàn giao thông tin truy cập và ghi chú cấu hình.')],
 rel=['ten-mien','cham-soc-website','thiet-ke-website'])
S['ten-mien']=dict(
 vis=('flow',['tenmien.vn','Nhà đăng ký','DNS: A / CNAME','DNS: MX / TXT','Web + Email'],'Tên miền qua nhà đăng ký và bản ghi DNS tới website và email'),
 steps=[('Chọn tên','Ngắn, dễ đọc qua điện thoại, tránh dấu gạch và ký tự dễ nhầm; kiểm tra nhãn hiệu trùng.'),('Chọn đuôi','.vn cho thị trường Việt Nam, .com cho thương hiệu quốc tế; có thể giữ cả hai.'),('Đăng ký đứng tên bạn','Thông tin chủ thể là doanh nghiệp hoặc cá nhân của bạn, không phải bên làm dịch vụ.'),('Cấu hình DNS','Trỏ bản ghi cho website, email, xác minh Google; bật DNSSEC khi nhà đăng ký hỗ trợ.'),('Theo dõi gia hạn','Ghi lại ngày hết hạn và bật tự gia hạn để không mất tên miền.')],
 exp=('Những điều dễ bỏ sót với tên miền',[('Chủ thể đứng tên','Tên miền đứng tên người khác thì khi có tranh chấp bạn rất khó lấy lại. Luôn để doanh nghiệp/bạn là chủ thể.'),('Bản ghi DNS chính','A/AAAA cho web, CNAME cho tên phụ, MX cho email, TXT cho SPF, DKIM, DMARC và xác minh dịch vụ.'),('Tên miền .vn','Do VNNIC quản lý, cần thông tin chủ thể chính xác theo quy định.'),('Hết hạn = mất địa chỉ','Quên gia hạn có thể làm web và email ngừng hoạt động, thậm chí bị người khác đăng ký mất.')]),
 deliv=['Tên miền đứng tên bạn','Thông tin tài khoản quản lý tên miền','Bản ghi DNS cho web và email đã cấu hình','Ghi chú ngày hết hạn và cách gia hạn'],
 tech=['DNS','DNSSEC','Cloudflare','WHOIS / RDAP','SPF · DKIM · DMARC'],
 fit=['Doanh nghiệp mới, chưa có tên miền','Tên miền đang do bên khác giữ, muốn chuyển về đứng tên mình','Cần cấu hình DNS cho web và email'],
 nofit=['Muốn mua lại tên miền đã có người sở hữu (cần thương lượng với chủ cũ)'],
 faq=[('Nên chọn .vn hay .com?','Khách chủ yếu ở Việt Nam thì .vn tạo cảm giác địa phương, tin cậy; .com dễ nhớ với khách quốc tế. Nếu ngân sách cho phép, đăng ký cả hai và chuyển hướng về một tên chính.'),('Tên miền đang ở bên khác có chuyển về được không?','Thường được, nếu bạn là chủ thể hoặc có giấy tờ chứng minh. Cần mã chuyển (auth code) và mở khoá chuyển; tôi hướng dẫn từng bước.')],
 rel=['email-doanh-nghiep','hosting-seo','thiet-ke-website'])
S['email-doanh-nghiep']=dict(
 vis=('flow',['ban@congty.vn','SPF: ai được gửi','DKIM: chữ ký','DMARC: chính sách','Hộp thư người nhận'],'Email doanh nghiệp đi qua SPF, DKIM, DMARC tới hộp thư người nhận'),
 steps=[('Chọn nền tảng','So sánh Google Workspace, Microsoft 365 hoặc email theo hosting theo số người dùng và nhu cầu.'),('Tạo tài khoản','Tạo hộp thư, nhóm (sales@, lienhe@), bí danh và phân quyền quản trị.'),('Cấu hình DNS','MX, SPF, DKIM, DMARC để thư đi không bị vào spam và chống giả mạo.'),('Chuyển thư cũ','Di chuyển email và danh bạ từ hộp thư cũ nếu cần.'),('Cài trên thiết bị','Cài trên điện thoại, máy tính; bật xác thực hai lớp cho từng người.')],
 exp=('Vì sao email hay vào spam',[('Thiếu SPF','Máy chủ nhận không biết dịch vụ nào được phép gửi thư thay tên miền của bạn.'),('Thiếu DKIM','Thư không có chữ ký số nên không chứng minh được không bị sửa trên đường đi.'),('Chưa có DMARC','Không có chính sách xử lý thư giả mạo; kẻ xấu có thể giả danh tên miền của bạn.'),('Mật khẩu yếu, không 2FA','Tài khoản bị chiếm thường được dùng để gửi spam, làm hỏng uy tín cả tên miền.')]),
 deliv=['Hộp thư theo tên miền cho từng người','Bản ghi MX, SPF, DKIM, DMARC đã kiểm tra','Hướng dẫn cài trên điện thoại / máy tính','Quyền quản trị chính thuộc về bạn'],
 tech=['Google Workspace','Microsoft 365','SPF','DKIM','DMARC','IMAP'],
 fit=['Đang dùng Gmail cá nhân để giao dịch với khách','Email gửi đi hay vào spam','Cần nhiều hộp thư theo phòng ban'],
 nofit=['Cần gửi email marketing hàng loạt (nên dùng nền tảng gửi thư chuyên dụng riêng)'],
 faq=[('Email doanh nghiệp khác Gmail thường thế nào?','Địa chỉ theo tên miền riêng (ban@congty.vn) tạo uy tín, doanh nghiệp quản lý được tài khoản của nhân viên và thu hồi khi nghỉ việc.'),('Phí bản quyền Google Workspace / Microsoft 365 tính thế nào?','Theo bảng giá, mức Google Workspace / Microsoft 365 tính theo người mỗi tháng, gồm phí bản quyền và hỗ trợ cài đặt; tài khoản đứng tên doanh nghiệp của bạn.')],
 rel=['ten-mien','hosting-seo','thiet-ke-website'])
S['google-maps']=dict(
 vis=('map',['Hồ sơ Google Business','Tên · Địa chỉ · SĐT','Giờ mở cửa','Ảnh thật','Đánh giá'],'Ghim bản đồ và các thành phần của hồ sơ doanh nghiệp trên Google'),
 steps=[('Kiểm tra hiện trạng','Tìm hồ sơ đã tồn tại hoặc bị trùng, ai đang quản lý.'),('Tạo / nhận quyền sở hữu','Tạo hồ sơ Google Business Profile đứng tên tài khoản của bạn.'),('Xác minh','Làm theo phương thức Google yêu cầu (video, điện thoại hoặc thư); bước này do Google quyết định.'),('Tối ưu hồ sơ','Danh mục chính xác, mô tả, giờ mở cửa, dịch vụ, ảnh thật của cửa hàng.'),('Duy trì','Hướng dẫn trả lời đánh giá, đăng cập nhật, giữ thông tin luôn đúng.')],
 exp=('Hồ sơ Maps tốt cần gì',[('NAP nhất quán','Tên, địa chỉ, số điện thoại giống hệt nhau trên Maps, website, Facebook để Google tin tưởng.'),('Danh mục chính đúng','Danh mục chính ảnh hưởng mạnh đến việc hiện ra với tìm kiếm gần đây.'),('Đánh giá thật','Xin đánh giá từ khách thật và trả lời lịch sự; đánh giá ảo vi phạm chính sách và có thể bị xoá.'),('Ảnh thật, cập nhật','Ảnh mặt tiền, bên trong, sản phẩm giúp khách nhận ra và tin tưởng.')]),
 deliv=['Hồ sơ Google Business đứng tên tài khoản của bạn','Thông tin, danh mục, giờ mở cửa đã tối ưu','Ảnh và mô tả được sắp xếp','Hướng dẫn trả lời đánh giá và đăng bài'],
 tech=['Google Business Profile','Google Maps','Schema LocalBusiness','Search Console'],
 fit=['Cửa hàng, quán, phòng khám, văn phòng có địa chỉ thật','Doanh nghiệp phục vụ khách theo khu vực'],
 nofit=['Không có địa chỉ đón khách và không phục vụ theo khu vực','Muốn tạo nhiều địa chỉ ảo để phủ bản đồ (vi phạm chính sách Google)'],
 faq=[('Có cam kết lên top Google Maps không?','Không. Thứ hạng phụ thuộc khoảng cách tới người tìm, mức liên quan và độ uy tín của hồ sơ. Tôi tối ưu những gì kiểm soát được.'),('Xác minh hồ sơ mất bao lâu?','Do Google quyết định và có thể khác nhau từng trường hợp. Tôi hỗ trợ chuẩn bị đúng thông tin để giảm khả năng bị từ chối.')],
 rel=['seo-tong-the','thiet-ke-website','quang-cao-google-facebook'])
S['quang-cao-google-facebook']=dict(
 vis=('funnel',['Hiển thị','Nhấp','Truy cập trang','Chuyển đổi'],'Phễu quảng cáo từ hiển thị, nhấp, truy cập tới chuyển đổi'),
 steps=[('Mục tiêu & ngân sách','Xác định kết quả cần đo: cuộc gọi, tin nhắn, form hay đơn hàng.'),('Cài đo lường','GA4, Google Ads conversion, Meta Pixel, UTM để biết tiền đi đâu ra gì.'),('Nghiên cứu & dựng chiến dịch','Từ khoá, đối tượng, cấu trúc nhóm quảng cáo, từ khoá phủ định.'),('Mẫu quảng cáo & trang đích','Nội dung, hình ảnh rõ lợi ích; trang đích khớp với lời hứa trong quảng cáo.'),('Tối ưu','Tắt nhóm kém, thử A/B mẫu quảng cáo, điều chỉnh giá thầu theo dữ liệu.'),('Báo cáo','Chi phí, lượt chuyển đổi, chi phí mỗi kết quả và việc sẽ làm tiếp.')],
 exp=('Quảng cáo hiệu quả dựa trên đo lường',[('Đo chuyển đổi trước khi chạy','Không đo được thì không tối ưu được; thuật toán cũng cần dữ liệu chuyển đổi để học.'),('Ý định tìm kiếm vs. sở thích','Google Search bắt người đang tìm; Facebook tiếp cận theo sở thích, hợp tạo nhu cầu và nhắc lại.'),('Trang đích quyết định','Cùng ngân sách, trang đích chậm hoặc khó liên hệ làm mất phần lớn khách đã nhấp.'),('Tuân thủ chính sách','Một số ngành bị hạn chế quảng cáo; nội dung sai chính sách dễ bị từ chối hoặc khoá tài khoản.')]),
 deliv=['Tài khoản quảng cáo đứng tên bạn','Đo lường chuyển đổi đã cài và kiểm tra','Cấu trúc chiến dịch và mẫu quảng cáo','Báo cáo định kỳ chi phí – kết quả'],
 tech=['Google Ads','Meta Ads Manager','GA4','Google Tag Manager','Meta Pixel','UTM'],
 fit=['Cần khách hàng trong thời gian ngắn','Đã có trang đích hoặc fanpage để nhận khách','Muốn biết rõ mỗi kết quả tốn bao nhiêu'],
 nofit=['Sản phẩm thuộc nhóm bị nền tảng cấm quảng cáo','Chưa có cách nhận và xử lý khách khi họ liên hệ'],
 faq=[('Ngân sách quảng cáo trả cho ai?','Bạn nạp tiền trực tiếp vào tài khoản quảng cáo của mình trên Google/Meta. Phí dịch vụ quản lý tính riêng và minh bạch.'),('Có cam kết số đơn không?','Không. Kết quả phụ thuộc sản phẩm, giá, thị trường và trang đích. Tôi cam kết đo lường rõ ràng và tối ưu dựa trên dữ liệu.')],
 rel=['thiet-ke-website','cham-soc-fanpage','phan-tich-du-lieu'])
S['cham-soc-fanpage']=dict(
 vis=('calendar',['Giáo dục','Sản phẩm','Hậu trường','Phản hồi KH','Ưu đãi'],'Lịch nội dung tuần với các tuyến bài khác nhau'),
 steps=[('Rà soát fanpage','Thông tin trang, nút hành động, bài cũ, tệp người theo dõi.'),('Định vị & tuyến nội dung','Chọn các tuyến bài: kiến thức, sản phẩm, hậu trường, phản hồi khách, ưu đãi.'),('Lịch đăng','Lên lịch tháng, duyệt trước với bạn, hẹn giờ đăng.'),('Sản xuất','Viết bài, thiết kế ảnh, video ngắn theo nhận diện thương hiệu.'),('Tương tác & đo','Theo dõi tiếp cận, tương tác, tin nhắn; điều chỉnh tuyến bài theo số liệu.')],
 exp=('Fanpage hiệu quả không chỉ là đăng đều',[('Tuyến nội dung rõ','Mỗi bài thuộc một tuyến có mục đích; tránh chỉ đăng bài bán hàng liên tục.'),('Định dạng phù hợp','Video ngắn, ảnh carousel, bài chữ: dùng định dạng hợp với nội dung và hành vi người xem.'),('Trả lời nhanh, đúng giọng','Tin nhắn và bình luận là nơi chốt khách; cần kịch bản trả lời thống nhất.'),('Số liệu thật','Đọc số liệu trong Meta Business Suite, không mua like hay tương tác ảo.')]),
 deliv=['Bộ tuyến nội dung và lịch đăng tháng','Bài viết, ảnh thiết kế theo lịch','Kịch bản trả lời tin nhắn thường gặp','Báo cáo số liệu tháng'],
 tech=['Meta Business Suite','Canva','Figma','CapCut'],
 fit=['Fanpage đăng thất thường, không có người phụ trách','Cần nội dung đồng bộ thương hiệu'],
 nofit=['Muốn tăng nhanh lượt thích bằng tài khoản ảo','Cần quản lý cộng đồng rất lớn liên tục ngoài giờ'],
 faq=[('Ai duyệt bài trước khi đăng?','Bạn. Lịch và nội dung được gửi trước để duyệt, chỉnh xong mới hẹn giờ đăng.'),('Có cần chạy quảng cáo kèm không?','Không bắt buộc. Tiếp cận tự nhiên của fanpage có giới hạn; khi cần mở rộng nhanh, quảng cáo là lựa chọn bổ sung.')],
 rel=['quang-cao-google-facebook','video-ai','zalo-oa-mini-app'])
S['cham-soc-website']=dict(
 vis=('checklist',['Cập nhật lõi, plugin','Sao lưu & thử khôi phục','Quét mã độc','Kiểm tra form, link hỏng','Tốc độ & uptime','Báo cáo tháng'],'Danh sách việc chăm sóc website hằng tháng'),
 steps=[('Kiểm tra ban đầu','Đánh giá phiên bản, plugin, sao lưu hiện có, lỗ hổng đã biết.'),('Thiết lập nền','Sao lưu tự động, giám sát hoạt động, tài khoản quản trị an toàn.'),('Bảo trì định kỳ','Cập nhật, quét bảo mật, dọn dữ liệu rác, kiểm tra form và liên kết.'),('Cập nhật nội dung','Đăng bài, sửa thông tin, thay ảnh theo yêu cầu trong phạm vi gói.'),('Báo cáo','Việc đã làm, sự cố phát hiện và đề xuất tháng sau.')],
 exp=('Vì sao website cần chăm sóc',[('Plugin cũ là lỗ hổng','Phần lớn website WordPress bị tấn công qua plugin, theme chưa cập nhật.'),('Cập nhật có kiểm soát','Sao lưu trước, cập nhật, kiểm tra lại; không bấm cập nhật hàng loạt trên web đang chạy.'),('Sao lưu ngoài máy chủ','Bản sao lưu để cùng máy chủ sẽ mất cùng lúc khi máy chủ gặp sự cố.'),('Form không báo lỗi','Form liên hệ có thể hỏng âm thầm; kiểm tra định kỳ tránh mất khách.')]),
 deliv=['Lịch bảo trì và sao lưu định kỳ','Nhật ký thay đổi','Báo cáo tháng','Hỗ trợ trong giờ làm việc'],
 tech=['WordPress','PHP','MySQL','Nginx','Cloudflare','Google Search Console','PageSpeed Insights'],
 fit=['Website đang chạy nhưng không ai lo kỹ thuật','Từng bị hack hoặc mất dữ liệu','Cần người cập nhật nội dung định kỳ'],
 nofit=['Cần đội trực sự cố liên tục ngoài giờ'],
 faq=[('Web bị hack thì xử lý thế nào?','Cô lập, khôi phục từ bản sao lưu sạch, đổi toàn bộ mật khẩu, vá lỗ hổng là nguyên nhân rồi theo dõi thêm. Có sao lưu tốt thì khôi phục nhanh hơn nhiều.'),('Chăm sóc web do bên khác làm được không?','Được, sau khi tôi kiểm tra mã nguồn và quyền truy cập. Nếu có vấn đề lớn, tôi báo trước khi nhận.')],
 rel=['hosting-seo','thiet-ke-website','seo-tong-the'])
S['bo-cong-thuong']=dict(
 vis=('checklist',['Xác định: thông báo hay đăng ký','Chính sách đổi trả, bảo mật','Thông tin chủ sở hữu trên web','Nộp hồ sơ online.gov.vn','Bổ sung theo yêu cầu','Gắn logo đã thông báo'],'Các bước thông báo website với Bộ Công Thương'),
 steps=[('Xác định loại hồ sơ','Website tự bán hàng thường thuộc diện thông báo; sàn hoặc website cho người khác bán thuộc diện đăng ký.'),('Rà soát website','Kiểm tra các nội dung bắt buộc: thông tin doanh nghiệp, chính sách, điều khoản.'),('Chuẩn bị nội dung','Soạn hoặc chỉnh trang chính sách đổi trả, vận chuyển, thanh toán, bảo mật thông tin.'),('Nộp hồ sơ','Tạo tài khoản và khai hồ sơ trên online.gov.vn bằng thông tin doanh nghiệp.'),('Theo dõi & bổ sung','Phản hồi yêu cầu chỉnh sửa của cơ quan quản lý cho đến khi được xác nhận.'),('Gắn logo','Gắn logo "Đã thông báo Bộ Công Thương" kèm liên kết xác thực lên website.')],
 exp=('Những điểm hồ sơ hay bị trả lại',[('Thiếu thông tin chủ sở hữu','Website cần hiển thị tên doanh nghiệp, mã số thuế, địa chỉ, liên hệ đúng giấy phép.'),('Chính sách chung chung','Chính sách đổi trả, giao hàng, thanh toán, bảo mật phải cụ thể cho cách bạn bán.'),('Nhầm loại hồ sơ','Sàn thương mại điện tử và website tự bán có yêu cầu khác nhau.'),('Thông tin không khớp','Thông tin trên hồ sơ, giấy phép và website phải thống nhất.')]),
 deliv=['Tư vấn loại hồ sơ phù hợp','Danh sách nội dung website cần bổ sung','Hỗ trợ khai hồ sơ trên online.gov.vn','Hướng dẫn gắn logo xác thực'],
 tech=['online.gov.vn','HTML','WordPress'],
 fit=['Website có chức năng đặt hàng, bán hàng online','Doanh nghiệp cần làm đúng quy định thương mại điện tử'],
 nofit=['Website chỉ giới thiệu, không có chức năng bán hàng (thường không bắt buộc, tôi sẽ tư vấn thật)'],
 faq=[('Website nào phải thông báo với Bộ Công Thương?','Theo quy định về thương mại điện tử, website bán hàng của chính doanh nghiệp thuộc diện thông báo; website sàn hoặc cung cấp dịch vụ TMĐT thuộc diện đăng ký. Tôi xem website cụ thể để tư vấn đúng diện.'),('Kết quả duyệt có phụ thuộc My Agent không?','Không. Việc xác nhận do cơ quan quản lý thực hiện. Tôi giúp hồ sơ đầy đủ, đúng để hạn chế bị yêu cầu bổ sung.')],
 rel=['thiet-ke-website','ten-mien','cham-soc-website'])
S['profile-doanh-nghiep']=dict(
 vis=('doc',['Giới thiệu','Năng lực','Dự án','Liên hệ'],'Các trang của một hồ sơ năng lực doanh nghiệp'),
 steps=[('Thu thập thông tin','Lịch sử, lĩnh vực, năng lực, dự án, hình ảnh, giấy tờ có thể công bố.'),('Cấu trúc nội dung','Sắp thứ tự trang theo người đọc: đối tác, nhà đầu tư hay khách hàng.'),('Biên tập','Viết gọn, đúng sự thật, đúng thuật ngữ ngành; không phóng đại.'),('Thiết kế dàn trang','Lưới trang, màu và chữ theo nhận diện, biểu đồ, hình minh hoạ.'),('Xuất file','Bản PDF nhẹ để gửi email và bản in đúng thông số.')],
 exp=('Profile thuyết phục khác profile đẹp',[('Viết cho người đọc','Đối tác cần năng lực và dự án tương tự; khách lẻ cần lợi ích. Một hồ sơ không nên nói với tất cả.'),('Bằng chứng cụ thể','Dự án, hình ảnh thật, giấy phép thật thay cho tính từ chung chung.'),('Hệ thống chữ & màu','Dùng nhất quán 1–2 font, bảng màu thương hiệu, khoảng trắng đủ để dễ đọc.'),('Hai bản xuất','PDF nén cho màn hình và bản in có lề xén, hệ màu phù hợp nhà in.')]),
 deliv=['File PDF để gửi qua email','File in theo thông số nhà in','File thiết kế gốc để sửa sau này','Nội dung đã biên tập'],
 tech=['Figma','Canva','Adobe Illustrator','PDF'],
 fit=['Doanh nghiệp đi đấu thầu, chào hàng đối tác','Cần tài liệu giới thiệu thống nhất'],
 nofit=['Chưa có thông tin, dự án thật để đưa vào'],
 faq=[('Tôi chưa có nhiều dự án thì làm profile được không?','Được. Tập trung vào năng lực, quy trình, đội ngũ và cam kết làm việc; không nên thêm dự án không có thật.'),('Có làm bản tiếng Anh không?','Có thể, nội dung tiếng Anh được dịch và rà soát lại thuật ngữ. Phạm vi trao đổi trong báo giá.')],
 rel=['thiet-ke-website','video-ai','cham-soc-fanpage'])
S['zalo-oa-mini-app']=dict(
 vis=('phone',['Zalo OA','Tin nhắn chào','Menu nhanh','Mini App: đặt lịch'],'Màn hình điện thoại với Zalo OA và Mini App'),
 steps=[('Tư vấn mô hình','Chỉ cần OA để chăm sóc khách, hay cần thêm Mini App để đặt hàng, đặt lịch.'),('Tạo & xác thực OA','Đăng ký Official Account đứng tên doanh nghiệp, làm theo thủ tục xác thực của Zalo.'),('Thiết lập OA','Ảnh bìa, thông tin, menu, tin nhắn chào, trả lời tự động.'),('Xây Mini App','Thiết kế và lập trình các màn hình cần thiết, kết nối dữ liệu.'),('Kiểm duyệt & phát hành','Gửi Mini App để Zalo kiểm duyệt, chỉnh theo phản hồi rồi phát hành.')],
 exp=('Hiểu đúng Zalo OA và Mini App',[('OA là kênh, Mini App là công cụ','OA để nhắn tin, gửi thông báo; Mini App là ứng dụng nhỏ chạy trong Zalo, khách không cần cài thêm.'),('Tuân thủ chính sách gửi tin','Gửi tin cho khách bị giới hạn theo chính sách và gói của Zalo; không spam.'),('Kiểm duyệt của Zalo','Mini App phải qua kiểm duyệt trước khi phát hành; nội dung và quyền dữ liệu cần rõ ràng.'),('Dữ liệu khách hàng','Chỉ xin quyền thông tin thật sự cần, có chính sách quyền riêng tư.')]),
 deliv=['Zalo OA đứng tên doanh nghiệp','Menu, tin nhắn tự động đã thiết lập','Mini App (nếu có) và mã nguồn','Hướng dẫn quản trị OA'],
 tech=['Zalo OA','Zalo Mini App','JavaScript','React','API'],
 fit=['Khách hàng chủ yếu liên lạc qua Zalo','Cần đặt lịch, tích điểm, đặt hàng đơn giản ngay trong Zalo'],
 nofit=['Cần ứng dụng độc lập trên kho ứng dụng (xem Thiết kế App)'],
 faq=[('Có cần giấy phép kinh doanh để làm OA không?','Để xác thực OA doanh nghiệp, Zalo thường yêu cầu giấy tờ doanh nghiệp. Yêu cầu cụ thể theo chính sách hiện hành của Zalo.'),('Mini App khác app thường thế nào?','Mini App chạy bên trong Zalo nên khách không phải tải; đổi lại phải theo giới hạn và quy định của nền tảng Zalo.')],
 rel=['thiet-ke-app','cham-soc-fanpage','phan-mem-noi-bo'])
S['thiet-ke-app']=dict(
 vis=('phone',['Đăng nhập','Danh sách','Chi tiết','Thông báo'],'Bản phác các màn hình chính của một ứng dụng di động'),
 steps=[('Xác định phạm vi','Liệt kê chức năng bắt buộc cho phiên bản đầu (MVP), tách phần làm sau.'),('Luồng & wireframe','Vẽ luồng người dùng và khung từng màn hình, bấm thử được trên Figma.'),('Thiết kế UI','Giao diện theo hướng dẫn iOS/Android, kích thước chạm, chế độ tối nếu cần.'),('Lập trình','Phát triển ứng dụng và phần máy chủ (API, cơ sở dữ liệu).'),('Kiểm thử','Thử trên nhiều máy và kích thước màn hình, kiểm tra lỗi và bảo mật cơ bản.'),('Phát hành','Chuẩn bị hồ sơ và đưa lên App Store / Google Play bằng tài khoản của bạn.')],
 exp=('Chọn hướng làm app hợp lý',[('App, Web App hay Mini App?','Nếu không cần tính năng máy (camera, thông báo đẩy, chạy offline), web app hoặc Mini App có thể đủ và rẻ hơn.'),('Đa nền tảng','Một mã nguồn chạy cả iOS và Android giúp giảm chi phí cho đa số ứng dụng doanh nghiệp.'),('MVP trước','Ra phiên bản nhỏ, đo người dùng thật rồi mới mở rộng.'),('Kiểm duyệt cửa hàng','Apple và Google có quy định riêng; tài khoản nhà phát triển nên đứng tên bạn.')]),
 deliv=['Bản thiết kế Figma','Ứng dụng iOS / Android','Phần máy chủ và tài liệu API','Mã nguồn sau khi thanh toán đủ','Hỗ trợ đưa lên cửa hàng ứng dụng'],
 tech=['Figma','Flutter','React Native','Python','SQL','REST API','Firebase'],
 fit=['Doanh nghiệp có quy trình rõ, cần app cho khách hoặc nhân viên','Muốn bắt đầu bằng phiên bản nhỏ để thử thị trường'],
 nofit=['Ý tưởng chưa rõ người dùng là ai','Cần sản phẩm quy mô rất lớn ngay từ đầu'],
 faq=[('Có nên làm app ngay không?','Chưa chắc. Tôi sẽ hỏi khách dùng app để làm gì, bao lâu một lần; nhiều trường hợp web app hoặc Zalo Mini App đáp ứng đủ với chi phí thấp hơn.'),('Tài khoản App Store / Google Play đứng tên ai?','Nên đứng tên doanh nghiệp của bạn. Chủ app tự trả phí tài khoản nhà phát triển (Apple Developer, Google Play Console); My Agent hỗ trợ đăng ký và cấu hình.')],
 rel=['zalo-oa-mini-app','phan-mem-noi-bo','thiet-ke-website'])
S['phan-mem-noi-bo']=dict(
 vis=('arch',['Trình duyệt','Phân quyền','Nghiệp vụ','Cơ sở dữ liệu','Báo cáo'],'Kiến trúc phần mềm nội bộ: trình duyệt, phân quyền, nghiệp vụ, cơ sở dữ liệu, báo cáo'),
 steps=[('Khảo sát quy trình','Ngồi cùng người làm thật để hiểu bước nào đang tốn thời gian, sai sót.'),('Mô hình dữ liệu','Xác định đối tượng (khách, đơn, công việc...), quan hệ và quyền xem sửa.'),('Bản mẫu','Dựng màn hình mẫu để người dùng góp ý trước khi lập trình sâu.'),('Phát triển theo đợt','Làm từng nhóm chức năng, bàn giao dần để dùng thử sớm.'),('Chuyển dữ liệu & đào tạo','Nhập dữ liệu cũ từ Excel, hướng dẫn từng nhóm người dùng.'),('Vận hành','Sao lưu, theo dõi lỗi, chỉnh sửa theo phản hồi.')],
 exp=('Phần mềm nội bộ dùng được lâu',[('Theo quy trình thật','Phần mềm theo quy trình đang chạy, không bắt đội ngũ đổi cách làm chỉ để vừa phần mềm.'),('Phân quyền rõ','Ai xem, ai sửa, ai duyệt; lưu nhật ký thay đổi khi cần truy vết.'),('Dữ liệu thuộc về bạn','Cơ sở dữ liệu xuất được ra Excel/CSV, không khoá dữ liệu.'),('Bảo mật cơ bản','HTTPS, mật khẩu mã hoá, sao lưu, cập nhật thư viện định kỳ.')]),
 deliv=['Phần mềm web chạy trên trình duyệt','Phân quyền người dùng','Tài liệu hướng dẫn sử dụng','Mã nguồn và cơ sở dữ liệu sau khi thanh toán đủ'],
 tech=['Python','SQL','PostgreSQL','JavaScript','HTML/CSS','Nginx','Power BI'],
 fit=['Đang quản lý bằng nhiều file Excel rời rạc','Quy trình đặc thù, phần mềm có sẵn không vừa'],
 nofit=['Phần mềm đóng gói có sẵn đã đáp ứng đủ nhu cầu (tôi sẽ nói thẳng)'],
 faq=[('Khác gì so với thuê phần mềm có sẵn?','Phần mềm có sẵn triển khai nhanh nhưng phải theo cách của họ; phần mềm riêng theo đúng quy trình của bạn và bạn sở hữu dữ liệu, đổi lại cần thời gian xây dựng.'),('Dữ liệu Excel cũ có đưa vào được không?','Thường được. Tôi làm sạch và chuẩn hoá trước khi nhập để tránh trùng, sai.')],
 rel=['ky-thuat-du-lieu','phan-tich-du-lieu','thiet-ke-app'])
S['phan-tich-du-lieu']=dict(
 vis=('dash',['Doanh thu','Đơn hàng','Khách quay lại','Tồn kho'],'Mô phỏng dashboard với biểu đồ cột, đường và các chỉ số'),
 steps=[('Trao đổi mục tiêu','Chốt câu hỏi kinh doanh cần trả lời và chỉ số (KPI) dùng để đo.'),('Nhận dữ liệu','Nhận file mẫu, kiểm tra cột, định dạng, độ đầy đủ; ẩn thông tin cá nhân không cần.'),('Làm sạch','Xử lý trùng, thiếu, sai định dạng ngày/tiền; ghi lại mọi bước biến đổi.'),('Phân tích','So sánh theo thời gian, sản phẩm, kênh, nhóm khách; kiểm tra lại số với nguồn.'),('Dashboard','Dựng báo cáo một trang chính, lọc theo thời gian, chi nhánh, kênh.'),('Bàn giao & hướng dẫn','Giải thích từng chỉ số, cách làm mới dữ liệu và đề xuất hành động.')],
 exp=('Phân tích đúng trước khi vẽ đẹp',[('Định nghĩa chỉ số','"Doanh thu" tính trước hay sau giảm giá, hoàn hàng? Chốt định nghĩa trước để số không vênh.'),('Đối chiếu số liệu','Tổng trên dashboard phải khớp với phần mềm bán hàng; lệch là phải tìm nguyên nhân.'),('Ít biểu đồ, nhiều ý','Mỗi biểu đồ trả lời một câu hỏi; ưu tiên so sánh và xu hướng thay vì trang trí.'),('Insight kèm hành động','Mỗi phát hiện đi kèm việc có thể làm, mức độ chắc chắn và giới hạn của dữ liệu.')]),
 deliv=['Bộ dữ liệu đã làm sạch','Dashboard Power BI hoặc Excel / Google Sheets','Bảng định nghĩa chỉ số','Báo cáo insight và đề xuất','Hướng dẫn làm mới dữ liệu'],
 tech=['Python','pandas','SQL','Power BI','Excel','Google Sheets'],
 fit=['Có dữ liệu bán hàng, quảng cáo nhưng chưa biết đọc','Muốn báo cáo định kỳ thay cho tổng hợp tay'],
 nofit=['Chưa ghi chép dữ liệu gì (nên bắt đầu từ ghi chép chuẩn)','Cần mô hình dự báo phức tạp ở quy mô lớn'],
 faq=[('Dashboard và báo cáo Excel khác gì nhau?','Dashboard tương tác: lọc theo thời gian, chi nhánh, sản phẩm và làm mới khi có dữ liệu mới. Excel phù hợp khi báo cáo đơn giản, ít người xem.')],
 rel=['ky-thuat-du-lieu','phan-mem-noi-bo','quang-cao-google-facebook'])
S['ky-thuat-du-lieu']=dict(
 vis=('etl',['POS','Sheets','Ads','CRM'],'Đường ống dữ liệu: nhiều nguồn được trích xuất, biến đổi và nạp vào kho rồi tới báo cáo'),
 steps=[('Khảo sát nguồn dữ liệu','Liệt kê nguồn, cách lấy (API, file xuất, cơ sở dữ liệu), tần suất cập nhật.'),('Thiết kế kho','Mô hình bảng sự kiện – bảng danh mục, quy ước tên, khoá liên kết.'),('Xây đường ống','Viết bước trích xuất, biến đổi, nạp; lập lịch chạy tự động.'),('Kiểm tra chất lượng','Kiểm tra trùng, thiếu, số dòng, tổng tiền so với nguồn sau mỗi lần chạy.'),('Nối báo cáo','Kết nối Power BI hoặc Sheets vào kho dữ liệu đã chuẩn.'),('Bàn giao & vận hành','Tài liệu, cảnh báo khi lỗi, hướng dẫn thêm nguồn mới.')],
 exp=('Đường ống dữ liệu tin cậy',[('Chạy lại không nhân đôi','Đường ống được thiết kế để chạy lại an toàn (idempotent), không sinh dữ liệu trùng.'),('Kiểm tra sau mỗi lần nạp','So số dòng, tổng tiền với nguồn; lệch thì cảnh báo thay vì im lặng.'),('Quyền tối thiểu','Tài khoản kết nối chỉ có quyền đọc cần thiết; khoá API lưu an toàn, không nằm trong mã.'),('Tài liệu dòng dữ liệu','Ghi rõ mỗi cột đến từ đâu, biến đổi gì, để người sau bảo trì được.')]),
 deliv=['Kho dữ liệu tập trung','Đường ống tự động có lịch chạy','Kiểm tra chất lượng và cảnh báo lỗi','Tài liệu mô hình dữ liệu','Kết nối sẵn cho báo cáo'],
 tech=['Python','SQL','PostgreSQL','BigQuery','Google Sheets API','Power BI','cron'],
 fit=['Dữ liệu ở nhiều phần mềm, mất nhiều giờ chép tay','Báo cáo cần cập nhật tự động hằng ngày/tuần'],
 nofit=['Chỉ có một file Excel nhỏ (Data Analyst là đủ)'],
 faq=[('ETL và ELT khác gì?','ETL biến đổi dữ liệu trước khi nạp vào kho; ELT nạp dữ liệu thô rồi biến đổi trong kho bằng SQL. Tôi chọn theo nguồn, khối lượng và công cụ bạn dùng.')],
 rel=['phan-tich-du-lieu','phan-mem-noi-bo','hosting-seo'])
S['video-ai']=dict(
 vis=('timeline',['Hook','Nội dung chính','CTA'],'Dòng thời gian dựng video với các lớp hình, chữ, âm thanh'),
 steps=[('Brief','Mục đích video, nền tảng đăng, độ dài, thông điệp chính.'),('Kịch bản','Câu mở đầu giữ người xem, nội dung chính, lời kêu gọi hành động.'),('Tư liệu','Quay mới, dùng tư liệu có bản quyền hoặc tạo bằng AI; kiểm tra quyền sử dụng.'),('Dựng','Cắt nhịp, phụ đề, nhạc, chuyển cảnh, màu theo nhận diện.'),('Xuất đa khung hình','Bản 9:16, 1:1, 16:9 cho từng nền tảng.'),('Chỉnh sửa','Sửa theo góp ý trong số lần đã thống nhất.')],
 exp=('Video ngắn giữ được người xem',[('Vài giây đầu','Câu mở đầu phải nói ngay lợi ích hoặc vấn đề, vì người xem lướt rất nhanh.'),('Phụ đề luôn có','Nhiều người xem không bật tiếng; phụ đề rõ, không che nội dung chính.'),('Đúng khung từng nền tảng','Video dọc cho Reels/TikTok/Shorts, ngang cho YouTube và website.'),('AI có kiểm soát','Dùng AI tạo giọng, hình phải đúng bản quyền và không giả mạo người thật.')]),
 deliv=['Video hoàn chỉnh theo các tỉ lệ khung hình','Phụ đề tiếng Việt','File dự án / tư liệu theo thoả thuận','Ảnh bìa (thumbnail)'],
 tech=['CapCut','Adobe Premiere Pro','Công cụ AI tạo giọng đọc','Công cụ AI tạo hình ảnh','Canva'],
 fit=['Cần video ngắn cho fanpage, TikTok, quảng cáo','Có sẵn tư liệu thô cần dựng lại chuyên nghiệp'],
 nofit=['Phim quảng cáo cần đoàn quay lớn, diễn viên, bối cảnh chuyên nghiệp'],
 faq=[('Video AI có dùng được cho quảng cáo không?','Được, nếu tư liệu đúng bản quyền và tuân thủ chính sách nền tảng. Một số nền tảng yêu cầu ghi chú nội dung tạo bởi AI.'),('Tôi cần chuẩn bị gì?','Thông điệp chính, logo, tư liệu sẵn có (ảnh, video sản phẩm) và ví dụ video bạn thích.')],
 rel=['cham-soc-fanpage','quang-cao-google-facebook','profile-doanh-nghiep'])
S['traffic-user']=dict(
 vis=('flow',['Nội dung hữu ích','Kênh phân phối','Người đọc thật','Website','Đo bằng GA4'],'Luồng traffic thật từ nội dung qua kênh phân phối tới website và đo lường'),
 steps=[('Đánh giá mục tiêu','Cần traffic để làm gì: bán hàng, nhận diện hay thử nội dung; trang nào nhận traffic.'),('Kiểm tra trang đích','Tốc độ, nội dung, đường liên hệ; trang kém thì traffic không có giá trị.'),('Chọn kênh','Mạng xã hội, cộng đồng, email, quảng cáo có nhắm mục tiêu.'),('Triển khai','Đăng và phân phối nội dung, gắn UTM cho từng kênh.'),('Đo & lọc','Theo dõi thời gian ở lại, tương tác, chuyển đổi trong GA4; cắt kênh kém.')],
 exp=('Traffic có giá trị khác traffic ảo',[('Người thật, có nhu cầu','Chỉ lượt truy cập từ người quan tâm thật mới có thể thành khách hàng.'),('Không dùng bot','Traffic tự động, click ảo có thể làm sai số liệu, lãng phí ngân sách và gây rủi ro với Google.'),('Đo bằng hành vi','Nhìn thời gian tương tác, trang đã xem, chuyển đổi, không chỉ nhìn số lượt.'),('Gắn UTM','Biết chính xác kênh nào mang lại khách để dồn ngân sách đúng chỗ.')]),
 deliv=['Kế hoạch kênh phân phối','Liên kết có gắn UTM','Báo cáo traffic theo kênh từ GA4','Đề xuất cải thiện trang đích'],
 tech=['GA4','UTM','Google Search Console','Meta Business Suite'],
 fit=['Website mới cần người đọc đầu tiên','Muốn thử phản hồi của thị trường với nội dung'],
 nofit=['Muốn tăng số lượt ảo để "đẹp" số liệu hoặc mong lên top Google nhờ traffic ảo'],
 faq=[('Traffic có giúp lên top Google không?','Không có cách nào đảm bảo. Traffic thật giúp kiểm chứng nội dung và có thể tạo đơn hàng, nhưng thứ hạng chủ yếu dựa vào nội dung, kỹ thuật và uy tín website.')],
 rel=['seo-tong-the','quang-cao-google-facebook','phan-tich-du-lieu'])

# --- v0.9.6 on-page SEO (kế hoạch từ khóa Peter 28/10/2026) ---
# 'intro' = (kicker, tiêu đề H2, [đoạn văn], [gạch đầu dòng]) chèn đầu khối chuyên sâu.
# Giá/thời gian viết bằng chỗ giữ {gia:<dịch vụ>/<gói>} và {tg:<dịch vụ>/<gói>}, svc_deep.py điền từ data/pricing.json.
S['thiet-ke-website']['intro']=[('thiết kế theo yêu cầu','Thiết kế web chuyên nghiệp <span class="gt">theo&nbsp;yêu cầu</span>',[
 'Một website chuyên nghiệp không phải là website nhiều hiệu ứng, mà là website khách mở ra hiểu ngay bạn làm gì, tin được và liên hệ được. My Agent thiết kế web theo yêu cầu từng doanh nghiệp: cấu trúc trang theo hành trình khách hàng, giao diện theo nhận diện thương hiệu, tốc độ tải nhanh trên điện thoại và SEO nền tảng ngay từ đầu.',
 'Web mẫu thay logo và màu là xong; thiết kế theo yêu cầu bắt đầu từ việc hỏi: khách của bạn tìm gì, cần thấy gì để tin, và bạn muốn họ làm gì (gọi, nhắn Zalo, đặt hàng). Từ đó mới dựng bố cục, nội dung và tính năng. Mức tùy biến linh hoạt: không phải dự án nào cũng cần lập trình lại từ đầu.',
 'Cần hệ thống có đăng nhập, phân quyền, dashboard (web app)? Xem <a href="phan-mem-noi-bo.html">phần mềm nội bộ &amp; web app theo yêu cầu</a>. Muốn một đầu mối lo cả tên miền, email, marketing? Xem <a href="../index.html">thiết kế web trọn gói</a> và <a href="../combo.html">combo dịch vụ</a>.'],
 ['Responsive, ưu tiên điện thoại; ảnh nén, tải trễ ảnh ngoài màn hình','SEO nền tảng: title/meta riêng từng trang, 1 H1, sitemap, schema, URL dễ đọc','Nút gọi, Zalo, form rõ ràng; gắn Google Maps','Hướng dẫn sử dụng và cập nhật nội dung sau bàn giao'])]
S['thiet-ke-website']['faq']+= [
 ('Thiết kế web theo yêu cầu có đắt hơn web mẫu?','Thường cao hơn vì có phân tích và thiết kế riêng. Khoảng giá từng loại có trong bảng giá tham khảo trên trang, báo giá chính xác sau khi trao đổi.'),
 ('Tôi có tự sửa nội dung được không?','Website giới thiệu và website bán hàng có trang quản trị (CMS) và được hướng dẫn cách cập nhật.'),
 ('Ở tỉnh khác có làm được không?','Có. Toàn bộ quy trình làm online: trao đổi, xem bản thử, duyệt và bàn giao từ xa.')]
S['thiet-ke-app']['intro']=[('trọn gói','Thiết kế app trọn gói <span class="gt">iOS, Android</span>',[
 'Một ứng dụng đáng làm khi khách quay lại thường xuyên: đặt lịch, mua lại, tích điểm, theo dõi đơn. My Agent thiết kế app đa nền tảng (iOS + Android từ một mã nguồn), trọn gói từ phân tích tính năng, thiết kế giao diện, lập trình, trang quản trị đến hỗ trợ đưa lên store. Làm việc online từ TP.HCM, nhận khách toàn quốc.',
 'Trọn gói gồm: phân tích tính năng và luồng màn hình → thiết kế UI → lập trình đa nền tảng → trang quản trị → kiểm thử → hỗ trợ đưa lên App Store/Google Play (gói bán hàng/đặt lịch trở lên) → bàn giao, hướng dẫn.',
 'Khi nào nên làm web app thay vì app? Nếu người dùng chủ yếu là nhân viên nội bộ hoặc dùng trên máy tính, <a href="phan-mem-noi-bo.html">web app theo yêu cầu</a> thường nhanh và tiết kiệm hơn. Nếu chỉ cần kênh chăm sóc khách qua Zalo, cân nhắc <a href="zalo-oa-mini-app.html">Zalo Mini App</a>.'],[])]
S['thiet-ke-app']['faq']+= [
 ('Một app làm cho cả iOS và Android được không?','Được, dùng công nghệ đa nền tảng: một mã nguồn chạy trên cả iOS và Android.'),
 ('Làm app mất bao lâu?','Theo bảng giá tham khảo: app MVP khoảng {tg:thiet-ke-app/co-ban}, app tích hợp thanh toán/CRM khoảng {tg:thiet-ke-app/nang-cao}, tùy phạm vi.'),
 ('Ngoài TP.HCM có làm được không?','Có, làm việc online và nhận khách toàn quốc.')]
S['phan-mem-noi-bo']['intro']=[('web app theo yêu cầu','Thiết kế <span class="gt">web app theo&nbsp;yêu cầu</span>',[
 'Khi công việc nằm rải rác trong nhiều file Excel và nhóm Zalo, một web app làm đúng theo quy trình của bạn thường gọn hơn việc cố uốn mình theo phần mềm đóng gói. Web app chạy trên trình duyệt, dùng được trên máy tính và điện thoại, có đăng nhập và phân quyền cho từng người. My Agent nhận thiết kế web app theo yêu cầu cho doanh nghiệp tại TP.HCM và trên toàn quốc. Chúng tôi bắt đầu bằng việc tìm hiểu cách đội ngũ đang làm việc, sau đó mới vẽ màn hình và viết mã.'],[]),
 ('so sánh','Web app theo yêu cầu khác <span class="gt">website và app di&nbsp;động</span> thế nào?',[],[
  '<b>Website:</b> dùng để giới thiệu và bán hàng, ai cũng xem được (xem <a href="thiet-ke-website.html">thiết kế website</a>).',
  '<b>Web app / phần mềm nội bộ:</b> có tài khoản, phân quyền, dữ liệu riêng và màn hình thao tác nghiệp vụ.',
  '<b>App di động:</b> cài từ kho ứng dụng, hợp khi khách dùng hằng ngày trên điện thoại (xem <a href="thiet-ke-app.html">thiết kế app</a>).']),
 ('năng lực','Những loại web app <span class="gt">My Agent có thể&nbsp;làm</span>',['<small class="muted">Đây là các loại việc chúng tôi có năng lực thực hiện, không phải danh sách dự án đã làm.</small>'],[
  '<b>Dashboard quản trị và báo cáo.</b> Tổng hợp doanh thu, đơn hàng và công việc lên một màn hình, có lọc theo thời gian và chi nhánh. Kết hợp được với <a href="phan-tich-du-lieu.html">dịch vụ Phân tích dữ liệu</a>.',
  '<b>CRM và ERP nhỏ.</b> Quản lý khách hàng, lịch sử chăm sóc, báo giá, đơn hàng và tồn kho, theo đúng các bước doanh nghiệp đang làm.',
  '<b>Cổng khách hàng.</b> Khách đăng nhập để xem tiến độ, tài liệu, hóa đơn hoặc gửi yêu cầu, thay cho việc hỏi lại qua tin nhắn.',
  '<b>Quản lý công việc nội bộ.</b> Giao việc, duyệt đề xuất, chấm công đơn giản, theo dõi hạn chót và lưu nhật ký thao tác.',
  '<b>Biểu mẫu và quy trình duyệt.</b> Thay giấy tờ bằng biểu mẫu có nhiều bước duyệt và thông báo cho người liên quan.']),
 ('khi nào nên làm','Khi nào nên làm <span class="gt">web app&nbsp;riêng?</span>',[],[
  'Nên làm khi dữ liệu nằm trong nhiều file rời rạc, khi quy trình đặc thù mà phần mềm có sẵn không đáp ứng, hoặc khi cần phân quyền rõ ai xem, ai sửa, ai duyệt.',
  'Chưa nên làm khi phần mềm đóng gói đã đủ dùng. Trường hợp đó My Agent sẽ nói thẳng.',
  'Cần nối dữ liệu nhiều nguồn: <a href="ky-thuat-du-lieu.html">Data Engineer</a>; máy chủ: <a href="hosting-seo.html">hosting/VPS</a>; bắt đầu: <a href="../lien-he.html">liên hệ</a> hoặc xem <a href="../bang-gia.html#gia-phan-mem-noi-bo">bảng giá</a>.'])]
# Thẻ/mục có ý cam kết dữ liệu, mã nguồn: chờ Peter chốt chính sách bàn giao, tạm để trung tính / bỏ.
S['phan-mem-noi-bo']['exp'][1][2]=('Xuất dữ liệu','Hỗ trợ xuất báo cáo ra Excel/CSV để dùng tiếp.')
S['phan-mem-noi-bo']['deliv']=[x for x in S['phan-mem-noi-bo']['deliv'] if 'Mã nguồn' not in x]
# FAQ riêng thay toàn bộ FAQ của trang (kể cả FAQ chung); giá/thời gian điền từ pricing.json.
S['phan-mem-noi-bo']['faq_replace']=True
S['phan-mem-noi-bo']['faq']=[
 ('Web app khác phần mềm có sẵn ở điểm nào?','Phần mềm có sẵn triển khai nhanh nhưng bạn phải làm theo cách của nó. Web app theo yêu cầu được xây quanh quy trình đang chạy của bạn, đổi lại cần thời gian khảo sát và phát triển.'),
 ('Web app có dùng được trên điện thoại không?','Có. Giao diện được thiết kế responsive, dùng ngay trên trình duyệt của máy tính và điện thoại mà không cần cài đặt.'),
 ('Dữ liệu Excel cũ có đưa vào được không?','Thường là được. Dữ liệu được làm sạch và chuẩn hóa trước khi nhập để tránh trùng và sai.'),
 ('Có kết nối với phần mềm đang dùng không?','Tùy phần mềm đó có cung cấp API hoặc cách xuất/nhập dữ liệu hay không. Việc này được kiểm tra ở bước khảo sát, và nếu cần tích hợp lớn thì sẽ báo giá riêng.'),
 ('Mất bao lâu để triển khai?','Tùy số module. Theo bảng giá tham khảo, công cụ 1 module khoảng {tg:phan-mem-noi-bo/co-ban}, hệ thống 3–5 module khoảng {tg:phan-mem-noi-bo/tieu-chuan}, còn mini ERP khoảng {tg:phan-mem-noi-bo/nang-cao}. Mốc cụ thể được chốt sau khảo sát.'),
 ('Chi phí làm web app khoảng bao nhiêu?','Theo bảng giá tham khảo trên trang (chưa gồm VAT): {so:phan-mem-noi-bo/co-ban} cho công cụ 1 module, {so:phan-mem-noi-bo/tieu-chuan} cho hệ thống 3–5 module, và {so:phan-mem-noi-bo/nang-cao} cho mini ERP. Báo giá chính xác được gửi sau khi trao đổi phạm vi.'),
 ('Làm sao để bắt đầu?','Gọi hoặc nhắn Zalo 0328 439 972, hoặc gửi form ở trang Liên hệ. Hãy mô tả ngắn quy trình đang gặp khó, My Agent sẽ hẹn buổi trao đổi để làm rõ nhu cầu.')]

# --- v0.9.13 brief 03 (app 3A / web app 3B), Peter chốt 29/10: bảng giá lên đầu trang, stack chỉ ghi "công nghệ đa nền tảng" ---
TBL=('<div class="bg-sc" tabindex="0" role="region" aria-label="So sánh app, web app và Zalo Mini App, vuốt ngang nếu cần"><table class="bg-t"><thead><tr><th scope="col"></th><th scope="col">App di động</th><th scope="col">Web app</th><th scope="col">Zalo Mini App</th></tr></thead><tbody>'
 '<tr><th scope="row">Người dùng</th><td>Khách dùng thường xuyên trên điện thoại</td><td>Nhân viên, quản lý, khách đăng nhập trên máy tính hoặc điện thoại</td><td>Khách đang dùng Zalo</td></tr>'
 '<tr><th scope="row">Tính năng máy</th><td>Camera, thông báo đẩy, chạy offline</td><td>Hạn chế, chạy trên trình duyệt</td><td>Theo giới hạn của Zalo</td></tr>'
 '<tr><th scope="row">Giá tham khảo</th><td>Từ {so:thiet-ke-app/co-ban}</td><td>Từ {so:phan-mem-noi-bo/co-ban}</td><td>Từ {so:zalo-oa-mini-app/tieu-chuan} (bán hàng/đặt lịch)</td></tr>'
 '<tr><th scope="row">Thời gian</th><td>{tg:thiet-ke-app/co-ban} (MVP)</td><td>{tg:phan-mem-noi-bo/co-ban} (1 module)</td><td>{tg:zalo-oa-mini-app/tieu-chuan}</td></tr>'
 '</tbody></table></div>')
OWN_APP='Sau khi bàn giao, app là của khách: mã nguồn và dữ liệu thuộc về khách. Mã nguồn được giao sau khi thanh toán đủ, như ghi trong bảng giá.'
OWN_WA='Sau khi bàn giao, web app là của khách: mã nguồn và dữ liệu thuộc về khách. Mã nguồn được giao sau khi thanh toán đủ, như ghi trong bảng giá.'
S['thiet-ke-app']['top_price']=True
S['thiet-ke-app']['tech']=['Figma','Công nghệ đa nền tảng','Trang quản trị','API','Cơ sở dữ liệu']
S['thiet-ke-app']['deliv']=['Bản thiết kế Figma','Ứng dụng iOS / Android','Phần máy chủ và tài liệu','Mã nguồn sau khi thanh toán đủ','Tài khoản App Store / Google Play đứng tên bạn']
S['thiet-ke-app']['intro']=[
 ('nên làm app?','Có nên <span class="gt">làm app&nbsp;không?</span>',[
  'Nên làm app khi khách dùng thường xuyên (đặt lịch, mua lại, tích điểm, theo dõi đơn) hoặc khi cần tính năng của điện thoại như camera, thông báo đẩy, chạy offline. Nếu người dùng chủ yếu là nhân viên, hoặc khách chỉ dùng thỉnh thoảng, <a href="phan-mem-noi-bo.html">thiết kế web app theo yêu cầu</a> hoặc <a href="zalo-oa-mini-app.html">Zalo Mini App</a> thường nhanh và rẻ hơn.'],[]),
 ('trọn gói','Thiết kế app trọn gói <span class="gt">gồm&nbsp;gì</span>',[
  'My Agent thiết kế app bằng công nghệ đa nền tảng: một mã nguồn chạy cả iOS và Android. Peter làm trực tiếp, online từ TP.HCM, nhận khách toàn quốc. Phù hợp app MVP và app vừa, nhỏ; sàn nhiều người bán hay hệ thống rất lớn hiện chưa phù hợp.'],
  ['Phân tích tính năng và luồng màn hình','Thiết kế giao diện (UI)','Lập trình đa nền tảng','Trang quản trị','Kiểm thử trên nhiều máy','Đưa lên App Store / Google Play bằng tài khoản của bạn (gói bán hàng/đặt lịch trở lên)']),
 ('so sánh','App, web app hay <span class="gt">Zalo Mini&nbsp;App?</span>',[TBL,
  'Giá chưa bao gồm VAT. Chi tiết: <a href="phan-mem-noi-bo.html">thiết kế web app theo yêu cầu</a>, <a href="zalo-oa-mini-app.html">Zalo OA &amp; Mini App</a>, <a href="../bang-gia.html">bảng giá</a>.'],[]),
 ('ví dụ','Ví dụ loại app <span class="gt">làm&nbsp;được</span>',['<small class="muted">Đây là các loại việc có năng lực làm, chưa phải dự án khách.</small>'],[
  '<b>App đặt lịch:</b> spa, phòng khám, salon; khách chọn giờ, nhận nhắc lịch, chủ xem lịch trong trang quản trị.',
  '<b>App bán hàng:</b> danh mục, giỏ hàng, theo dõi đơn, thông báo khuyến mãi.',
  '<b>App tích điểm:</b> thẻ thành viên, điểm thưởng, ưu đãi cho khách quay lại.',
  '<b>Sản phẩm mẫu:</b> Hướng Nghiệp 360 là web app mẫu do Peter làm (mở lần đầu mất khoảng 30 giây). Xem tại <a href="../du-an.html">sản phẩm mẫu</a>.']),
 ('quyền sở hữu','Bàn giao &amp; <span class="gt">quyền sở&nbsp;hữu</span>',[OWN_APP],[
  'Bản thiết kế Figma, ứng dụng iOS/Android, phần máy chủ kèm tài liệu','Mã nguồn được giao sau khi thanh toán đủ','Tài khoản App Store / Google Play đứng tên bạn; chủ app tự trả phí tài khoản nhà phát triển'])]
S['thiet-ke-app']['faq_replace']=True
S['thiet-ke-app']['faq']=[
 ('Thiết kế app giá bao nhiêu?','Theo bảng giá tham khảo (chưa bao gồm VAT): app MVP ≤8 màn hình {so:thiet-ke-app/co-ban}, app bán hàng/đặt lịch ≤15 màn hình {so:thiet-ke-app/tieu-chuan}, app tích hợp thanh toán/CRM {so:thiet-ke-app/nang-cao}. Báo giá chính xác sau khi phân tích tính năng.'),
 ('Làm app mất bao lâu?','Theo bảng giá tham khảo: app MVP {tg:thiet-ke-app/co-ban}, app bán hàng/đặt lịch {tg:thiet-ke-app/tieu-chuan}, app tích hợp thanh toán/CRM {tg:thiet-ke-app/nang-cao}. Mốc cụ thể được chốt sau khi thống nhất phạm vi.'),
 ('Một app chạy cả iOS và Android được không?','Được. App dùng công nghệ đa nền tảng: một mã nguồn chạy trên cả iOS và Android, giúp giảm chi phí so với làm hai app riêng.'),
 ('Tài khoản App Store / Google Play đứng tên ai?','Nên đứng tên doanh nghiệp của bạn. Chủ app tự trả phí tài khoản nhà phát triển (Apple Developer, Google Play Console); My Agent hỗ trợ đăng ký và cấu hình.'),
 ('Nên làm app hay web app?','Làm app khi khách dùng thường xuyên trên điện thoại hoặc cần camera, thông báo đẩy, chạy offline. Nếu người dùng chủ yếu là nhân viên hoặc dùng trên máy tính, web app thường nhanh và rẻ hơn.'),
 ('Làm MVP là gì?','MVP là phiên bản đầu chỉ gồm các chức năng bắt buộc, để đưa cho người dùng thật dùng thử rồi mới mở rộng. Cách này giúp giảm chi phí và rủi ro ban đầu.'),
 ('Sau bàn giao ai sở hữu app?',OWN_APP),
 ('Thanh toán thế nào?','Có hợp đồng bằng văn bản. Đặt cọc 30–50%, phần còn lại thanh toán sau khi ký biên bản nghiệm thu. Bảo hành lỗi kỹ thuật 60 ngày. Giá chưa bao gồm VAT.')]
S['phan-mem-noi-bo']['top_price']=True
S['phan-mem-noi-bo']['tech']=['Công nghệ đa nền tảng','Cơ sở dữ liệu','Phân quyền','Sao lưu','Xuất Excel/CSV']
S['phan-mem-noi-bo']['deliv']=['Phần mềm web chạy trên trình duyệt','Phân quyền người dùng','Tài liệu hướng dẫn sử dụng','Mã nguồn sau khi thanh toán đủ; dữ liệu thuộc về bạn']
_i=S['phan-mem-noi-bo']['intro']
_i[0]=('web app là gì?','Web app theo yêu cầu <span class="gt">là&nbsp;gì?</span>',[
 'Web app là phần mềm chạy trên trình duyệt, có đăng nhập, phân quyền và dữ liệu riêng, dùng được trên máy tính và điện thoại mà không cần cài đặt. Khi công việc nằm rải rác trong nhiều file Excel và nhóm Zalo, một web app làm đúng quy trình của bạn thường gọn hơn việc cố uốn mình theo phần mềm đóng gói.'],[])
_i[1]=('so sánh',_i[1][1],_i[1][2],_i[1][3]+['Cần chọn giữa app, web app hay Zalo Mini App? Xem bảng so sánh ở trang <a href="thiet-ke-app.html">thiết kế app di động</a>.'])
S['phan-mem-noi-bo']['intro']=_i[:3]+[
 ('ví dụ minh hoạ','Ví dụ: <span class="gt">XN Linh Kiện Máy&nbsp;In</span>',[
  'Bản demo web app quản lý xưởng gia công linh kiện máy in: tổng quan sản lượng, lệnh sản xuất dạng Kanban, kho, QC, báo giá và công nợ. Đây là <b>sản phẩm mẫu, toàn bộ là dữ liệu mẫu</b>, không phải dự án khách. Xem <a href="https://xnlinhkien.myagentvn.com" target="_blank" rel="noopener">bản demo</a> hoặc <a href="../du-an.html">các sản phẩm mẫu</a>.'],[]),
 ('khi nào nên làm','Khi nào nên, <span class="gt">chưa nên&nbsp;làm?</span>',[],[
  'Nên làm khi dữ liệu nằm trong nhiều file rời rạc, quy trình đặc thù mà phần mềm có sẵn không đáp ứng, hoặc cần phân quyền rõ ai xem, ai sửa, ai duyệt.',
  '<b>Nếu phần mềm đóng gói đủ dùng, tôi nói thẳng</b>: bạn không cần làm riêng.',
  'Phù hợp với 1 module đến 5 module hoặc mini ERP; hệ thống rất lớn hiện chưa phù hợp.',
  'Cần dashboard Power BI riêng: <a href="phan-tich-du-lieu.html">phân tích dữ liệu</a>; nối dữ liệu nhiều nguồn: <a href="ky-thuat-du-lieu.html">Data Engineer</a>; máy chủ: <a href="hosting-seo.html">hosting/VPS</a>.']),
 ('bảo mật','Bảo mật <span class="gt">&amp; dữ&nbsp;liệu</span>',[
  'Peter có nền tảng phân tích dữ liệu và an ninh mạng cơ bản, nên web app được làm với các biện pháp bảo vệ cơ bản sau. Các biện pháp này giúp giảm rủi ro, không loại bỏ hoàn toàn.'],[
  'HTTPS cho mọi kết nối','Mật khẩu được mã hoá, không lưu dạng đọc được','Phân quyền theo vai trò và nhật ký thao tác','Sao lưu định kỳ','Xuất dữ liệu ra Excel/CSV bất cứ lúc nào', OWN_WA])]
S['phan-mem-noi-bo']['faq']=[
 ('Web app là gì?','Web app là phần mềm chạy trên trình duyệt, có đăng nhập, phân quyền và dữ liệu riêng, dùng trên máy tính và điện thoại mà không cần cài đặt.'),
 ('Làm phần mềm quản lý theo yêu cầu giá bao nhiêu?','Theo bảng giá tham khảo (chưa bao gồm VAT): {so:phan-mem-noi-bo/co-ban} cho công cụ 1 module, {so:phan-mem-noi-bo/tieu-chuan} cho hệ thống 3–5 module, {so:phan-mem-noi-bo/nang-cao} cho mini ERP. Báo giá chính xác sau khi tìm hiểu quy trình.'),
 ('Có nên thay Excel bằng web app?','Nên khi nhiều người cùng sửa một file, dữ liệu hay trùng hoặc sai, hoặc cần phân quyền và báo cáo tự động. Nếu chỉ một hai người dùng và Excel vẫn đủ, chưa cần làm.'),
 ('Có dùng được trên điện thoại không?','Có. Giao diện responsive, dùng ngay trên trình duyệt của máy tính và điện thoại mà không cần cài đặt.'),
 ('Dữ liệu có xuất ra Excel được không?','Được. Dữ liệu xuất ra Excel/CSV bất cứ lúc nào; dữ liệu Excel cũ cũng được làm sạch và nhập vào khi bắt đầu.'),
 ('Mất bao lâu?','Theo bảng giá tham khảo: công cụ 1 module {tg:phan-mem-noi-bo/co-ban}, hệ thống 3–5 module {tg:phan-mem-noi-bo/tieu-chuan}, mini ERP {tg:phan-mem-noi-bo/nang-cao}. Mốc cụ thể được chốt sau khảo sát.'),
 ('Có kết nối với phần mềm đang dùng không?','Tùy phần mềm đó có API hoặc cách xuất/nhập dữ liệu hay không. Việc này được kiểm tra khi khảo sát; tích hợp lớn sẽ báo giá riêng.'),
 ('Sau bàn giao ai sở hữu web app?',OWN_WA),
 ('Làm sao để bắt đầu?','Gửi mô tả quy trình hiện tại qua form ở trang Liên hệ, hoặc gọi/nhắn Zalo 0328 439 972 để đặt 15 phút tư vấn.')]

# --- v0.9.15 brief 02: thiết kế web theo yêu cầu (không "trọn gói" ở title/H1/meta), bảng giá lên đầu trang ---
TBL_W=('<div class="bg-sc" tabindex="0" role="region" aria-label="So sánh web mẫu, web theo yêu cầu và trọn gói, vuốt ngang nếu cần"><table class="bg-t"><thead><tr><th scope="col"></th><th scope="col">Web mẫu (template)</th><th scope="col">Theo yêu cầu</th><th scope="col">Trọn gói</th></tr></thead><tbody>'
 '<tr><th scope="row">Là gì</th><td>Chọn giao diện có sẵn, thay logo, màu, nội dung</td><td>Bố cục và giao diện dựng riêng theo khách hàng, ngành và thương hiệu</td><td>Cách làm dịch vụ: một đầu mối lo từ đầu đến cuối, có thể dùng web mẫu hoặc theo yêu cầu</td></tr>'
 '<tr><th scope="row">Bắt đầu từ</th><td>Giao diện</td><td>Brief và wireframe</td><td>Phạm vi gói</td></tr>'
 '<tr><th scope="row">Hợp khi</th><td>Cần nhanh, nội dung đơn giản</td><td>Đã có thương hiệu, quy trình bán hàng hoặc tính năng đặc thù</td><td>Muốn ít đầu việc phải tự lo</td></tr>'
 '<tr><th scope="row">Xem thêm</th><td colspan="3"><a href="../index.html">Thiết kế web trọn gói</a> · <a href="../bang-gia.html#gia-thiet-ke-website">bảng giá</a></td></tr>'
 '</tbody></table></div>')
OWN_W='Sau khi bàn giao, website là của khách: mã nguồn và dữ liệu thuộc về khách. Mã nguồn được giao sau khi thanh toán đủ, như ghi trong bảng giá.'
W=S['thiet-ke-website']
W['top_price']=True
W['faq_replace']=True
W['tech']=['Figma (wireframe, giao diện)','WordPress hoặc code tay','Google Search Console','GA4']
W['deliv']=['Website chạy trên tên miền của bạn, có HTTPS','Giao diện máy tính và điện thoại','Sitemap, robots.txt, thẻ SEO từng trang','Form liên hệ gửi về email của bạn','Hướng dẫn cập nhật nội dung','Mã nguồn sau khi thanh toán đủ; 2 lần chỉnh sửa trong phạm vi; bảo hành lỗi kỹ thuật 60 ngày']
W['exp']=('Một website chuyên nghiệp cần gì',S['thiet-ke-website']['exp'][1])
W['intro']=[
 ('là gì?','Thiết kế web theo yêu cầu <span class="gt">là&nbsp;gì?</span>',[
  'Thiết kế web theo yêu cầu là làm website bắt đầu từ khách của bạn: họ tìm gì, cần thấy gì để tin, và bạn muốn họ làm gì (gọi, nhắn Zalo, đặt hàng). Trả lời xong ba câu đó mới dựng bố cục, nội dung, rồi mới đến giao diện theo nhận diện thương hiệu và tính năng cần thiết.',
  'Peter làm trực tiếp từ wireframe đến lúc đưa web lên mạng, làm việc online từ TP.HCM và nhận khách toàn quốc.'],[]),
 ('so sánh','Theo yêu cầu khác <span class="gt">web mẫu và trọn gói</span> thế nào?',[TBL_W,
  'Đọc thêm: <a href="../blog/web-template-hay-web-theo-yeu-cau.html">web template hay web theo yêu cầu</a> và <a href="../blog/thiet-ke-web-tron-goi-gom-nhung-gi.html">thiết kế web trọn gói gồm những gì</a>.'],[]),
 ('mức tùy biến','Mức tùy biến linh hoạt: <span class="gt">không phải dự án nào cũng lập trình từ&nbsp;đầu</span>',[
  'Theo yêu cầu nghĩa là bố cục, nội dung và trải nghiệm được làm riêng, không có nghĩa mọi dòng mã đều viết mới. Tùy cách bạn dùng web, có hai mức chính:'],[
  '<b>Tùy biến giao diện trên WordPress:</b> hợp khi bạn tự đăng bài, sản phẩm thường xuyên; giao diện vẫn được thiết kế theo thương hiệu và hành trình khách.',
  '<b>Code tay (HTML/CSS/JS):</b> nhẹ, tải nhanh, ít phụ thuộc plugin; hợp với web giới thiệu ít thay đổi hoặc landing page cần tốc độ.',
  ]),
 ('chuyên nghiệp','Một website chuyên nghiệp <span class="gt">cần&nbsp;gì?</span>',[
  'Tốc độ, responsive, SEO kỹ thuật, bảo mật cơ bản và khả năng tiếp cận được làm ngay từ đầu, chi tiết ở phần góc nhìn chuyên môn bên dưới và bài <a href="../blog/website-chuyen-nghiep-can-gi.html">website chuyên nghiệp cần gì</a>.'],[]),
 ('phần theo yêu cầu','Bước 1–2 là phần <span class="gt">“theo yêu cầu”</span>',[
  'Trong quy trình 6 bước bên dưới, brief và wireframe quyết định web có khác web mẫu hay không: thống nhất mục tiêu, khách chính, rồi duyệt sơ đồ trang trước khi vẽ giao diện, khi sửa còn rẻ. Mỗi dự án có hợp đồng và biên bản nghiệm thu bằng văn bản.'],[]),
 ('sản phẩm mẫu','Sản phẩm <span class="gt">mẫu</span>',['<small class="muted">Đây là sản phẩm mẫu do Peter làm để minh họa năng lực, dùng dữ liệu mẫu, không phải dự án khách.</small>'],[
  '<b>NhàĐất Việt (sản phẩm mẫu):</b> website bất động sản có tìm kiếm, bộ lọc và so sánh tin đăng.',
  '<b>NHỊP (sản phẩm mẫu):</b> website bán hàng có danh mục, giỏ hàng và đặt hàng.',
  'Xem tất cả tại <a href="../du-an.html">sản phẩm mẫu</a>.']),
 ('web app?','Cần đăng nhập, phân quyền, <span class="gt">dashboard?</span>',[
  'Khi web cần tài khoản người dùng, phân quyền, báo cáo hay quy trình duyệt, đó là web app chứ không còn là website giới thiệu. Xem <a href="phan-mem-noi-bo.html">web app theo yêu cầu</a>.'],[])]
W['faq']=[
 ('Thiết kế web theo yêu cầu là gì?','Là làm website bắt đầu từ khách của bạn: họ tìm gì, cần thấy gì để tin và bạn muốn họ làm gì. Từ đó mới dựng bố cục, nội dung, giao diện theo thương hiệu và tính năng, thay vì chọn một giao diện có sẵn rồi thay chữ.'),
 ('Thiết kế web theo yêu cầu có đắt hơn web mẫu không?','Thường cao hơn web mẫu vì có phân tích và thiết kế riêng. Theo bảng giá tham khảo (chưa bao gồm VAT): landing page {so:thiet-ke-website/landing}, website giới thiệu {so:thiet-ke-website/gioi-thieu}, website bán hàng {so:thiet-ke-website/ban-hang}; mỗi trang thêm {pq:thiet-ke-website/x}.'),
 ('Có phải code từ đầu không?','Không phải dự án nào cũng lập trình lại từ đầu. Có thể tùy biến giao diện trên WordPress hoặc code tay HTML/CSS/JS; mức nào phù hợp được chọn theo cách bạn dùng và cập nhật web.'),
 ('Nên làm web bằng WordPress hay code tay?','WordPress hợp khi bạn tự đăng bài, sản phẩm thường xuyên. Code tay nhẹ, tải nhanh và ít phụ thuộc plugin, hợp với web giới thiệu ít thay đổi. Lựa chọn được tư vấn dựa trên cách bạn sẽ dùng web.'),
 ('Tôi có tự sửa nội dung được không?','Được. Website giới thiệu và website bán hàng có trang quản trị (CMS), và bạn được hướng dẫn cách cập nhật nội dung, hình ảnh, sản phẩm sau bàn giao.'),
 ('Cần chuẩn bị gì trước khi làm web theo yêu cầu?','Ngành và sản phẩm chính, khách hàng chính của bạn, hành động muốn khách làm, logo và màu thương hiệu nếu có, cùng 3 website bạn thích và lý do.'),
 ('Website mới có lên Google ngay không?','Không ngay: Google cần thời gian lập chỉ mục, sitemap được gửi qua Search Console. Thứ hạng phụ thuộc nội dung và mức cạnh tranh, My Agent không hứa thứ hạng.'),
 ('Bao lâu thì xong?','Theo bảng giá tham khảo: landing page {tg:thiet-ke-website/landing}, website giới thiệu {tg:thiet-ke-website/gioi-thieu}, website bán hàng {tg:thiet-ke-website/ban-hang}, tính từ khi chốt nội dung và nhận đủ tư liệu.'),
 ('Sau bàn giao ai sở hữu website?',OWN_W),
 ('Thanh toán thế nào?','Có hợp đồng bằng văn bản. Đặt cọc 30–50%, phần còn lại thanh toán sau khi ký biên bản nghiệm thu. Có 2 lần chỉnh sửa trong phạm vi và bảo hành lỗi kỹ thuật 60 ngày. Giá chưa bao gồm VAT.')]
