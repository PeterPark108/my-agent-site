'use client';
import { useEffect,useState,useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
const subscribeHost=()=>()=>{};
const getHost=()=>document.getElementById('quote-export-host');
const serverHost=()=>null;
function selection(){const items=Array.from(document.querySelectorAll<HTMLElement>('.bg-svc')).filter(el=>el.querySelector<HTMLInputElement>('input[type=checkbox]')?.checked).map(el=>({serviceId:el.dataset.id,tierId:el.querySelector<HTMLSelectElement>('.tier')?.value,complexity:el.querySelector<HTMLSelectElement>('.cx')?.value||'tieu-chuan',quantity:Number(el.querySelector<HTMLInputElement>('.qty')?.value||0),budgetNote:el.querySelector<HTMLInputElement>('.budget')?.value||''}));return {items,rush:(document.getElementById('bg-rush') as HTMLSelectElement)?.value||'binh-thuong',prepay:(document.getElementById('bg-prepay') as HTMLSelectElement)?.value||'monthly'}}
export function QuoteExport(){
 const host=useSyncExternalStore(subscribeHost,getHost,serverHost);
 const [busy,setBusy]=useState(false),[message,setMessage]=useState('');
 useEffect(()=>{function prefill(){const values=new URLSearchParams(location.search).get('dv')?.split(',')||[];values.forEach(id=>{if(!/^[a-z0-9-]+$/.test(id))return;const box=document.getElementById('bg-'+id) as HTMLInputElement|null;if(box){box.checked=true;box.dispatchEvent(new Event('change',{bubbles:true}))}})}window.addEventListener('myagent:pricing-ready',prefill);if(document.querySelector('.bg-svc'))prefill();return()=>window.removeEventListener('myagent:pricing-ready',prefill)},[]);
 async function download(){
  const chosen=selection();if(!chosen.items.length){setMessage('Hãy chọn ít nhất một dịch vụ trước khi xuất PDF.');return}
  setBusy(true);setMessage('Đang tạo PDF báo giá…');
  try{const [{createQuotePdf},{normalizeSelection}]=await Promise.all([import('@/lib/quote-pdf'),import('@/lib/quote')]);const bytes=await createQuotePdf(normalizeSelection(chosen));const blob=new Blob([bytes as BlobPart],{type:'application/pdf'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='My-Agent-Bao-gia-tham-khao.pdf';document.body.appendChild(a);a.click();setTimeout(()=>{a.remove();URL.revokeObjectURL(url)},60000);setMessage('Đã tạo PDF theo lựa chọn hiện tại. Giá chưa bao gồm VAT.')}catch{setMessage('Chưa tạo được PDF. Vui lòng thử lại; các lựa chọn của bạn vẫn được giữ.')}finally{setBusy(false)}
 }
 if(!host)return null;
 return createPortal(<div className="quote-export"><button className="content-button pdf-export-button" type="button" disabled={busy} onClick={download}>{busy?'Đang tạo PDF…':'Tải PDF báo giá'}<span aria-hidden="true">↓</span></button><p role="status" aria-live="polite">{message||'PDF gồm hạng mục đã chọn, chiết khấu, phụ phí và các khoản thương lượng.'}</p></div>,host);
}
