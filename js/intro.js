/* My Agent — intro trang chủ: chỉ logo, xuất hiện hoành tráng. Bật/tắt: introEnabled trong js/config.js; ?intro=1 ép hiện, ?intro=0 bỏ qua. Xem docs/intro.md */
(function(){
var d=document,h=d.documentElement;
if(!h.classList.contains('intro-on'))return;
var KEY='myagent_intro_seen',DUR=3300,HIT=1100,done=false,raf=0,timers=[],last=d.activeElement;
try{sessionStorage.setItem(KEY,'1')}catch(e){}
var o=d.createElement('div');o.id='ma-intro';o.setAttribute('role','dialog');o.setAttribute('aria-modal','true');o.setAttribute('aria-label','My Agent');
o.innerHTML='<canvas aria-hidden="true"></canvas><div class="mi-stage" aria-hidden="true"><i class="mi-ring"></i><i class="mi-ring r2"></i><i class="mi-flash"></i></div><div class="mi-logo-wrap"><img class="mi-logo" src="assets/logo-dark.svg" alt="My Agent" width="260" height="64"><img class="mi-logo mi-ghost g1" src="assets/logo-dark.svg" alt="" aria-hidden="true"><img class="mi-logo mi-ghost g2" src="assets/logo-dark.svg" alt="" aria-hidden="true"><i class="mi-sweep" aria-hidden="true"></i></div><button type="button" class="mi-skip">Bỏ qua <span aria-hidden="true">›</span></button>';
d.body.appendChild(o);
var kids=[].filter.call(d.body.children,function(n){return n!==o&&n.tagName!=='SCRIPT'});
kids.forEach(function(n){n.inert=true;n.setAttribute('aria-hidden','true')});
var skip=o.querySelector('.mi-skip');
skip.addEventListener('click',finish);
function key(e){if(e.key==='Escape'){e.preventDefault();finish()}else if(e.key==='Tab'){e.preventDefault();skip.focus()}}
d.addEventListener('keydown',key);
try{skip.focus({preventScroll:true})}catch(e){}
/* canvas: tia sáng hội tụ vào tâm, rồi hạt bung ra khi logo xuất hiện */
var cv=o.querySelector('canvas'),cx=cv.getContext&&cv.getContext('2d'),W,H,dpr=Math.min(window.devicePixelRatio||1,1.5),streaks=[],parts=[],burst=false;
var COL=['255,45,61','61,123,255','120,220,255'];
function size(){W=innerWidth;H=innerHeight;cv.width=W*dpr;cv.height=H*dpr;cv.style.width=W+'px';cv.style.height=H+'px';if(cx)cx.setTransform(dpr,0,0,dpr,0,0)}
size();addEventListener('resize',size);
var NS=W<600?28:46;
for(var i=0;i<NS;i++){var a=Math.random()*6.283;streaks.push({a:a,d0:.55+Math.random()*.6,len:.08+Math.random()*.14,del:Math.random()*.35,c:COL[i%3]})}
function boom(){burst=true;var n=W<600?60:110;for(var i=0;i<n;i++){var a=Math.random()*6.283,v=2+Math.random()*7;parts.push({x:W/2,y:H/2,vx:Math.cos(a)*v,vy:Math.sin(a)*v,l:1,c:COL[i%3],s:1+Math.random()*2})}}
var t0=performance.now();
function frame(now){
 var t=now-t0;
 if(cx){cx.clearRect(0,0,W,H);var R=Math.hypot(W,H)/2;cx.globalCompositeOperation='lighter';
  if(t<HIT){for(var i=0;i<streaks.length;i++){var s=streaks[i],p=Math.max(0,Math.min(1,(t/HIT-s.del)/(1-s.del)));if(!p)continue;p=p*p;
   var r1=R*s.d0*(1-p),r2=r1+R*s.len*(1-p*.6),ca=Math.cos(s.a),sa=Math.sin(s.a);
   var g=cx.createLinearGradient(W/2+ca*r1,H/2+sa*r1,W/2+ca*r2,H/2+sa*r2);g.addColorStop(0,'rgba('+s.c+',.95)');g.addColorStop(1,'rgba('+s.c+',0)');
   cx.strokeStyle=g;cx.lineWidth=1.6;cx.beginPath();cx.moveTo(W/2+ca*r1,H/2+sa*r1);cx.lineTo(W/2+ca*r2,H/2+sa*r2);cx.stroke()}}
  else if(!burst)boom();
  for(var j=parts.length-1;j>=0;j--){var q=parts[j];q.x+=q.vx;q.y+=q.vy;q.vx*=.97;q.vy*=.97;q.l-=.012;if(q.l<=0){parts.splice(j,1);continue}
   cx.fillStyle='rgba('+q.c+','+q.l.toFixed(3)+')';cx.fillRect(q.x,q.y,q.s,q.s)}
  cx.globalCompositeOperation='source-over'}
 if(t>=DUR){finish();return}
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
 setTimeout(function(){o.remove()},650)}
})();
