#!/usr/bin/env python3
"""Check crawlable sitemap pages and intentional utility exclusions (stdlib)."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://myagentvn.com/'

class Head(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.canonicals = []
        self.robots = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.robots.extend(x.strip() for x in attrs.get('content', '').split(','))

class IndexingTests(unittest.TestCase):
    def test_sitemap_pages(self):
        urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertTrue(urls)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertNotIn(BASE + 'tra-cuu-tien-do.html', urls)
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(url.startswith(BASE))
                head = Head((ROOT / (url[len(BASE):] or 'index.html')).read_text())
                self.assertEqual([x.rstrip('/') for x in head.canonicals], [url.rstrip('/')])
                self.assertNotIn('noindex', head.robots)
    def test_tracking_stays_excluded(self):
        head = Head((ROOT / 'tra-cuu-tien-do.html').read_text())
        self.assertIn('noindex', head.robots)
        self.assertIn('follow', head.robots)
        self.assertEqual(head.canonicals, [BASE + 'tra-cuu-tien-do.html'])
    def test_tracking_rsc_parity(self):
        metadata = '["$","meta","tracking-robots",{"name":"robots","content":"noindex, follow"}]'
        self.assertIn(metadata, (ROOT / 'tra-cuu-tien-do.html.txt').read_text())
        html = (ROOT / 'tra-cuu-tien-do.html').read_text()
        payloads = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', html)
        self.assertTrue(any(metadata in json.loads(payload) for payload in payloads))

    def test_error_and_redirect_exclusions(self):
        for file in ['404.html', '_not-found.html', 'blog/index.html', 'tin-tuc/index.html', 'tra-cuu-tien-do/index.html']:
            with self.subTest(file=file):
                self.assertIn('noindex', Head((ROOT / file).read_text()).robots)

if __name__ == '__main__':
    unittest.main()
