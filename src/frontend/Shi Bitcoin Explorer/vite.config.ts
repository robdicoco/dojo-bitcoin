import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import fs from 'fs'
import path from 'path'

export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    https: {
      key: fs.readFileSync(path.resolve(__dirname, '../keys/privkey.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, '../keys/fullchain.pem')),
    },
    port: 5173, // Optional: Specify a port (default is 5173)
    proxy: {
      '/api': {
        target: 'https://shisatoshi.758206.xyz:5000', // Backend server URL
        changeOrigin: true, // Required for virtual hosted sites
        rewrite: (path) => path.replace(/^\/api/, ''), // Remove `/api` prefix
        secure: true, // Disable SSL verification (not recommended for production)
      },
      '/api2': {
        target: 'http://127.0.0.1:8000', // Backend server URL
        changeOrigin: true, // Required for virtual hosted sites
        rewrite: (path) => path.replace(/^\/api2/, ''), // Remove `/api2` prefix
        secure: false, // Disable SSL verification (not recommended for production)
      },
    },
  },
})
