/* ==== CẤU HÌNH WEBSITE MY AGENT — chỉ cần sửa ở đây ====
   siteUrl   : địa chỉ gốc của web (đổi bằng scripts/set-domain.sh <tên-miền>)
   formEmail : email nhận form liên hệ (FormSubmit.co). Lần gửi đầu tiên FormSubmit gửi mail kích hoạt -> bấm "Activate".
   zaloPhone : số Zalo, chỉ chữ số, vd 0901234567
   gaId      : Google Analytics 4 Measurement ID (vd G-ABC123XYZ). Để 'G-XXXXXXXXXX' = tắt. */
window.MYAGENT_CONFIG = {
  siteUrl: 'https://myagentvn.com/',
  formEmail: 'vantungn044@gmail.com',
  zaloPhone: 'PHONE_HERE',
  gaId: 'G-XXXXXXXXXX'
};
/* GA4: chỉ tải khi gaId hợp lệ. Lưu ý: nếu nhắm khách EU/cần tuân thủ dữ liệu cá nhân (NĐ 13/2023), nên thêm banner đồng ý cookie trước khi bật. */
(function(c){var id=c.gaId;if(!/^G-[A-Z0-9]{4,}$/.test(id)||id==='G-XXXXXXXXXX')return;
var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+id;document.head.appendChild(s);
window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',id,{anonymize_ip:true});})(window.MYAGENT_CONFIG);
