# Web-design keyword clusters and analytics (12 November 2026)

## Intent and evidence
Owner requested web-design keyword SEO and integration of the supplied Google tag, preserving the UI. GSC domain property combines root-domain and subdomain traffic. Screenshots show 14 clicks / 458 impressions, average position 41.5; brand query accounts for 8 clicks and `website trọn gói` has 7 impressions. These aggregate figures do not describe a specific keyword rank. Filter pages starting `https://myagentvn.com/` before measuring the service site.

## Keyword-to-page mapping
- `/`: My Agent and website design in TP.HCM (existing positioning).
- `/dich-vu/thiet-ke-website.html`: general professional/custom website design (existing hub).
- `/dich-vu/thiet-ke-website-doanh-nghiep.html`: business brochure websites; capabilities, CMS, content and handover.
- `/dich-vu/thiet-ke-landing-page.html`: campaign landing pages; message, lead form, scope and measurement.
- `/dich-vu/thiet-ke-website-ban-hang.html`: commerce/catalogue sites; product data, orders, payment limitations and operations.
- Existing cost and process articles remain canonical supporting material; do not duplicate them for minor keyword variations.

Three homepage solution cards retain all text/style/layout; only destination URLs change. New pages reuse the existing service template, quote existing published price ranges as nonbinding references, and contain unique visible FAQs mirrored by generated schema. No rank/revenue guarantees, fake testimonials or fictional customer projects.

## Analytics
Owner image contains GTM-KBZK7NMC. Its published gtm.js was fetched and contained GA4 destination G-2J09FVVE0E; this is distinct from old unused G-BZ5E2WMZLJ in legacy config.js.
The shared component loads GTM once, not an extra GA config/page_view. Host guard limits loading to root/www production host. DNT/GPC and existing `myagent_ga_off` opt-out remain honoured. Advertising storage, ad personalization and advertising user data are denied before the container loads; Google signals and advertising personalization are disabled. The old legacy GA configuration is blank to prevent two destinations on pages that load legacy scripts. No form values or custom user identifiers are pushed by our code.
Container settings remain remote and can change independently. Validate tag behavior in Tag Assistant and GA Realtime after deployment. The initial public container contains user-provided-data capabilities, so never lift the ad_user_data denial or introduce form data without reviewing privacy and authorization. No network browser measurement has yet been claimed verified.

## Verification
- lint/typecheck/build: pass.
- test:seo: 63 sitemap pages pass (main baseline 60 plus 3 new routes).
- test:flight: exported HTML and RSC valid.
- keyword-cluster-tests.mjs: all 60 original body snapshots unchanged after normalizing exactly the intended 3 link targets; new content, CTA/link integrity, GTM singleton and privacy guards pass.
- Browser suite: attempted; Chromium cannot launch in this executor (socket operation not permitted/crashpad). This is blocked environment coverage, not passed browser QA.

## REQUIRED release guard
Branch is based on main 05dec31, not a fresh VPS snapshot. Public live currently has additional content (sitemap62), and remote production diverges from main. DO NOT replace live with this whole generated tree without reconciling current VPS files/source and preserving newer pages, assets and edits. Do not turn on the paused pull schedule. Deployment is pending authenticated VPS access, fresh backup/baseline, reconciliation and browser QA. Keep UI snapshot fixtures unchanged.

## Fresh reconciliation (12 November, before release)
Authenticated read-only VPS inspection confirms HEAD remains main05dec31 with dirty/untracked blog exports. A fresh public HTTPS crawl fetched all62 sitemap pages successfully. Exactly12 blog pages/listings differ from main and match production-branch body text. Only those blog records were reconciled into the candidate; the existing security article's original related links were deliberately retained rather than accepting production's unrelated change. Current main UI remains intact.

Added a separate `live-ui-2026-11-12.json` fixture derived from the public62-page snapshot. The older fixture is untouched. Build and all62 exact body-hash comparisons pass after excluding scripts and normalizing only the3 explicitly requested homepage destinations. Candidate sitemap now contains65 URLs. Newer live articles and related links are preserved. Backend/customer data and cron are outside the patch. Release still requires source/hash and concurrent-writer checks, a fresh backup/stage, rendered QA and post-release verification; this document does not assert deployment.
