(()=>{const d=document,RM=matchMedia('(prefers-reduced-motion:reduce)').matches,FINE=matchMedia('(pointer:fine)').matches;d.documentElement.classList.add('js');
const hdr=d.getElementById('hdr'),onS=()=>hdr.classList.toggle('sc',scrollY>10);onS();addEventListener('scroll',onS,{passive:true});
const b=d.querySelector('.burger'),nav=d.querySelector('nav');b.onclick=()=>{const o=nav.classList.toggle('open');b.setAttribute('aria-expanded',o)};
d.querySelectorAll('.has>a').forEach(a=>a.addEventListener('click',e=>{if(innerWidth<=960){e.preventDefault();a.parentNode.classList.toggle('open')}}));
// contact form -> FormSubmit.co (config in js/config.js)
const C=window.MYAGENT_CONFIG||{},EM=C.formEmail||'',ZP=(C.zaloPhone||'').replace(/\D/g,''),okEM=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(EM);
d.querySelectorAll('a[data-mailto]').forEach(a=>{if(okEM)a.href='mailto:'+EM;else a.hidden=true});
d.querySelectorAll('a[data-zalo]').forEach(a=>{if(ZP)a.href='https://zalo.me/'+ZP;else a.hidden=true});
// floating call button: mobile dials via tel:, desktop shows number popover
const TEL=ZP||'0328439972',TF=TEL.replace(/^(\d{4})(\d{3})(\d+)$/,'$1 $2 $3');
d.querySelectorAll('a[data-tel]').forEach(a=>{a.href='tel:'+TEL});
const fb=d.getElementById('fab-call');if(fb){fb.setAttribute('aria-label','Gọi '+TF);let pop;
const close=(f)=>{if(!pop||pop.hidden)return;pop.classList.remove('on');pop.hidden=true;fb.setAttribute('aria-expanded','false');if(f)fb.focus()};
fb.addEventListener('click',e=>{if(!(matchMedia('(pointer:fine)').matches&&innerWidth>960))return;e.preventDefault();
if(!pop){pop=d.createElement('div');pop.className='fab-pop';pop.id='fab-pop';pop.setAttribute('role','dialog');pop.setAttribute('aria-label','Số điện thoại My Agent');pop.hidden=true;
pop.innerHTML='<button type="button" class="x" aria-label="Đóng">×</button><span class="k mono">// Điện thoại / Zalo</span><strong class="num">'+TF+'</strong><div class="acts"><button type="button" class="cp">Sao chép số</button><a class="pri" href="tel:'+TEL+'">Gọi</a><a href="https://zalo.me/'+TEL+'" target="_blank" rel="noopener">Chat Zalo</a></div><span class="sr" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)"></span>';
d.body.appendChild(pop);pop.querySelector('.x').onclick=()=>close(1);
const cp=pop.querySelector('.cp');cp.onclick=async()=>{let ok=false;try{await navigator.clipboard.writeText(TEL);ok=true}catch(_){const ta=d.createElement('textarea');ta.value=TEL;d.body.appendChild(ta);ta.select();try{ok=d.execCommand('copy')}catch(_){}ta.remove()}
cp.textContent=ok?'✓ Đã sao chép':'Không sao chép được';cp.classList.toggle('ok',ok);pop.querySelector('.sr').textContent=ok?'Đã sao chép số '+TF:'';setTimeout(()=>{cp.textContent='Sao chép số';cp.classList.remove('ok')},2000)}}
if(!pop.hidden){close(1);return}pop.hidden=false;fb.setAttribute('aria-expanded','true');requestAnimationFrame(()=>pop.classList.add('on'));pop.querySelector('.cp').focus()});
d.addEventListener('keydown',e=>{if(e.key==='Escape')close(1)});
d.addEventListener('click',e=>{if(pop&&!pop.hidden&&!pop.contains(e.target)&&!fb.contains(e.target))close()})}
d.querySelectorAll('.form-alt').forEach(p=>{if(!okEM&&!ZP)p.hidden=true});
d.querySelectorAll('form[data-contact]').forEach(f=>{const st=f.querySelector('.form-status'),bt=f.querySelector('button[type=submit]'),say=(m,c)=>{st.textContent=m;st.className='form-status '+(c||'')};
f.addEventListener('submit',async e=>{e.preventDefault();if(f._honey&&f._honey.value)return;
const bad=[...f.elements].find(x=>x.willValidate&&!x.checkValidity());if(bad){bad.focus();say(bad.type=='tel'?'Số điện thoại chưa hợp lệ.':bad.type=='email'?'Email chưa hợp lệ.':'Vui lòng điền đủ thông tin bắt buộc.','err');return}
if(!okEM){say('Form tạm thời chưa nhận được tin nhắn. Vui lòng thử lại sau ít phút.','err');return}
const fd=new FormData(f);fd.delete('_honey');fd.append('_subject','Yêu cầu tư vấn mới từ website My Agent');fd.append('_template','table');fd.append('_captcha','false');fd.append('_url',location.href);
bt.disabled=true;say('Đang gửi...');
try{const r=await fetch('https://formsubmit.co/ajax/'+encodeURIComponent(EM),{method:'POST',headers:{Accept:'application/json'},body:fd});const j=await r.json().catch(()=>({}));
if(/activat/i.test(j.message||'')){bt.disabled=false;st.innerHTML='Hệ thống nhận form đang chờ kích hoạt. Anh/chị vui lòng gửi tạm qua <a href="mailto:'+EM+'">'+EM+'</a>'+(ZP?' hoặc <a href="https://zalo.me/'+ZP+'">Zalo</a>':'')+'.';st.className='form-status err';return}
if(!r.ok||j.success===false||j.success==='false')throw 0;
f.innerHTML='<span class="k">// đã gửi</span><h3>Cảm ơn anh/chị!</h3><p class="muted">My Agent sẽ liên hệ lại trong thời gian sớm nhất.</p>'}
catch(_){bt.disabled=false;say('Gửi chưa thành công. Vui lòng thử lại hoặc liên hệ qua Email/Zalo.','err')}})});
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
