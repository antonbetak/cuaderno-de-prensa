import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
export default defineConfig({
  plugins: [react()],
  base: './',
  resolve: { alias: { '@': path.resolve(import.meta.dirname, '.') } },
  server: { host: '127.0.0.1', watch: { usePolling: true } },
});
