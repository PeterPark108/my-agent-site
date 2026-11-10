// Verify the deployed static output, not just source metadata.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { load } from 'cheerio';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const normalize = value => value.replace(/\s+/g, ' ').trim();
const urls = [...fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map(match => match[1]);
assert.equal(urls.length, new Set(urls).size, 'Sitemap URLs must be unique');
const titles = new Set();
let faqPages = 0;
for (const url of urls) {
  const route = new URL(url).pathname;
  const $ = load(fs.readFileSync(path.join(root, route === '/' ? 'index.html' : route.slice(1)), 'utf8'));
  const title = $('head title').text();
  const description = $('meta[name="description"]').attr('content');
  assert.equal($('head title').length, 1, `${route}: one title`);
  assert.ok(title && description, `${route}: title and description exist`);
  assert.ok(!titles.has(title), `${route}: unique title`);
  titles.add(title);
  const rsc = fs.readFileSync(path.join(root, route === '/' ? 'index.txt' : route.slice(1) + '.txt'), 'utf8');
  assert.ok(rsc.includes(JSON.stringify(title).slice(1, -1)), `${route}: fresh title in React payload`);
  assert.ok(rsc.includes(JSON.stringify(description).slice(1, -1)), `${route}: fresh description in React payload`);
  assert.equal($('meta[property="og:title"]').attr('content'), title, `${route}: search/OG title parity`);
  assert.equal($('meta[name="twitter:title"]').attr('content'), title, `${route}: search/Twitter title parity`);
  assert.equal($('meta[property="og:description"]').attr('content'), description, `${route}: search/OG description parity`);
  assert.equal($('link[rel="canonical"]').length, 1, `${route}: one canonical`);
  assert.equal(new URL($('link[rel="canonical"]').attr('href')).href, url, `${route}: canonical matches sitemap`);
  assert.equal(new URL($('meta[property="og:url"]').attr('content')).href, url, `${route}: OG URL matches canonical`);
  assert.ok(!($('meta[name="robots"]').attr('content') || '').includes('noindex'), `${route}: sitemap page remains indexable`);
  assert.equal($('main h1').length, 1, `${route}: one primary heading`);
  const visible = $('.faq details').toArray().map(element => {
    const detail = $(element).clone();
    detail.find('[aria-hidden="true"], script, style, svg').remove();
    const question = normalize(detail.children('summary').text());
    detail.children('summary').remove();
    return [question, normalize(detail.text())];
  });
  const nodes = $('script[type="application/ld+json"]').toArray().flatMap(element => {
    const node = JSON.parse($(element).text());
    return node['@graph'] || [node];
  });
  const faq = nodes.filter(node => node['@type'] === 'FAQPage');
  assert.equal(faq.length, visible.length ? 1 : 0, `${route}: FAQ schema only where visible`);
  if (visible.length) {
    faqPages++;
    assert.deepEqual(faq[0].mainEntity.map(q => [q.name, q.acceptedAnswer.text]), visible, `${route}: exact FAQ parity`);
  }
  if (route === '/') {
    assert.match(title, /Thiết kế website/);
    assert.match($('h1').text(), /WEBSITE ĐẸP/);
    assert.equal(visible.length, 3);
  }
}
const tracking = load(fs.readFileSync(path.join(root, 'tra-cuu-tien-do.html'), 'utf8'));
assert.match(tracking('meta[name="robots"]').attr('content'), /noindex/);
assert.ok(!urls.some(url => url.endsWith('/tra-cuu-tien-do.html')));
console.log(`PASS: ${urls.length} sitemap pages, ${faqPages} exact FAQ schemas, metadata and intentional noindex exclusions`);
