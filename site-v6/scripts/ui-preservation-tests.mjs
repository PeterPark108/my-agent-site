import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { load } from 'cheerio';
const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.resolve(site, '..');
const fixture = JSON.parse(fs.readFileSync(path.join(site, 'tests/fixtures/live-ui-2026-11-14-mobile.json'), 'utf8'));
const order = ['/#trai-nghiem', '/#he-sinh-thai', '/#dich-vu', '/#quy-trinh', '/#lien-he'];
for (const [file, expected] of Object.entries(fixture.hashes)) {
  const $ = load(fs.readFileSync(path.join(root, file), 'utf8'));
  assert.deepEqual($('#navigation > a').toArray().map(e => $(e).attr('href')), order, `${file}: current hydrated navigation order`);
  $('body script').remove();
  // Mobile UX repair adds state/type attributes only; retain all original content fixtures.
  assert.equal($('.header').attr('data-menu-open'), 'false');
  assert.equal($('.menu-button').attr('type'), 'button');
  $('.header').removeAttr('data-menu-open');
  $('.menu-button').removeAttr('type');
  if (file === 'index.html') {
    // Intentional SEO routing change only; retain the original visual fixture.
    const targets = ['thiet-ke-website-doanh-nghiep', 'thiet-ke-landing-page', 'thiet-ke-website-ban-hang'];
    const cards = $('#dich-vu a[data-service]');
    assert.equal(cards.length, 3);
    targets.forEach((slug, i) => {
      assert.equal(cards.eq(i).attr('href'), `/dich-vu/${slug}.html`);
      cards.eq(i).attr('href', '/dich-vu/thiet-ke-website.html');
    });
  }
  assert.equal(crypto.createHash('sha256').update($('body').html()).digest('hex'), expected, `${file}: current visible UI must be preserved`);
}
for (const file of ['projects/nha-giua-vuon.webp', ...[480, 960, 1600].map(size => `assets/projects/nha-giua-vuon-${size}.webp`)])
  assert.ok(fs.statSync(path.join(root, file)).size > 0, `${file}: existing live image retained`);
console.log(`PASS: ${Object.keys(fixture.hashes).length} production UI snapshots and four live demo assets`);

for (const [file, expected] of Object.entries(fixture.main_hashes || {})) {
  const $ = load(fs.readFileSync(path.join(root, file), 'utf8'));
  assert.equal(crypto.createHash('sha256').update($('main').html()).digest('hex'), expected, `${file}: latest published blog main content preserved exactly`);
}
