/* My Agent — intro "khởi động hệ thống" cho trang chủ. Bật/tắt: introEnabled trong js/config.js; ?intro=1 ép hiện, ?intro=0 bỏ qua. Xem docs/intro.md */
(function(){
var d=document,h=d.documentElement;
if(!h.classList.contains('intro-on'))return;
var KEY='myagent_intro_seen',DUR=3600,done=false,raf=0,timers=[],last=d.activeElement;
try{sessionStorage.setItem(KEY,'1')}catch(e){}
var lines=['> khởi tạo My Agent...','> nạp module: AI · tự động hóa · phần mềm...','> kết nối hạ tầng web · SEO · dữ liệu...','> sẵn sàng.'];
var o=d.createElement('div');o.id='ma-intro';o.setAttribute('role','dialog');o.setAttribute('aria-modal','true');o.setAttribute('aria-label','Giới thiệu My Agent');
o.innerHTML='<canvas aria-hidden="true"></canvas><div class="mi-box"><img class="mi-logo" src="assets/logo-dark.svg" alt="My Agent" width="260" height="64"><pre class="mi-term mono" aria-live="off"></pre><div class="mi-bar" aria-hidden="true"><i></i></div><span class="mi-pct mono" aria-hidden="true">0%</span></div><button type="button" class="mi-skip">Bỏ qua <span aria-hidden="true">›</span></button>';
d.body.appendChild(o);
var kids=[].filter.call(d.body.children,function(n){return n!==o&&n.tagName!=='SCRIPT'});
kids.forEach(function(n){n.inert=true;n.setAttribute('aria-hidden','true')});
var term=o.querySelector('.mi-term'),bar=o.querySelector('.mi-bar i'),pct=o.querySelector('.mi-pct'),skip=o.querySelector('.mi-skip');
skip.addEventListener('click',finish);
function key(e){if(e.key==='Escape'){e.preventDefault();finish()}else if(e.key==='Tab'){e.preventDefault();skip.focus()}}
d.addEventListener('keydown',key);
try{skip.focus({preventScroll:true})}catch(e){}
/* gõ chữ */
var full=lines.join('\n'),per=(DUR-900)/full.length;
var t0=performance.now();
/* nền: ký tự mã rơi nhẹ + lưới */
var cv=o.querySelector('canvas'),cx=cv.getContext&&cv.getContext('2d'),W,H,cols=[],fs=14,dpr=Math.min(window.devicePixelRatio||1,1.5);
function size(){W=innerWidth;H=innerHeight;cv.width=W*dpr;cv.height=H*dpr;cv.style.width=W+'px';cv.style.height=H+'px';if(cx)cx.setTransform(dpr,0,0,dpr,0,0);
 var n=Math.min(Math.ceil(W/fs/1.6),70);cols=[];for(var i=0;i<n;i++)cols.push({x:i*W/n,y:Math.random()*-H,v:.6+Math.random()*1.4})}
size();addEventListener('resize',size);
var CH='01アイウエオカキクケコ<>/{}=+MYAGENT';
function frame(now){
 var t=now-t0,p=Math.min(t/DUR,1);
 var nch=Math.min(full.length,Math.floor(t/per));term.textContent=full.slice(0,nch)+(p<1?'▌':'');
 bar.style.transform='scaleX('+p+')';pct.textContent=Math.round(p*100)+'%';
 if(cx){cx.fillStyle='rgba(5,7,15,.22)';cx.fillRect(0,0,W,H);cx.font=fs+'px '+'monospace';
  for(var i=0;i<cols.length;i++){var c=cols[i];cx.fillStyle=i%5?'rgba(61,123,255,.35)':'rgba(255,45,61,.45)';cx.fillText(CH[(Math.random()*CH.length)|0],c.x,c.y);c.y+=fs*c.v*.5;if(c.y>H)c.y=Math.random()*-80}}
 if(p>=1){finish();return}
 raf=requestAnimationFrame(frame)}
raf=requestAnimationFrame(frame);
function vis(){if(d.hidden){cancelAnimationFrame(raf);raf=0}else if(!raf&&!done){raf=requestAnimationFrame(frame)}}
d.addEventListener('visibilitychange',vis);
timers.push(setTimeout(finish,6000));
function finish(){if(done)return;done=true;cancelAnimationFrame(raf);timers.forEach(clearTimeout);
 d.removeEventListener('keydown',key);d.removeEventListener('visibilitychange',vis);removeEventListener('resize',size);
 kids.forEach(function(n){n.inert=false;n.removeAttribute('aria-hidden')});
 o.classList.add('mi-out');h.classList.remove('intro-on');
 try{(last&&last!==d.body&&last.focus)?last.focus({preventScroll:true}):0}catch(e){}
 setTimeout(function(){o.remove()},600)}
})();
