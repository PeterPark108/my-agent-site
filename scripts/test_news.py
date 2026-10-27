#!/usr/bin/env python3
"""Kiểm thử bộ dựng Tin tức (stdlib unittest): Markdown an toàn, validator, RSS, idempotent.
Chạy: python3 scripts/test_news.py"""
import sys,re,json,pathlib,tempfile,unittest,datetime,xml.etree.ElementTree as ET
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import news_md as M, news_build as B
GOOD_BODY=('## Bối cảnh\n\n'+'Đây là đoạn nội dung tự viết để kiểm thử bộ dựng tin tức của My Agent. '*30+'\n\n## Ý nghĩa\n\n- Một\n- Hai\n')
def fm(**kw):
  base=dict(title='"Tiêu đề kiểm thử đủ dài cho bộ dựng tin"',date='2026-10-20',topic='ai',
    summary='"'+('Tóm tắt kiểm thử tự viết bằng lời của mình cho bộ dựng tin tức My Agent, đủ độ dài yêu cầu của validator. ')*1+'Thêm một câu nữa cho đủ."',
    insight='"Góc nhìn kiểm thử: doanh nghiệp nhỏ nên thử quy trình nhỏ trước."')
  base.update(kw); body=base.pop('body',GOOD_BODY); src=base.pop('sources','sources:\n  - name: Nguồn A\n    url: https://example.com/a\n')
  return '---\n'+''.join(f'{k}: {v}\n' for k,v in base.items() if v is not None)+src+'---\n'+body
def run(files):
  d=pathlib.Path(tempfile.mkdtemp())
  for n,t in files.items(): (d/n).write_text(t,encoding='utf-8')
  e=[];w=[]; it=B.load(d,e,w); return it,e,w

class MD(unittest.TestCase):
  def r(self,s): h,_,c=M.render(s); return h,c
  def test_script_escaped(self):
    h,_=self.r('Xin chào <script>alert(1)</script> <img src=x onerror=alert(1)> <iframe src="//x"></iframe>')
    self.assertNotIn('<script',h); self.assertNotIn('<img',h); self.assertNotIn('<iframe',h); self.assertIn('&lt;script&gt;',h)
  def test_js_links_blocked(self):
    for u in ('javascript:alert(1)','JaVaScRiPt:alert(1)','data:text/html,x','vbscript:x','java&#115;cript:x','//evil.com'):
      h,c=self.r(f'[bấm]({u})'); self.assertNotIn('href',h,u); self.assertTrue(c.err,u)
  def test_attr_injection(self):
    h,_=self.r('[a](https://x.com/"onmouseover="alert(1))'); self.assertNotIn('onmouseover="',h)
    h,_=self.r('[a](https://x.com/?q=1&b=2)'); self.assertIn('href="https://x.com/?q=1&amp;b=2"',h)
  def test_external_rel(self):
    h,_=self.r('[a](https://example.com) [b](../lien-he.html) [c](https://myagentvn.com/dich-vu.html)')
    self.assertIn('href="https://example.com" target="_blank" rel="noopener noreferrer"',h)
    self.assertIn('<a href="../lien-he.html">',h); self.assertIn('<a href="https://myagentvn.com/dich-vu.html">',h)
  def test_img_onerror_and_external(self):
    h,c=self.r('![x" onerror="alert(1)](https://evil.com/a.png)'); self.assertNotIn('<img',h); self.assertTrue(c.err)
    h,c=self.r('![](assets/news/a.png)'); self.assertTrue(any('alt' in e for e in c.err))
  def test_blocks(self):
    h,_=self.r('## A\n\n### B\n\n> trích **đậm**\n\n1. một\n2. hai\n\n| x | y |\n|---|---|\n| 1 | <b>2</b> |\n\n```html\n<script>x</script>\n```\n\n---\n\nĐoạn *nghiêng* và `code<>`')
    for t in ('<h2 id="a">A</h2>','<h3 id="b">B</h3>','<blockquote><p>trích <strong>đậm</strong></p></blockquote>','<ol><li>một</li>','<th scope="col">x</th>','<td>&lt;b&gt;2&lt;/b&gt;</td>','<pre><code class="language-html">&lt;script&gt;x&lt;/script&gt;</code></pre>','<hr>','<em>nghiêng</em>','<code>code&lt;&gt;</code>'):
      self.assertIn(t,h)
  def test_h1_rejected(self):
    _,c=self.r('# H1'); self.assertTrue(c.err)
  def test_dup_heading_ids(self):
    h,_=self.r('## Ý nghĩa\n\n## Ý nghĩa'); self.assertIn('id="y-nghia"',h); self.assertIn('id="y-nghia-2"',h)

class Validator(unittest.TestCase):
  def ok(self,t,name='2026-10-20-bai-thu.md'):
    it,e,w=run({name:t}); return it,e
  def has(self,e,s): self.assertTrue(any(s in x for x in e),f'không thấy "{s}" trong {e}')
  def test_good(self):
    it,e=self.ok(fm()); self.assertEqual(e,[]); self.assertEqual(it[0]['slug'],'bai-thu')
  def test_missing_field(self): self.has(self.ok(fm(insight=None))[1],'thiếu trường bắt buộc "insight"')
  def test_bad_date(self): self.has(self.ok(fm(date='20-10-2026'))[1],'date phải là YYYY-MM-DD')
  def test_future(self):
    d=(B.today()+datetime.timedelta(days=3)).isoformat()
    self.has(self.ok(fm(date=d),f'{d}-tuong-lai.md')[1],'tương lai')
  def test_date_mismatch(self): self.has(self.ok(fm(date='2026-10-19'))[1],'khác ngày ở tên file')
  def test_topic(self): self.has(self.ok(fm(topic='game'))[1],'topic "game" không hợp lệ')
  def test_no_source(self): self.has(self.ok(fm(sources='sources:\n'))[1],'ít nhất 1 nguồn')
  def test_http_source(self): self.has(self.ok(fm(sources='sources:\n  - name: A\n    url: http://x.com\n'))[1],'https://')
  def test_affiliate(self): self.has(self.ok(fm(sources='sources:\n  - name: A\n    url: https://imp.i384100.net/abc\n'))[1],'affiliate')
  def test_title_len(self): self.has(self.ok(fm(title='"'+'A'*75+'"'))[1],'title dài 75')
  def test_summary_len(self): self.has(self.ok(fm(summary='"ngắn quá"'))[1],'summary dài')
  def test_forbidden(self):
    for p in ('Hỗ trợ 24/7','học ở FPT Polytechnic','cam kết top 1 Google','đảm bảo lên top','100% lên top'):
      self.has(self.ok(fm(body=GOOD_BODY+'\n'+p+'\n'))[1],'cụm từ bị cấm')
  def test_short_body(self): self.has(self.ok(fm(body='## A\n\nquá ngắn'))[1],'tối thiểu 250')
  def test_bad_filename(self): self.has(self.ok(fm(),'Bai Thu.md')[1],'tên file')
  def test_unknown_field(self): self.has(self.ok(fm(author='X'))[1],'trường lạ "author"')
  def test_js_link_in_body(self): self.has(self.ok(fm(body=GOOD_BODY+'\n[x](javascript:alert(1))\n'))[1],'link bị chặn')
  def test_draft_skipped(self):
    it,e=self.ok(fm(draft='true',topic='sai')); self.assertEqual((it,e),([],[]))
  def test_slug_collision(self):
    it,e,w=run({'2026-10-20-trung.md':fm(),'2026-10-19-trung.md':fm(date='2026-10-19')}); self.has(e,'trùng')
  def test_no_frontmatter(self): self.has(self.ok('chỉ có nội dung')[1],'front-matter')

class Output(unittest.TestCase):
  def test_feed_and_ld(self):
    it,e,w=run({'2026-10-20-bai-thu.md':fm(),'2026-10-18-the-link.md':fm(date='2026-10-18',type='link',body='',title='"Thẻ link kiểm thử với tiêu đề khác"',summary='"'+'Tóm tắt khác cho thẻ link kiểm thử, viết bằng lời của mình và đủ độ dài yêu cầu tối thiểu của bộ kiểm tra tin tức. Thêm câu.'+'"')})
    self.assertEqual(e,[]); it.sort(key=lambda x:(x['date'],x['slug']),reverse=True)
    x=B.feed(it); root=ET.fromstring(x.encode()); ch=root.find('channel')
    self.assertEqual(root.get('version'),'2.0'); items=ch.findall('item'); self.assertEqual(len(items),2)
    for i in items:
      for k in ('title','link','guid','pubDate','description'): self.assertTrue(i.find(k).text,k)
      self.assertTrue(re.fullmatch(r'\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} \+0700',i.find('pubDate').text))
      self.assertTrue(i.find('link').text.startswith('https://'))
    self.assertEqual(B.feed(it),x)
    arts=[a for a in it if a['type']=='article']
    rel,h=B.article_page(arts[0],arts,it); self.assertEqual(rel,'tin-tuc/bai-thu.html')
    lds=[json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S)]
    self.assertEqual(lds[0]['@type'],'NewsArticle'); self.assertEqual(lds[0]['headline'],arts[0]['title'])
    self.assertEqual(h.count('<h1'),1); self.assertIn('Nguồn tham',h); self.assertIn('rel="noopener noreferrer"',h)
    self.assertEqual(B.article_page(arts[0],arts,it)[1],h)
if __name__=='__main__': unittest.main(verbosity=1)
