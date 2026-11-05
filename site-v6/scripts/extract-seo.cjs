/* eslint-disable @typescript-eslint/no-require-imports -- Standalone Node script. */
// Trích og:*, twitter:* và JSON-LD từ HTML bản cũ -> src/content/seo.json. Dùng: node scripts/extract-seo.cjs <thư-mục-html-cũ>
const fs=require('fs'),path=require('path'),c=require('cheerio');
const src=path.resolve(process.argv[2]||'content/source'),pages=require('../src/content/pages.json'),abs=u=>u?new URL(u,'https://myagentvn.com/').href:u,out={};
for(const route of ['/',...Object.keys(pages)]){const f=path.join(src,route==='/'?'index.html':route.slice(1));if(!fs.existsSync(f))continue;const $=c.load(fs.readFileSync(f,'utf8'));
const m={};$('meta[property^="og:"],meta[name^="twitter:"]').each((_,e)=>{const k=$(e).attr('property')||$(e).attr('name');let v=$(e).attr('content')||'';if(/:(url|image)$/.test(k))v=abs(v);m[k]=v});
const ld=$('script[type="application/ld+json"]').map((_,e)=>$(e).html().trim()).get().filter(s=>{try{JSON.parse(s);return true}catch{return false}});out[route]={meta:m,ld}}
fs.writeFileSync(path.join(__dirname,'../src/content/seo.json'),JSON.stringify(out));console.log('seo routes',Object.keys(out).length);
