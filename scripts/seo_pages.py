"""Dữ liệu SEO từng trang (title ≤60, description ≤155). Từ khóa chính đã chốt với Peter:
mỗi từ khóa chính chỉ gắn 1 trang. 'h1'/'lead' = (cũ, mới) chỉ khi cần đổi chữ (đã ghi trong báo cáo cho MJ duyệt).
'kw' = tên dịch vụ dùng cho Service schema."""
B=' | My Agent'
PAGES={
'index.html':dict(title='Thiết kế web trọn gói TP.HCM, chi phí hợp lý'+B,
  desc='Dịch vụ thiết kế web trọn gói tại TP.HCM: website, landing page, web bán hàng. Chi phí hợp lý, báo giá rõ ràng trước khi làm. Nhận khách toàn quốc.',
  lead=('My Agent thiết kế và làm website, landing page, web bán hàng','My Agent nhận thiết kế web trọn gói tại TP.HCM: website, landing page, web bán hàng')),
'dich-vu/thiet-ke-website.html':dict(title='Thiết kế web chuyên nghiệp theo yêu cầu'+B,kw='Thiết kế web chuyên nghiệp theo yêu cầu',
  desc='Thiết kế web chuyên nghiệp theo yêu cầu: website doanh nghiệp, bán hàng, landing page chuẩn SEO, responsive. Báo giá rõ theo phạm vi, nhận khách toàn quốc.',
  h1=('<h1 class="gt2">Thiết kế website chuẩn&nbsp;SEO</h1>','<h1 class="gt2">Thiết kế website chuyên nghiệp theo&nbsp;yêu cầu</h1>'),
  lead=('giữ chân khách và thúc đẩy mua hàng.</p>','giữ chân khách và thúc đẩy mua hàng. Nhận làm web doanh nghiệp, web bán hàng có quản lý đơn hàng, landing page và web cho shop/cá nhân, hiển thị tốt trên mọi thiết bị.</p>')),
'dich-vu.html':dict(title='Dịch vụ marketing online, dữ liệu và website'+B,
  desc='Danh sách dịch vụ My Agent: marketing online, SEO, quảng cáo, Data Analyst, Data Engineer, website, app. Phục vụ TP.HCM và khách toàn quốc.'),
'combo.html':dict(title='Combo website trọn gói và marketing'+B,kw='Combo website trọn gói và marketing',
  desc='Gộp website, tên miền, email doanh nghiệp và marketing thành combo. Giảm theo số dịch vụ, báo giá rõ từng hạng mục trước khi làm.'),
'du-an.html':dict(title='Dự án mẫu website và dữ liệu'+B,desc='Dự án mẫu của My Agent: website, landing page, web bán hàng và các dự án phân tích, kỹ thuật dữ liệu. Xem cách chúng tôi triển khai.'),
've-chung-toi.html':dict(title='Về My Agent – dịch vụ số tại TP.HCM'+B[:0]+' | My Agent',desc='Giới thiệu My Agent: đơn vị thiết kế website và dịch vụ số tại TP.HCM, làm việc minh bạch, báo giá rõ ràng trước khi làm, nhận khách toàn quốc.'),
'lien-he.html':dict(title='Liên hệ tư vấn, báo giá'+B,desc='Liên hệ My Agent qua form, Zalo hoặc email để được tư vấn và báo giá rõ ràng cho website, marketing online và dịch vụ dữ liệu.'),
'cong-cu.html':dict(title='Công cụ miễn phí cho website'+B,desc='Bộ công cụ miễn phí từ My Agent hỗ trợ chủ website và người làm marketing, dùng ngay trên trình duyệt, không cần cài đặt.'),
'chinh-sach-bao-mat.html':dict(title='Chính sách bảo mật thông tin khách hàng'+B,desc='Chính sách bảo mật của My Agent: cách chúng tôi thu thập, sử dụng và bảo vệ thông tin khi bạn liên hệ hoặc sử dụng dịch vụ.'),
'tin-tuc.html':dict(title='Tin tức công nghệ: AI, bảo mật, SEO'+B,desc='Tin công nghệ chọn lọc về AI, bảo mật, web & SEO, dữ liệu và Zalo, có link nguồn gốc và góc nhìn My Agent cho doanh nghiệp nhỏ, cập nhật thường xuyên.'),
'tai-nguyen-ai-agent.html':dict(title='Lộ trình học AI Agent: tài nguyên từ A đến Z'+B,desc='Tổng hợp tài nguyên học AI agent: video, GitHub, hướng dẫn, sách, bài nghiên cứu và khóa học, kèm mô tả tiếng Việt và link gốc tới từng nguồn.'),
'ghi-nguon.html':dict(title='Ghi nguồn và giấy phép'+B,desc='Ghi nguồn và giấy phép font, hình ảnh, biểu tượng được dùng trên website My Agent.'),
'tra-cuu-tien-do.html':dict(title='Tra cứu tiến độ đơn hàng'+B,desc='Khách hàng My Agent nhập mã đơn để xem tiến độ dự án.'),
}
SV={ # file: (từ khóa chính trong title, tên dịch vụ schema, câu desc)
'seo-tong-the':('Dịch vụ SEO tổng thể tại TP.HCM','SEO tổng thể','Dịch vụ SEO tổng thể tại TP.HCM: tối ưu kỹ thuật, nội dung, AI Content SEO cho website. Quy trình rõ ràng, báo cáo minh bạch, nhận khách toàn quốc.'),
'quang-cao-google-facebook':('Quảng cáo Google Ads, Facebook Ads','Quảng cáo Google Ads, Facebook Ads','Chạy quảng cáo Google Ads, Facebook Ads tại TP.HCM: nhắm đúng người đang có nhu cầu, tối ưu chi phí mỗi đơn. Báo giá rõ ràng, nhận khách toàn quốc.'),
'cham-soc-fanpage':('Dịch vụ chăm sóc Fanpage tại TP.HCM','Chăm sóc Fanpage','Dịch vụ chăm sóc Fanpage tại TP.HCM: nội dung đều đặn, tương tác tốt, khách hàng luôn nhớ tới bạn. Báo giá rõ ràng, nhận khách toàn quốc.'),
'cham-soc-website':('Dịch vụ chăm sóc website tại TP.HCM','Chăm sóc website','Dịch vụ chăm sóc website tại TP.HCM: cập nhật nội dung, sao lưu, vá bảo mật hằng tháng kèm báo cáo minh bạch. Nhận khách toàn quốc.'),
'email-doanh-nghiep':('Email doanh nghiệp theo tên miền tại HCM','Email doanh nghiệp','Email doanh nghiệp theo tên miền riêng tại TP.HCM: chống spam, tăng uy tín khi giao dịch. Hỗ trợ cài đặt, báo giá rõ ràng, nhận khách toàn quốc.'),
'google-maps':('Đăng ký Google Maps doanh nghiệp tại HCM','Đăng ký Google Maps doanh nghiệp','Đăng ký Google Maps doanh nghiệp tại TP.HCM: tạo, xác minh và tối ưu hồ sơ để khách quanh khu vực tìm là thấy. Báo giá rõ ràng.'),
'hosting-seo':('Hosting SEO tốc độ cao tại TP.HCM','Hosting SEO','Hosting SEO tốc độ cao: máy chủ riêng, SSD NVMe, sao lưu tự động, hỗ trợ kỹ thuật. Phục vụ khách TP.HCM và toàn quốc, báo giá rõ ràng.'),
'ten-mien':('Đăng ký tên miền .com, .vn tại TP.HCM','Đăng ký tên miền','Đăng ký tên miền .com, .net, .vn dễ nhớ, đứng tên chính doanh nghiệp. Hỗ trợ trỏ DNS, phục vụ khách TP.HCM và toàn quốc.'),
'thiet-ke-app':('Thiết kế app trọn gói iOS, Android tại TP.HCM','Thiết kế app trọn gói iOS, Android','Thiết kế app chuyên nghiệp, trọn gói iOS và Android: app bán hàng, đặt lịch, MVP. Báo giá theo số màn hình và tính năng, nhận khách toàn quốc.'),
'phan-mem-noi-bo':('Thiết kế web app, phần mềm nội bộ tại TP.HCM','Thiết kế web app và phần mềm nội bộ theo yêu cầu','Thiết kế web app theo yêu cầu: dashboard, CRM nhỏ, cổng khách hàng, phần mềm quản lý nội bộ chạy trên trình duyệt. Phân tích nghiệp vụ trước, báo giá rõ.'),
'phan-tich-du-lieu':('Data Analyst – phân tích dữ liệu HCM','Data Analyst - Phân tích dữ liệu','Dịch vụ Data Analyst tại TP.HCM: gom dữ liệu bán hàng, quảng cáo, tồn kho từ Excel và phần mềm thành báo cáo, dashboard dễ đọc. Báo giá rõ ràng.'),
'ky-thuat-du-lieu':('Data Engineer – kỹ thuật dữ liệu HCM','Data Engineer - Kỹ thuật dữ liệu','Dịch vụ Data Engineer tại TP.HCM: kết nối dữ liệu từ website, Google Sheets, quảng cáo, POS, CRM về một nơi, tự động cập nhật. Báo giá rõ ràng.'),
'profile-doanh-nghiep':('Thiết kế profile doanh nghiệp tại TP.HCM','Thiết kế profile doanh nghiệp','Thiết kế profile, hồ sơ năng lực doanh nghiệp chuyên nghiệp tại TP.HCM, gửi đi là tạo ấn tượng với đối tác. Báo giá rõ ràng.'),
'bo-cong-thuong':('Đăng ký website với Bộ Công Thương','Đăng ký website với Bộ Công Thương','Hỗ trợ thông báo, đăng ký website với Bộ Công Thương đúng quy định cho doanh nghiệp tại TP.HCM và toàn quốc. Báo giá rõ ràng.'),
'traffic-user':('Dịch vụ Traffic User cho website tại HCM','Traffic User','Dịch vụ Traffic User: lượt truy cập từ người dùng thật, hỗ trợ tín hiệu SEO cho website. Phục vụ khách TP.HCM và toàn quốc.'),
'video-ai':('Dịch vụ edit video, video AI tại TP.HCM','Edit Video - Video AI','Dịch vụ edit video, video AI tại TP.HCM: dựng video đủ khung hình cho mọi nền tảng. Báo giá rõ ràng, nhận khách toàn quốc.'),
'zalo-oa-mini-app':('Zalo OA, Zalo Mini App cho doanh nghiệp','Zalo OA - Mini App','Xây dựng Zalo Official Account và Zalo Mini App tương tác trực tiếp với khách hàng, cho doanh nghiệp tại TP.HCM và toàn quốc.'),
}
for k,(t,n,d) in SV.items(): PAGES[f'dich-vu/{k}.html']=dict(title=t+B,desc=d,kw=n)
PAGES['dich-vu/thiet-ke-app.html'].update(h1=('<h1 class="gt2">Thiết kế&nbsp;App</h1>','<h1 class="gt2">Thiết kế app trọn gói iOS, Android tại&nbsp;TP.HCM</h1>'),
  lead=('<p class="lead">Ứng dụng di động iOS/Android, máy tính bảng.</p>','<p class="lead">Thiết kế app chuyên nghiệp đa nền tảng iOS và Android: app bán hàng, đặt lịch, MVP, kèm trang quản trị. Nhận khách TP.HCM và toàn quốc.</p>'))
PAGES['dich-vu/phan-mem-noi-bo.html'].update(h1=('<h1 class="gt2">Phần mềm nội bộ&nbsp;Agency</h1>','<h1 class="gt2">Thiết kế web app &amp; phần mềm nội&nbsp;bộ</h1>'),
  lead=('<p class="lead">Phần mềm quản lý theo quy trình riêng, chạy trên trình duyệt.</p>','<p class="lead">Web app theo yêu cầu cho doanh nghiệp tại TP.HCM và toàn quốc: phần mềm quản lý nội bộ, dashboard, cổng khách hàng, chạy trên trình duyệt.</p>'))
PAGES['ve-chung-toi.html']['title']='Về My Agent – dịch vụ số tại TP.HCM'
if __name__=='__main__':
  for k,v in PAGES.items(): print(len(v['title']),len(v['desc']),k)
