/* My Agent — lớp animation toàn site. Tắt: motionEnabled:false (js/config.js) hoặc ?motion=0. Xem docs/animation.md */
(()=>{const d=document,h=d.documentElement,C=window.MYAGENT_CONFIG||{},q=/[?&]motion=([01])/.exec(location.search);
if(q?q[1]==='0':C.motionEnabled===false)return;if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
h.classList.add('mo');const FINE=matchMedia('(pointer:fine)').matches,W=()=>innerWidth;
const intro=()=>h.classList.contains('intro-on'),afterIntro=f=>{if(!intro())return f();const mo=new MutationObserver(()=>{if(!intro()){mo.disconnect();f()}});mo.observe(h,{attributes:true,attributeFilter:['class']})};
// thanh tiến trình cuộn
const pb=d.createElement('div');pb.className='mv-prog';pb.setAttribute('aria-hidden','true');d.body.appendChild(pb);let tk=0;
const prog=()=>{tk=0;const m=h.scrollHeight-innerHeight;pb.style.transform='scaleX('+(m>0?scrollY/m:0)+')'};addEventListener('scroll',()=>{if(!tk){tk=1;requestAnimationFrame(prog)}},{passive:true});prog();
// hero: hiện lần lượt
afterIntro(()=>requestAnimationFrame(()=>h.classList.add('mv-go')));
// reveal tự động cho phần tử con trong lưới (chỉ phần dưới màn hình đầu)
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1,rootMargin:'0px 0px -30px 0px'});
d.querySelectorAll('main .grid>*:not(.rv),main .plans>*:not(.rv),main .bento>*:not(.rv),main .cta-box,main .t:not(.rv)').forEach(el=>{if(el.getBoundingClientRect().top<innerHeight)return;
const i=[...el.parentNode.children].indexOf(el);el.classList.add('mv');el.style.transitionDelay=Math.min(i%6,5)*80+'ms';io.observe(el)});
setTimeout(()=>d.querySelectorAll('.mv:not(.in)').forEach(el=>{if(el.getBoundingClientRect().top<innerHeight)el.classList.add('in')}),3000);
// tiêu đề mục: vạch neon tự vẽ
d.querySelectorAll('main .t').forEach(t=>{const o=new IntersectionObserver(([e])=>{if(e.isIntersecting){t.classList.add('mv-line');o.disconnect()}});o.observe(t)});
// thẻ: nghiêng 3D (desktop); nút: gợn sóng
if(FINE)d.querySelectorAll('main .card').forEach(c=>c.classList.add('tilt'));
d.addEventListener('pointerdown',e=>{const b=e.target.closest&&e.target.closest('.btn');if(!b)return;const r=b.getBoundingClientRect(),s=d.createElement('span'),z=Math.max(r.width,r.height)*2;
s.className='mv-rip';s.style.cssText=`width:${z}px;height:${z}px;left:${e.clientX-r.left-z/2}px;top:${e.clientY-r.top-z/2}px`;b.appendChild(s);setTimeout(()=>s.remove(),650)},{passive:true});
// parallax nhẹ ở hero (chuột, desktop)
const hero=d.querySelector('.hero');if(hero&&FINE){const L=hero.querySelectorAll('.console,canvas.net');let raf=0,x=0,y=0;
hero.addEventListener('pointermove',e=>{const r=hero.getBoundingClientRect();x=(e.clientX-r.left)/r.width-.5;y=(e.clientY-r.top)/r.height-.5;if(!raf)raf=requestAnimationFrame(()=>{raf=0;L.forEach((el,i)=>el.style.translate=`${x*(i?-14:10)}px ${y*(i?-10:8)}px`)})});
hero.addEventListener('pointerleave',()=>L.forEach(el=>el.style.translate=''))}
// menu: vạch chỉ báo trượt theo link (desktop)
const ul=d.querySelector('header nav>ul');if(ul&&FINE){const bar=d.createElement('i');bar.className='mv-ind';bar.setAttribute('aria-hidden','true');ul.appendChild(bar);
const to=a=>{if(!a||W()<=960){bar.style.opacity=0;return}const r=a.getBoundingClientRect(),u=(bar.offsetParent||ul).getBoundingClientRect();bar.style.opacity=1;bar.style.transform=`translateX(${r.left-u.left}px) scaleX(${r.width/100})`};
const on=()=>to(ul.querySelector(':scope>li>a.on'));ul.querySelectorAll(':scope>li>a').forEach(a=>a.addEventListener('pointerenter',()=>to(a)));ul.addEventListener('pointerleave',on);addEventListener('resize',on);setTimeout(on,60)}
// chuyển trang mượt (an toàn: bỏ qua tab mới, phím bổ trợ, tel/mailto, hash, tải file)
d.addEventListener('click',e=>{if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;const a=e.target.closest&&e.target.closest('a[href]');if(!a||a.target||a.hasAttribute('download'))return;
const u=new URL(a.href,location.href);if(u.origin!==location.origin||!/^https?:$/.test(u.protocol))return;if(u.pathname===location.pathname&&u.search===location.search)return;
e.preventDefault();h.classList.add('mv-leave');setTimeout(()=>location.href=u.href,170)});
addEventListener('pageshow',e=>{h.classList.remove('mv-leave')});
})();
