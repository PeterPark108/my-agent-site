'use client';
import Image from 'next/image';
import { useRef, useState } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { featuredProjects } from '@/content/featured-projects';

gsap.registerPlugin(useGSAP, ScrollTrigger);
const destinations = [
  { id: 'services', label: 'Dịch vụ', number: '01', angle: -12, roll: -4 },
  { id: 'projects', label: 'Dự án', number: '02', angle: 14, roll: 5 },
  { id: 'connect', label: 'Kết nối', number: '03', angle: -6, roll: 3 },
] as const;
type Destination = typeof destinations[number]['id'];

function OrbitIcon({ kind }: { kind: Destination }) {
  return <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {kind === 'services' ? <><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/></> : kind === 'projects' ? <><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01m1 6 4 2.5-4 2.5v-5Z"/></> : <><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5H4l-1 1v-8.5A8.5 8.5 0 0 1 11.5 4h1a8.5 8.5 0 0 1 8.5 7.5Z"/><path d="M8 11h8M8 15h5"/></>}
  </svg>;
}

export function CosmicNavigator() {
  const root = useRef<HTMLDivElement>(null);
  const buttons = useRef<(HTMLButtonElement | null)[]>([]);
  const turn = useRef<((angle: number, roll: number) => void) | null>(null);
  const [active, setActive] = useState<Destination | null>(null);
  const [projectIndex, setProjectIndex] = useState(0);
  const destination = destinations.find(item => item.id === active);
  const project = featuredProjects[projectIndex];

  // Selection turns its own wrapper; the existing orb still owns pointer tilt and floating.
  useGSAP(() => {
    const mm = gsap.matchMedia();
    mm.add('(prefers-reduced-motion: no-preference)', () => {
      const orientation = root.current?.querySelector('.orb-orientation');
      if (!orientation) return;
      const yaw = gsap.quickTo(orientation, 'rotationY', { duration: .9, ease: 'power3.out' });
      const roll = gsap.quickTo(orientation, 'rotation', { duration: .9, ease: 'power3.out' });
      turn.current = (angle, tilt) => { yaw(angle); roll(tilt); };
      return () => { turn.current = null; };
    }, root);
    return () => mm.revert();
  }, { scope: root });

  useGSAP(() => {
    turn.current?.(destination?.angle ?? 0, destination?.roll ?? 0);
    const mm = gsap.matchMedia();
    mm.add('(prefers-reduced-motion: no-preference)', () => {
      const panel = root.current?.querySelector<HTMLElement>('.orbit-console');
      if (panel) {
        const timeline = gsap.timeline({ defaults: { ease: 'power3.out', clearProps: 'opacity,transform' } })
          .fromTo(panel, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .35 });
        const items = panel.querySelectorAll('[data-orbit-item]');
        if (items.length) timeline.fromTo(items, { opacity: 0, y: 6 }, { opacity: 1, y: 0, duration: .28, stagger: .04 }, '-=.2');
      }
    }, root);
    // The mobile panel adds real document height; refresh only on open/close or resize.
    let revealPanel = Boolean(active);
    const refresh = gsap.delayedCall(.1, () => {
      ScrollTrigger.refresh();
      if (revealPanel && matchMedia('(max-width: 1375px)').matches) {
        root.current?.querySelector('.orbit-console')?.scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
      }
      revealPanel = false;
    });
    const resize = new ResizeObserver(() => refresh.restart(true));
    if (root.current) resize.observe(root.current);
    return () => { resize.disconnect(); mm.revert(); };
  }, { scope: root, dependencies: [active], revertOnUpdate: true });

  useGSAP(() => {
    if (active !== 'projects') return;
    const mm = gsap.matchMedia();
    mm.add('(prefers-reduced-motion: no-preference)', () => {
      gsap.fromTo('.orbit-project-preview', { opacity: .5, x: 8 }, { opacity: 1, x: 0, duration: .25, ease: 'power2.out', clearProps: 'opacity,transform' });
    }, root);
    return () => mm.revert();
  }, { scope: root, dependencies: [active, projectIndex], revertOnUpdate: true });

  function close() {
    const index = destinations.findIndex(item => item.id === active);
    setActive(null);
    buttons.current[index]?.focus({ preventScroll: !matchMedia('(max-width: 1375px)').matches });
  }
  return <div ref={root} className="hero-art orbit-explorer" data-orbit={active ?? 'idle'} onKeyDown={event => {
    if (event.key === 'Escape' && active) { event.preventDefault(); event.stopPropagation(); close(); }
  }}>
    <div className="orbit-stage">
      <div className="orb-orientation" aria-hidden="true">
        <div className="orb-halo"/>
        <div className="orbit-float orbit-float-one"><div className="tech-orbit tech-orbit-one"><i/></div></div>
        <div className="orb"><div className="orb-grid"/><div className="orb-latitude latitude-one"/><div className="orb-latitude latitude-two"/><div className="orb-meridian meridian-one"/><div className="orb-meridian meridian-two"/><div className="orb-equator"/><div className="orb-shine"/><span className="orb-mark">M</span><span className="orb-code">MY AGENT / DIGITAL CORE</span></div>
        <div className="orbit-float orbit-float-two"><div className="tech-orbit tech-orbit-two"><i/></div></div>
        <div className="orbit-float orbit-float-three"><div className="tech-orbit tech-orbit-three"><i/></div></div>
      </div>
      <div className="orbit-destinations" role="group" aria-label="Khám phá My Agent qua ba quỹ đạo">
        {destinations.map((item, index) => <button key={item.id} ref={el => { buttons.current[index] = el; }} id={'orbit-'+item.id} className={'orbit-node orbit-node-'+item.id} type="button" aria-expanded={active === item.id} aria-controls="orbit-content" onClick={() => setActive(active === item.id ? null : item.id)} onKeyDown={event => {
          let next = index;
          if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % 3;
          else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index + 2) % 3;
          else if (event.key === 'Home') next = 0;
          else if (event.key === 'End') next = 2;
          else return;
          event.preventDefault(); buttons.current[next]?.focus();
        }}><span className="orbit-node-light" aria-hidden="true"/><OrbitIcon kind={item.id}/><span>{item.label}</span><span className="orbit-node-index" aria-hidden="true">{item.number}</span></button>)}
      </div>
      <div className="art-coordinates" aria-hidden="true">TP. HỒ CHÍ MINH<br/>PHỤC VỤ TOÀN QUỐC</div>
      <div className="art-index" aria-hidden="true">DESIGN × TECHNOLOGY</div>
      <p className="orbit-hint">Chọn một quỹ đạo để khám phá <span aria-hidden="true">↗</span></p>
    </div>
    <div id="orbit-content" hidden={!active}>
      {destination && <section className="orbit-console" aria-labelledby="orbit-panel-title">
        <div className="orbit-console-heading"><span>{destination.number} / {destination.label}</span><button type="button" className="orbit-close" aria-label="Đóng bảng khám phá" onClick={close}>×</button></div>
        <h2 id="orbit-panel-title">{active === 'services' ? 'Bạn muốn bắt đầu từ đâu?' : active === 'projects' ? 'Khám phá sản phẩm mẫu.' : 'Cùng bắt đầu dự án.'}</h2>
        {active === 'services' && <>
          <div className="orbit-service-links">
            <a data-orbit-item href="/dich-vu/thiet-ke-website.html"><span>Website doanh nghiệp<small>Giới thiệu · Bán hàng · Landing page</small></span><b aria-hidden="true">↗</b></a>
            <a data-orbit-item href="/dich-vu/quang-cao-google-facebook.html"><span>Quảng cáo Google & Facebook<small>Kết nối với khách hàng</small></span><b aria-hidden="true">↗</b></a>
            <a data-orbit-item href="/dich-vu/phan-mem-noi-bo.html"><span>Phần mềm nội bộ<small>Công cụ cho công việc của bạn</small></span><b aria-hidden="true">↗</b></a>
          </div>
          <a className="orbit-more" data-orbit-item href="/dich-vu.html">Xem đủ 18 dịch vụ <span aria-hidden="true">↗</span></a>
        </>}
        {active === 'projects' && <>
          <a className="orbit-project-preview" href={project.href} target="_blank" rel="noopener noreferrer">
            <Image src={project.image} alt={project.alt} width={1600} height={900} sizes="(max-width:700px) 80vw, 320px"/>
            <span><strong>{project.name}</strong><span>Mở demo <span aria-hidden="true">↗</span></span></span>
          </a>
          <div className="orbit-project-controls"><span role="status" aria-live="polite" aria-atomic="true">{project.name} · {projectIndex + 1}/{featuredProjects.length}</span><button type="button" aria-label="Dự án trước" onClick={() => setProjectIndex((projectIndex + featuredProjects.length - 1) % featuredProjects.length)}>←</button><button type="button" aria-label="Dự án tiếp theo" onClick={() => setProjectIndex((projectIndex + 1) % featuredProjects.length)}>→</button></div>
          <p className="orbit-note">Sản phẩm mẫu do Peter thực hiện.</p>
        </>}
        {active === 'connect' && <>
          <p className="orbit-connect-intro">Chia sẻ nhu cầu của bạn với My Agent.</p>
          <a className="orbit-contact-primary" data-orbit-item href="https://zalo.me/0328439972" target="_blank" rel="noopener noreferrer">Chat Zalo <span aria-hidden="true">↗</span></a>
          <div className="orbit-contact-links"><a data-orbit-item href="tel:+84328439972">Gọi 0328 439 972 <span aria-hidden="true">↗</span></a><a data-orbit-item href="mailto:vantungn044@gmail.com">Gửi email <span aria-hidden="true">↗</span></a></div>
          <a className="orbit-more" data-orbit-item href="/lien-he.html">Gửi yêu cầu tư vấn <span aria-hidden="true">↗</span></a>
        </>}
      </section>}
    </div>
  </div>;
}
