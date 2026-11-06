# Service diagrams, icons and article headings

## Reported problems and cause

All 18 service pages retained their SVG geometry, but the migrated content shell omitted the legacy diagram and glass-icon presentation rules. SVG's default black fill concealed labels, outlines and details. Article links with `.nw-a` also inherited a 10px rule instead of the surrounding 19px heading; unlinked headlines therefore looked larger.

## Changes

- Added a shared, scoped `content-visuals.css` with explicit SVG fills/strokes and dark/light palettes. No legacy stylesheet or animation-dependent hiding is reintroduced.
- Restored the diagrams for all 18 services, with readable captions and a keyboard-focusable horizontal viewport on narrow screens. A visible mobile hint explains horizontal scrolling.
- Refined the website wireframe bounds to contain its footer and remove unused side space. Wrapped three long labels in the email/domain diagrams within their original nodes.
- Arranged specialist notes in two columns on larger screens and one on mobile. Moved service-card icons above their headings, aligned the detail links, and used a 2-by-2 arrangement for groups of four related services.
- Made linked news/blog headings inherit the same 19px type and weight as unlinked reference headlines. This applies to the main lists, topic lists and pagination. Added a keyboard focus treatment and heading anchor clearance below the sticky header.

## Verification performed

- ESLint, TypeScript and production build passed. Final build generated 61 static pages. The same local Windows mkdir compatibility preload and webpack build described in the GSAP handover were used; no build configuration/dependency patch is committed.
- Inspected all 18 service routes in Chromium at 1280px and 390px: no page overflow, black default SVG labels/icons or labels extending outside their nodes. Checked all 18 again at 390px in the light theme after page initialization completed.
- Checked all 8 blog/news listing, topic and pagination routes at 1280px and 390px: linked and unlinked headlines all computed to 19px, with no page overflow.
- Additional 320px checks passed for website service, Blog and Tin công nghệ. The diagram scroller responds to the keyboard. Confirmed the related service icons precede the headings and the group of four uses two columns on desktop.
- Captured desktop diagram, related-service cards, Blog, news and mobile/light screenshots, plus route-level visual QA data. Browser diagnostics returned no warning/error entries during the checked navigation.

Not run: real Safari/iOS/Android hardware, full Playwright suite, Lighthouse or axe. These checks do not establish a site-wide accessibility or performance certification.

The updated static export and source belong in the existing draft PR #77. Production deployment still requires the repository owner's review. No service claims, prices, article wording, contact data or API behavior were changed.
