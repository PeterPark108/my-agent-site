import type { NextConfig } from 'next';
const config: NextConfig = { output: 'export', distDir: '.next-v5', generateBuildId: async () => 'myagent-v6', poweredByHeader: false, reactStrictMode: true, images: { unoptimized: true } };
export default config;
