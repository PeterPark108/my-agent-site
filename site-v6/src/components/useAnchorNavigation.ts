'use client';
import gsap from 'gsap';
import { ScrollToPlugin } from 'gsap/ScrollToPlugin';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(ScrollToPlugin, ScrollTrigger, useGSAP);

export function useAnchorNavigation() {
  useGSAP((_context, contextSafe) => {
    let disposed = false;
    let frame = 0;
    let scrolling: gsap.core.Tween | undefined;
    const focusTargets = new Set<HTMLElement>();
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const cancel = () => { scrolling?.kill(); };
    const jump = contextSafe!((animate = false, focus = false) => {
      if (disposed || location.pathname !== '/' || !location.hash) return;
      let id: string;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      const target = document.getElementById(id);
      if (!target) return;
      cancel();
      ScrollTrigger.refresh();
      const offset = (document.querySelector('header')?.getBoundingClientRect().height || 80) + 28;
      if (focus) {
        if (!target.hasAttribute('tabindex')) {
          target.setAttribute('tabindex', '-1');
          focusTargets.add(target);
        }
        target.focus({ preventScroll: true });
      }
      const distance = Math.abs(target.getBoundingClientRect().top - offset);
      scrolling = gsap.to(window, {
        scrollTo: { y: target, offsetY: offset, autoKill: true },
        duration: animate && !reduced.matches ? gsap.utils.clamp(.3, .85, distance / 2200) : 0,
        ease: 'power2.inOut', overwrite: 'auto',
      });
    });
    const navigate = (event: MouseEvent) => {
      if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const link = (event.target as Element).closest<HTMLAnchorElement>('a[href]');
      if (!link || link.target || link.hasAttribute('download')) return;
      const url = new URL(link.href, location.href);
      if (location.pathname !== '/' || url.origin !== location.origin || url.pathname !== '/' || url.search !== location.search || !url.hash) return;
      let target: HTMLElement | null;
      try { target = document.getElementById(decodeURIComponent(url.hash.slice(1))); } catch { return; }
      if (!target) return;
      event.preventDefault();
      if (location.hash !== url.hash) history.pushState(null, '', url.hash);
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => jump(!link.classList.contains('skip'), true));
    };
    const hash = () => jump();
    const keyboard = (event: KeyboardEvent) => {
      if (['Escape', 'PageDown', 'PageUp', 'Home', 'End', 'ArrowDown', 'ArrowUp', ' '].includes(event.key)) cancel();
    };
    document.addEventListener('click', navigate);
    document.addEventListener('keydown', keyboard);
    window.addEventListener('hashchange', hash);
    window.addEventListener('wheel', cancel, { passive: true });
    window.addEventListener('touchstart', cancel, { passive: true });
    reduced.addEventListener('change', cancel);
    void document.fonts.ready.then(() => {
      if (!disposed) frame = requestAnimationFrame(() => { frame = requestAnimationFrame(() => jump()); });
    });
    return () => {
      disposed = true; cancelAnimationFrame(frame); cancel();
      focusTargets.forEach(target => target.removeAttribute('tabindex'));
      document.removeEventListener('click', navigate); document.removeEventListener('keydown', keyboard);
      window.removeEventListener('hashchange', hash); window.removeEventListener('wheel', cancel); window.removeEventListener('touchstart', cancel);
      reduced.removeEventListener('change', cancel);
    };
  }, []);
}
