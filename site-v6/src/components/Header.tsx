'use client';
/* eslint-disable @next/next/no-html-link-for-pages -- Full navigation resets legacy tool listeners. */
import Image from 'next/image';
import { useAnchorNavigation } from './useAnchorNavigation';
import { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { usePathname } from 'next/navigation';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(useGSAP);
const links=[['/dich-vu.html','Dịch vụ'],['/du-an.html','Sản phẩm mẫu'],['/bang-gia.html','Bảng giá'],['/blog.html','Kiến thức'],['/tin-tuc.html','Tin công nghệ']];
const more=[['/dich-vu.html','Tất cả dịch vụ'],['/combo.html','Combo dịch vụ'],['/bang-gia.html','Bảng giá & tính giá'],['/du-an.html','Sản phẩm mẫu'],['/tra-cuu-tien-do.html','Tra cứu tiến độ'],['/tin-tuc.html','Tin công nghệ'],['/blog.html','Blog / Kiến thức'],['/cong-cu.html','Công cụ miễn phí'],['/tai-nguyen-ai-agent.html','Tài nguyên AI Agent'],['/ve-chung-toi.html','Về My Agent'],['/lien-he.html','Liên hệ đầy đủ'],['/dieu-khoan-dich-vu.html','Điều khoản & dịch vụ'],['/chinh-sach-bao-mat.html','Chính sách bảo mật']];
function readTheme(){try{return localStorage.getItem('ma-theme')==='light'?'light':'dark'}catch{return 'dark'}}
function subscribeTheme(callback:()=>void){window.addEventListener('myagent:theme',callback);window.addEventListener('storage',callback);return()=>{window.removeEventListener('myagent:theme',callback);window.removeEventListener('storage',callback)}}

export function Header() {
 const [open,setOpen]=useState(false);
 const root=useRef<HTMLElement>(null);
 const menuButton=useRef<HTMLButtonElement>(null);
 const nav=useRef<HTMLElement>(null);
 const pathname=usePathname();
 const theme=useSyncExternalStore(subscribeTheme,readTheme,()=> 'dark');
 useAnchorNavigation();
 useEffect(()=>{document.documentElement.dataset.theme=theme},[theme]);
 useGSAP(()=>{
  if(!open||!nav.current)return;
  const mm=gsap.matchMedia();
  mm.add('(prefers-reduced-motion: no-preference)',()=>{
   gsap.timeline({defaults:{duration:.2,ease:'power2.out',clearProps:'transform,opacity'}})
    .fromTo(nav.current,{opacity:.6,y:-6},{opacity:1,y:0});
  },root);
  return()=>mm.revert();
 },{scope:root,dependencies:[open],revertOnUpdate:true});
 useEffect(()=>{
  if(!open)return;
  const previousOverflow=document.body.style.overflow;
  document.body.style.overflow='hidden';
  nav.current?.querySelector<HTMLAnchorElement>('a')?.focus();
  const close=(restore=true)=>{setOpen(false);if(restore)menuButton.current?.focus();};
  const keyboard=(event:KeyboardEvent)=>{
   if(event.key==='Escape'){event.preventDefault();close();return;}
   if(event.key!=='Tab')return;
   const items=Array.from(root.current?.querySelectorAll<HTMLElement>('a[href],button,summary')??[]).filter(el=>el.getClientRects().length>0);
   const first=items[0],last=items[items.length-1];
   if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}
   else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
  };
  const wide=matchMedia('(min-width:1051px)');
  const resize=()=>{if(wide.matches)close(false);};
  document.addEventListener('keydown',keyboard);
  wide.addEventListener('change',resize);
  const inertElements=Array.from(document.body.children).filter(el=>el instanceof HTMLElement&&!el.contains(root.current)&&!['SCRIPT','STYLE','LINK'].includes(el.tagName)) as HTMLElement[];
  const previousInert=inertElements.map(el=>el.inert);
  inertElements.forEach(el=>{el.inert=true;});
  return()=>{document.body.style.overflow=previousOverflow;document.removeEventListener('keydown',keyboard);wide.removeEventListener('change',resize);inertElements.forEach((el,i)=>{el.inert=previousInert[i];});};
 },[open]);
 function toggleTheme(){const next=theme==='dark'?'light':'dark';document.documentElement.dataset.theme=next;try{localStorage.setItem('ma-theme',next)}catch{}window.dispatchEvent(new Event('myagent:theme'));}
 function current(href:string){return pathname===href||((href==='/blog.html'||href==='/tin-tuc.html'||href==='/dich-vu.html')&&pathname.startsWith(href.replace('.html','/')));}
 return <header ref={root} className="header" data-shared-shell="v6"><div className="container header-inner">
  <a href="/" aria-label="My Agent — trang chủ"><Image priority src={theme==='light'?'/assets/logo.svg':'/brand/logo-dark.svg'} alt="My Agent" width={163} height={40}/></a>
  <button ref={menuButton} className="menu-button" type="button" aria-expanded={open} aria-controls="navigation" onClick={()=>setOpen(!open)}>{open?'Đóng':'Menu'}<span aria-hidden="true">{open?'−':'+'}</span></button>
  <nav ref={nav} id="navigation" aria-label="Điều hướng chính" className={open?'navigation open':'navigation'}>
   {links.map(([href,label])=><a href={href} key={href} aria-current={current(href)?'page':undefined} onClick={()=>setOpen(false)}>{label}</a>)}
   <details className="all-pages-menu" onKeyDown={event=>{if(event.key==='Escape'){event.currentTarget.open=false;event.currentTarget.querySelector('summary')?.focus();}}}><summary>Khám phá <span aria-hidden="true">⌄</span></summary><div className="all-pages-panel">{more.map(([href,label])=><a href={href} key={href} onClick={()=>setOpen(false)}>{label}</a>)}</div></details>
   <a className="mobile-nav-cta" href="/lien-he.html" onClick={()=>setOpen(false)}>Trao đổi dự án ↗</a>
  </nav>
  <a className="header-cta" href="/lien-he.html">Trao đổi dự án <span aria-hidden="true">↗</span></a>
  <button className="theme-button" type="button" aria-label={'Chuyển sang giao diện '+(theme==='dark'?'sáng':'tối')} onClick={toggleTheme}>{theme==='dark'?'☼':'☾'}</button>
 </div></header>;
}
