import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/monitor/',
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8901',
        changeOrigin: true
      }
    }
  }
})
