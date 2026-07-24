import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  root: '.',
  plugins: [react()],
  resolve: { extensions: ['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json'] },
});
