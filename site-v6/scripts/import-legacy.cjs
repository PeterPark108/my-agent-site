/* eslint-disable @typescript-eslint/no-require-imports -- Standalone Node script. */
// Nhập trang blog/tin tức do blog_build.py/news_build.py dựng (HTML kiểu cũ) vào khung v6.
// Dùng: node scripts/import-legacy.cjs <thư-mục-gốc-site-cũ-vừa-dựng>
// - Chép HTML vào content/source, thêm route vào docs/LEGACY-INVENTORY.json
// - Chuyển nội dung bằng chính migrate-pages.cjs (chạy trong thư mục tạm, chỉ các route này)
// - Gộp vào src/content/pages.json (giữ meta/actions đã biên tập của route cũ) và src/content/seo.json (og/twitter/JSON-LD)
const fs=require('fs'),path=require('path'),os=require('os'),{execFileSync}=require('child_process');
const V6=path.resolve(__dirname,'..'),L=path.resolve(process.argv[2]||'');if(!process.argv[2]||!fs.existsSync(path.join(L,'blog.html')))throw Error('Cần thư mục site cũ có blog.html');
const c=require(path.join(V6,'node_modules/cheerio'));
const walk=d=>fs.existsSync(d)?fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):[path.join(d,e.name)]):[];
const routes=['/blog.html','/tin-tuc.html',...walk(path.join(L,'blog')),...walk(path.join(L,'tin-tuc'))].map(x=>x.startsWith('/')&&!x.startsWith(L)?x:'/'+path.relative(L,x).split(path.sep).join('/')).filter(r=>r.endsWith('.html')&&!/\/index\.html$/.test(r)).filter(r=>!/http-equiv="refresh"/.test(fs.readFileSync(path.join(L,r.slice(1)),'utf8')));
const invFile=path.join(V6,'docs/LEGACY-INVENTORY.json'),inv=JSON.parse(fs.readFileSync(invFile,'utf8'));
const pagesFile=path.join(V6,'src/content/pages.json'),pages=JSON.parse(fs.readFileSync(pagesFile,'utf8'));
const seoFile=path.join(V6,'src/content/seo.json'),seo=JSON.parse(fs.readFileSync(seoFile,'utf8'));
const T=fs.mkdtempSync(path.join(os.tmpdir(),'v6imp-'));
for(const d of ['docs','content/source','public/js','src/content','src/lib'])fs.mkdirSync(path.join(T,d),{recursive:true});
fs.symlinkSync(path.join(V6,'node_modules'),path.join(T,'node_modules'));
for(const f of ['public/js/main.js','public/js/combo-calculator.js'])fs.copyFileSync(path.join(V6,f),path.join(T,f));
fs.writeFileSync(path.join(T,'docs/LEGACY-INVENTORY.json'),JSON.stringify({...inv,pages:routes}));
const abs=u=>u?new URL(u,'https://myagentvn.com/').href:u;let added=[];
for(const r of routes){const html=fs.readFileSync(path.join(L,r.slice(1)),'utf8');
 for(const dst of [path.join(V6,'content/source',r.slice(1)),path.join(T,'public',r.slice(1))]){fs.mkdirSync(path.dirname(dst),{recursive:true});fs.writeFileSync(dst,html)}
 if(!inv.pages.includes(r)){inv.pages.push(r);added.push(r)}
 const $=c.load(html),m={};$('meta[property^="og:"],meta[name^="twitter:"]').each((_,e)=>{const k=$(e).attr('property')||$(e).attr('name');let v=$(e).attr('content')||'';if(/:(url|image)$/.test(k))v=abs(v);m[k]=v});
 seo[r]={meta:m,ld:$('script[type="application/ld+json"]').map((_,e)=>$(e).html().trim()).get().filter(s=>{try{JSON.parse(s);return true}catch{return false}})};}
execFileSync(process.execPath,[path.join(V6,'scripts/migrate-pages.cjs')],{cwd:T,stdio:'pipe'});
const conv=JSON.parse(fs.readFileSync(path.join(T,'src/content/pages.json'),'utf8'));
for(const r of routes){const n=conv[r];if(!n)throw Error('Không chuyển được '+r);const old=pages[r];
 if(old){n.meta=old.meta;n.actions=old.actions}else{const $=c.load(fs.readFileSync(path.join(L,r.slice(1)),'utf8')),h=$('main').first().children('section').first(),me=h.find('[class*=meta]').first(),kids=me.children().map((_,e)=>$(e).text().replace(/\s+/g,' ').trim()).get().filter(Boolean);
  n.meta=kids.length>1?kids.join(' · '):me.text().replace(/\s+/g,' ').trim();n.actions=h.find('a.btn').map((_,e)=>{const u=new URL($(e).attr('href'),'https://myagentvn.com'+r);return {href:u.pathname+u.hash,label:$(e).text().replace(/\s+/g,' ').trim()}}).get()}
 pages[r]=Object.fromEntries(['title','description','category','kind','sections','toc','scripts','meta','actions'].map(k=>[k,n[k]]));}
fs.writeFileSync(pagesFile,JSON.stringify(pages,null,2));fs.writeFileSync(seoFile,JSON.stringify(seo));fs.writeFileSync(invFile,JSON.stringify(inv,null,2));
fs.rmSync(T,{recursive:true,force:true});
console.log('Đã nhập '+routes.length+' trang blog/tin tức vào v6'+(added.length?'; route mới: '+added.join(', '):''));
