import { test, expect } from '@playwright/test';

test('current homepage structure, seven demos and responsive frame survive hydration', async ({ page }, info) => {
  const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  await expect(page).toHaveTitle('Thiết kế website tại TP.HCM | My Agent');
  await expect(page.locator('.hero-title-main')).toHaveText('WEBSITE ĐẸP');
  await expect(page.locator('.scroll-cue')).toHaveAttribute('href', '#trai-nghiem');
  expect(await page.locator('#main > section[id]').evaluateAll(elements => elements.map(e => e.id)))
    .toEqual(['trai-nghiem', 'he-sinh-thai', 'dich-vu', 'quy-trinh', 'lien-he']);
  expect(await page.locator('#navigation > a').allTextContents()).toEqual(['Dự án', 'Hệ dịch vụ', 'Giải pháp', 'Quy trình', 'Liên hệ']);
  await expect(page.locator('.project-select button')).toHaveCount(7);
  await expect(page.locator('.project-card')).toHaveCount(7);
  await expect(page.locator('.demo-live-link')).toHaveAttribute('href', 'https://3d.myagentvn.com/');
  const firstImage = page.locator('.project-card').first().locator('img');
  await firstImage.scrollIntoViewIfNeeded();
  await expect.poll(() => firstImage.evaluate((image: HTMLImageElement) => image.complete && image.naturalWidth > 0)).toBe(true);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  const nav = page.locator('.project-navigation');
  await nav.scrollIntoViewIfNeeded();
  expect(await nav.evaluate(element => {
    const frame = element.closest('.project-screen')!.getBoundingClientRect();
    return [...element.querySelectorAll('button,.demo-live-link')].every(item => {
      const box = item.getBoundingClientRect();
      return box.left >= frame.left - 2 && box.right <= frame.right + 2 && box.bottom <= frame.bottom + 2;
    });
  })).toBe(true);
  await page.screenshot({ path: info.outputPath('live-ui-projects.png') });
  expect(errors).toEqual([]);
});

test('homepage to portfolio, back and forward retain the current demo and metadata', async ({ page, request }, info) => {
  const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  await page.locator('a[href="/du-an.html"]').filter({ hasText: 'Xem toàn bộ portfolio' }).click();
  await expect(page).toHaveURL(/\/du-an\.html$/);
  await expect(page.locator('main h1')).toHaveText('Dự án mẫu');
  await expect(page.locator('main a[href="https://3d.myagentvn.com/"]')).toHaveCount(1);
  await expect(page.locator('main h3').first()).toContainText('Nhà giữa vườn');
  const portfolioTitle = await page.title();
  const payload = await request.get('/du-an.html.txt');
  expect(payload.ok()).toBe(true);
  expect(await payload.text()).toContain('Nhà giữa vườn');
  await page.screenshot({ path: info.outputPath('live-ui-portfolio.png') });
  await page.goBack();
  await expect(page).toHaveTitle('Thiết kế website tại TP.HCM | My Agent');
  await expect(page.locator('.project-select button')).toHaveCount(7);
  await page.goForward();
  await expect(page).toHaveTitle(portfolioTitle);
  await expect(page.locator('main a[href="https://3d.myagentvn.com/"]')).toHaveCount(1);
  expect(errors).toEqual([]);
});

test('demo switching and mobile menu remain usable without external actions', async ({ page }, info) => {
  test.skip(info.project.name === 'desktop-motion', 'Selector state tested with deterministic reduced motion; motion layout and navigation covered separately');
  const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  for (const [index, href] of [[6, 'https://dongho.myagentvn.com/'], [1, 'https://preview.myagentvn.com/mycons/'], [0, 'https://3d.myagentvn.com/']] as const) {
    await page.locator('.project-select button').nth(index).click();
    await expect(page.locator('.project-select button').nth(index)).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('.demo-live-link')).toHaveAttribute('href', href);
  }
  if (info.project.name === 'mobile') {
    await page.evaluate(() => scrollTo(0, 0));
    await page.locator('.menu-button').click();
    await expect(page.locator('.menu-button')).toHaveAttribute('aria-expanded', 'true');
    await page.locator('#navigation > a').first().click();
    await expect(page.locator('.menu-button')).toHaveAttribute('aria-expanded', 'false');
    await expect(page).toHaveURL(/#trai-nghiem$/);
  }
  expect(errors).toEqual([]);
});

test('current blog article and related links survive release reconciliation', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
  await page.goto('/blog.html');
  const route = '/blog/quy-trinh-lam-website-cho-doanh-nghiep-nho.html';
  const articleLink = page.locator('main a').filter({ hasText: 'Quy trình làm website cho doanh nghiệp nhỏ: từ trao đổi đến bàn giao' }).first();
  await articleLink.click();
  await expect(page).toHaveURL(new RegExp(route.replaceAll('.', '\\.')));
  await expect(page.locator('main h1')).toHaveText('Quy trình làm website cho doanh nghiệp nhỏ: từ trao đổi đến bàn giao');
  await expect(page.locator('.nwa-body')).toBeVisible();
  await expect(page.locator('.page-sidebar nav a').first()).toHaveAttribute('href', /^#/);
  await page.goBack();
  await expect(page).toHaveURL(/\/blog\.html$/);
  await expect(articleLink).toBeVisible();
  await expect(articleLink).toHaveJSProperty('pathname', route);
  expect(errors).toEqual([]);
});

test('mobile navigation fits short screens, reaches every link and dismisses predictably', async ({ page }, info) => {
  test.skip(info.project.name !== 'mobile', 'Mobile navigation regression matrix');
  // Set storage before hydration, avoiding a race with the SSR default theme.
  await page.addInitScript(() => localStorage.setItem('ma-theme', 'dark'));
  for (const viewport of [{width:320,height:568},{width:360,height:640},{width:390,height:844},{width:485,height:757},{width:768,height:480},{width:844,height:390}]) {
    await page.setViewportSize(viewport);
    await page.goto('/');
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    const menu = page.locator('.menu-button');
    const nav = page.locator('#navigation');
    await expect(menu).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    for (const selector of ['.menu-button','.theme-button']) {
      const box=await page.locator(selector).boundingBox();
      expect(box!.height).toBeGreaterThanOrEqual(44);expect(box!.width).toBeGreaterThanOrEqual(44);
      expect(box!.x+box!.width).toBeLessThanOrEqual(viewport.width);
    }
    await menu.click();
    await nav.locator('summary').click();
    const box=await nav.boundingBox();
    expect(box!.y+box!.height).toBeLessThanOrEqual(viewport.height);
    expect(await nav.evaluate(e=>getComputedStyle(e).overflowY)).toBe('auto');
    expect(await nav.locator('.all-pages-panel').evaluate(e=>getComputedStyle(e).overflowY)).toBe('visible');
    const last=nav.getByRole('link',{name:'Chính sách bảo mật',exact:true});
    await last.scrollIntoViewIfNeeded();
    const lastBox=await last.boundingBox();
    expect(lastBox!.y).toBeGreaterThanOrEqual(box!.y);
    expect(lastBox!.y+lastBox!.height).toBeLessThanOrEqual(box!.y+box!.height+1);
    await page.screenshot({path:info.outputPath(`mobile-menu-${viewport.width}.png`)});
    await page.keyboard.press('Escape');
    await expect(menu).toBeFocused();
    await expect(menu).toHaveAttribute('aria-expanded','false');
    await menu.click();
    await expect(nav.locator('details')).not.toHaveAttribute('open','');
    // Tap page margin outside the non-modal navigation, without submitting a form.
    await page.mouse.click(2, Math.min(viewport.height-10,110));
    await expect(menu).toHaveAttribute('aria-expanded','false');
    await page.locator('.theme-button').click();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
    await menu.click();
    expect(await nav.evaluate(e=>getComputedStyle(e).backgroundColor)).toBe('rgb(232, 238, 249)');
    await page.screenshot({path:info.outputPath(`mobile-menu-light-${viewport.width}.png`)});
    await nav.getByRole('link',{name:'Liên hệ',exact:true}).click();
    await expect(menu).toHaveAttribute('aria-expanded','false');
    await expect(page).toHaveURL(/#lien-he$/);
  }
});

for (const [label,id] of [['Dự án','trai-nghiem'],['Hệ dịch vụ','he-sinh-thai'],['Giải pháp','dich-vu'],['Quy trình','quy-trinh'],['Liên hệ','lien-he']]) {
  test(`menu ${label} reaches its section from homepage, subpage and repeated click`, async ({page},info)=>{
    for(const route of ['/','/bang-gia.html']){
      await page.goto(route);
      if(info.project.name==='mobile')await page.locator('.menu-button').click();
      await page.locator('#navigation').getByRole('link',{name:label,exact:true}).click();
      await expect(page).toHaveURL(new RegExp('/#'+id+'$'));
      await expect.poll(()=>page.locator('#'+id).evaluate(e=>Math.round(e.getBoundingClientRect().top))).toBeGreaterThanOrEqual(60);
      await expect.poll(()=>page.locator('#'+id).evaluate(e=>Math.round(e.getBoundingClientRect().top))).toBeLessThan(180);
      await page.evaluate(()=>scrollTo(0,0));
      if(info.project.name==='mobile')await page.locator('.menu-button').click();
      await page.locator('#navigation').getByRole('link',{name:label,exact:true}).click();
      await expect.poll(()=>page.locator('#'+id).evaluate(e=>Math.round(e.getBoundingClientRect().top))).toBeLessThan(180);
      await expect.poll(()=>page.locator('#'+id).evaluate(e=>Math.round(e.getBoundingClientRect().top))).toBeGreaterThanOrEqual(60);
    }
  });
}

test('newly published November blog content survives mobile release and history', async ({page})=>{
  const entries=[['website-dung-de-lam-gi-cho-doanh-nghiep-nho','Website dùng để làm gì cho doanh nghiệp nhỏ'],['chon-ten-mien-va-hosting-cho-doanh-nghiep-nho','Chọn tên miền và hosting cho doanh nghiệp nhỏ: cần biết gì']];
  await page.goto('/blog.html');
  for(const [slug,title] of entries){
    const link=page.locator('#blog-list h2 a').filter({hasText:title});
    await link.click();
    await expect(page).toHaveURL(new RegExp('/blog/'+slug+'\\.html$'));
    await expect(page.locator('main h1')).toHaveText(title);
    await expect(page.locator('.nwa-body')).toBeVisible();
    await page.goBack();
    await expect(link).toBeVisible();
  }
});
