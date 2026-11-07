'use client';
import Image from 'next/image';
import { featuredProjects } from '@/content/featured-projects';
import { useRef,useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(ScrollTrigger,useGSAP);
const projects = featuredProjects;
export function ProjectShowcase(){const root=useRef<HTMLElement>(null);const timeline=useRef<gsap.core.Timeline|null>(null);const [active,setActive]=useState(0);const [enhanced,setEnhanced]=useState(false);
 useGSAP(()=>{const mm=gsap.matchMedia();mm.add('(min-width: 1100px) and (min-height: 760px) and (prefers-reduced-motion: no-preference)',()=>{
  const cards=gsap.utils.toArray<HTMLElement>('.project-card');gsap.set('.project-stack',{height:'clamp(420px,58vh,600px)'});gsap.set(cards,{position:'absolute',inset:0,minHeight:0});cards.forEach((c,i)=>gsap.set(c,{zIndex:i+1}));gsap.set(cards.slice(1),{yPercent:105});
  const tl=gsap.timeline({scrollTrigger:{trigger:'.project-screen',start:'top 110px',end:()=>'+='+window.innerHeight*1.6,pin:true,scrub:.65,invalidateOnRefresh:true},onUpdate:()=>{let n=0;for(let i=1;i<cards.length;i++)if(tl.time()>=(tl.labels['project-'+i]??Infinity))n=i;setActive(n)}});timeline.current=tl;
  tl.addLabel('project-0').to({}, {duration:.35});
  cards.slice(1).forEach((card,i)=>tl.to(card,{yPercent:0,duration:.9,ease:'power2.inOut'}).addLabel('project-'+(i+1)).to('.electric-edge',{opacity:.8,duration:.08}).to('.electric-edge',{opacity:0,duration:.24}).to({}, {duration:.35}));
  setEnhanced(true);return ()=>{timeline.current=null;setEnhanced(false)};
 });return ()=>mm.revert()},{scope:root});
 useGSAP(()=>{
  if(enhanced)return;
  const mm=gsap.matchMedia();
  mm.add('(prefers-reduced-motion: no-preference)',()=>{
   const card=root.current?.querySelector<HTMLElement>('.project-card[data-active=true]');
   if(card)gsap.fromTo(card,{opacity:.45,y:12},{opacity:1,y:0,duration:.38,ease:'power2.out',clearProps:'opacity,transform'});
   // Card copy/imagery can change the height of the section.
   gsap.delayedCall(.05,()=>ScrollTrigger.refresh());
  },root);
  return()=>mm.revert();
 },{scope:root,dependencies:[active,enhanced],revertOnUpdate:true});
 function go(i:number){
  const tl=timeline.current;
  if(tl?.scrollTrigger){
   ScrollTrigger.refresh();const trigger=tl.scrollTrigger;
   const time=(tl.labels['project-'+i]??0)+(i>0?.33:.03);
   const position=time/tl.duration();
   window.scrollTo({top:trigger.start+(trigger.end-trigger.start)*position,behavior:'instant'});
   tl.time(time);ScrollTrigger.update();
  }
  setActive(i);
 }

 return <section id="trai-nghiem" className="section showcase" aria-labelledby="showcase-title" ref={root}><div className="container"><div className="work-heading"><div className="section-heading" data-reveal><p className="eyebrow">02 / SẢN PHẨM MẪU</p><h2 id="showcase-title">Năng lực được nhìn thấy.<br/><span className="muted">Qua sản phẩm chạy được.</span></h2><p>Sản phẩm mẫu do Peter tự thiết kế và phát triển, được giới thiệu trên My Agent. Không phải dự án khách hàng.</p></div><a className="text-link" href="/du-an.html">Xem toàn bộ portfolio ↗</a></div><div className="project-screen"><div className="screen-toolbar"><span><i/> MY AGENT / SELECTED DEMOS</span><a href="#quy-trinh">BỎ QUA PHẦN CUỘN ↓</a></div><div className="project-stack" data-layered={enhanced}>{projects.map((p,i)=><article className="project-card real-project" key={p.id} aria-hidden={active!==i} inert={active!==i} data-active={active===i} data-layered={enhanced}><div className="real-project-top"><div><span className="project-kicker">{p.category}</span><h3>{p.name}</h3></div><span className="demo-badge">DỰ ÁN MẪU / {p.id}</span></div><div className="project-image"><Image src={p.image} alt={p.alt} width={1600} height={900} sizes="(max-width:700px) 90vw, 1200px" loading="lazy"/></div><div className="real-project-bottom"><p>{p.description}</p><div className="tags">{p.tags.map(t=><span key={t}>{t}</span>)}</div></div></article>)}</div><div className="project-navigation"><p className="sr-only" role="status" aria-live="polite">{projects[active].name} · {active+1}/{projects.length}</p><div className="project-select" role="group" aria-label="Chọn sản phẩm mẫu">{projects.map((p,i)=><button key={p.id} type="button" aria-pressed={active===i} onClick={()=>go(i)}><span>{p.id}</span>{p.name}</button>)}</div><a className="demo-live-link" href={projects[active].href} target="_blank" rel="noopener noreferrer">Mở demo {projects[active].name} ↗</a></div><div className="led-scan" aria-hidden="true"/><div className="electric-edge" aria-hidden="true"/></div><p className="portfolio-note">Dữ liệu, sản phẩm và đặt phòng trong các demo chỉ để minh họa. Bản chạy trên hosting miễn phí có thể khởi động chậm.</p></div></section>
}
