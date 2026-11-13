'use client';
import { useEffect,useRef,useState,useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
const subscribeHost=()=>()=>{};
const getHost=()=>document.getElementById('quote-export-host');
const serverHost=()=>null;
function selection(){const items=Array.from(document.querySelectorAll<HTMLElement>('.bg-svc')).filter(el=>el.querySelector<HTMLInputElement>('input[type=checkbox]')?.checked).map(el=>({serviceId:el.dataset.id,tierId:el.querySelector<HTMLSelectElement>('.tier')?.value,complexity:el.querySelector<HTMLSelectElement>('.cx')?.value||'tieu-chuan',quantity:Number(el.querySelector<HTMLInputElement>('.qty')?.value||0),budgetNote:el.querySelector<HTMLInputElement>('.budget')?.value||''}));return {items,rush:(document.getElementById('bg-rush') as HTMLSelectElement)?.value||'binh-thuong',prepay:(document.getElementById('bg-prepay') as HTMLSelectElement)?.value||'monthly'}}
type Summary={total:string;items:{id:string;label:string}[];lines:string[]};
export function QuoteExport(){
 const host=useSyncExternalStore(subscribeHost,getHost,serverHost);
 const [busy,setBusy]=useState(false),[message,setMessage]=useState('');
 const [summary,setSummary]=useState<Summary>({total:'Chưa chọn dịch vụ',items:[],lines:[]});
 const dialog=useRef<HTMLDialogElement>(null);const detailsButton=useRef<HTMLButtonElement>(null);
 useEffect(()=>{
  function update(){setSummary({total:document.getElementById('bg-total')?.textContent||'Chưa chọn dịch vụ',items:Array.from(document.querySelectorAll<HTMLElement>('.bg-svc.on')).map(el=>({id:el.dataset.id||'',label:el.querySelector('.bg-h span')?.childNodes[0]?.textContent?.trim()||'Dịch vụ'})),lines:Array.from(document.querySelectorAll('#bg-detail .row')).map(el=>el.textContent||'')})}
  function prefill(){const values=new URLSearchParams(location.search).get('dv')?.split(',')||[];values.forEach(id=>{if(!/^[a-z0-9-]+$/.test(id))return;const box=document.getElementById('bg-'+id) as HTMLInputElement|null;if(box){box.checked=true;box.dispatchEvent(new Event('change',{bubbles:true}))}});update()}
  window.addEventListener('myagent:pricing-ready',prefill);window.addEventListener('myagent:quote-updated',update);
  if(document.querySelector('.bg-svc'))prefill();
  return()=>{window.removeEventListener('myagent:pricing-ready',prefill);window.removeEventListener('myagent:quote-updated',update)};
 },[]);
 function remove(id:string){const box=document.getElementById('bg-'+id) as HTMLInputElement|null;if(box){box.checked=false;box.dispatchEvent(new Event('change',{bubbles:true}))}}
 async function download(){
  const chosen=selection();if(!chosen.items.length){setMessage('Hãy chọn ít nhất một dịch vụ trước khi xuất PDF.');return}
  setBusy(true);setMessage('Đang tạo PDF báo giá…');
  try{const [{createQuotePdf},{normalizeSelection}]=await Promise.all([import('@/lib/quote-pdf'),import('@/lib/quote')]);const bytes=await createQuotePdf(normalizeSelection(chosen));const blob=new Blob([bytes as BlobPart],{type:'application/pdf'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='My-Agent-Bao-gia-tham-khao.pdf';document.body.appendChild(a);a.click();setTimeout(()=>{a.remove();URL.revokeObjectURL(url)},60000);setMessage('Đã tạo PDF theo lựa chọn hiện tại. Giá chưa bao gồm VAT.')}catch{setMessage('Chưa tạo được PDF. Vui lòng thử lại; các lựa chọn của bạn vẫn được giữ.')}finally{setBusy(false)}
 }
 if(!host)return null;
 return <>{createPortal(<div className="quote-export"><div className="quote-selected" aria-label="Dịch vụ đã chọn">{summary.items.map(item=><button type="button" key={item.id} onClick={()=>remove(item.id)} aria-label={'Bỏ '+item.label}>{item.label} <span aria-hidden="true">×</span></button>)}</div><button className="content-button pdf-export-button" type="button" disabled={busy} onClick={download}>{busy?'Đang tạo PDF…':'Tải PDF báo giá'}<span aria-hidden="true">↓</span></button><p role="status" aria-live="polite">{message||'PDF gồm hạng mục đã chọn, chiết khấu, phụ phí và các khoản thương lượng. Giá chưa bao gồm VAT.'}</p></div>,host)}
 {createPortal(<><div className="quote-mobile-bar"><span>Tạm tính · chưa VAT<strong>{summary.total}</strong></span><button type="button" ref={detailsButton} onClick={()=>dialog.current?.showModal()}>Xem chi tiết</button></div><dialog className="quote-mobile-details" ref={dialog} aria-labelledby="quote-details-title" onClose={()=>detailsButton.current?.focus()}><h2 id="quote-details-title">Cấu hình báo giá</h2><p>{summary.total}</p><ul>{summary.lines.length?summary.lines.map((line,i)=><li key={i}>{line}</li>):<li>Chọn dịch vụ để xem tạm tính.</li>}</ul><p>Giá chưa bao gồm VAT; khoản thương lượng cần được xác nhận riêng.</p><button type="button" onClick={()=>{dialog.current?.close();document.getElementById('bg-total')?.scrollIntoView({block:'center',behavior:'auto'});document.querySelector<HTMLButtonElement>('.pdf-export-button')?.focus({preventScroll:true})}}>Đến báo giá & tải PDF</button> <button type="button" autoFocus onClick={()=>dialog.current?.close()}>Đóng chi tiết</button></dialog></>,document.body)}
 </>;
}
