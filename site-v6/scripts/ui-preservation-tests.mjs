import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { load } from 'cheerio';
const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.resolve(site, '..');
const fixture = JSON.parse(fs.readFileSync(path.join(site, 'tests/fixtures/live-ui-2026-11.json'), 'utf8'));
const order = ['/#trai-nghiem', '/#he-sinh-thai', '/#dich-vu', '/#quy-trinh', '/#lien-he'];
for (const [file, expected] of Object.entries(fixture.hashes)) {
  const $ = load(fs.readFileSync(path.join(root, file), 'utf8'));
  assert.deepEqual($('#navigation > a').toArray().map(e => $(e).attr('href')), order, `${file}: current hydrated navigation order`);
  $('body script').remove();
  assert.equal(crypto.createHash('sha256').update($('body').html()).digest('hex'), expected, `${file}: current visible UI must be preserved`);
}
for (const file of ['projects/nha-giua-vuon.webp', ...[480, 960, 1600].map(size => `assets/projects/nha-giua-vuon-${size}.webp`)])
  assert.ok(fs.statSync(path.join(root, file)).size > 0, `${file}: existing live image retained`);
console.log(`PASS: ${Object.keys(fixture.hashes).length} production UI snapshots and four live demo assets`);
