import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { load } from 'cheerio';
const root='..';
const slugs=['thiet-ke-website-doanh-nghiep','thiet-ke-landing-page','thiet-ke-website-ban-hang'];
const original=JSON.parse(fs.readFileSync('tests/fixtures/live-ui-2026-11-14-mobile.json','utf8'));
const crypto=await import('node:crypto');
for(const [file,hash] of Object.entries(original.hashes)){
 const $=load(fs.readFileSync(`${root}/${file}`,'utf8'));
 $('body script').remove();
 assert.equal($('.header').attr('data-menu-open'),'false');
 assert.equal($('.menu-button').attr('type'),'button');
 $('.header').removeAttr('data-menu-open');$('.menu-button').removeAttr('type');
 if(file==='index.html')for(const slug of slugs)$(`a[href="/dich-vu/${slug}.html"]`).attr('href','/dich-vu/thiet-ke-website.html');
 assert.equal(crypto.createHash('sha256').update($('body').html()).digest('hex'),hash,`${file}: baseline body preserved apart from intended homepage destinations`);
}
for(const slug of slugs){
 const $=load(fs.readFileSync(`${root}/dich-vu/${slug}.html`,'utf8'));
 assert.equal($('h1').length,1);assert.ok($('main').text().length>3500);assert.equal($('.faq details').length,3);
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
console.log('PASS: all original UI bodies unchanged except three intended link targets; 3 rich linked pages; single GTM bootstrap, opt-out/DNT/host guards, ad-user-data denied.');
