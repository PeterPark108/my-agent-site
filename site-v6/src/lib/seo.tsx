import type { Metadata } from 'next';
import seoData from '@/content/seo.json';
const seo=seoData as Record<string,{meta:Record<string,string>;ld:string[]}>;
export function seoMetadata(route:string,fallback:{title:string;description?:string}):Pick<Metadata,'openGraph'|'twitter'>{
 const m=seo[route]?.meta||{},url='https://myagentvn.com'+route,image=m['og:image']||'https://myagentvn.com/assets/og-image.png',title=m['og:title']||fallback.title,description=m['og:description']||fallback.description;
 return {openGraph:{type:m['og:type']==='article'?'article':'website',locale:m['og:locale']||'vi_VN',siteName:m['og:site_name']||'My Agent',title,description,url:m['og:url']||url,images:[{url:image,width:Number(m['og:image:width']||1200),height:Number(m['og:image:height']||630)}]},
  twitter:{card:'summary_large_image',title:m['twitter:title']||title,description:m['twitter:description']||description,images:[m['twitter:image']||image]}};
}
export function JsonLd({route}:{route:string}){return <>{(seo[route]?.ld||[]).map((json,i)=><script key={i} type="application/ld+json" dangerouslySetInnerHTML={{__html:json.replace(/</g,'\\u003c')}}/>)}</>}
