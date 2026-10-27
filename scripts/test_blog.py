#!/usr/bin/env python3
"""Kiểm thử mục Blog / Kiến thức (stdlib unittest). Chạy: python3 scripts/test_blog.py
- Validator: từ cấm, số liệu/giá chưa đánh dấu, độ dài, services, slug trùng, ngày sai...
- Dựng thử đầu-cuối trên BẢN SAO TẠM của repo với 2 bài mẫu (không đụng data/blog/ thật),
  kiểm tra trang bài, Article + BreadcrumbList JSON-LD, breadcrumb, mục lục, dịch vụ liên quan,
  sitemap, RSS, noindex khi chưa có bài, idempotent, seo_audit 0 vấn đề."""
import sys,re,json,shutil,pathlib,tempfile,subprocess,unittest,xml.etree.ElementTree as ET
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import blog_build as B
R=B.R
P=('Bài viết này giải thích từng bước một cách dễ hiểu để chủ doanh nghiệp nhỏ tự làm được tại nhà mà không cần nền tảng kỹ thuật sâu. ')
BODY=('## Vì sao cần làm\n\n'+P*9+'\n\n## Chuẩn bị gì\n\n- Một tài khoản quản trị\n- Danh sách việc cần làm\n\n'+P*9+'\n\n### Lưu ý nhỏ\n\n'+P*4+'\n\n## Các bước thực hiện\n\n1. Mở trang quản trị\n2. Kiểm tra lại\n\n'+P*5+'\n\nXem thêm [dịch vụ thiết kế website](../dich-vu/thiet-ke-website.html).\n')
def fm(**kw):
  base=dict(title='"Hướng dẫn kiểm thử bộ dựng blog cho người mới"',date='2026-10-20',category='website',
    description='"Bài kiểm thử bộ dựng blog của My Agent: hướng dẫn từng bước dễ hiểu cho chủ doanh nghiệp nhỏ, có mục lục và dịch vụ liên quan để đọc tiếp."',
    services='[thiet-ke-website, seo-tong-the]',tags='[website, hướng dẫn]')
  base.update(kw); body=base.pop('body',BODY)
  return '---\n'+''.join(f'{k}: {v}\n' for k,v in base.items() if v is not None)+'---\n'+body
def run(files):
  d=pathlib.Path(tempfile.mkdtemp())
  for n,t in files.items(): (d/n).write_text(t,encoding='utf-8')
  e=[]; it=B.load(d,e); shutil.rmtree(d); return it,e

class Validator(unittest.TestCase):
  def ok(self,**kw):
    it,e=run({'bai-kiem-thu.md':fm(**kw)}); self.assertEqual(e,[],e); return it[0]
  def err(self,needle,name='bai-kiem-thu.md',**kw):
    it,e=run({name:fm(**kw)}); self.assertTrue(any(needle in x for x in e),(needle,e)); return e
  def test_good(self):
    it=self.ok(); self.assertEqual(it['slug'],'bai-kiem-thu'); self.assertEqual([s for s,_ in it['svc']],['thiet-ke-website','seo-tong-the']); self.assertGreaterEqual(it['words'],300)
  def test_forbidden(self):
    for ph in ('hỗ trợ 24/7','phản hồi 24h','lên top 1 Google','cam kết lên top','đảm bảo thứ hạng','cam kết thứ hạng','học viên FPT Polytechnic','bảo đảm lên trang 1'):
      self.err('cụm từ bị cấm',body=BODY+'\n\n'+ph+'.\n')
  def test_numbers_need_mark(self):
    self.err('chưa đánh dấu',body=BODY+'\n\nGiá làm web chỉ 3 triệu.\n')
    self.err('chưa đánh dấu',body=BODY+'\n\nTăng 45% đơn hàng.\n')
    self.err('chưa đánh dấu',body=BODY+'\n\nĐã phục vụ 200 khách hàng.\n')
    self.ok(body=BODY+'\n\nVí dụ (giả định): ngân sách 3 triệu mỗi tháng.\n')
    self.ok(body=BODY+'\n\nTheo [báo cáo của Google](https://example.com/r), 53% người dùng rời trang chậm.\n')
    self.ok(body=BODY+'\n\nLàm trong 3 bước, mất khoảng 10 phút.\n')
  def test_lengths(self):
    self.err('title dài',title='"Ngắn quá"'); self.err('title dài',title='"'+'Tiêu đề rất dài '*6+'"')
    self.err('description dài',description='"Mô tả ngắn."')
  def test_required(self):
    for k in ('title','date','description','category'): self.err(f'thiếu trường bắt buộc "{k}"',**{k:None})
    self.err('ít nhất 1 dịch vụ',services=None); self.err('không có trang dich-vu/khong-co',services='[khong-co]')
    self.err('category',category='linh-tinh'); self.err('trường lạ',author='Ai đó')
  def test_dates(self):
    for d in ('27/10/2026','2026-13-01','2026-1-5'): self.err('date',date=d)
    self.err('tương lai',date='2099-01-01'); self.err('updated không được trước date',updated='2026-01-01')
  def test_slug(self):
    self.err('tên file','Bai_Sai.md'); self.err('phải trùng tên file',slug='khac')
    it,e=run({'a-bai.md':fm(),'b-bai.md':fm()}); self.assertTrue(any('trùng' in x for x in e),e)
    self.err('trang hệ thống','feed.md')
  def test_words_and_md(self):
    self.err('tối thiểu 300',body='## A\n\nNgắn.\n')
    self.err('',body=BODY+'\n\n[x](javascript:alert(1))\n')
    self.err('H1',body='# Tiêu đề H1\n\n'+BODY)
  def test_template_is_valid(self):
    it,e=run({'mau.md':(R/'data/blog/_template.md.example').read_text(encoding='utf-8')}); self.assertEqual(e,[],e); self.assertEqual(len(it),1)
  def test_template_not_published(self):
    self.assertNotIn('_template.md.example',[p.name for p in (R/'data/blog').glob('*.md')])  # .example không bị dựng
    self.assertFalse((R/'data/blog/_template.md').exists())
  def test_draft_skipped(self):
    it,e=run({'nhap.md':fm(draft='true',title=None)}); self.assertEqual((it,e),([],[]))

class EndToEnd(unittest.TestCase):
  @classmethod
  def setUpClass(c):
    c.t=pathlib.Path(tempfile.mkdtemp())/'site'
    shutil.copytree(R,c.t,ignore=shutil.ignore_patterns('.git','__pycache__'))
  @classmethod
  def tearDownClass(c): shutil.rmtree(c.t.parent)
  def py(self,s,*a): return subprocess.run([sys.executable,str(self.t/'scripts'/s),*a],cwd=self.t,capture_output=True,text=True)
  def build(self):
    r=self.py('blog_build.py','--no-chatbot'); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
    r=self.py('tech_pass.py'); self.assertEqual(r.returncode,0,r.stderr)
  def test_flow(self):
    t=self.t; d=t/'data/blog'
    for f in d.glob('*.md'): f.unlink()
    # 0 bài: trạng thái sắp ra mắt, noindex, không có trong sitemap
    self.build(); s=(t/'blog.html').read_text()
    self.assertIn('Bài viết đầu tiên sắp ra',s); self.assertIn('content="noindex, follow"',s)
    sm=(t/'sitemap.xml').read_text(); self.assertNotIn('blog',sm)
    self.assertEqual(self.py('seo_audit.py').returncode,0)
    # 2 bài mẫu tạm
    (d/'bai-mau-mot.md').write_text(fm(),encoding='utf-8')
    (d/'bai-mau-hai.md').write_text(fm(title='"Bài mẫu thứ hai để kiểm tra liên kết"',date='2026-10-21',category='seo',updated='2026-10-22',services='[seo-tong-the]',
      description='"Bài mẫu thứ hai của bộ kiểm thử blog My Agent, dùng để kiểm tra bài trước sau, bài liên quan, RSS và sitemap khi có nhiều hơn một bài viết."'),encoding='utf-8')
    self.build(); snap={p:p.read_bytes() for p in t.rglob('*.*') if p.suffix in ('.html','.xml','.css')}
    self.build(); self.assertEqual(snap,{p:p.read_bytes() for p in t.rglob('*.*') if p.suffix in ('.html','.xml','.css')},'không idempotent')
    s=(t/'blog/bai-mau-mot.html').read_text(); lst=(t/'blog.html').read_text()
    self.assertNotIn('noindex',lst); self.assertIn('blog/bai-mau-mot.html',lst); self.assertIn('blog/bai-mau-hai.html',lst)
    lds=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)]
    art=[o for o in lds if o.get('@type')=='Article'][0]; bc=[o for o in lds if o.get('@type')=='BreadcrumbList'][0]
    self.assertEqual(art['headline'],'Hướng dẫn kiểm thử bộ dựng blog cho người mới')
    self.assertEqual(art['url'],'https://myagentvn.com/blog/bai-mau-mot.html'); self.assertEqual(art['author']['name'],'My Agent'); self.assertEqual(art['publisher']['name'],'My Agent')
    self.assertTrue(art['datePublished'].startswith('2026-10-20'))
    self.assertEqual([x['name'] for x in bc['itemListElement']],['Trang chủ','Blog kiến thức','Hướng dẫn kiểm thử bộ dựng blog cho người mới'])
    self.assertIn('<link rel="canonical" href="https://myagentvn.com/blog/bai-mau-mot.html">',s); self.assertIn('property="og:type" content="article"',s)
    self.assertRegex(s,r'<nav class="crumb mono"[^>]*><a href="\.\./index\.html">home</a> / <a href="\.\./blog\.html">blog</a>')
    self.assertIn('aria-label="Mục lục"',s); self.assertIn('href="#vi-sao-can-lam"',s)
    self.assertIn('href="../dich-vu/thiet-ke-website.html"',s); self.assertIn('href="../lien-he.html"',s); self.assertIn('rel="prev" href="bai-mau-hai.html"',s)
    self.assertIn('href="../blog.html" class=on>Blog<',s)
    s2=(t/'blog/bai-mau-hai.html').read_text(); self.assertIn('Cập nhật <time datetime="2026-10-22"',s2)
    sm=(t/'sitemap.xml').read_text(); self.assertIn('<loc>https://myagentvn.com/blog/bai-mau-mot.html</loc><lastmod>2026-10-20</lastmod>',sm); self.assertIn('blog/bai-mau-hai.html</loc><lastmod>2026-10-22',sm); self.assertIn('blog.html</loc>',sm)
    rss=ET.parse(t/'blog/feed.xml').getroot(); self.assertEqual(len(rss.find('channel').findall('item')),2)
    r=self.py('seo_audit.py'); self.assertEqual(r.returncode,0,r.stdout)
    # xoá bài -> trang bài bị dọn, sitemap không còn URL chết
    (d/'bai-mau-hai.md').unlink(); self.build()
    self.assertFalse((t/'blog/bai-mau-hai.html').exists()); self.assertNotIn('bai-mau-hai',(t/'sitemap.xml').read_text())
if __name__=='__main__': unittest.main(verbosity=1)
