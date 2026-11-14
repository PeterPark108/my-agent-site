import assert from 'node:assert/strict';
import fs from 'node:fs';
import { load } from 'cheerio';
const slugs = ['thiet-ke-website', 'thiet-ke-website-doanh-nghiep', 'thiet-ke-landing-page', 'thiet-ke-website-ban-hang'];
for (const slug of slugs) {
  const url = `https://myagentvn.com/dich-vu/${slug}.html`;
  const $ = load(fs.readFileSync(`../dich-vu/${slug}.html`, 'utf8'));
  const nodes = $('script[type="application/ld+json"]').toArray().flatMap(e => { const n = JSON.parse($(e).text()); return n['@graph'] || [n]; });
  const service = nodes.find(n => n['@type'] === 'Service');
  const page = nodes.find(n => n['@type'] === 'WebPage');
  assert.equal(service['@id'], `${url}#service`);
  assert.equal(service.provider['@id'], 'https://myagentvn.com/#org');
  assert.equal(page.mainEntity['@id'], service['@id']);
  assert.equal(page.url, url);
  const faq = nodes.find(n => n['@type'] === 'FAQPage');
  assert.equal(faq.mainEntity.length, $('.faq details').length);
  if (slug !== 'thiet-ke-website') {
    assert.match($('#muc-tieu h2').text(), /\?/);
    assert.match($('.faq details').first().text(), /chưa VAT/);
    assert.match($('.faq details').first().text(), /ngày/);
    assert.equal($('.faq details').first().find('a').attr('href'), '/bang-gia.html');
  }
}
console.log('PASS: 4 linked Service/WebPage entities and visible answer blocks; no unsupported AI-specific markup');
