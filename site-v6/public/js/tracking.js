(function(){'use strict';
var STEPS=['Tiếp nhận','Lên kế hoạch – thiết kế','Thực hiện','Duyệt','Bàn giao'];
var MAXF=5,COOL=60000,KEY='ma_trk_fail';
var f=document.getElementById('trk-form'),inp=document.getElementById('trk-code'),btn=f.querySelector('button'),out=document.getElementById('trk-out'),msg=document.getElementById('trk-msg');
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function fd(d){var p=String(d).split('-');return p.length===3?p[2]+'/'+p[1]+'/'+p[0]:esc(d)}
function st(){try{return JSON.parse(sessionStorage.getItem(KEY))||{n:0,u:0}}catch(e){return{n:0,u:0}}}
function sv(o){try{sessionStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
var tmr;
function lockLeft(){var s=st();return s.u>Date.now()?s.u-Date.now():0}
function tick(){var l=lockLeft();clearTimeout(tmr);if(l>0){btn.disabled=true;say('Bạn đã nhập sai nhiều lần. Thử lại sau '+Math.ceil(l/1000)+' giây.','err');tmr=setTimeout(tick,1000)}else{if(btn.disabled){btn.disabled=false;say('')}}}
function say(t,c){msg.textContent=t;msg.className='trk-msg'+(c?' '+c:'')}
function render(o,code){
 var p=Math.max(0,Math.min(100,+o.percent||0)),h='';
 h+='<div class="trk-head"><div><span class="k mono">// mã đơn</span><p class="trk-code mono">'+esc(code)+'</p></div><span class="trk-badge">'+(p>=100?'Hoàn tất':'Đang xử lý')+'</span></div>';
 h+='<ol class="trk-steps">'+STEPS.map(function(n,i){var raw=(o.steps||[])[i],s=raw==='done'||raw==='current'?raw:'pending',lb={done:'Đã xong',current:'Đang làm',pending:'Chưa bắt đầu'}[s];return '<li class="'+s+'"'+(s==='current'?' aria-current="step"':'')+'><i aria-hidden="true">'+(s==='done'?'✓':i+1)+'</i><span>'+n+'<small class="sr">: '+lb+'</small></span></li>'}).join('')+'</ol>';
 h+='<div class="trk-pct"><div class="trk-row"><b>'+esc(o.status||'')+'</b><span class="mono">'+p+'%</span></div><div class="trk-bar" role="progressbar" aria-label="Tiến độ tổng" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+p+'"><span style="width:'+p+'%"></span></div></div>';
 h+='<div class="trk-last"><span class="k mono">// cập nhật mới nhất · '+fd(o.updated)+'</span><p>'+esc(o.note||'')+'</p></div>';
 var hs=(o.history||[]).slice(0,8);
 if(hs.length>1){h+='<button type="button" class="trk-tg" aria-expanded="false" aria-controls="trk-hist">Xem lịch sử <span aria-hidden="true">▾</span></button><ul class="trk-hist" id="trk-hist" hidden>'+hs.map(function(x){return '<li><time class="mono">'+fd(x.d)+'</time><span>'+esc(x.n)+'</span></li>'}).join('')+'</ul>'}
 out.innerHTML='<div class="card glass trk-card">'+h+'</div>';
 var tg=out.querySelector('.trk-tg');if(tg)tg.addEventListener('click',function(){var e=tg.getAttribute('aria-expanded')==='true';tg.setAttribute('aria-expanded',String(!e));tg.firstChild.nodeValue=e?'Xem lịch sử ':'Ẩn lịch sử ';document.getElementById('trk-hist').hidden=e});
}
function notFound(){var s=st();s.n++;if(s.n>=MAXF){s.n=0;s.u=Date.now()+COOL}sv(s);
 out.innerHTML='<div class="card glass trk-card trk-nf"><b>Không tìm thấy</b><p>Mã chưa đúng hoặc đơn chưa được tạo. Kiểm tra lại mã, hoặc liên hệ <a href="mailto:lienhe@myagentvn.com">lienhe@myagentvn.com</a>.</p></div>';
 if(s.u>Date.now())tick();else say('Còn '+(MAXF-s.n)+' lần thử trước khi tạm khoá 60 giây.','err')}
function look(raw){
 var code=String(raw||'').trim();out.replaceChildren();
 if(!code){say('Vui lòng nhập mã truy cập đã được My Agent cấp.','err');inp.focus();return}
 if(lockLeft()){tick();return}
 btn.disabled=true;say('Đang tra cứu…');
 fetch('/api/tracking',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code:code}),cache:'no-store',signal:AbortSignal.timeout(10000)})
 .then(function(r){if(r.status===404){notFound();return null}if(r.status===429){var delay=Number(r.headers.get('Retry-After'))||60;sv({n:0,u:Date.now()+Math.min(600,delay)*1000});tick();return null}if(!r.ok)throw Error('unavailable');return r.json()})
 .then(function(data){if(data&&data.ok&&data.order){sv({n:0,u:0});say('Đã tìm thấy đơn.','ok');render(data.order,code)}})
 .catch(function(){say('Tra cứu chưa sẵn sàng. Vui lòng thử lại hoặc liên hệ My Agent.','err')})
 .finally(function(){btn.disabled=lockLeft()>0});
}
f.addEventListener('submit',function(e){e.preventDefault();look(inp.value)});
// Access codes are submitted in a POST body, never read from URL or stored locally.
if(new URLSearchParams(location.search).has('ma')){var url=new URL(location.href);url.searchParams.delete('ma');history.replaceState(null,'',url.pathname+url.search+url.hash);say('Vui lòng nhập mã trực tiếp; không chia sẻ mã qua đường dẫn.');}
tick();
})();
