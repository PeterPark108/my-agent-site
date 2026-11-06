import Image from 'next/image';

export function Hero() {
  return <section className="hero-stage" aria-labelledby="hero-title"><div className="hero container">
    <div className="hero-copy">
      <p className="eyebrow">My Agent · Thiết kế & công nghệ</p>
      <h1 id="hero-title">Website cho<br/>doanh nghiệp<span className="hero-title-accent">của bạn.</span></h1>
      <p className="hero-description">Thiết kế website, xây dựng nội dung và kết nối các dịch vụ số. Từ ý tưởng đầu tiên đến vận hành.</p>
      <div className="actions"><a className="button" href="#lien-he">Trao đổi dự án <span aria-hidden="true">↗</span></a><a className="button button-outline" href="#dich-vu">Xem các dịch vụ <span aria-hidden="true">↓</span></a></div>
      <p className="hero-location">TP. Hồ Chí Minh · Phục vụ toàn quốc</p>
    </div>
    <a className="hero-work" href="https://gio.myagentvn.com/" target="_blank" rel="noopener noreferrer" aria-label="Mở website mẫu Nhà Gió trong tab mới">
      <div className="hero-work-heading"><span>Website mẫu</span><strong>Nhà Gió</strong><span aria-hidden="true">↗</span></div>
      <div className="hero-work-image"><Image priority src="/projects/nhagio.webp" alt="Website mẫu Nhà Gió do Peter thiết kế, với hình ảnh khu nghỉ dưỡng và công cụ chọn ngày đặt phòng" width={1600} height={900} sizes="(max-width: 960px) 90vw, 55vw"/></div>
    </a>
  </div></section>;
}
