import { seoMetadata, JsonLd } from '@/lib/seo';
import type { Metadata } from 'next';
export const metadata:Metadata={alternates:{canonical:'https://myagentvn.com/'},...seoMetadata('/',{title:'My Agent — Website tạo dấu ấn'})};
import { Ecosystem } from '@/components/Ecosystem';
import { Cosmos } from '@/components/Cosmos';
import { Header } from '@/components/Header';
import { Motion } from '@/components/Motion';
import { Hero } from '@/components/Hero';
import { Services, Process, Contact, FAQ, Footer, Showcase } from '@/components/Sections';
export default function Home() {
  return <><JsonLd route="/"/><Cosmos/><a className="skip" href="#main">Đến nội dung chính</a><Header/><Motion><main id="main"><Hero/><div className="container credibility-strip"><span>MY AGENT / TỪ Ý TƯỞNG ĐẾN VẬN HÀNH</span><p>Website có bản sắc.</p><p>Nội dung rõ ràng.</p><p>Công cụ phù hợp.</p></div><Showcase/><Ecosystem/><Services/><Process/><FAQ/><Contact/></main></Motion><Footer home/></>;
}
