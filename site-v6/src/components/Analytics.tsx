import Script from 'next/script';

// The owner supplied GTM-KBZK7NMC. Its published configuration points to
// G-2J09FVVE0E. Load the container once; do not add a second GA config/page_view.
// Ads/user-provided data remain denied; honour the site's existing opt-out.
const bootstrap = `(function(w,d){
if(!/^(www\\.)?myagentvn\\.com$/.test(w.location.hostname)||w.__myagentGtm)return;
var id='G-2J09FVVE0E',key='myagent_ga_off',n=w.navigator||{},off=false;
try{off=w.localStorage.getItem(key)==='1'}catch(e){}
var blocked=n.doNotTrack==='1'||w.doNotTrack==='1'||n.msDoNotTrack==='1'||n.globalPrivacyControl===true;
w.MYAGENT_GA={id:id,blocked:blocked,optedOut:off,set:function(value){
try{value?w.localStorage.setItem(key,'1'):w.localStorage.removeItem(key)}catch(e){}
w['ga-disable-'+id]=!!value;
if(value&&w.gtag)w.gtag('consent','update',{analytics_storage:'denied'});
if(!value)w.location.reload();
}};
function controls(){var b=d.querySelector('[data-ga-toggle]'),s=d.querySelector('[data-ga-state]');if(!b)return;
function render(){b.hidden=blocked;b.textContent=w.MYAGENT_GA.optedOut?'Bật lại đo lường':'Tắt đo lường trên trình duyệt này';if(s)s.textContent=blocked?'Đang tắt theo lựa chọn riêng tư của trình duyệt.':(w.MYAGENT_GA.optedOut?'Đang tắt trên trình duyệt này.':'Đang bật đo lường lượt truy cập.');}
if(!b.dataset.gaBound){b.dataset.gaBound='1';b.addEventListener('click',function(){w.MYAGENT_GA.optedOut=!w.MYAGENT_GA.optedOut;w.MYAGENT_GA.set(w.MYAGENT_GA.optedOut);render();});}render();}
controls();d.addEventListener('DOMContentLoaded',controls,{once:true});
if(blocked||off){w['ga-disable-'+id]=true;return;}
w.__myagentGtm=true;w.dataLayer=w.dataLayer||[];
w.gtag=w.gtag||function(){w.dataLayer.push(arguments)};
w.gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'granted'});
w.gtag('set',{allow_google_signals:false,allow_ad_personalization_signals:false,ads_data_redaction:true,user_data:null});
w.dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});
var s=d.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtm.js?id=GTM-KBZK7NMC';d.head.appendChild(s);
})(window,document);`;

export function Analytics() {
  if (process.env.MYAGENT_LOCAL_QA === '1') return null;
  return <Script id="myagent-analytics" strategy="afterInteractive">{bootstrap}</Script>;
}
