/* ==== CẤU HÌNH WEBSITE MY AGENT — chỉ cần sửa ở đây ====
   siteUrl   : địa chỉ gốc của web (đổi bằng scripts/set-domain.sh <tên-miền>)
   formEmail : email nhận form liên hệ; dùng cho nút "Gửi qua Email" (mailto) khi form lỗi, và cho FormSubmit.co nếu chưa có formEndpoint.
   formEndpoint: máy chủ nhận form trên VPS ('/api/contact', POST JSON -> Telegram của Peter). Chỉ báo "Đã gửi" khi trả JSON {ok:true}; mọi trường hợp khác -> 3 nút dự phòng Email/Zalo/Gọi. Xem docs/lien-he-form.md
   formSubmitEnabled: true = dùng FormSubmit.co (chỉ khi formEndpoint = ''). Mặc định false = không gọi FormSubmit.
   formTimeoutMs: thời gian chờ tối đa khi gửi form (5000 = 5 giây).
   zaloPhone : số Zalo, chỉ chữ số, vd 0901234567
   motionEnabled: true = bật hiệu ứng chuyển động toàn site, false = tắt (hoặc thêm ?motion=0 vào link). Xem docs/animation.md
   introEnabled: true = bật màn intro trang chủ (mỗi phiên 1 lần), false = tắt. Xem docs/intro.md
   chatbotEnabled: true = bật trợ lý MJ (góc dưới trái), false = tắt (hoặc ?chat=0). Xem docs/chatbot.md
   gaId      : Google Analytics 4 Measurement ID (vd G-ABC123XYZ). Để 'G-XXXXXXXXXX' = tắt. */
window.MYAGENT_CONFIG = {
  siteUrl: 'https://myagentvn.com/',
  formEmail: 'vantungn044@gmail.com',
  zaloPhone: '0328439972',
  formEndpoint: '/api/contact',
  formSubmitEnabled: false,
  formTimeoutMs: 5000,
  introEnabled: true,
  motionEnabled: true,
  chatbotEnabled: true,
  gaId: 'G-XXXXXXXXXX'
};
/* GA4: chỉ tải khi gaId hợp lệ. Lưu ý: nếu nhắm khách EU/cần tuân thủ dữ liệu cá nhân (NĐ 13/2023), nên thêm banner đồng ý cookie trước khi bật. */
(function(c){var id=c.gaId;if(!/^G-[A-Z0-9]{4,}$/.test(id)||id==='G-XXXXXXXXXX')return;
var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+id;document.head.appendChild(s);
window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',id,{anonymize_ip:true});})(window.MYAGENT_CONFIG);
