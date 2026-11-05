import type { NextConfig } from 'next';
// Xuất tĩnh: VPS phục vụ thư mục gốc repo bằng git pull. Header bảo mật đặt ở nginx.
const config: NextConfig = { output: 'export', distDir: '.next-v5', generateBuildId: async () => 'myagent-v7', poweredByHeader: false, reactStrictMode: true, images: { unoptimized: true } };
export default config;
