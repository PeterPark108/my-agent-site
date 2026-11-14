import type { Metadata } from 'next';
import seoData from '@/content/seo.json';
import ogImageData from '@/content/og-images.json';
// Per-route social share images (14/11), kept outside seo.json because scripts/import-legacy.cjs rewrites listing entries there.
const ogImages=ogImageData as Record<string,{image:string;alt:string}>;
const seo=seoData as Record<string,{meta:Record<string,string>;ld:string[]}>;
export function seoMetadata(route:string,fallback:{title:string;description?:string}):Pick<Metadata,'openGraph'|'twitter'>{
 const m=seo[route]?.meta||{},og=ogImages[route],url='https://myagentvn.com'+route,image=og?'https://myagentvn.com'+og.image:m['og:image']||'https://myagentvn.com/assets/og-image.png',alt=og?.alt||m['og:image:alt']||undefined,title=m['og:title']||fallback.title,description=m['og:description']||fallback.description;
 return {openGraph:{type:m['og:type']==='article'?'article':'website',locale:m['og:locale']||'vi_VN',siteName:m['og:site_name']||'My Agent',title,description,url:m['og:url']||url,images:[{url:image,width:og?1200:Number(m['og:image:width']||1200),height:og?630:Number(m['og:image:height']||630),...(og?{type:'image/jpeg'}:{}),...(alt?{alt}:{})}]},
  twitter:{card:'summary_large_image',title:m['twitter:title']||title,description:m['twitter:description']||description,images:[og?{url:image,...(alt?{alt}:{})}:m['twitter:image']||image]}};
}
export function JsonLd({route}:{route:string}){return <>{(seo[route]?.ld||[]).map((json,i)=><script key={i} type="application/ld+json" dangerouslySetInnerHTML={{__html:json.replace(/</g,'\\u003c')}}/>)}</>}
