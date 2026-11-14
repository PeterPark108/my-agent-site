import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { load } from 'cheerio';
const root='..';
const slugs=['thiet-ke-website-doanh-nghiep','thiet-ke-landing-page','thiet-ke-website-ban-hang'];
// Shared regression guard permits only the reviewed AEO answer edits.
await import('./ui-preservation-tests.mjs');
for(const slug of slugs){
 const $=load(fs.readFileSync(`${root}/dich-vu/${slug}.html`,'utf8'));
 assert.equal($('h1').length,1);assert.ok($('main').text().length>3500);assert.equal($('.faq details').length,4);
 assert.ok($('a[href="/lien-he.html"]').length);assert.ok($('a[href="/dich-vu/thiet-ke-website.html"]').length);
 for(const e of $('main a[href^="/"]').toArray()){const path=$(e).attr('href').split('#')[0];assert.ok(fs.existsSync(root+path),`${slug}: ${path}`);}
}
const source=fs.readFileSync('src/components/Analytics.tsx','utf8');
const literal=source.match(/const bootstrap = (`[\s\S]*?`);/)[1];const code=vm.runInNewContext(literal);
function run(host='myagentvn.com',opt=false,dnt=false){
 const inserted=[];const w={location:{hostname:host,reload(){}},navigator:{doNotTrack:dnt?'1':'0'},localStorage:{getItem:()=>opt?'1':null,setItem(){},removeItem(){}}};
 const d={querySelector:()=>null,addEventListener(){},createElement:()=>({}),head:{appendChild:s=>inserted.push(s)}};
 const context={window:w,document:d,Date};vm.runInNewContext(code,context);vm.runInNewContext(code,context);return {w,inserted};
}
let a=run();assert.equal(a.inserted.length,1);assert.match(a.inserted[0].src,/GTM-KBZK7NMC/);
const consent=Array.from(a.w.dataLayer[0]);assert.equal(consent[0],'consent');assert.equal(consent[2].ad_user_data,'denied');assert.equal(consent[2].ad_personalization,'denied');
assert.equal(a.w.dataLayer.filter(x=>x[0]==='config').length,0,'No duplicate GA config');
for(const args of [['localhost'],['myagentvn.com',true],['myagentvn.com',false,true],['nhadat.myagentvn.com']])assert.equal(run(...args).inserted.length,0);
console.log('PASS: original UI preserved except reviewed AEO copy and three intended link targets; 3 rich linked pages; single GTM bootstrap, opt-out/DNT/host guards, ad-user-data denied.');
