# GSAP motion upgrade — 06/11/2026

Based on production/main c249664bdce8494734ed708c6894ffc0e818bdda.

## Changes

- Hero copy/art entrance uses one labeled timeline; quieter desktop orbital motion and bounded pointer response.
- Services reveal individually; decorative chip/workflow SVG strokes draw with DrawSVGPlugin.
- Ecosystem tabs use a shared Flip selection marker and short panel staggers. Arrow keys, Home/End, tab roles and native links remain intact.
- Anchor navigation uses ScrollToPlugin with a measured header offset. Wheel, touch, navigation keys and reduced-motion changes cancel scrolling. Focus follows the destination; modified clicks and external/download links retain native behavior.
- Non-pinned project selection fades/slides briefly. Desktop pinning remains scoped to the existing large-viewport mode.
- A decorative reading-progress line tracks native scroll. Mobile has fewer stars, no star twinkle, no perpetual GSAP artwork loops and shorter reveals.
- MatchMedia and useGSAP revert owned animations on mode changes/unmount. Off-screen/background artwork pauses. Font/image loads, FAQ and tab layout changes refresh scroll geometry.

## Eight skill areas

Core (tweens and matchMedia); Timeline (hero sequencing); ScrollTrigger (reveal and progress); Plugins (Flip, DrawSVG, ScrollTo); Utils (selector, toArray, clamp, mapRange, wrap); Performance (quickTo, transform/opacity, visibility and mobile reductions); React (scoped useGSAP and cleanup); Frameworks (reviewed lifecycle/scope principles and followed its React routing instruction). No Vue/Svelte runtime is added to this Next/React site.

## Verification

PASS: ESLint and TypeScript. Production static build generated 61 pages with the existing dependencies. Windows local build used `next build --webpack` and a workspace-only filesystem compatibility preload because async mkdir failed on Next's generated segment folders; no dependency patch or production build configuration change is committed.

PASS: in-app Chromium browser QA at 320, 390, 768 and 1440px, no horizontal overflow in the observed views. At 390px menu closes on navigation, all four demo choices work and no pinned spacer remains. At 1440x900 one project pin exists, selecting NHỊP updates the active card and live-demo link. Resizing between desktop and mobile restored the corresponding layout.

PASS: ecosystem tabs by click/arrow/Home/End; one active panel and selection marker align. Home anchor destinations land below the header (observed about 114–116px). Navigating from the pricing page back to the ecosystem works. FAQ opens normally; light/dark theme both render. Destination keyboard focus was checked after the final change. No warning/error entries were reported by the browser during these interactions.

The accompanying route-check JSON records HTTP/shell checks for the current content routes. Screenshots are supplied in the review ZIP. No real contact form, phone call, email or order lookup was submitted.

NOT RUN: full existing Playwright suite, Lighthouse/axe, real Safari/iOS/Android hardware, OS-level reduced-motion switching and JS-disabled browser QA. Reduced-motion behavior was implemented and code-reviewed, not claimed as a completed browser test.

## Review and deployment

This is a review build, not confirmation that myagentvn.com was updated. Follow the repository PR workflow: changes to dev, PR to production, owner review before merge/deployment. Keep the existing VPS/domain, server files and API configuration.

The root static export accompanies source changes so the existing VPS workflow can serve the upgrade after approval. Older hashed `_next` files are retained for clients with old open tabs. The ZIP contains `website/` (normalized static export), `source/` (changed source files) and `review/` (screenshots/checks); it contains no server credentials or dependencies. It does not replace VPS API configuration.

Rollback: restore the previous approved release/commit c249664bdce8494734ed708c6894ffc0e818bdda using the existing deployment procedure. Do not change DNS for this upgrade.
