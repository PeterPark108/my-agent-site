// Read-only, sequential UTF-8 byte-boundary audit for this static Next export.
// It does not substitute for browser hydration or navigation testing.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export function decodeFlight(text, label = 'Flight stream') {
  const bytes = Buffer.from(text, 'utf8');
  const utf8 = new TextDecoder('utf-8', { fatal: true });
  const records = [];
  let offset = 0;
  while (offset < bytes.length) {
    const start = offset;
    const colon = bytes.indexOf(58, start);
    assert.ok(colon >= start, `${label}: missing record colon at byte ${start}`);
    const id = bytes.subarray(start, colon).toString('ascii');
    assert.match(id, /^[0-9a-f]*$/, `${label}: invalid record boundary at byte ${start}`);
    offset = colon + 1;
    if (bytes[offset] === 84) { // T<hex byte length>,<UTF-8 text>
      const comma = bytes.indexOf(44, offset);
      assert.ok(comma > offset, `${label}: missing T length delimiter`);
      const lengthHex = bytes.subarray(offset + 1, comma).toString('ascii');
      assert.match(lengthHex, /^[0-9a-f]+$/, `${label}: invalid T byte length`);
      const length = Number.parseInt(lengthHex, 16);
      const payloadStart = comma + 1;
      const end = payloadStart + length;
      assert.ok(Number.isSafeInteger(length) && end <= bytes.length, `${label}: truncated T record ${id}`);
      const value = utf8.decode(bytes.subarray(payloadStart, end));
      records.push({ id, tag: 'T', value, start, end });
      offset = end;
      continue;
    }
    let end = bytes.indexOf(10, offset);
    if (end < 0) end = bytes.length;
    const raw = utf8.decode(bytes.subarray(offset, end));
    const tag = raw.match(/^[A-Z]+/)?.[0] || '';
    // These are the observed line-based tags in this project. Fail closed
    // when the export changes protocol instead of silently skipping a row.
    assert.ok(['', 'I', 'HL', 'HC', 'D', 'W', 'E', 'C', 'X'].includes(tag), `${label}: unsupported tag ${tag}`);
    const payload = raw.slice(tag.length);
    let value;
    if (['C', 'X'].includes(tag) && !payload.length) value = null;
    else {
      try { value = JSON.parse(payload); }
      catch (error) { throw new Error(`${label}: invalid JSON record ${id} at byte ${start}: ${error.message}`); }
    }
    records.push({ id, tag, value, start, end });
    offset = end + (end < bytes.length ? 1 : 0);
  }
  assert.ok(records.length > 0, `${label}: empty stream`);
  return records;
}

export function inlineFlight(html, label = 'HTML') {
  const chunks = [...html.matchAll(/<script>self\.__next_f\.push\((\[1,[\s\S]*?\])\)<\/script>/g)];
  assert.ok(chunks.length > 0, `${label}: missing inline Flight chunks`);
  return chunks.map(match => {
    const data = JSON.parse(match[1]);
    assert.equal(typeof data[1], 'string', `${label}: non-text inline chunk`);
    return data[1];
  }).join('');
}

export function auditRoot(root) {
  const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
  const routes = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(match => new URL(match[1]).pathname);
  assert.ok(routes.length > 0, 'Empty sitemap');
  const checked = new Set();
  let htmlCount = 0;
  let recordCount = 0;
  for (const route of routes) {
    const file = route === '/' ? 'index.html' : route.slice(1);
    assert.ok(file.endsWith('.html') && !file.split('/').includes('..'), `Unexpected sitemap path: ${file}`);
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    recordCount += decodeFlight(inlineFlight(html, file), `${file}: inline`).length;
    htmlCount++;
    const payloads = route === '/' ? ['index.txt', '__next._full.txt', '__next.__PAGE__.txt'] : [file + '.txt'];
    for (const payload of payloads) {
      if (checked.has(payload)) continue;
      // Missing generated payloads are failures, not silent legacy exclusions.
      const text = fs.readFileSync(path.join(root, payload), 'utf8');
      recordCount += decodeFlight(text, payload).length;
      checked.add(payload);
    }
  }
  return { htmlCount, standaloneCount: checked.size, streamCount: htmlCount + checked.size, recordCount };
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  assert.ok(process.argv[2], 'Usage: node validate-flight-streams.mjs EXPORT_ROOT');
  console.log('PASS: sequential Flight byte/JSON audit', auditRoot(path.resolve(process.argv[2])));
}
