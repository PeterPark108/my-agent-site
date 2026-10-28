/* My Agent — trợ lý MJ (chatbot chạy 100% trong trình duyệt, không gửi dữ liệu đi đâu).
   Nguồn trả lời: data/chatbot-kb.json (tạo bằng scripts/chatbot_build.py). Tắt: chatbotEnabled:false trong js/config.js hoặc ?chat=0. Xem docs/chatbot.md */
(function(){
var w=window,d=document,h=d.documentElement,C=w.MYAGENT_CONFIG||{},ss=w.sessionStorage;
var q=/[?&]chat=([01])/.exec(location.search);
if(q&&q[1]==='0'||(!q&&C.chatbotEnabled===false))return;
var sc=d.currentScript,B=sc?sc.src.replace(/js\/chat(\.min)?\.js.*$/,''):'';
var PH=(C.zaloPhone||'0328439972').replace(/\D/g,''),PHS=PH.replace(/(\d{4})(\d{3})(\d{3})/,'$1 $2 $3');
var K='mj_chat',st;try{st=JSON.parse(ss.getItem(K))||{}}catch(e){st={}}st.m=st.m||[];
function save(){try{ss.setItem(K,JSON.stringify(st))}catch(e){}}
var RM=w.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var AV='<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false"><path d="M50 14Q69.9 2 75.5 24.5Q98 30.1 86 50Q98 69.9 75.5 75.5Q69.9 98 50 86Q30.1 98 24.5 75.5Q2 69.9 14 50Q2 30.1 24.5 24.5Q30.1 2 50 14Z" fill="#E23636"/><path d="M50 14Q69.9 2 75.5 24.5Q98 30.1 86 50Q98 69.9 75.5 75.5Q69.9 98 50 86Q30.1 98 24.5 75.5Q2 69.9 14 50Q2 30.1 24.5 24.5Q30.1 2 50 14Z" fill="url(#mjg)"/><defs><radialGradient id="mjg" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#FF5A66"/><stop offset=".6" stop-color="#E23636" stop-opacity=".2"/><stop offset="1" stop-color="#B71E2A"/></radialGradient></defs><g class="mj-ey" fill="#fff"><ellipse cx="39" cy="46" rx="4.2" ry="5.4"/><ellipse cx="61" cy="46" rx="4.2" ry="5.4"/></g><path d="M40 60q10 9 20 0" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/></svg>';
function el(t,c,x){var e=d.createElement(t);if(c)e.className=c;if(x!=null)e.innerHTML=x;return e}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
/* ---------- tìm kiếm ---------- */
function nz(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/[^a-z0-9]+/g,' ').trim()}
var STOP=' la va cua cho co khong ko k the nao gi toi minh ban em anh chi a o thi de duoc nhu voi mot nhung cac can muon hoi cho biet ve this lam sao ra sao vay nhe a oi duoc khong hom nay gio dang tui may '.split(' ').reduce(function(o,x){o[x]=1;return o},{});
var SYN={web:'website',webs:'website',site:'website',trang:'website',app:'ung dung',gia:'bang gia bao gia chi phi',tien:'chi phi gia',seo:'seo google top',ads:'quang cao',qc:'quang cao',fb:'facebook fanpage',face:'facebook',fanpage:'facebook fanpage',map:'google maps',maps:'google maps',ten:'ten mien',domain:'ten mien',hosting:'hosting may chu',mail:'email',gmail:'email',sdt:'dien thoai',dt:'dien thoai',hotline:'dien thoai',data:'du lieu',bct:'bo cong thuong',oa:'zalo oa',mini:'mini app',clip:'video',tiktok:'video',bao:'bao mat',hack:'bao mat',ai:'ai agent tri tue nhan tao',chatbot:'ai agent',bi:'power bi phan tich'};
function tok(s,bi){var o=[],pv='';nz(s).split(' ').forEach(function(t){if(t&&!STOP[t]){o.push(t);if(SYN[t])o.push.apply(o,SYN[t].split(' '));if(pv)o.push(pv+'_'+t);pv=t}else pv=''});return o}
var KB=null,IX=null,LD=null;
function load(){if(LD)return LD;LD=fetch(B+'data/chatbot-kb.json?v='+((/[?&]v=([^&]+)/.exec(sc&&sc.src||'')||[])[1]||'1')).then(function(r){return r.json()}).then(function(j){KB=j.d;build()}).catch(function(){KB=[]});return LD}
function build(){var df={},N=KB.length,L=0;IX=KB.map(function(r){var f={},ts=tok(r[2]+' '+r[2]+' '+r[1]+' '+r[3]);ts.forEach(function(t){f[t]=(f[t]||0)+1});Object.keys(f).forEach(function(t){df[t]=(df[t]||0)+1});L+=ts.length;return{f:f,l:ts.length}});IX.avg=L/N;IX.df=df;IX.N=N}
function search(qs,filt){var qt=tok(qs),best=[],k1=1.4,b=.7;if(!IX)return best;var u={};qt=qt.filter(function(t){return u[t]?0:(u[t]=1)});
KB.forEach(function(r,i){if(filt&&!filt(r))return;var x=IX[i],s=0,hit=0,bh=0;qt.forEach(function(t){var tf=x.f[t];if(!tf)return;if(t.indexOf('_')>0)bh=1;else hit++;var idf=Math.log(1+(IX.N-IX.df[t]+.5)/(IX.df[t]+.5));s+=idf*tf*(k1+1)/(tf+k1*(1-b+b*x.l/IX.avg))});if(r[4]==='faq')s*=1.15;if(r[2]===r[1])s*=1.3;var nu=qt.filter(function(t){return t.indexOf('_')<0}).length||1;if(hit)best.push([s*(.6+.4*hit/nu),i,hit/nu,bh])});
best.sort(function(a,b){return b[0]-a[0]});return best}
function sent(t,n){return t.split(/(?<=[.!?…])\s+/).slice(0,n||3).join(' ').trim()}
var CT=[['Gọi '+PHS,'tel:'+PH],['Chat Zalo','https://zalo.me/'+PH],['Gửi form liên hệ','lien-he.html']];
function svcList(){var o=[];KB.forEach(function(r){if(/^dich-vu\//.test(r[0])&&r[2]===r[1]&&o.indexOf(r[1])<0)o.push(r[1])});return o}
function answer(raw){var n=' '+nz(raw)+' ';
function has(re){return re.test(n)}
if(n.trim().length<2)return{t:'Bạn gõ câu hỏi giúp mình nhé, ví dụ: "Làm website mất bao lâu?"'};
if(has(/ (ban|may|em) (la )?(nguoi that|nguoi|robot|bot|ai that|may) |nguoi that|co phai (la )?(nguoi|ai|bot)/))return{t:'Mình là MJ, trợ lý tự động (AI) của My Agent, không phải người thật. Mình chỉ trả lời dựa trên nội dung có trên website. Cần chắc chắn, bạn hãy liên hệ trực tiếp anh Tùng nhé.',l:CT};
if(has(/ (ban|may|em) la ai | ten (ban|em) | ai do | gioi thieu (ve )?(ban|em) /))return{t:'Mình là MJ, trợ lý tự động của My Agent. Mình giúp bạn tìm thông tin về dịch vụ, bảng giá tham khảo, quy trình, tra cứu tiến độ và cách liên hệ.',l:[['Về chúng tôi','ve-chung-toi.html']]};
if(has(/^ (xin )?chao|^ (hello|hi|helo|alo|hey) /)&&n.split(' ').length<7)return{t:'Chào bạn! Mình là MJ. Bạn cần tìm hiểu dịch vụ nào của My Agent?',c:1};
if(has(/ (cam on|thank|thanks|tks|ok cam) /))return{t:'Không có gì ạ! Bạn cần thêm gì cứ hỏi mình nhé.'};
if(has(/ (lien he|so dien thoai|dien thoai|sdt|hotline|zalo|email|gmail|goi (cho|dien)) /)&&!has(/ (zalo oa|mini app|email doanh nghiep|email ten mien) /))return{t:'Bạn liên hệ My Agent qua điện thoại/Zalo '+PHS+', email '+(C.formEmail||'')+' hoặc gửi form trên trang Liên hệ. Thông tin được phản hồi trong 1 ngày làm việc (theo trang Liên hệ).',l:CT};
if(has(/ (tra cuu|tien do|ma don|don hang|trang thai don) /))return{t:'Bạn vào trang Tra cứu tiến độ và nhập mã đơn My Agent đã gửi để xem dự án đang ở bước nào.',l:[['Tra cứu tiến độ','tra-cuu-tien-do.html']]};
if(has(/ (nhung|cac|danh sach|bao nhieu|co gi|nao) dich vu | dich vu (gi|nao|cua ban|cua my agent|ben ban)| lam (duoc )?(nhung )?gi | (ben ban|my agent) (co|lam) /)&&!has(/ gia /)){var s=svcList();return{t:'My Agent có '+s.length+' dịch vụ: '+s.join(', ')+'. Bạn quan tâm dịch vụ nào, mình nói chi tiết hơn.',l:[['Tất cả dịch vụ','dich-vu.html'],['Combo','combo.html']]}}
if(has(/ (ai|nguoi nao) (la )?(nguoi )?(lam|thuc hien|dung sau|so huu|sang lap)| chu (web|website|my agent) | peterpark | (anh )?tung la ai /))return{t:'My Agent là thương hiệu dịch vụ của Nguyễn Văn Tùng (PeterPark). Anh làm việc trực tiếp với từng khách, từ thiết kế giao diện, làm web đến đưa web lên mạng, và nhận dự án vừa và nhỏ.',l:[['Về chúng tôi','ve-chung-toi.html']]};
var pick=function(){var x=search(raw,function(x){return x[2]===x[1]});return x[0]&&x[0][2]>=.5?x:null},r,top=function(f){var x=search(raw,f);return x[0]&&x[0][0]>3&&(x[0][2]>=.67||x[0][2]>=.5&&x[0][3]||x[0][2]>=.99)?x:null};
var FQ=function(h){var d=KB.filter(function(x){return x[0]==='bang-gia.html'&&x[2]===h})[0];return d&&{t:d[3],l:[['Bảng giá & tự tính giá','bang-gia.html#tinh-gia']].concat(CT.slice(0,2))}};
if(has(/ (dat coc|coc|thanh toan|tra truoc) /)){var fq=FQ('Thanh toán thế nào?');if(fq)return fq}
if(has(/ ten mien /)&&has(/ hosting /)&&has(/ (gom|bao gom|chua gom|tinh rieng) /)){var fq2=FQ('Giá thiết kế đã gồm tên miền và hosting chưa?');if(fq2)return fq2}
if(has(/ (gia|bao gia|chi phi|bao nhieu tien|bang gia|tien) /)||has(/ phi /)&&!has(/ mien phi /)){var raw0=raw;raw=nz(raw).replace(/\b(bang gia|bao gia|chi phi|bao nhieu tien|bao nhieu|gia|phi|tien|lam)\b/g,' ');r=pick();raw=raw0;var pu=r&&KB[r[0][1]][0];if(has(/ app /)&&!has(/ (mini app|zalo) /))pu='dich-vu/thiet-ke-app.html';var pd=pu&&KB.filter(function(x){return x[0]===pu&&x[4]==='price'})[0];
if(pd)return{t:pd[3],l:[[pd[1],pd[0]]].concat(CT.slice(0,2))};
return{t:'Giá phụ thuộc vào phạm vi công việc. Trang Bảng giá có khoảng giá tham khảo (chưa gồm VAT) và công cụ tự tính giá combo; giá chỉ mang tính tham khảo, báo giá chính xác sau khi trao đổi nhu cầu. Hosting/VPS và quảng cáo: thương lượng.',l:[['Bảng giá & tự tính giá','bang-gia.html#tinh-gia']].concat(pu&&pu!=='bang-gia.html'?[[KB[r[0][1]][1],pu]]:[]).concat(CT)}}
if(has(/ bao lau | may ngay | thoi gian (lam|trien khai|hoan thanh) /)){var raw0=raw;raw=nz(raw).replace(/\b(bao lau|may ngay|thoi gian|mat|lam|trien khai|hoan thanh|xong)\b/g,' ');var pg=pick();raw=raw0;var f=function(x){return x[4]==='faq'&&/bao lau|thoi gian/.test(nz(x[2]))};r=pg&&search(raw+' bao lau trien khai',function(x){return f(x)&&x[0]===KB[pg[0][1]][0]});if(!r||!r[0])r=search(raw+' bao lau trien khai',f);if(r[0]){var t=KB[r[0][1]],pp=pg?KB[pg[0][1]]:t;return{t:t[2]+' '+sent(t[3],2),l:[[pp[1],pp[0]]].concat(CT.slice(0,2))}}}
r=top();
if(r){var a=KB[r[0][1]],L=[[a[1],a[0]]],o=r[1]&&KB[r[1][1]];if(o&&o[0]!==a[0]&&r[1][0]>r[0][0]*.8)L.push([o[1],o[0]]);return{t:(a[4]==='faq'?'':a[2]+': ')+sent(a[3],3),l:L}}
return{t:'Mình chưa chắc về câu này, vì mình chỉ trả lời theo nội dung trên website My Agent. Bạn hỏi trực tiếp anh Tùng nhé:',l:CT,fb:1}}
w.MJ_answer=function(t){return load().then(function(){return answer(t)})}; /* dùng cho scripts/chatbot_eval.py */
/* ---------- giao diện ---------- */
var CH=['Dịch vụ thiết kế website','Bảng giá / báo giá','Tra cứu tiến độ','Liên hệ'];
var root,btn,pan,log,inp,bub,typ,last;
function link(l){var u=/^(tel:|https?:)/.test(l[1])?l[1]:B+l[1],ext=/^https?:/.test(l[1]);return'<a class="mj-lk'+(/^tel:/.test(l[1])?' pri':'')+'" href="'+esc(u)+'"'+(ext?' target="_blank" rel="noopener"':'')+'>'+esc(l[0])+'</a>'}
function render(m,anim){var e=el('div','mj-m '+(m.r==='u'?'u':'b')+(anim&&!RM?' in':''));e.innerHTML='<p>'+esc(m.t)+'</p>'+(m.l&&m.l.length?'<div class="mj-lks">'+m.l.map(link).join('')+'</div>':'');log.appendChild(e);log.scrollTop=log.scrollHeight}
function add(m,anim){st.m.push(m);if(st.m.length>60)st.m=st.m.slice(-60);save();render(m,anim)}
function ask(t){t=String(t).slice(0,300).trim();if(!t)return;add({r:'u',t:t},1);typ.hidden=false;log.scrollTop=log.scrollHeight;
load().then(function(){setTimeout(function(){typ.hidden=true;var a=answer(t);add({r:'b',t:a.t,l:a.l},1);if(a.c)chips()},RM?0:450+Math.random()*350)})}
function chips(){var c=pan.querySelector('.mj-ch');c.hidden=false}
function hello(){if(!st.m.length)add({r:'b',t:'Xin chào! Mình là MJ, trợ lý tự động của My Agent. Bạn muốn hỏi gì về dịch vụ? Chọn nhanh bên dưới hoặc gõ câu hỏi nhé.'},0)}
function open(){if(!pan)ui();last=d.activeElement;root.classList.add('on');pan.hidden=false;btn.setAttribute('aria-expanded','true');hideBub();st.o=1;save();load();hello();
requestAnimationFrame(function(){pan.classList.add('show');log.scrollTop=log.scrollHeight;inp.focus({preventScroll:true})})}
function close(){if(!pan)return;pan.classList.remove('show');root.classList.remove('on');btn.setAttribute('aria-expanded','false');st.o=0;save();setTimeout(function(){if(!pan.classList.contains('show'))pan.hidden=true},RM?0:220);(last&&last!==d.body?last:btn).focus({preventScroll:true})}
function hideBub(){if(bub){bub.remove();bub=null}try{ss.setItem('mj_greet','1')}catch(e){}}
function ui(){pan=el('div','mj-pan');pan.id='mj-pan';pan.hidden=true;pan.setAttribute('role','dialog');pan.setAttribute('aria-modal','false');pan.setAttribute('aria-labelledby','mj-ttl');
pan.innerHTML='<div class="mj-hd"><span class="mj-av">'+AV+'</span><div class="mj-id"><p class="mj-ttl" id="mj-ttl">MJ – Trợ lý My Agent <b class="mj-ai">AI</b></p><p class="mj-dis">Trợ lý tự động, có thể chưa đúng — cần chắc chắn hãy liên hệ trực tiếp</p></div><button type="button" class="mj-ib mj-clr" aria-label="Xóa cuộc trò chuyện" title="Xóa cuộc trò chuyện"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button><button type="button" class="mj-ib mj-x" aria-label="Đóng trợ lý" title="Đóng (Esc)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div><div class="mj-log" role="log" aria-live="polite" aria-relevant="additions"></div><div class="mj-typ" hidden aria-label="MJ đang trả lời"><i></i><i></i><i></i></div><div class="mj-ch" role="group" aria-label="Câu hỏi nhanh">'+CH.map(function(c){return'<button type="button">'+c+'</button>'}).join('')+'</div><form class="mj-f" role="search" autocomplete="off"><label class="mj-sr" for="mj-in">Câu hỏi cho MJ</label><input id="mj-in" type="text" maxlength="300" enterkeyhint="send" placeholder="Hỏi MJ về dịch vụ..."><button type="submit" aria-label="Gửi câu hỏi"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12l16-8-6 16-2-7z" fill="currentColor"/></svg></button></form>';
root.appendChild(pan);log=pan.querySelector('.mj-log');inp=pan.querySelector('input');typ=pan.querySelector('.mj-typ');
st.m.forEach(function(m){render(m,0)});
pan.querySelector('.mj-x').onclick=close;
pan.querySelector('.mj-clr').onclick=function(){st.m=[];save();log.innerHTML='';hello();inp.focus()};
pan.querySelector('.mj-ch').onclick=function(e){var b=e.target.closest('button');if(b)ask(b.textContent)};
pan.querySelector('form').onsubmit=function(e){e.preventDefault();var v=inp.value;inp.value='';ask(v)};
pan.addEventListener('keydown',function(e){if(e.key==='Escape'){e.stopPropagation();close()}if(e.key==='Tab'&&matchMedia('(max-width:560px)').matches){var f=pan.querySelectorAll('button,a[href],input'),a=f[0],z=f[f.length-1];if(e.shiftKey&&d.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&d.activeElement===z){e.preventDefault();a.focus()}}})}
function start(){root=el('div','mj-root');root.id='mj-root';
btn=el('button','mj-btn',AV);btn.type='button';btn.setAttribute('aria-label','Mở trợ lý MJ (AI) – hỏi về dịch vụ My Agent');btn.setAttribute('aria-controls','mj-pan');btn.setAttribute('aria-expanded','false');btn.onclick=function(){root.classList.contains('on')?close():open()};
root.appendChild(btn);d.body.appendChild(root);requestAnimationFrame(function(){root.classList.add('rdy')});
if(st.o)open();else{var g;try{g=ss.getItem('mj_greet')}catch(e){}if(!g)setTimeout(function(){if(root.classList.contains('on')||bub)return;bub=el('div','mj-bub','<button type="button" class="mj-bt">Xin chào! Mình là MJ, hỏi mình về dịch vụ nhé</button><button type="button" class="mj-bx" aria-label="Ẩn lời chào">×</button>');root.appendChild(bub);bub.querySelector('.mj-bt').onclick=open;bub.querySelector('.mj-bx').onclick=hideBub},4000)}}
function go(){if(h.classList.contains('intro-on')){var mo=new MutationObserver(function(){if(!h.classList.contains('intro-on')){mo.disconnect();setTimeout(start,400)}});mo.observe(h,{attributes:true,attributeFilter:['class']})}else start()}
d.readyState==='loading'?d.addEventListener('DOMContentLoaded',go):go();
})();
