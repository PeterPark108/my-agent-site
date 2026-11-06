# UI/UX revision — 2026-11-06

The site is an existing service business with an established brand. This revision preserves its logos, palette, Vietnamese font, routes, business content and honest sample-project labels. It supersedes the earlier hero entrance, decorative loops and pinned portfolio described in `GSAP-UPGRADE-2026-11-06.md`.

## Result

- Restored all 18 service diagrams and related icons with explicit, theme-aware SVG presentation. Refined geometry and long labels for website, domain and email diagrams.
- Linked and unlinked Blog/Technology News card titles share the owner's requested 19px bold treatment. Body text is 16px; metadata and actions are legible; lists use three, two or one column.
- Search matches Vietnamese text with or without accents on the current page. It reports the visible count, provides an empty state, and clears back to all articles. Existing category links and pagination remain functional.
- Direct top-level service, portfolio, pricing, knowledge and technology news links. Mobile menu locks background scrolling, moves focus into navigation, contains keyboard focus, closes on Escape and restores focus. Mobile contents links land below the header and focus the destination.
- Home names the service and uses the existing Nhà Gió sample screenshot. Four sample websites are visible in a stable grid with direct demo links.
- Opaque navigation and quiet surfaces improve long-form reading. Remove random stars, infinite ornament loops, content reveals, pointer tilt, magnetic buttons and scroll-pinned project cards.

## Skill application

- **Core:** bounded transform/opacity transitions and reduced-motion matchMedia.
- **Timeline:** short, scoped menu and SVG interaction timelines.
- **ScrollTrigger:** reading indicator and debounced geometry refresh after fonts/content change; no hidden content awaiting scroll.
- **Plugins:** ScrollTo for anchors, Flip for the existing service selector, DrawSVG for a hover interaction.
- **Utils:** scoped element selection, bounded scroll duration and keyboard wrap.
- **React:** useGSAP, scopes, revertOnUpdate and listener cleanup.
- **Frameworks:** lifecycle/scoping principles reviewed; Vue/Svelte code is not applicable to this Next/React repository.
- **Performance:** remove per-card reveal triggers, repeated ambient work and unused italic font imports; reuse timelines and avoid per-frame layout reads.
- **Design taste:** stronger hierarchy, one brand system, equal content edges, readable cards, a real existing work image and restrained interactions. Existing-site adaptations preserve requested 19px bold headings, captions explaining technical diagrams, useful service tabs, real contacts and content-driven section heights instead of forcing long content into the skill's single-page template.

## Verification

- ESLint, TypeScript and production static build passed; 61 generated pages. Windows QA uses the documented local-only mkdir preload with `next build --webpack`; no build configuration workaround is committed.
- Browser: home + 18 services + 8 blog/news list/topic/pagination pages at 1440px and 390px: no document overflow, black diagram labels, missing loaded images or hidden content sections; article headings consistently 19px.
- Additional home/blog/news/website-service checks at 1024, 820, 768 and 320px: no document overflow (70 route/viewport observations in total).
- Manually verified accent-insensitive search, empty/reset states, mobile menu focus/scroll lock/Escape restoration, mobile contents navigation, and light/dark presentation. SVGs retain contained horizontal scrolling for small screens with a visible hint.
- The design skill's screenshot runner was attempted but returned `Chrome did not start`. Its consistency/layout/performance suites therefore have no passing result to report; browser screenshots and DOM/interaction checks were used instead.
- No full Playwright suite, Lighthouse/axe, real iOS/Android/Safari, or OS-level reduced-motion emulation was run. Reduced-motion behavior was reviewed in code. Contact/chat forms were not submitted.

GSAP primary references checked: https://gsap.com/resources/React/ , https://gsap.com/docs/v3/Plugins/ScrollTrigger/ , https://gsap.com/docs/v3/Plugins/Flip/ .

This is a draft on `dev` for PR review. Production deployment requires the repository's normal human review/merge process.
