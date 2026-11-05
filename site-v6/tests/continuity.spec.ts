import { test, expect } from '@playwright/test';
test('consent blocks submission, confirmed response succeeds',async({page})=>{
 let sent=0;
 await page.route('**/api/contact',async route=>{sent++;expect(route.request().postDataJSON().consent).toBe('Đồng ý');await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:true})})});
 await page.goto('/');await page.locator('.brief-form input[name=name]').fill('Kiểm thử giao diện');await page.locator('.brief-form input[name=phone]').fill('0900000000');
 await page.getByRole('button',{name:'Gửi yêu cầu tư vấn',exact:true}).click();expect(sent).toBe(0);
 await page.locator('#contact-consent').check();await page.getByRole('button',{name:'Gửi yêu cầu tư vấn',exact:true}).click();
 await expect(page.locator('.form-status')).toContainText('đã nhận yêu cầu');expect(sent).toBe(1);
});
test('contact API rejects missing consent without contacting upstream',async({request})=>{
 const response=await request.post('/api/contact',{data:{name:'Kiểm thử',phone:'0900000000',consent:''}});expect(response.status()).toBe(400);
});
test('MJ opens and original tools and policies remain local',async({page,request})=>{
 for(const path of ['/dich-vu.html','/dich-vu/thiet-ke-website.html','/combo.html','/bang-gia.html','/tra-cuu-tien-do.html','/chinh-sach-bao-mat.html','/dieu-khoan-dich-vu.html','/data/pricing.json','/data/chatbot-kb.json']){const r=await request.get(path);expect(r.ok(),path).toBe(true)}
 await page.goto('/');await expect(page.locator('.mj-btn')).toBeVisible();
 // The original mascot has a continuous transform animation; its real hit target is clickable.
 await page.locator('.mj-btn').click({force:true});await expect(page.locator('#mj-in')).toBeVisible();
 await expect(page.locator('.support-call')).toHaveAttribute('href','tel:0328439972');
 await page.goto('/bang-gia.html');await expect(page.locator('#bg-list')).not.toBeEmpty();
});
