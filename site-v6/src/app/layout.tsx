import { SupportWidgets } from '@/components/SupportWidgets';
import type { Metadata, Viewport } from 'next';
import '@fontsource/be-vietnam-pro/vietnamese-400.css';
import '@fontsource/be-vietnam-pro/vietnamese-600.css';
import '@fontsource/be-vietnam-pro/vietnamese-800.css';
import '@fontsource/be-vietnam-pro/latin-400.css';
import '@fontsource/be-vietnam-pro/latin-600.css';
import '@fontsource/be-vietnam-pro/latin-800.css';
import '@fontsource/be-vietnam-pro/vietnamese-400-italic.css';
import '@fontsource/be-vietnam-pro/latin-400-italic.css';
import './chat-widget.css';
import './globals.css';
export const metadata: Metadata = {
  metadataBase: new URL('https://myagentvn.com'),
  title: 'My Agent — Website tạo dấu ấn',
  description: 'Thiết kế website, landing page và website bán hàng. My Agent tại TP.HCM, nhận khách toàn quốc.',
  icons: { icon: '/brand/favicon.svg' },
};
export const viewport: Viewport = { themeColor: '#05070F' };
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>) {
  return <html lang="vi"><body>{children}<SupportWidgets/></body></html>;
}

