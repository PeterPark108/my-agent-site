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
    media.add('(prefers-reduced-motion: no-preference)', () => {
      const scope = root.current!;
      let disposed = false;
      const cleanup: (() => void)[] = [];
      // Content never waits for an entrance animation.
      gsap.fromTo(scope.querySelector('.reading-progress'), { scaleX: 0 }, {
        scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: true },
      });
      gsap.utils.toArray<HTMLElement>('.glass-icon', scope).forEach(icon => {
        const paths = icon.querySelectorAll('svg path, svg rect, svg circle');
        const stroke = gsap.timeline({ paused: true, defaults: { duration: .28, ease: 'power2.out' } })
          .to(paths, { drawSVG: '12% 88%', stagger: .025 })
          .to(paths, { drawSVG: '0% 100%', stagger: .025 });
        const play = () => stroke.restart();
        icon.addEventListener('pointerenter', play);
        cleanup.push(() => icon.removeEventListener('pointerenter', play));
      });
      const refresh = gsap.delayedCall(.15, () => ScrollTrigger.refresh()).pause();
      const schedule = () => { refresh.restart(true); };
      scope.addEventListener('load', schedule, true);
      scope.addEventListener('toggle', schedule, true);
      void document.fonts.ready.then(() => { if (!disposed) schedule(); });
      return () => {
        disposed = true;
        scope.removeEventListener('load', schedule, true);
        scope.removeEventListener('toggle', schedule, true);
        cleanup.forEach(remove => remove());
      };
    }, root);
    return () => media.revert();
  }, { scope: root });
  return <div ref={root}><div className="reading-progress" aria-hidden="true"/>{children}</div>;
}
