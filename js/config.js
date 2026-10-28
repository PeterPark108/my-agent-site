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
   gaId      : Google Analytics 4 Measurement ID (vd G-ABC123XYZ). Để '' = tắt. Khách có thể tự tắt đo lường tại chinh-sach-bao-mat.html (lưu localStorage 'myagent_ga_off'); tôn trọng Do Not Track / Global Privacy Control. */
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
  gaId: 'G-BZ5E2WMZLJ'
};
/* GA4 (v0.9.10): nguồn tải duy nhất cho mọi trang (tech_pass chèn config.js vào <head>). Tải async, không chặn hiển thị.
   Ẩn danh IP, tắt Google signals và cá nhân hoá quảng cáo; không tải nếu khách bật DNT/GPC hoặc đã chọn tắt. */
(function(c,w,d){var id=c.gaId,K='myagent_ga_off';if(!/^G-[A-Z0-9]{4,}$/.test(id)||id==='G-XXXXXXXXXX')return;
function off(){try{return localStorage.getItem(K)==='1'}catch(e){return false}}
var n=w.navigator||{},dnt=n.doNotTrack==='1'||w.doNotTrack==='1'||n.msDoNotTrack==='1'||n.globalPrivacyControl===true;
w.MYAGENT_GA={id:id,blocked:dnt,optedOut:off(),set:function(v){try{v?localStorage.setItem(K,'1'):localStorage.removeItem(K)}catch(e){}w['ga-disable-'+id]=!!v}};
if(dnt||off()){w['ga-disable-'+id]=true;return}
if(w.__myagentGa)return;w.__myagentGa=1;
w.dataLayer=w.dataLayer||[];w.gtag=function(){dataLayer.push(arguments)};
gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'granted'});
gtag('js',new Date());gtag('config',id,{anonymize_ip:true,allow_google_signals:false,allow_ad_personalization_signals:false});
var s=d.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+id;(d.head||d.documentElement).appendChild(s);
})(window.MYAGENT_CONFIG,window,document);
/* Nút bật/tắt đo lường trên trang chính sách bảo mật: <button data-ga-toggle> + <span data-ga-state> */
document.addEventListener('DOMContentLoaded',function(){var g=window.MYAGENT_GA,b=document.querySelector('[data-ga-toggle]'),st=document.querySelector('[data-ga-state]');if(!b||!g)return;
function r(){var o=g.blocked||g.optedOut;if(st)st.textContent=g.blocked?'Đang tắt (trình duyệt bật Do Not Track / Global Privacy Control).':(o?'Đang tắt trên trình duyệt này.':'Đang bật (ẩn danh).');b.textContent=g.optedOut?'Bật lại đo lường':'Tắt đo lường trên trình duyệt này';b.hidden=g.blocked}
b.addEventListener('click',function(){g.optedOut=!g.optedOut;g.set(g.optedOut);r()});r()});
