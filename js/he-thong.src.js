(()=>{const D=/*DATA*/null,d=document,$=s=>d.querySelector(s),$$=s=>[...d.querySelectorAll(s)];
// category tabs (dich-vu.html)
const tabs=$$('.cat-tabs [role=tab]'),panels=$$('.cat-panel');
if(tabs.length){d.documentElement.classList.add('tabs-on');const show=id=>{if(id==='du-lieu-phan-mem')id='du-lieu';if(!panels.some(p=>p.id==id))id=panels[0].id;panels.forEach(p=>p.hidden=p.id!=id);tabs.forEach(t=>{const on=t.getAttribute('aria-controls')==id;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1})};
tabs.forEach((t,i)=>{t.addEventListener('click',e=>{e.preventDefault();const id=t.getAttribute('aria-controls');show(id);history.replaceState(null,'','#'+id)});t.addEventListener('keydown',e=>{const k={ArrowRight:1,ArrowLeft:-1}[e.key];if(k){const n=tabs[(i+k+tabs.length)%tabs.length];n.focus();n.click()}})});
show(location.hash.slice(1));addEventListener('hashchange',()=>show(location.hash.slice(1)))}
// combo builder (combo.html)
const B=$('#builder');if(B){const bx=$$('#builder input[type=checkbox]'),out=$('#bout'),go=$('#bgo');
const upd=()=>{const sel=bx.filter(x=>x.checked).map(x=>x.value);if(!sel.length){out.textContent='Chưa chọn dịch vụ nào.';go.href='lien-he.html#form';go.setAttribute('aria-disabled','true');return}
out.innerHTML='';const p=d.createElement('p');p.textContent=sel.length+' dịch vụ: '+sel.map(s=>D.sv[s]).join(', ')+'.';out.append(p);go.href='lien-he.html?dv='+sel.join(',')+'#form';go.removeAttribute('aria-disabled')};
bx.forEach(x=>x.addEventListener('change',upd));$('#bclr').onclick=()=>{bx.forEach(x=>x.checked=false);upd()};
$$('[data-preset]').forEach(b=>b.onclick=()=>{const c=D.combos.find(c=>c.id==b.dataset.preset);bx.forEach(x=>x.checked=c.sv.includes(x.value));upd()});
go.addEventListener('click',e=>{if(go.hasAttribute('aria-disabled')){e.preventDefault();out.textContent='Hãy tích ít nhất một dịch vụ.'}});upd()}
// prefill contact form
const F=$('form[data-contact]');if(F&&F.service){const q=new URLSearchParams(location.search),sel=F.service,msg=F.message;let svs=null,label='';
const c=D.combos.find(c=>c.id==q.get('combo'));if(c){svs=c.sv;label='Combo '+c.name}
else if(q.get('dv')){svs=q.get('dv').split(',').filter(s=>D.sv[s]);label='Combo tự chọn'}
else if(q.get('dich-vu')&&D.sv[q.get('dich-vu')]){sel.value=D.sv[q.get('dich-vu')]}
if(svs&&svs.length){sel.value=label;if(msg&&!msg.value)msg.value=(c?'Tôi quan tâm '+label+', gồm: ':'Tôi muốn báo giá combo tự chọn gồm: ')+svs.map(s=>D.sv[s]).join(', ')+'.\nNhu cầu cụ thể: '}}
})();
