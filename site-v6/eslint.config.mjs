import { defineConfig, globalIgnores } from 'eslint/config';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTs from 'eslint-config-next/typescript';
export default defineConfig([...nextVitals,...nextTs,globalIgnores(['.next/**','.next-preview/**','.next-v4/**','.next-v5/**','public/js/**','src/lib/pricing-engine.cjs','scripts/prepare-build.cjs','playwright-report/**','test-results/**'])]);

