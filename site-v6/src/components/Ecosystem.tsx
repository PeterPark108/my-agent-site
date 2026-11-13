'use client';
import { useRef, useState } from 'react';
import gsap from 'gsap';
import { Flip } from 'gsap/Flip';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(Flip, ScrollTrigger, useGSAP);
const groups=[
 {id:'website',label:'Website & hạ tầng',code:'01',title:'Nền tảng cho thương hiệu số.',description:'Từ website đầu tiên đến hạ tầng để vận hành lâu dài.',items:[['Thiết kế website','thiet-ke-website'],['Hosting SEO','hosting-seo'],['Tên miền','ten-mien'],['Email doanh nghiệp','email-doanh-nghiep'],['Chăm sóc website','cham-soc-website']]},
 {id:'growth',label:'Marketing & tăng trưởng',code:'02',title:'Kết nối website với khách hàng.',description:'Các dịch vụ hiện có trên My Agent cho tìm kiếm, quảng cáo và hiện diện trực tuyến.',items:[['SEO tổng thể','seo-tong-the'],['Google & Facebook Ads','quang-cao-google-facebook'],['Traffic User','traffic-user'],['Google Maps','google-maps']]},
 {id:'content',label:'Nội dung & mạng xã hội',code:'03',title:'Một tiếng nói thương hiệu nhất quán.',description:'Nội dung và điểm chạm trên những kênh doanh nghiệp đang sử dụng.',items:[['Edit Video · Video AI','video-ai'],['Chăm sóc Fanpage','cham-soc-fanpage'],['Zalo OA · Mini App','zalo-oa-mini-app'],['Profile doanh nghiệp','profile-doanh-nghiep']]},
 {id:'software',label:'Dữ liệu & phần mềm',code:'04',title:'Từ dữ liệu đến công cụ vận hành.',description:'Khám phá dịch vụ dữ liệu, web app và phần mềm theo nhu cầu.',items:[['Data Analyst','phan-tich-du-lieu'],['Data Engineer','ky-thuat-du-lieu'],['Phần mềm nội bộ Agency','phan-mem-noi-bo'],['Thiết kế App','thiet-ke-app']]},
 {id:'legal',label:'Thủ tục & combo',code:'05',title:'Hoàn thiện những phần còn lại.',description:'Xem dịch vụ thủ tục và cách kết hợp các hạng mục trên website hiện tại.',items:[['Đăng ký Bộ Công Thương','bo-cong-thuong'],['Khám phá combo','@combo']]},
];
export function Ecosystem(){
 const [selected,setSelected]=useState(0);
 const root=useRef<HTMLElement>(null);
 const indicator=useRef<HTMLSpanElement>(null);
 const previous=useRef<ReturnType<typeof Flip.getState>|null>(null);
 const refs=useRef<(HTMLButtonElement|null)[]>([]);
 // Capturing geometry creates no animation; the effect owns the Flip tween.
 const choose=(index:number)=>{
  if(index===selected)return;
  if(indicator.current)previous.current=Flip.getState(indicator.current);
  setSelected(index);
 };
 useGSAP(()=>{
  const mm=gsap.matchMedia();
  mm.add({all:'all',reduce:'(prefers-reduced-motion: reduce)'},context=>{
   const button=refs.current[selected],mark=indicator.current;
   const panel=root.current?.querySelector<HTMLElement>('[role=tabpanel]:not([hidden])');
   if(!button||!mark||!panel)return;
   let geometry='';
   const align=()=>{
    const box={x:button.offsetLeft,y:button.offsetTop,width:button.offsetWidth,height:button.offsetHeight};
    const signature=JSON.stringify(box);
    if(signature===geometry)return;
    geometry=signature;
    gsap.set(mark,box);
   };
   // One marker moves between tabs; the buttons retain native keyboard behavior.
   align();
   if(!context.conditions?.reduce){
    if(previous.current)Flip.from(previous.current,{duration:.42,ease:'power3.out',scale:true});
    gsap.fromTo(panel.children,{y:10,opacity:0},{y:0,opacity:1,duration:.35,stagger:.045,ease:'power2.out',clearProps:'transform,opacity'});
   }
   previous.current=null;
   const refresh=gsap.delayedCall(.15,()=>ScrollTrigger.refresh());
   const resize=new ResizeObserver(()=>{context.add(align);refresh.restart(true)});
   resize.observe(button.parentElement!);
   return()=>{resize.disconnect()};
  },root);
  return()=>mm.revert();
 },{scope:root,dependencies:[selected],revertOnUpdate:true});
 return <section ref={root} id="he-sinh-thai" className="section container ecosystem" aria-labelledby="ecosystem-title"><div className="section-heading" data-reveal><p className="eyebrow">HỆ SINH THÁI MY AGENT</p><h2 id="ecosystem-title">Một đối tác.<br/><span className="muted">Nhiều điểm kết nối.</span></h2><p>Không dừng ở một giao diện đẹp. Khám phá các nhóm dịch vụ đang có trên My Agent.</p></div><div className="ecosystem-console glass-panel"><div className="ecosystem-tabs" role="tablist" aria-label="Nhóm dịch vụ" aria-orientation="vertical"><span ref={indicator} className="ecosystem-indicator" aria-hidden="true"/>{groups.map((g,i)=><button key={g.id} id={'tab-'+g.id} ref={el=>{refs.current[i]=el}} role="tab" aria-selected={selected===i} aria-controls={'panel-'+g.id} tabIndex={selected===i?0:-1} onClick={()=>choose(i)} onKeyDown={e=>{let next=i;if(e.key==='ArrowDown'||e.key==='ArrowRight')next=gsap.utils.wrap(0,groups.length,i+1);else if(e.key==='ArrowUp'||e.key==='ArrowLeft')next=gsap.utils.wrap(0,groups.length,i-1);else if(e.key==='Home')next=0;else if(e.key==='End')next=groups.length-1;else return;e.preventDefault();choose(next);refs.current[next]?.focus()}}><span>{g.code}</span>{g.label}<b aria-hidden="true">↗</b></button>)}</div><div className="ecosystem-panels">{groups.map((g,i)=><div key={g.id} role="tabpanel" id={'panel-'+g.id} aria-labelledby={'tab-'+g.id} hidden={selected!==i} tabIndex={0} className="ecosystem-panel"><span className="console-label">MY AGENT / {g.id.toUpperCase()}</span><h3>{g.title}</h3><p>{g.description}</p><div className="ecosystem-links">{g.items.map(([label,slug])=><a href={slug==='@combo'?'/combo.html':'/dich-vu/'+slug+'.html'} key={slug}>{label}<span aria-hidden="true">↗</span></a>)}</div><div className="console-footnote">Phạm vi và chi phí được trao đổi theo từng nhu cầu.</div></div>)}</div></div></section>}
