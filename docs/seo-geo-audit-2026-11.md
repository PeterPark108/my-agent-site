# SEO/GEO and live-UI reconciliation

Baseline: production main at 54c3c84, plus verified live-only UI edits. Older design PRs #37/#38 were not merged.

## Improvements

- Search title/description now agree with the curated social metadata across 59 sitemap pages. Homepage metadata identifies website design, TP.HCM and nationwide service without changing visible H1 or hero copy.
- FAQ JSON-LD is generated from visible, sanitized answers. All 21 FAQ pages match their displayed text, removing stale homepage timeline claims and decorative plus signs from schema.
- Static export retains fresh React navigation payloads. The previous export discarded these and left stale files, including a malformed portfolio payload and a missing news-page payload. The full rebuild regenerates them correctly.

## Preserve current production UI

Production contained four modified tracked files and four untracked demo images absent from main. Those changes are now in buildable source: seven demos including Nha giua vuon, homepage section order, current menu order, homepage-specific footer order, section numbering, scroll target and the four project-navigation frame rules. The H1, hero copy, other page layout, animations, pricing, forms and backend remain unchanged. The source menu now renders the same order already applied globally by the live JavaScript.

A fixture records all 59 current production page bodies, excluding scripts and normalizing the pre-hydration menu to its live order. The regenerated export matches every fixture. Demo images are the exact public production files, not new generated replacements.

## Checks

From site-v6:
- npm run lint
- npm run typecheck
- bash scripts/export-static.sh
- npm run test:seo
- npm run test:ui
- npm run test:flight
- npm run test:browser

From root: python3 scripts/test_indexing.py.

The Flight validator sequentially checks UTF-8 byte-counted records and JSON rather than assuming regex-matched metadata proves navigation works. Browser checks cover desktop/mobile, normal/reduced motion, homepage to portfolio and back/forward, seven demo selectors, mobile menu, image loading, responsive project frame and runtime errors. Browser results are recorded separately from static checks. API/security tests requiring absent backend routes are not used to imply backend coverage. No real forms are submitted.

## Release safeguards

Back up the current site before release and preserve existing owner edits and demo assets. Validate the exact reviewed build, retain prior hashed assets for cached clients, and keep backend behavior unchanged. Deployment must leave normal updates operational and retain a verified rollback. Publication requires owner authorization and passing repository gates. Operational server details are intentionally not included in this public report.

## Follow-up content work

Some existing service FAQs still repeat generic website ownership/timeline terms on unrelated services. This patch makes schema accurate to current visible text, not new business commitments. Review those answers with the owner separately. Original project walkthroughs and actual Search Console/analytics measurements are useful next steps; a site search alone is not an indexing diagnosis.

## Evidence and limits

- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://developers.openai.com/api/docs/bots

No special AI schema, llms.txt benefit, ranking guarantee, FAQ rich-result promise or guaranteed AI citation is claimed. URLs, sitemap, intentional tracking noindex and crawler policies are preserved.
