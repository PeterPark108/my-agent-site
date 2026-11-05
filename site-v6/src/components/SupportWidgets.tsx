 'use client';
import Script from 'next/script';
import { useEffect,useRef,useState } from 'react';
export function SupportWidgets(){
 const [open,setOpen]=useState(false);const toggle=useRef<HTMLButtonElement>(null);const panel=useRef<HTMLDivElement>(null);
 useEffect(()=>{if(open)panel.current?.querySelector<HTMLElement>('a,button')?.focus();},[open]);
 function close(){setOpen(false);toggle.current?.focus();}
 return <><Script src="/js/config.js" strategy="afterInteractive" onLoad={()=>{const script=document.createElement('script');script.src='/js/chat.js';script.id='myagent-mj-script';script.async=true;if(!document.getElementById(script.id))document.body.appendChild(script)}}/>
 <aside className="support-actions" aria-label="Liên hệ nhanh" onKeyDown={e=>{if(e.key==='Escape'){e.stopPropagation();close()}}}>
 <div ref={panel} id="support-panel" className="support-panel" hidden={!open}>
 <a className="support-call" href="tel:0328439972">Gọi 0328 439 972</a>
 <a className="support-zalo" href="https://zalo.me/0328439972" target="_blank" rel="noopener noreferrer">Chat Zalo ↗</a>
 <button type="button" onClick={()=>{toggle.current?.focus();document.querySelector<HTMLButtonElement>('.mj-btn')?.click();setOpen(false)}}>Hỏi trợ lý MJ</button>
 <button type="button" onClick={close}>Đóng kết nối</button>
 </div>
 <button className="support-toggle" ref={toggle} type="button" aria-controls="support-panel" aria-expanded={open} onClick={()=>open?close():setOpen(true)}>Kết nối <span aria-hidden="true">{open?'×':'+'}</span></button>
 </aside></>;
}
