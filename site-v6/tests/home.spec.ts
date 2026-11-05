import {test,expect} from '@playwright/test';
test('navigation, asset, FAQ, contact and overflow',async({page,isMobile})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/');await expect(page.locator('h1')).toBeVisible();
 expect(await page.locator('header img').evaluate((el:HTMLImageElement)=>el.complete&&el.naturalWidth>0)).toBe(true);
 if(isMobile){await page.getByRole('button',{name:'Menu'}).click();}
 await page.getByRole('navigation').getByRole('link',{name:'Giải pháp',exact:true}).click();
 await expect(page).toHaveURL(/#dich-vu$/);
 const question=page.locator('summary').filter({hasText:'Có nhận khách ngoài TP.HCM không?'});await question.click();
 await expect(page.locator('details[open]')).toContainText('toàn quốc');
 await expect(page.locator('.contact-methods a[href^="mailto:"]')).toHaveAttribute('href',/^mailto:/);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
 expect(errors).toEqual([]);
});
test('reduced motion keeps content visible',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');
 await expect(page.locator('h1')).toHaveCSS('opacity','1');
 await page.locator('#lien-he').scrollIntoViewIfNeeded();await expect(page.locator('#contact-title')).toBeVisible();
});

test('service explorer and real demo selector',async({page})=>{
 await page.goto('/');
 await page.getByRole('tab',{name:/Dữ liệu & phần mềm/}).click();
 await expect(page.getByRole('tabpanel')).toContainText('Data Engineer');
 await page.locator('.project-select button').nth(1).click();
 await expect(page.locator('.project-select button').nth(1)).toHaveAttribute('aria-pressed','true');
 await expect(page.locator('.demo-live-link')).toHaveAttribute('href','https://gio.myagentvn.com/');
 await expect(page.locator('.brief-form')).toBeAttached();
 expect(await page.locator('.brief-form').evaluate((form:HTMLFormElement)=>form.checkValidity())).toBe(false);
});

test('ecosystem menu lands on the actual section from home and subpage',async({page,isMobile})=>{for(const route of ['/','/bang-gia.html']){await page.goto(route);if(isMobile)await page.getByRole('button',{name:'Menu',exact:true}).click();await page.locator('#navigation').getByRole('link',{name:'Hệ dịch vụ',exact:true}).click();await expect(page).toHaveURL(/\/#he-sinh-thai$/);await expect.poll(()=>page.locator('#he-sinh-thai').evaluate(el=>Math.round(el.getBoundingClientRect().top))).toBeGreaterThan(60);await expect.poll(()=>page.locator('#he-sinh-thai').evaluate(el=>Math.round(el.getBoundingClientRect().top))).toBeLessThan(180);await expect(page.locator('#he-sinh-thai .section-heading')).toHaveCSS('opacity','1')}await expect(page.locator('.project-select button')).toHaveText(['01NhàĐất Việt','02Nhà Gió','03NHỊP']);await expect(page.locator('.project-image img').first()).toHaveCSS('object-fit','contain')});
