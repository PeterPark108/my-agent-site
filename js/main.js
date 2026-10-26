(()=>{const d=document,RM=matchMedia('(prefers-reduced-motion:reduce)').matches,FINE=matchMedia('(pointer:fine)').matches;d.documentElement.classList.add('js');
const hdr=d.getElementById('hdr'),onS=()=>hdr.classList.toggle('sc',scrollY>10);onS();addEventListener('scroll',onS,{passive:true});
const b=d.querySelector('.burger'),nav=d.querySelector('nav');b.onclick=()=>{const o=nav.classList.toggle('open');b.setAttribute('aria-expanded',o)};
d.querySelectorAll('.has>a').forEach(a=>a.addEventListener('click',e=>{if(innerWidth<=960){e.preventDefault();a.parentNode.classList.toggle('open')}}));
d.querySelectorAll('form').forEach(f=>{if(f.classList.contains('domain'))return;f.onsubmit=e=>{e.preventDefault();f.innerHTML='<span class="k">// đã gửi</span><h3>Cảm ơn anh/chị!</h3><p class="muted">My Agent sẽ liên hệ lại trong thời gian sớm nhất.</p>'}});
// reveal + counters
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -40px 0px'});
d.querySelectorAll('.rv,.tl').forEach((el,i)=>{el.style.transitionDelay=(i%4)*70+'ms';io.observe(el)});
// pointer effects
if(FINE&&!RM){const g=d.querySelector('.glow-cursor');addEventListener('pointermove',e=>{g.style.left=e.clientX+'px';g.style.top=e.clientY+'px'},{passive:true});
d.querySelectorAll('.card').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;c.style.setProperty('--mx',x+'px');c.style.setProperty('--my',y+'px');if(c.classList.contains('tilt'))c.style.transform=`perspective(900px) rotateX(${(y/r.height-.5)*-5}deg) rotateY(${(x/r.width-.5)*5}deg) translateY(-4px)`});c.addEventListener('pointerleave',()=>c.style.transform='')});
d.querySelectorAll('.btn').forEach(m=>{m.addEventListener('pointermove',e=>{const r=m.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;m.style.setProperty('--x',x+'px');m.style.setProperty('--y',y+'px');if(m.classList.contains('mag'))m.style.transform=`translate(${(x-r.width/2)*.15}px,${(y-r.height/2)*.25}px)`});m.addEventListener('pointerleave',()=>m.style.transform='')})}
// spider-web network canvas
d.querySelectorAll('canvas.net').forEach(cv=>{const cx=cv.getContext('2d'),host=cv.parentNode;let W,H,pts=[],m={x:-999,y:-999},run=false,DPR=Math.min(devicePixelRatio||1,2);
const size=()=>{W=host.clientWidth;H=host.clientHeight;cv.width=W*DPR;cv.height=H*DPR;cx.setTransform(DPR,0,0,DPR,0,0);const n=Math.min(Math.round(W*H/(cv.classList.contains('mini')?16000:11000)),110);pts=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,r:Math.random()*1.6+.6,c:Math.random()<.35}))};
size();addEventListener('resize',size);host.addEventListener('pointermove',e=>{const r=cv.getBoundingClientRect();m.x=e.clientX-r.left;m.y=e.clientY-r.top});host.addEventListener('pointerleave',()=>{m.x=m.y=-999});
const L=130;const draw=()=>{cx.clearRect(0,0,W,H);for(const p of pts){if(!RM){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;const dx=m.x-p.x,dy=m.y-p.y,dd=Math.hypot(dx,dy);if(dd<160){p.x+=dx*.012;p.y+=dy*.012}}}
for(let i=0;i<pts.length;i++){const a=pts[i];for(let j=i+1;j<pts.length;j++){const b=pts[j],dx=a.x-b.x,dy=a.y-b.y,q=dx*dx+dy*dy;if(q<L*L){const o=1-Math.sqrt(q)/L;cx.strokeStyle=a.c||b.c?`rgba(255,45,61,${o*.45})`:`rgba(91,140,255,${o*.35})`;cx.lineWidth=o;cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x,b.y);cx.stroke()}}
const dm=Math.hypot(m.x-a.x,m.y-a.y);if(dm<180){cx.strokeStyle=`rgba(255,90,102,${(1-dm/180)*.8})`;cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(m.x,m.y);cx.stroke()}
cx.fillStyle=a.c?'#FF2D3D':'#7FA6FF';cx.beginPath();cx.arc(a.x,a.y,a.r,0,7);cx.fill()}if(run&&!RM)requestAnimationFrame(draw)};
new IntersectionObserver(([e])=>{const w=run;run=e.isIntersecting;if(run&&!w)requestAnimationFrame(draw)}).observe(cv);draw()});
// agent console
const t=d.getElementById('term');if(t){const L=[['c1','$ my-agent run --goal "tăng khách hàng"'],['c2','› Phân tích website hiện tại...'],['','  ✓ Tốc độ tải: tối ưu 0.8s'],['','  ✓ SEO onpage: 38 điểm cần sửa'],['c2','› Khởi tạo hệ sinh thái:'],['','  [■■■■■■■■■■] website · hosting · email'],['','  [■■■■■■■□□□] SEO · ADS · Google Maps'],['','  [■■■■■□□□□□] Fanpage · Zalo OA · Video AI'],['c3','✔ Kế hoạch sẵn sàng. Bắt đầu chuyển đổi 24/7.']];
const esc=s=>s.replace(/</g,'&lt;');if(RM){t.innerHTML=L.map(([c,s])=>`<span class="${c}">${esc(s)}</span>`).join('\n');return}
let i=0,j=0,out='';const step=()=>{if(i>=L.length){t.innerHTML=out+'<span class="cur"></span>';setTimeout(()=>{i=j=0;out='';step()},4000);return}const [c,s]=L[i];j++;t.innerHTML=out+`<span class="${c}">${esc(s.slice(0,j))}</span><span class="cur"></span>`;if(j>=s.length){out+=`<span class="${c}">${esc(s)}</span>\n`;i++;j=0;setTimeout(step,350)}else setTimeout(step,i==0?45:14)};
new IntersectionObserver(([e],o)=>{if(e.isIntersecting){o.disconnect();step()}}).observe(t)}
})();
