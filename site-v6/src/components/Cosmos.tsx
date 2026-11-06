'use client';
import { useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(useGSAP);

export function Cosmos() {
  const root = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  useGSAP(() => {
    const media = gsap.matchMedia();
    media.add({ all: 'all', small: '(max-width: 700px)', reduce: '(prefers-reduced-motion: reduce)' }, context => {
      const surface = canvas.current;
      const field = surface?.getContext('2d');
      if (!surface || !field || !root.current) return;
      const reduced = Boolean(context.conditions?.reduce);
      const small = Boolean(context.conditions?.small);
      let width = 1, height = 1, light = false, elapsed = 0, ticking = false;
      let seed = 72619;
      const random = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
      const stars = Array.from({ length: small ? 85 : 155 }, (_, index) => {
        const depth = index % 3;
        return { x: random(), y: random(), depth, radius: .45 + depth * .34 + random() * .25, alpha: .22 + depth * .17 + random() * .2 };
      });
      const draw = () => {
        field.clearRect(0, 0, width, height);
        for (const star of stars) {
          const x = star.x * width, y = star.y * height;
          field.fillStyle = light ? '#31517e' : star.depth === 2 ? '#e4efff' : '#a8c5f6';
          if (star.depth === 2 && !light) {
            field.globalAlpha = star.alpha * .07;
            field.beginPath(); field.arc(x, y, star.radius * 3.8, 0, Math.PI * 2); field.fill();
          }
          field.globalAlpha = star.alpha;
          field.beginPath(); field.arc(x, y, star.radius, 0, Math.PI * 2); field.fill();
        }
        field.globalAlpha = 1;
      };
      const resize = () => {
        width = root.current!.clientWidth; height = root.current!.clientHeight;
        const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
        surface.width = Math.round(width * ratio); surface.height = Math.round(height * ratio);
        field.setTransform(ratio, 0, 0, ratio, 0, 0);
        draw();
      };
      const readTheme = () => { light = document.documentElement.dataset.theme === 'light'; draw(); };
      const tick = (_time: number, delta: number) => {
        elapsed += Math.min(delta, 64);
        if (elapsed < 1000 / 30) return;
        const seconds = elapsed / 1000; elapsed = 0;
        for (const star of stars) {
          const travel = (4 + star.depth * 7) * (small ? .75 : 1) * seconds;
          star.x -= travel / width; star.y += travel * .28 / height;
          if (star.x < -.01) star.x += 1.02;
          if (star.y > 1.01) star.y -= 1.02;
        }
        draw();
      };
      resize(); readTheme();
      const observer = new ResizeObserver(resize); observer.observe(root.current);
      const themeObserver = new MutationObserver(readTheme);
      themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

      const meteor = (kind: 'small' | 'large', period: number, flight: number) => {
        const element = root.current!.querySelector<HTMLElement>('.cosmic-meteor-'+kind)!;
        let passes = 0;
        const record = () => { element.dataset.pass = String(++passes); element.dataset.startedAt = performance.now().toFixed(0); };
        const distance = () => Math.min(width * (kind === 'large' ? .85 : .5), kind === 'large' ? 980 : 580);
        const timeline = gsap.timeline({ delay: period, repeat: -1, repeatDelay: period - flight, repeatRefresh: true, onStart: record, onRepeat: record });
        timeline.fromTo(element, {
          x: () => width * gsap.utils.random(kind === 'large' ? .65 : .35, .97),
          y: () => height * gsap.utils.random(.06, kind === 'large' ? .35 : .65),
          rotation: -15.64, opacity: 0,
        }, { x: () => '-='+distance(), y: () => '+='+distance() * .28, duration: flight, ease: 'none' }, 0)
          .to(element, { opacity: 1, duration: .1, ease: 'none' }, 0)
          .to(element, { opacity: 0, duration: .3, ease: 'power1.out' }, flight - .3);
        return timeline;
      };
      const meteors = reduced ? [] : [meteor('small', 5, .9), meteor('large', 10, 1.6)];
      const sync = () => {
        const paused = document.hidden || reduced;
        root.current?.setAttribute('data-paused', String(paused));
        meteors.forEach(animation => animation.paused(paused));
        if (paused && ticking) { gsap.ticker.remove(tick); ticking = false; }
        else if (!paused && !ticking) { elapsed = 0; gsap.ticker.add(tick); ticking = true; }
      };
      document.addEventListener('visibilitychange', sync); sync();
      return () => { observer.disconnect(); themeObserver.disconnect(); document.removeEventListener('visibilitychange', sync); gsap.ticker.remove(tick); };
    }, root);
    return () => media.revert();
  }, { scope: root });
  return <div className="cosmos cosmic-flight" ref={root} aria-hidden="true">
    <div className="cosmos-nebula"/>
    <canvas ref={canvas} className="cosmos-field"/>
    <span className="cosmic-meteor cosmic-meteor-small" data-pass="0"/>
    <span className="cosmic-meteor cosmic-meteor-large" data-pass="0"/>
  </div>;
}
