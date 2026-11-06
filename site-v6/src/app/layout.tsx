import { SupportWidgets } from '@/components/SupportWidgets';
import type { Metadata, Viewport } from 'next';
import '@fontsource/be-vietnam-pro/vietnamese-400.css';
import '@fontsource/be-vietnam-pro/vietnamese-600.css';
import '@fontsource/be-vietnam-pro/vietnamese-800.css';
import '@fontsource/be-vietnam-pro/latin-400.css';
import '@fontsource/be-vietnam-pro/latin-600.css';
import '@fontsource/be-vietnam-pro/latin-800.css';
import './chat-widget.css';
import './globals.css';
import './content-visuals.css';
import './ui-refinement.css';
export const metadata: Metadata = {
  metadataBase: new URL('https://myagentvn.com'),
  title: 'My Agent — Website tạo dấu ấn',
  description: 'Thiết kế website, landing page và website bán hàng. My Agent tại TP.HCM, nhận khách toàn quốc.',
  other: { 'page-type': 'service', 'site-kind': 'other' },
  icons: { icon: '/brand/favicon.svg' },
};
export const viewport: Viewport = { themeColor: '#05070F' };
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>) {
  return <html lang="vi" data-type="service" data-motion="on"><body>{children}<SupportWidgets/></body></html>;
}

