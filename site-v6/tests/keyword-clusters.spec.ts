import { test, expect } from '@playwright/test';
for (const slug of ['thiet-ke-website-doanh-nghiep','thiet-ke-landing-page','thiet-ke-website-ban-hang']) {
 test(`keyword landing ${slug}`,async({page},info)=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',route=>new URL(route.request().url()).hostname==='127.0.0.1'?route.continue():route.abort());
  await page.goto(`/dich-vu/${slug}.html`);
  await expect(page.locator('h1')).toHaveCount(1);
  await expect(page.locator('.faq details')).toHaveCount(3);
  await page.locator('.faq summary').first().click();
  await expect(page.locator('.faq details').first()).toHaveAttribute('open','');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  await page.screenshot({path:info.outputPath(`${slug}.png`),fullPage:true});
  await page.locator('.subpage-actions a').first().click();await expect(page).toHaveURL(/lien-he.html$/);
  await page.goBack();await expect(page.locator('h1')).toHaveCount(1);expect(errors).toEqual([]);
 });
}
