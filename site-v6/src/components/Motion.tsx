'use client';
import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(ScrollTrigger,useGSAP);
export function Motion({children}:{children:React.ReactNode}){
 const root=useRef<HTMLDivElement>(null);
 useGSAP(()=>{
  const media=gsap.matchMedia();
  media.add('(prefers-reduced-motion: no-preference)',()=>{
   gsap.from('[data-intro]',{y:24,opacity:0,stagger:0.09,duration:0.8,ease:'power3.out',clearProps:'all'});
   gsap.utils.toArray<HTMLElement>('[data-reveal]').forEach(el=>gsap.from(el,{y:32,opacity:0,duration:0.7,ease:'power2.out',scrollTrigger:{trigger:el,start:'top 92%',once:true},clearProps:'all'}));
   // Motion wrappers preserve the CSS perspective of each glass ring.
   const ambience=gsap.timeline();
   ambience.to('.orbit-float-one',{y:-46,x:14,rotation:8,duration:4.6,repeat:-1,yoyo:true,ease:'sine.inOut'},0)
    .to('.orbit-float-two',{y:40,x:-20,rotation:-10,duration:5.7,repeat:-1,yoyo:true,ease:'sine.inOut'},0)
    .to('.orb',{y:-12,duration:5,repeat:-1,yoyo:true,ease:'sine.inOut'},0)
;
   // A single light-on pulse each 3 seconds, without a rapid strobe.
   const light=gsap.timeline({repeat:-1,repeatDelay:2.5});
   light.to('.orb-mark',{opacity:.25,duration:.12,ease:'power1.in'}).to('.orb-mark',{opacity:1,duration:.38,ease:'power3.out'});
   ScrollTrigger.create({trigger:'.hero-stage',start:'top bottom',end:'bottom top',onToggle:self=>{
    [ambience,light].forEach(animation=>self.isActive?animation.resume():animation.pause());
   }});
   gsap.from('.hero-art',{scale:.86,opacity:0,rotation:-5,duration:1.5,ease:'power3.out'});

   const type=gsap.timeline({scrollTrigger:{trigger:'.type-heading',start:'top 78%',once:true}});
   type.from('.type-heading .type-char',{opacity:0,clipPath:'inset(0 100% 0 0)',duration:.025,stagger:.035,ease:'none',clearProps:'all'});
   gsap.from('[data-service]',{y:70,rotationX:-9,opacity:0,stagger:.16,duration:.85,ease:'power3.out',scrollTrigger:{trigger:'.service-list',start:'top 88%',once:true},clearProps:'all'});
   gsap.utils.toArray<HTMLElement>('.glass-icon').forEach(icon=>{
    const float=gsap.to(icon.querySelector('.icon-plate'),{y:-12,rotation:8,duration:3.2,repeat:-1,yoyo:true,ease:'sine.inOut'});
    const orbit=gsap.to(icon.querySelector('.icon-orbit'),{rotation:35,duration:5,repeat:-1,yoyo:true,ease:'sine.inOut'});
    ScrollTrigger.create({trigger:icon,start:'top bottom',end:'bottom top',onToggle:self=>[float,orbit].forEach(a=>self.isActive?a.resume():a.pause())});
   });

  });
  return ()=>media.revert();
 },{scope:root});
 return <div ref={root}>{children}</div>;
}
