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
    port: 5173,
    host: 'shisatoshi.758206.xyz', // Explicitly set the host
    hmr: {
      host: 'shisatoshi.758206.xyz', // Set HMR host to match the server
      port: 5173, // Set HMR port to match the server
    },
    proxy: {
      '/reg': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/reg/, ''),
        secure: false,
        // onProxyReq: (proxyReq, req, res) => {
        //   console.log('Proxying request:', req.url) // Debugging
        // },,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Proxying request:', req.url) // Log the request URL
          })
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Proxy response:', proxyRes.statusCode) // Log the response status
          })
          proxy.on('error', (err, req, res) => {
            console.error('Proxy error:', err) // Log any errors
          })
        },
      },
      '/api': {
        target: 'https://shisatoshi.758206.xyz:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: true,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Proxying request:', req.url) // Log the request URL
          })
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Proxy response:', proxyRes.statusCode) // Log the response status
          })
          proxy.on('error', (err, req, res) => {
            console.error('Proxy error:', err) // Log any errors
          })
        },
      },
    },
  },
})
