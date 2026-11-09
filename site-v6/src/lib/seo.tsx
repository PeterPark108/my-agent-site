import type { Metadata } from 'next';
import { load } from 'cheerio';
import seoData from '@/content/seo.json';
import pageData from '@/content/pages.json';
import { faqs, homeSeo } from '@/lib/content';
import { safeContent } from '@/lib/safe-content';

const seo = seoData as Record<string, { meta: Record<string, string>; ld: string[] }>;
const pages = pageData as Record<string, { sections: { html: string }[] }>;
type JsonObject = Record<string, unknown>;
const normalize = (value: string) => value.replace(/\s+/g, ' ').trim();

export function seoMetadata(route: string, fallback: { title: string; description?: string }): Pick<Metadata, 'title' | 'description' | 'openGraph' | 'twitter' | 'robots'> {
  const m = seo[route]?.meta || {};
  const url = 'https://myagentvn.com' + route;
  const image = m['og:image'] || 'https://myagentvn.com/assets/og-image.png';
  // Use curated search metadata, not the long hero copy. The homepage is
  // maintained separately from the legacy content imported into subpages.
  const title = route === '/' ? homeSeo.title : m['og:title'] || fallback.title;
  const description = route === '/' ? homeSeo.description : m['og:description'] || fallback.description;
  return {
    title, description,
    ...(route === '/tra-cuu-tien-do.html' ? { robots: { index: false, follow: true } } : {}),
    openGraph: {
      type: m['og:type'] === 'article' ? 'article' : 'website',
      locale: m['og:locale'] || 'vi_VN', siteName: m['og:site_name'] || 'My Agent',
      title, description, url,
      images: [{ url: image, width: Number(m['og:image:width'] || 1200), height: Number(m['og:image:height'] || 630) }],
    },
    twitter: { card: 'summary_large_image', title, description, images: [m['twitter:image'] || image] },
  };
}

// Derive FAQ data from the same sanitized content people can read. Imported
// legacy FAQ scripts are replaced so redesigns cannot leave hidden answers.
function visibleFaq(route: string): string[][] {
  if (route === '/') return faqs;
  const html = (pages[route]?.sections || []).map(section => safeContent(section.html)).join('');
  const $ = load(html);
  return $('.faq details').toArray().flatMap(element => {
    const detail = $(element).clone();
    detail.find('[aria-hidden="true"], script, style, svg').remove();
    const question = normalize(detail.children('summary').text());
    detail.children('summary').remove();
    const answer = normalize(detail.text());
    return question && answer ? [[question, answer]] : [];
  });
}
function withoutFaq(node: JsonObject): JsonObject | null {
  const type = node['@type'];
  if (type === 'FAQPage' || (Array.isArray(type) && type.includes('FAQPage'))) return null;
  if (Array.isArray(node['@graph'])) {
    return { ...node, '@graph': node['@graph'].map(item => withoutFaq(item as JsonObject)).filter(Boolean) };
  }
  return node;
}
export function JsonLd({ route }: { route: string }) {
  const nodes = (seo[route]?.ld || []).map(json => withoutFaq(JSON.parse(json) as JsonObject)).filter((node): node is JsonObject => node !== null);
  const questions = visibleFaq(route);
  if (questions.length) nodes.push({
    '@context': 'https://schema.org', '@type': 'FAQPage',
    '@id': 'https://myagentvn.com' + route + '#faq', inLanguage: 'vi',
    mainEntity: questions.map(([question, answer]) => ({
      '@type': 'Question', name: question, acceptedAnswer: { '@type': 'Answer', text: answer },
    })),
  });
  return <>{nodes.map((node, i) => <script key={i} type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(node).replace(/</g, '\\u003c') }} />)}</>;
}
