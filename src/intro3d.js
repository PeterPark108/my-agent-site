import {WebGLRenderer,Scene,PerspectiveCamera,BufferGeometry,BufferAttribute,Points,ShaderMaterial,AdditiveBlending,Mesh,PlaneGeometry,BoxGeometry,EdgesGeometry,LineSegments,LineBasicMaterial,MeshBasicMaterial,MeshStandardMaterial,CanvasTexture,SRGBColorSpace,Color,Group,PointLight,AmbientLight,MathUtils,Sprite,SpriteMaterial} from 'three';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import {EffectComposer} from 'three/examples/jsm/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/examples/jsm/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/examples/jsm/postprocessing/OutputPass.js';
import {Vector2,Vector3,NormalBlending,TorusGeometry,MeshPhysicalMaterial,PMREMGenerator,EquirectangularReflectionMapping,Shape,ShapeGeometry,Line} from 'three';

// v0.9.28: intro gắn vào trang chủ myagentvn.com, mọi thứ giới hạn trong #i3d (không chiếm cả trang)
const root=document.getElementById('i3d');if(!root)throw 0;
const Q=new URLSearchParams(location.search);
const CAPTURE=Q.has('capture');if(CAPTURE)root.classList.add('capture');
let REDUCE=matchMedia('(prefers-reduced-motion: reduce)').matches||Q.has('reduce');
const MOBILE=matchMedia('(max-width: 760px)').matches;
const TEAL=0x2ee6d6,BLUE=0x3a8bff,CORAL=0xff6b5e;

// ---------- loader (real steps + smooth display) ----------
// không có màn tải: chữ HTML hiện ngay (LCP), canvas mờ dần vào khi sẵn sàng
function step(p){if(p>=100){root.classList.add('gl-ready');window.__ready=true}}
root.classList.add('js');

// ---------- language ----------
const langBtn=document.getElementById('i3d-lang');let lang='vi';
langBtn.addEventListener('click',()=>{
  lang=lang==='vi'?'en':'vi';root.lang=lang;
  root.querySelectorAll('[data-vi]').forEach(el=>el.innerHTML=el.dataset[lang]);
  langBtn.innerHTML=lang==='vi'?'VI <span>/ EN</span>':'EN <span>/ VI</span>';
});

// ---------- theme ----------
let LIGHT=root.classList.contains('light');const themeHooks=[];
document.getElementById('i3d-theme').addEventListener('click',()=>{LIGHT=!LIGHT;root.classList.toggle('light',LIGHT);try{localStorage.setItem('ma-i3d-theme',LIGHT?'light':'dark')}catch(e){};themeHooks.forEach(f=>f())});
window.__setTheme=l=>{if(l!==LIGHT)document.getElementById('i3d-theme').click()};

// ---------- chuyển cảnh từng nấc (snap) ----------
const sections=[...root.querySelectorAll('.scene')];
const idx=document.getElementById('i3d-idx');
const N=sections.length,END=N-1;
const DUR=REDUCE?.25:1.2; // giây, mọi lần chuyển như nhau
const OUT=.4;            // 40% đầu: cảnh cũ mờ ra; 60% sau: cảnh mới hiện
const ease=u=>u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2; // easeInOutCubic
let vclock=0;const now=()=>CAPTURE?vclock:performance.now()/1000;
const S={cur:0,from:0,to:0,t0:-99,busy:false};
window.__log=[];
function go(i){
  i=MathUtils.clamp(i|0,0,END);
  if((S.busy&&now()-S.t0<DUR)||i===S.cur)return false;
  S.from=S.cur;S.to=i;S.t0=now();S.busy=true;S.cur=i;
  window.__log.push({ev:'start',from:S.from,to:i,t:performance.now()});
  updDots();return true;
}
window.__go=go;window.__state=()=>({cur:S.cur,busy:S.busy});
// tiến trình 0..1 của lần chuyển hiện tại
function tstate(){
  if(!S.busy)return{u:1,pos:S.cur};
  let u=(now()-S.t0)/DUR;
  if(u>=1){u=1;S.busy=false;window.__log.push({ev:'end',to:S.to,t:performance.now(),prev:window.__prevTick||0});}
  const e=ease(u);
  // giảm chuyển động: không bay camera, đổi cảnh tức thì khi chữ cũ đã mờ hết
  const pos=REDUCE?(u<OUT?S.from:S.to):S.from+(S.to-S.from)*e;
  return{u,pos};
}
function overlay(st){
  sections.forEach((s,i)=>{
    let o=0,dy=0;
    if(!S.busy||st.u>=1){o=i===S.cur?1:0}
    else if(i===S.from){const k=Math.min(1,st.u/OUT);o=1-ease(k);dy=-k*24*Math.sign(S.to-S.from)}
    else if(i===S.to){const k=Math.max(0,(st.u-OUT)/(1-OUT));o=ease(k);dy=(1-k)*24*Math.sign(S.to-S.from)}
    if(REDUCE)dy=0;
    s.classList.toggle('on',o>0);
    const cp=s.firstElementChild;cp.style.opacity=o.toFixed(3);cp.style.transform=dy?`translateY(${dy.toFixed(1)}px)`:'none';
    cp.style.setProperty('--hl',o>.6?1:0);s.style.setProperty('--fo',o.toFixed(3));
  });
  idx.textContent='0'+(S.cur+1);
}
// chấm điều hướng
const dotsEl=document.getElementById('i3d-dots');
sections.forEach((s,i)=>{const b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Cảnh '+(i+1));b.addEventListener('click',()=>go(i));dotsEl.appendChild(b)});
function updDots(){[...dotsEl.children].forEach((b,i)=>{b.classList.toggle('on',i===S.cur);b.toggleAttribute('aria-current',i===S.cur)})}
updDots();
root.querySelectorAll('a[href="#i3d"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();go(0)}));
// bánh xe: 1 nấc = 1 cảnh; bỏ qua khi đang chuyển và quán tính trackpad ngay sau đó
// chỉ bắt cuộn khi intro đang ở đầu trang; cảnh cuối + cuộn xuống = cuộn trang bình thường xuống nội dung đầy đủ
const atTop=()=>scrollY<4;
const wants=d=>atTop()&&!(d>0&&S.cur===END)&&!(d<0&&S.cur===0);
let wheelQuiet=0;
addEventListener('wheel',e=>{
  if(e.ctrlKey||!wants(e.deltaY))return;
  e.preventDefault();const t=performance.now();const quiet=t-wheelQuiet;wheelQuiet=t;
  if((S.busy&&now()-S.t0<DUR)||Math.abs(e.deltaY)<2)return;
  if(quiet<140&&window.__lastEnd&&t-window.__lastEnd<400)return; // đuôi quán tính
  go(S.cur+(e.deltaY>0?1:-1));
},{passive:false});
// vuốt
let ty=null,tx=0,cap=null;
addEventListener('touchstart',e=>{ty=e.touches[0].clientY;tx=e.touches[0].clientX;cap=atTop()?null:false},{passive:true});
addEventListener('touchmove',e=>{if(ty==null||cap===false)return;const dy=ty-e.touches[0].clientY;
  if(cap===null){if(Math.abs(dy)<6)return;cap=wants(dy)}
  if(cap&&e.cancelable)e.preventDefault()},{passive:false});
addEventListener('touchend',e=>{if(ty==null)return;const t=e.changedTouches[0];const dy=ty-t.clientY,dx=tx-t.clientX;ty=null;
  if(!cap)return;cap=null;
  if(Math.abs(dy)>Math.max(40,innerHeight*.06)&&Math.abs(dy)>Math.abs(dx))go(S.cur+(dy>0?1:-1))},{passive:true});
// bàn phím
addEventListener('keydown',e=>{
  if(e.target.closest&&e.target.closest('input,textarea,select,[contenteditable],nav,header,dialog'))return;
  if(e.altKey||e.ctrlKey||e.metaKey)return;
  const k=e.key;let d=null;
  if(k==='ArrowDown'||k==='PageDown'||(k===' '&&!e.shiftKey))d=S.cur+1;
  else if(k==='ArrowUp'||k==='PageUp'||(k===' '&&e.shiftKey))d=S.cur-1;
  else if(k==='Home')d=0;else if(k==='End')d=END;
  if(d==null||!wants(d-S.cur)||k==='Home'&&S.cur===0)return;if(k==='End'&&S.cur===END)return;e.preventDefault();go(d);
});
function tickUI(){const st=tstate();window.__prevTick=performance.now();if(!st.busy&&S.busy===false&&window.__wasBusy){window.__lastEnd=performance.now()}window.__wasBusy=S.busy;overlay(st);return st}
let uiOnly=true;
(function uiLoop(){if(!uiOnly||CAPTURE)return;tickUI();requestAnimationFrame(uiLoop)})();
overlay({u:1,pos:0});

// ---------- WebGL ----------
let renderer;
try{
  const cv=document.getElementById('i3d-gl');
  const gl=Q.has('nogl')?null:(cv.getContext('webgl2')||cv.getContext('webgl'));
  if(!gl)throw 0;
  renderer=new WebGLRenderer({canvas:cv,context:gl,antialias:false,alpha:false,powerPreference:'high-performance'});
}catch(e){root.classList.add('no-webgl');}

if(renderer){
const PR=CAPTURE?1:Math.min(devicePixelRatio||1,MOBILE?1.5:1.75);
renderer.setPixelRatio(PR);renderer.setClearColor(0x050b1a,1);renderer.outputColorSpace=SRGBColorSpace;
const scene=new Scene();
const VW=()=>root.clientWidth||innerWidth,VH=()=>root.clientHeight||innerHeight;
const camera=new PerspectiveCamera(MOBILE?52:42,VW()/VH(),.1,400);
const U={uTime:{value:0},uPR:{value:PR},uTw:{value:REDUCE?0:1}};
const D=26; // khoảng cách giữa các cảnh theo trục z

scene.add(new AmbientLight(0x6a8cff,.35));
const lT=new PointLight(TEAL,0,40,1.6),lC=new PointLight(CORAL,0,40,1.6); // v4: bỏ đèn điểm (gây chấm đỏ chói trên mép kính)

// stars
{
  const n=MOBILE?1400:2600,p=new Float32Array(n*3),s=new Float32Array(n),sd=new Float32Array(n),c=new Float32Array(n*3);
  const pal=[new Color(0xffffff),new Color(TEAL),new Color(0x9cc8ff),new Color(CORAL)];
  for(let i=0;i<n;i++){
    const a=Math.random()*6.283,r=6+Math.random()*40;
    p[i*3]=Math.cos(a)*r;p[i*3+1]=Math.sin(a)*r*.7;p[i*3+2]=20-Math.random()*(D*(N-1)+70);
    s[i]=.6+Math.random()*Math.random()*2.6;sd[i]=Math.random();
    const k=Math.random();const col=pal[k<.7?0:k<.88?1:k<.97?2:3];c.set([col.r,col.g,col.b],i*3);
  }
  const g=new BufferGeometry();g.setAttribute('position',new BufferAttribute(p,3));g.setAttribute('aSize',new BufferAttribute(s,1));g.setAttribute('aSeed',new BufferAttribute(sd,1));g.setAttribute('aColor',new BufferAttribute(c,3));
  const sm=new ShaderMaterial({uniforms:U,transparent:true,depthWrite:false,blending:AdditiveBlending,
    vertexShader:`attribute float aSize,aSeed;attribute vec3 aColor;uniform float uTime,uPR,uTw;varying vec3 vC;varying float vA;
void main(){vec4 mv=modelViewMatrix*vec4(position,1.);gl_Position=projectionMatrix*mv;
float tw=1.-uTw*.5*(.5+.5*sin(uTime*(.5+aSeed*2.5)+aSeed*50.));
gl_PointSize=min(aSize*uPR*(90./-mv.z),10.*uPR);vA=tw*smoothstep(.5,5.,-mv.z)*.85;vC=aColor;}`,
    fragmentShader:`uniform float uDark;varying vec3 vC;varying float vA;void main(){float d=length(gl_PointCoord-.5);float a=smoothstep(.5,0.,d);gl_FragColor=vec4(vC*uDark,a*a*vA);}`});
  sm.uniforms.uDark={value:1};scene.add(new Points(g,sm));themeHooks.push(()=>{sm.blending=LIGHT?NormalBlending:AdditiveBlending;sm.uniforms.uDark.value=LIGHT?.25:1;sm.needsUpdate=true});
}

// soft glow texture (cheap fake bloom)
function glowTex(hex){
  const c=document.createElement('canvas');c.width=c.height=128;const x=c.getContext('2d');
  const g=x.createRadialGradient(64,64,0,64,64,64);const col=new Color(hex);const rgb=`${col.r*255|0},${col.g*255|0},${col.b*255|0}`;
  g.addColorStop(0,`rgba(${rgb},.55)`);g.addColorStop(.35,`rgba(${rgb},.18)`);g.addColorStop(1,`rgba(${rgb},0)`);
  x.fillStyle=g;x.fillRect(0,0,128,128);const t=new CanvasTexture(c);t.colorSpace=SRGBColorSpace;return t;
}
const GT=glowTex(TEAL),GC=glowTex(CORAL),GB=glowTex(BLUE);
const glows=[];function glow(tex,sz,op=1){const m=new SpriteMaterial({map:tex,transparent:true,depthWrite:false,blending:AdditiveBlending,opacity:op});m.userData.op=op;glows.push(m);const s=new Sprite(m);s.scale.set(sz,sz,1);return s}

// nebula haze along the path
[[TEAL,9,-4,-8,30],[CORAL,-10,6,-30,26],[BLUE,10,-6,-58,34],[TEAL,-9,4,-84,28],[CORAL,8,5,-108,30],[BLUE,0,0,-136,40]].forEach(([c,x,y,z,s])=>{
  const g=glow(c===TEAL?GT:c===CORAL?GC:GB,s,.35);g.position.set(x,y,z);scene.add(g);
});

// ---------- v4: thiết bị kính mờ (glassmorphism 3D) ----------
const LITE_Q=Q.has('lite'),FULL_Q=Q.has('full')||CAPTURE;
const COARSE=matchMedia('(pointer: coarse)').matches;
let LITE=LITE_Q||(!FULL_Q&&(WEAK0()||(MOBILE&&COARSE)));
function WEAK0(){return MOBILE&&(navigator.hardwareConcurrency||4)<=4}
// envMap tự tạo: gradient nhỏ tím-cam-trắng → PMREM (cho mép kính phản chiếu)
const envTex=(()=>{const c=document.createElement('canvas');c.width=512;c.height=256;const x=c.getContext('2d');
  const g=x.createLinearGradient(0,0,0,256);g.addColorStop(0,'#c9c2f0');g.addColorStop(.48,'#6a63a8');g.addColorStop(.52,'#2a2752');g.addColorStop(1,'#0e0f24');x.fillStyle=g;x.fillRect(0,0,512,256);
  const blob=(X,Y,R,col)=>{const r=x.createRadialGradient(X,Y,0,X,Y,R);r.addColorStop(0,col);r.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=r;x.fillRect(0,0,512,256)};
  blob(110,95,70,'rgba(255,170,110,.65)');blob(370,90,80,'rgba(190,120,255,1)');blob(250,170,60,'rgba(90,160,255,.9)');
  x.fillStyle='#ffffff';[[40,40,46,90],[200,22,120,26],[300,60,26,80],[450,36,40,70]].forEach(([X,Y,W,H])=>{x.filter='blur(3px)';x.fillRect(X,Y,W,H)});x.filter='none';
  const t=new CanvasTexture(c);t.mapping=EquirectangularReflectionMapping;t.colorSpace=SRGBColorSpace;return t})();
const pmrem=new PMREMGenerator(renderer);const ENV=pmrem.fromEquirectangular(envTex).texture;pmrem.dispose();
const glassMats=[];
function glassMat(o={}){
  const m=new MeshPhysicalMaterial({color:0xffffff,metalness:0,roughness:o.r??.32,transmission:1,thickness:o.th??.7,ior:1.45,
    iridescence:.85,iridescenceIOR:1.3,iridescenceThicknessMinimum:250,iridescenceThicknessMaximum:520,clearcoat:1,clearcoatRoughness:.06,
    envMap:ENV,envMapIntensity:1.25,attenuationColor:new Color(0xd8d0ff),attenuationDistance:3,transparent:true,specularIntensity:1});
  m.userData.glass=1;glassMats.push(m);return m}
const GLASS=glassMat(),GLASS_THIN=glassMat({th:.2,r:.25});
// lõi màn hình: gradient navy → xanh sáng + vài khối UI mờ
function coreTex(kind,w,h){
  const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');
  const g=x.createLinearGradient(0,0,w*.7,h);g.addColorStop(0,'#16248f');g.addColorStop(.55,'#2d63e8');g.addColorStop(1,'#4fb6ff');x.fillStyle=g;x.fillRect(0,0,w,h);
  const r2=x.createRadialGradient(w*.75,h*.85,0,w*.75,h*.85,w*.8);r2.addColorStop(0,'rgba(140,220,255,.45)');r2.addColorStop(1,'rgba(140,220,255,0)');x.fillStyle=r2;x.fillRect(0,0,w,h);
  const u=Math.min(w,h)/100;x.fillStyle='rgba(255,255,255,.13)';
  const rr=(X,Y,W,H,r)=>{x.beginPath();x.roundRect(X,Y,W,H,r);x.fill()};
  if(kind==='web'){rr(8*u,8*u,w*.35,5*u,2.5*u);rr(8*u,18*u,w-16*u,h*.38,3*u);x.fillStyle='rgba(255,255,255,.09)';for(let i=0;i<3;i++)rr(8*u+i*(w-16*u)/3,h*.62,(w-16*u)/3-4*u,h*.26,3*u)}
  else if(kind==='shop'){rr(8*u,8*u,w-16*u,h*.2,3*u);x.fillStyle='rgba(255,255,255,.09)';for(let r=0;r<2;r++)for(let i=0;i<2;i++)rr(8*u+i*(w-16*u)/2,h*.32+r*h*.32,(w-16*u)/2-5*u,h*.27,4*u)}
  else if(kind==='app'){rr(10*u,10*u,w-20*u,h*.18,5*u);x.fillStyle='rgba(255,255,255,.09)';for(let i=0;i<4;i++)rr(10*u,h*.34+i*h*.14,w-20*u,h*.1,5*u)}
  else{x.fillStyle='rgba(255,255,255,.18)';[.35,.5,.42,.66,.58,.8].forEach((v,i)=>rr((10+i*14)*u,h-10*u-(h-26*u)*v,9*u,(h-26*u)*v,2*u))}
  const t=new CanvasTexture(c);t.colorSpace=SRGBColorSpace;return t}
const coreLines=[];
function roundRectShape(w,h,r){const s=new Shape();const x=-w/2,y=-h/2;s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);s.lineTo(x+w,y+h-r);s.quadraticCurveTo(x+w,y+h,x+w-r,y+h);s.lineTo(x+r,y+h);s.quadraticCurveTo(x,y+h,x,y+h-r);s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);return s}
function core(kind,w,h,r){
  const g=new Group();
  const m=new MeshBasicMaterial({map:coreTex(kind,Math.round(512*w/Math.max(w,h)),Math.round(512*h/Math.max(w,h))),toneMapped:false});
  const sh=roundRectShape(w,h,r);const geo=new ShapeGeometry(sh,8);
  // UV theo khung
  const pa=geo.attributes.position,uv=geo.attributes.uv;for(let i=0;i<pa.count;i++)uv.setXY(i,pa.getX(i)/w+.5,pa.getY(i)/h+.5);
  g.add(new Mesh(geo,m));
  const lm=new MeshBasicMaterial({color:0x9fe4ff,transparent:true,toneMapped:false});coreLines.push(lm);
  const bw=Math.min(w,h)*.022;const ring=roundRectShape(w,h,r);ring.holes.push(roundRectShape(w-bw*2,h-bw*2,Math.max(.01,r-bw)));
  const bm=new Mesh(new ShapeGeometry(ring,8),lm);bm.position.z=.002;g.add(bm);
  return g}
// slab kính dày bo tròn + lõi xanh nổi phía trước mặt kính
function slab(kind,W,H,D,R,inset=.13){
  const g=new Group();g.add(new Mesh(new RoundedBoxGeometry(W,H,D,4,R),GLASS));
  const c=core(kind,W-inset*2*Math.min(W,H)/1.2,H-inset*2*Math.min(W,H)/1.2,R*.7);c.position.z=D/2+.006;g.add(c);
  const gl=glow(GB,Math.max(W,H)*1.9,.35);gl.position.z=-D;g.add(gl);return g}
function shadowTex(){const c=document.createElement('canvas');c.width=c.height=128;const x=c.getContext('2d');const r=x.createRadialGradient(64,64,0,64,64,64);
  r.addColorStop(0,'rgba(110,100,255,.75)');r.addColorStop(.45,'rgba(140,120,255,.3)');r.addColorStop(1,'rgba(140,120,255,0)');x.fillStyle=r;x.fillRect(0,0,128,128);const t=new CanvasTexture(c);t.colorSpace=SRGBColorSpace;return t}
const SHT=shadowTex();const shadowMats=[];
function shadow(w,d){const m=new MeshBasicMaterial({map:SHT,transparent:true,depthWrite:false,opacity:.5});shadowMats.push(m);const s=new Mesh(new PlaneGeometry(w,d),m);s.rotation.x=-Math.PI/2;return s}
function laptop(kind){
  const g=new Group(),W=3.4,H=2.15;
  const base=new Mesh(new RoundedBoxGeometry(W,.16,2.3,4,.07),GLASS);g.add(base);
  const kb=core('kb',W*.78,1.2,.1);kb.rotation.x=-Math.PI/2;kb.position.set(0,.082,.15);kb.children[0].material.opacity=.35;kb.children[0].material.transparent=true;base.add(kb);
  const lid=new Group();lid.position.set(0,.06,-1.12);lid.rotation.x=-.22;g.add(lid);
  const s=slab(kind,W,H,.3,.15,.13);s.position.y=H/2;lid.add(s);
  const sh=shadow(W*1.6,3.2);sh.position.y=-.2;g.add(sh);return g}
function monitor(kind){
  const g=new Group(),W=3.9,H=2.45;
  const s=slab(kind,W,H,.32,.16,.11);s.position.y=1.45;g.add(s);
  const neck=new Mesh(new RoundedBoxGeometry(.38,1.0,.14,3,.06),GLASS);neck.position.set(0,.05,-.08);g.add(neck);
  const foot=new Mesh(new RoundedBoxGeometry(1.5,.09,.8,3,.04),GLASS);foot.position.set(0,-.42,0);g.add(foot);
  const sh=shadow(3.6,2.2);sh.position.y=-.5;g.add(sh);return g}
function tablet(kind){const g=slab(kind,1.95,2.65,.46,.23,.17);const sh=shadow(2.6,1.6);sh.position.y=-1.65;g.add(sh);return g}
function phone(kind){const g=slab(kind,1.1,2.2,.38,.19,.15);const sh=shadow(1.6,1.1);sh.position.y=-1.4;g.add(sh);return g}
// thẻ kính nhỏ: cột / donut / check
function iconTex(kind){const c=document.createElement('canvas');c.width=c.height=128;const x=c.getContext('2d');x.lineCap='round';
  if(kind==='bars'){x.fillStyle='#ff8a5c';x.beginPath();x.roundRect(14,14,22,20,5);x.fill();x.strokeStyle='#fff';x.lineWidth=4;x.beginPath();x.moveTo(19,24);x.lineTo(24,29);x.lineTo(31,19);x.stroke();
    x.fillStyle='#3d6bff';[.35,.5,.4,.75,.95,.55].forEach((v,i)=>{x.fillRect(22+i*15,110-70*v,10,70*v)});x.fillRect(18,112,94,3)}
  else if(kind==='donut'){x.lineWidth=16;x.strokeStyle='#bcd0ff';x.beginPath();x.arc(64,64,34,0,7);x.stroke();x.strokeStyle='#3d6bff';x.beginPath();x.arc(64,64,34,-1.57,2.6);x.stroke()}
  else{x.fillStyle='#ff8a5c';x.beginPath();x.roundRect(14,14,26,24,6);x.fill();x.strokeStyle='#fff';x.lineWidth=5;x.beginPath();x.moveTo(20,26);x.lineTo(26,32);x.lineTo(35,20);x.stroke();
    x.fillStyle='#3d8bff';x.beginPath();x.moveTo(34,70);x.lineTo(60,96);x.lineTo(104,48);x.lineTo(92,40);x.lineTo(60,76);x.lineTo(44,60);x.closePath();x.fill()}
  const t=new CanvasTexture(c);t.colorSpace=SRGBColorSpace;return t}
const ICONS={bars:iconTex('bars'),donut:iconTex('donut'),check:iconTex('check')};
const CARDGL=new MeshPhysicalMaterial({color:0xffffff,roughness:.3,metalness:0,transparent:true,opacity:.42,clearcoat:1,envMap:ENV,envMapIntensity:1.4,iridescence:.5,depthWrite:false});
function card(kind,s=.62){const g=new Group();g.add(new Mesh(new RoundedBoxGeometry(s,s,.07,3,.06),CARDGL));
  const f=new Mesh(new PlaneGeometry(s*.86,s*.86),new MeshBasicMaterial({map:ICONS[kind],transparent:true,toneMapped:false}));f.position.z=.04;g.add(f);g.userData.card=1;return g}
// vòng kính mảnh quỹ đạo
const RINGMAT=new MeshPhysicalMaterial({color:0xe8e4ff,roughness:.15,metalness:0,transparent:true,opacity:.75,clearcoat:1,envMap:ENV,envMapIntensity:1.8,iridescence:.8,iridescenceThicknessMinimum:300,iridescenceThicknessMaximum:600,emissive:0x6a6aff,emissiveIntensity:.05});
function orbit(R,tube=.028){const t=new Mesh(new TorusGeometry(R,tube,12,180),RINGMAT);t.rotation.set(1.28,0,.22);t.userData.orbit=1;return t}
function deco(g,R,cards){g.add(orbit(R));const cs=cards.map(([k,x,y,z,s])=>{const c=card(k,s);c.position.set(x,y,z);c.rotation.y=-x*.06;g.add(c);return c});g.userData.cards=cs}

// stations: [x,y] desktop offset of the cluster; mobile puts it below the copy
const side=[1,-1,1,-1,1,0];
const floaters=[];
function station(i,build){
  const g=new Group();build(g);
  const sx=MOBILE?(i===0?-.2:0):side[i]*(i===0?3.0:2.6), sy=MOBILE?(i===END?-1.75:-1.45):0;
  g.position.set(sx,sy,-i*D);Object.assign(g.userData,{i,base:g.position.clone(),ph:i*1.7});
  if(MOBILE)g.scale.setScalar(i===0?.58:i===END?.72:.85);
  if(!MOBILE&&i===0){g.scale.setScalar(.8);g.position.z-=2.2;g.userData.base.copy(g.position)}
  const mats=new Set();g.traverse(o=>{if(o.material){if(!o.material.userData.own){const was=o.material;o.material=was.clone();o.material.userData.own=1;o.material.userData.op=was.opacity;o.material.transparent=true;
    if(was.userData.glass){glassMats.push(o.material)}if(was.isSpriteMaterial)glows.push(o.material);if(coreLines.includes(was))coreLines.push(o.material);if(shadowMats.includes(was))shadowMats.push(o.material)}mats.add(o.material)}});
  g.userData.mats=[...mats];scene.add(g);floaters.push(g);return g;
}
// cùng 1 vật liệu trong 1 trạm được clone 1 lần → dùng map để không clone lặp
// 0 hero: laptop + tablet + điện thoại, vòng quỹ đạo, 3 thẻ kính
station(0,g=>{const l=laptop('web');l.rotation.set(.16,-.42,0);g.add(l);
  const t=tablet('shop');t.position.set(1.85,.25,.9);t.rotation.set(.05,-.38,0);t.scale.setScalar(.8);g.add(t);
  const p=phone('app');p.position.set(2.85,-.15,1.5);p.rotation.set(.05,-.35,0);p.scale.setScalar(.78);g.add(p);
  deco(g,3.6,[['bars',2.9,2.4,-.2,.8],['check',-2.5,1.6,.3,.62],['donut',3.9,-.6,.6,.6]])});
station(1,g=>{const m=monitor('web');m.position.y=-1.1;m.rotation.set(.1,.42,0);g.add(m);deco(g,3.3,[['bars',2.4,1.9,.2,.66],['donut',-2.6,-.9,.4,.58]])});
station(2,g=>{const t=tablet('shop');t.rotation.set(.05,-.45,.04);g.add(t);deco(g,2.4,[['check',-1.9,1.5,.3,.6],['donut',1.8,-1.2,.4,.55]])});
station(3,g=>{const p=phone('app');p.rotation.set(.05,.42,-.04);p.scale.setScalar(1.15);g.add(p);const p2=phone('web');p2.position.set(1.4,-.3,-.9);p2.rotation.set(.05,.3,.06);p2.scale.setScalar(.85);g.add(p2);
  deco(g,2.4,[['check',-1.7,1.6,.3,.58],['bars',2.2,1.5,-.2,.6]])});
station(4,g=>{const l=laptop('mkt');l.rotation.set(.18,-.45,0);g.add(l);const p=phone('app');p.position.set(2.0,-.2,1);p.rotation.set(.05,-.4,0);p.scale.setScalar(.7);g.add(p);
  deco(g,3.3,[['bars',-2.4,1.8,.3,.7],['donut',2.6,2.0,-.3,.58]])});
station(END,g=>{const ring=new Group();g.userData.ring=ring;g.add(ring);
  const R=MOBILE?2.25:4.6,n=6,make=[k=>laptop(['web','mkt'][k%2]),k=>tablet('shop'),k=>phone('app')];
  for(let k=0;k<n;k++){const a=k/n*Math.PI*2;const d=make[k%3](k);d.scale.setScalar(k%3===0?.42:.55);d.position.set(Math.cos(a)*R,Math.sin(a)*R*.62,Math.sin(a)*.8-1);d.rotation.y=-Math.cos(a)*.5;d.userData.a=a;d.traverse(o=>{if(o.material)o.material=o.material.clone()});ring.add(d)}
  const t1=orbit(R*.82,.03);t1.rotation.set(Math.PI/2-.0,0,0);t1.scale.set(1,.62,1);t1.rotation.x=0;t1.position.z=-1.6;t1.userData.orbit=0;g.add(t1);
  const t2=orbit(R*1.18,.02);t2.rotation.x=0;t2.scale.set(1,.62,1);t2.position.z=-2;t2.userData.orbit=0;g.add(t2);
  const gl=glow(GB,R*3.2,.3);gl.position.z=-3;g.add(gl);});
{const st=floaters[floaters.length-1];st.userData.ring.children.forEach(d=>{const ms=new Set();d.traverse(o=>{if(o.material)ms.add(o.material)});d.userData.mats=[...ms]});
 st.userData.mats=st.userData.mats.filter(m=>!st.userData.ring.children.some(d=>d.userData.mats.includes(m)))}
function setLite(on){LITE=on;root.classList.toggle('lite',on);
  glassMats.forEach(m=>{m.transmission=on?0:1;m.userData.op=on?.38:1;m.depthWrite=!on;m.needsUpdate=true});
  if(typeof applyTheme==='function')applyTheme()}
window.__setLite=setLite;
const endCopy=sections[END].querySelector('.copy');let txtR=null;const _v=new Vector3();
function txtRect(){const r=endCopy.getBoundingClientRect(),o=root.getBoundingClientRect();txtR={l:r.left-o.left,r:r.right-o.left,t:r.top-o.top,b:r.bottom-o.top}}
step(85);

// camera path
const camZ=i=>-i*D+(MOBILE?(i===END?9:10.5):9);
let p=0,mx=0,my=0,tmx=0,tmy=0;
addEventListener('pointermove',e=>{tmx=e.clientX/innerWidth-.5;tmy=e.clientY/innerHeight-.5},{passive:true});
const lightBg=(()=>{const c=document.createElement('canvas');c.width=256;c.height=4;const x=c.getContext('2d');const g=x.createLinearGradient(0,0,256,0);g.addColorStop(0,'#EFF2FB');g.addColorStop(.55,'#E4E0FA');g.addColorStop(1,'#CFC7F6');x.fillStyle=g;x.fillRect(0,0,256,4);const t=new CanvasTexture(c);t.colorSpace=SRGBColorSpace;return t})();
let GK=1;const WEAK=WEAK0();
const composer=new EffectComposer(renderer);composer.addPass(new RenderPass(scene,camera));
const bloom=new UnrealBloomPass(new Vector2(256,256),MOBILE?.22:.3,.3,.96);composer.addPass(bloom);composer.addPass(new OutputPass());
let useBloom=!WEAK;
function applyTheme(){
  scene.background=LIGHT?lightBg:null;
  coreLines.forEach(m=>{m.color.setHex(LIGHT?0x8fe0ff:0xa8e8ff).multiplyScalar(LIGHT?1:1.1)});
  shadowMats.forEach(m=>{m.blending=LIGHT?NormalBlending:AdditiveBlending;m.userData.op=LIGHT?.55:.22;m.needsUpdate=true});
  glows.forEach(m=>{m.blending=LIGHT?NormalBlending:AdditiveBlending;m.needsUpdate=true});
  GK=LIGHT?.3:.8;
  glassMats.forEach(m=>{m.emissive.setHex(LIGHT?0x000000:0x6a64b8);m.emissiveIntensity=LIGHT?0:.32;m.envMapIntensity=LIGHT?1.5:1.15});
  useBloom=!WEAK&&!LITE&&!LIGHT&&!Q.has('nobloom');
  // Ghi chú: qua EffectComposer (đo trên SwiftShader) màu bị mã hoá sRGB hai lần → nền bạc; dùng output tuyến tính khi bật bloom.
  renderer.outputColorSpace=useBloom?'srgb-linear':SRGBColorSpace;
  renderer.setClearColor(useBloom?0x1f2d4d:0x050b1a,1);
}
themeHooks.push(applyTheme);applyTheme();
function resize(){const w=VW(),h=VH();renderer.setSize(w,h,false);composer.setSize(w,h);bloom.resolution.set(w*(MOBILE?.5:.6),h*(MOBILE?.5:.6));camera.aspect=w/h;camera.updateProjectionMatrix()}
addEventListener('resize',()=>{resize();txtR=null});resize();langBtn.addEventListener('click',()=>txtR=null);

let running=!CAPTURE,last=performance.now(),time=0;
let autoDone=false;window.__fps=[];let fc=0,fl=performance.now();
function draw(dt,tp){
  time+=REDUCE?0:dt;U.uTime.value=time;
  p+=REDUCE||CAPTURE?(tp-p):(tp-p)*(1-Math.pow(.0015,dt));
  mx+=(tmx-mx)*.05;my+=(tmy-my)*.05;
  const f=p*(N-1),i0=Math.floor(f),fr=f-i0;
  const z=MathUtils.lerp(camZ(i0),camZ(Math.min(N-1,i0+1)),fr);
  const sway=Math.sin(fr*Math.PI)*(MOBILE?.6:1.4)*(i0%2?1:-1);
  camera.position.set(sway+mx*.6,-my*.4,z);camera.lookAt(sway*.4+mx*.2,-my*.15,z-10);
  lT.position.set(4,3,z-6);lC.position.set(-5,-2,z-10);
  const fl1=REDUCE?1:.9+.1*Math.sin(time*2.1)*Math.sin(time*.73+1);
  for(const g of floaters){const {base,ph,mats,ring}=g.userData;
    if(!REDUCE){g.position.y=base.y+Math.sin(time*.9+ph)*.14;g.rotation.y=Math.sin(time*.4+ph)*.08;g.rotation.x=Math.sin(time*.5+ph)*.03;
      g.children.forEach(o=>{if(o.userData.orbit)o.rotation.z=.22+time*.12});
      if(g.userData.cards)g.userData.cards.forEach((c,k)=>{c.userData.y0??=c.position.y;c.position.y=c.userData.y0+Math.sin(time*1.1+k*2)*.09;c.rotation.z=Math.sin(time*.7+k)*.05})}
    if(ring){const r=time*.12;ring.children.forEach(d=>{const a=d.userData.a+r,R=MOBILE?2.25:5.4;d.position.set(Math.cos(a)*R,Math.sin(a)*R*.62,Math.sin(a)*.8-1);d.rotation.y=-Math.cos(a)*.5;
      // thiết bị tới gần vùng chữ CTA thì mờ đi, không đi qua sau chữ
      d.getWorldPosition(_v).project(camera);const sx=(_v.x+1)/2*VW(),sy=(1-_v.y)/2*VH();if(!txtR)txtRect();
      const ddx=Math.max(txtR.l-sx,0,sx-txtR.r),ddy=Math.max(txtR.t-sy,0,sy-txtR.b);const dist=Math.min(Math.hypot(ddx,ddy),Math.max(0,sy-(MOBILE?40:56))*1.5);
      const pad=MOBILE?55:110;d.userData.k=MathUtils.smoothstep(dist,pad*.45,pad*1.35)})}
    // mờ dần theo khoảng cách: chỉ cảnh gần camera hiện rõ
    const dz=z-g.position.z;const fade=MathUtils.clamp(1-(dz-11)/9,0,1)*MathUtils.clamp((dz+1)/3,0,1);
    g.visible=fade>.01;if(g.visible)mats.forEach(m=>{m.opacity=(m.userData.op??1)*fade*(m.isSpriteMaterial?GK:1);});
    if(ring&&g.visible)ring.children.forEach(d=>{const kk=fade*d.userData.k;d.visible=kk>.01;d.userData.mats.forEach(m=>{m.opacity=(m.userData.op??1)*kk*(m.isSpriteMaterial?GK:1);})});
  }
  if(useBloom)composer.render();else renderer.render(scene,camera);
}
function frame(now){
  if(!running)return;requestAnimationFrame(frame);
  const dt=Math.min(.05,(now-last)/1000);last=now;draw(dt,tickUI().pos/(N-1));
  fc++;if(now-fl>=500){window.__fps.push(fc*1000/(now-fl));fc=0;fl=now;
    // đo 3 giây đầu: máy không kéo nổi kính khúc xạ thì tự chuyển chế độ rẻ
    if(!autoDone&&window.__fps.length>=7){autoDone=true;const a=window.__fps.slice(1).reduce((x,y)=>x+y,0)/(window.__fps.length-1);window.__autoFps=a;if(!LITE&&!FULL_Q&&a<24){setLite(true);window.__autoLite=true}}}
}
// chế độ dựng khung xác định cho quay video: __renderAt(t giây, p tiến độ 0..1)
let lastT=0;window.__renderAt=t=>new Promise(r=>requestAnimationFrame(()=>{vclock=t;const st=tickUI();draw(t-lastT,st.pos/(N-1));lastT=t;time=t;requestAnimationFrame(()=>r())}));
// dừng vẽ khi tab ẩn hoặc intro đã cuộn khuất (đỡ tốn pin/CPU khi đọc nội dung bên dưới)
let inView=true;
function setRun(){const r=!document.hidden&&inView&&!CAPTURE;if(r&&!running){running=true;last=performance.now();requestAnimationFrame(frame)}else running=r}
document.addEventListener('visibilitychange',setRun);
if('IntersectionObserver' in window)new IntersectionObserver(es=>{inView=es[es.length-1].isIntersecting;setRun()},{threshold:0}).observe(root);
window.__running=()=>running;
uiOnly=false;if(LITE)setLite(true);renderer.compile(scene,camera);draw(0,0);step(100);
if(!CAPTURE)requestAnimationFrame(frame);
}
