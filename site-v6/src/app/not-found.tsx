/* eslint-disable @next/next/no-html-link-for-pages -- Full navigation resets the existing legacy page tools. */
import type { Metadata } from 'next';
import { Cosmos } from '@/components/Cosmos';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Sections';

export const metadata: Metadata = {
  title: 'Không tìm thấy trang | My Agent',
  robots: { index: false, follow: true },
};

export default function NotFound() {
  return <>
    <Cosmos />
    <Header />
    <main id="main" className="container section legal-directory">
      <p className="eyebrow">MY AGENT / 404</p>
      <h1>Không tìm thấy trang.</h1>
      <p>Đường dẫn có thể đã thay đổi hoặc không còn tồn tại. Bạn có thể về trang chủ hoặc khám phá các dịch vụ của My Agent.</p>
      <div className="actions">
        <a className="button" href="/">Về trang chủ <span aria-hidden="true">↗</span></a>
        <a className="text-link" href="/dich-vu.html">Khám phá dịch vụ</a>
      </div>
    </main>
    <Footer />
  </>;
}
