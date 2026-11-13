/* Trang Tài nguyên AI Agent: tab theo nhóm + tìm kiếm (không JS vẫn xem đủ danh sách) */
(()=>{const d=document,bar=d.querySelector('.rs-bar');if(!bar)return;
const tabs=[...bar.querySelectorAll('[role=tab]')],q=d.getElementById('rs-q'),cnt=d.getElementById('rs-count'),
groups=[...d.querySelectorAll('.rs-group')],em=d.querySelector('.rs-empty'),
norm=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d');
const idx=groups.map(g=>({g,cards:[...g.querySelectorAll('.rs-card')].map(c=>({c,t:norm(c.textContent)}))}));
let cur='all';
function apply(){const v=norm(q.value.trim());let n=0;
 idx.forEach(({g,cards})=>{const gOn=cur==='all'||g.dataset.g===cur;let k=0;
  cards.forEach(({c,t})=>{const on=gOn&&(!v||t.includes(v));c.hidden=!on;if(on){k++;c.classList.add('in')}});
  g.hidden=!k;n+=k});
 em.hidden=n>0;cnt.textContent=n?n+' tài nguyên':'0 kết quả'}
function sel(t,focus){cur=t.dataset.g;tabs.forEach(x=>{const on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1});if(focus)t.focus();apply()}
tabs.forEach((t,i)=>{t.addEventListener('click',ev=>{ev.preventDefault();sel(t)});
 t.addEventListener('keydown',ev=>{let j=null;if(ev.key==='ArrowRight')j=(i+1)%tabs.length;else if(ev.key==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;else if(ev.key==='Home')j=0;else if(ev.key==='End')j=tabs.length-1;else if(ev.key===' '){ev.preventDefault();sel(t)}
  if(j!==null){ev.preventDefault();sel(tabs[j],true)}})});
q.addEventListener('input',apply);
q.addEventListener('keydown',ev=>{if(ev.key==='Escape'&&q.value){q.value='';apply()}});
const h=location.hash.slice(3),t0=tabs.find(x=>x.dataset.g===h);if(t0)sel(t0)})();
