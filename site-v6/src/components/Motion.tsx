'use client';
import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(ScrollTrigger, DrawSVGPlugin, useGSAP);

export function Motion({ children }: { children: React.ReactNode }) {
  const root = useRef<HTMLDivElement>(null);
  useGSAP(() => {
    const media = gsap.matchMedia();
    media.add({
      desktop: '(min-width: 961px) and (hover: hover) and (pointer: fine)',
      mobile: '(max-width: 960px), (hover: none), (pointer: coarse)',
      reduce: '(prefers-reduced-motion: reduce)',
    }, context => {
      if (context.conditions?.reduce) return;
      const desktop = context.conditions?.desktop;
      const scope = root.current!;
      const select = gsap.utils.selector(scope);
      const cleanups: (() => void)[] = [];
      const loops: { target: Element; animation: gsap.core.Animation }[] = [];
      let disposed = false;
      // Server HTML remains visible without JavaScript.
      const intro = gsap.timeline({ defaults: { duration: .75, ease: 'power3.out', clearProps: 'transform,opacity,visibility' } });
      intro.addLabel('copy').from(select('[data-intro]'), { y: desktop ? 26 : 14, autoAlpha: 0, stagger: .09 }, 'copy');
      if (select('.hero-art').length) {
        intro.from(select('.hero-art'), { scale: .94, autoAlpha: 0, duration: 1.1 }, 'copy+=0.08')
          .from(select('.art-label, .art-coordinates, .art-index'), { autoAlpha: 0, y: 8, stagger: .08 }, 'copy+=0.35');
      }
      const reveals = new Map<Element, gsap.core.Tween>();
      gsap.utils.toArray<HTMLElement>('[data-reveal], [data-service]', scope).forEach(el => {
        reveals.set(el, gsap.from(el, {
          y: desktop ? 28 : 14, opacity: 0, duration: desktop ? .65 : .4,
          ease: 'power2.out', clearProps: 'transform,opacity',
          scrollTrigger: { trigger: el, start: 'clamp(top 94%)', once: true },
        }));
      });
      const focus = (event: FocusEvent) => {
        for (const [el, tween] of reveals) if (el.contains(event.target as Node)) tween.progress(1);
      };
      scope.addEventListener('focusin', focus);
      cleanups.push(() => scope.removeEventListener('focusin', focus));
      const heading = select('.type-heading')[0];
      if (heading) gsap.timeline({ scrollTrigger: { trigger: heading, start: 'clamp(top 88%)', once: true } })
        .from(select('.type-heading .type-char'), {
          opacity: 0, y: 5, duration: .22, stagger: { amount: desktop ? .65 : .25 },
          ease: 'power2.out', clearProps: 'transform,opacity',
        });
      gsap.utils.toArray<HTMLElement>('.glass-icon', scope).forEach(icon => {
        gsap.from(icon.querySelectorAll('svg path, svg rect, svg circle'), {
          drawSVG: '0%', duration: 1, stagger: .06, ease: 'power2.inOut',
          scrollTrigger: { trigger: icon, start: 'clamp(top 90%)', once: true },
        });
        if (desktop) loops.push({ target: icon, animation: gsap.to(icon.querySelector('.icon-plate'), {
          y: -8, rotation: 4, duration: 4, repeat: -1, yoyo: true, ease: 'sine.inOut', paused: true,
        }) });
      });
      const art = scope.querySelector<HTMLElement>('.hero-art');
      if (art && desktop) {
        const ambience = gsap.timeline({ paused: true, defaults: { repeat: -1, yoyo: true, ease: 'sine.inOut' } })
          .to(select('.orbit-float-one'), { y: -24, x: 10, rotation: 6, duration: 5.5 }, 0)
          .to(select('.orbit-float-two'), { y: 20, x: -12, rotation: -7, duration: 6.5 }, 0)
          .to(select('.orb'), { y: -9, duration: 5 }, 0);
        loops.push({ target: art, animation: ambience });
        const orb = art.querySelector<HTMLElement>('.orb');
        if (orb) {
          const x = gsap.quickTo(orb, 'rotationY', { duration: .6, ease: 'power3.out' });
          const y = gsap.quickTo(orb, 'rotationX', { duration: .6, ease: 'power3.out' });
          const clamp = gsap.utils.clamp(-1, 1);
          let bounds: DOMRect | null = null;
          const enter = () => { bounds = art.getBoundingClientRect(); };
          const move = (event: PointerEvent) => {
            if (!bounds) enter();
            if (!bounds?.width || !bounds.height) return;
            x(clamp(gsap.utils.mapRange(bounds.left, bounds.right, -1, 1, event.clientX)) * 5);
            y(-clamp(gsap.utils.mapRange(bounds.top, bounds.bottom, -1, 1, event.clientY)) * 4);
          };
          const reset = () => { bounds = null; x(0); y(0); };
          art.addEventListener('pointerenter', enter); art.addEventListener('pointermove', move); art.addEventListener('pointerleave', reset);
          window.addEventListener('scroll', reset, { passive: true });
          cleanups.push(() => {
            art.removeEventListener('pointerenter', enter); art.removeEventListener('pointermove', move); art.removeEventListener('pointerleave', reset);
            window.removeEventListener('scroll', reset);
          });
        }
      }
      // Only visible artwork animates; all loops pause in background tabs.
      const visible = new Set<Element>();
      const sync = () => loops.forEach(({ target, animation }) => animation.paused(document.hidden || !visible.has(target)));
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => { if (entry.isIntersecting) visible.add(entry.target); else visible.delete(entry.target); }); sync();
      });
      loops.forEach(({ target }) => observer.observe(target));
      document.addEventListener('visibilitychange', sync);
      if (desktop) gsap.utils.toArray<HTMLElement>('.hero .button', scope).forEach(button => {
        const x = gsap.quickTo(button, 'x', { duration: .3, ease: 'power3.out' });
        const y = gsap.quickTo(button, 'y', { duration: .3, ease: 'power3.out' });
        const clamp = gsap.utils.clamp(-5, 5);
        let bounds: DOMRect | null = null;
        const enter = () => { bounds = button.getBoundingClientRect(); };
        const move = (e: PointerEvent) => {
          if (!bounds) enter();
          if (!bounds) return;
          x(clamp((e.clientX - bounds.left - bounds.width / 2) * .08));
          y(clamp((e.clientY - bounds.top - bounds.height / 2) * .12));
        };
        const reset = () => { bounds = null; x(0); y(0); };
        button.addEventListener('pointerenter', enter); button.addEventListener('pointermove', move); button.addEventListener('pointerleave', reset);
        button.addEventListener('focus', reset); window.addEventListener('scroll', reset, { passive: true });
        cleanups.push(() => {
          button.removeEventListener('pointerenter', enter); button.removeEventListener('pointermove', move); button.removeEventListener('pointerleave', reset);
          button.removeEventListener('focus', reset); window.removeEventListener('scroll', reset);
        });
      });
      gsap.fromTo(select('.reading-progress'), { scaleX: 0 }, {
        scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: true },
      });
      // Refresh geometry after font/image loads and native FAQ expansion.
      const refresh = gsap.delayedCall(.15, () => ScrollTrigger.refresh()).pause();
      const scheduleRefresh = () => { refresh.restart(true); };
      scope.addEventListener('load', scheduleRefresh, true); scope.addEventListener('toggle', scheduleRefresh, true);
      void document.fonts.ready.then(() => { if (!disposed) scheduleRefresh(); });
      return () => {
        disposed = true; observer.disconnect(); document.removeEventListener('visibilitychange', sync);
        scope.removeEventListener('load', scheduleRefresh, true); scope.removeEventListener('toggle', scheduleRefresh, true);
        cleanups.forEach(cleanup => cleanup());
      };
    }, root);
    return () => media.revert();
  }, { scope: root });
  return <div ref={root}><div className="reading-progress" aria-hidden="true" />{children}</div>;
}
