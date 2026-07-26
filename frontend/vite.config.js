import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
     plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',   // 与后端地址一致
        changeOrigin: true,
        // 若仍有问题可添加：
        // configure: (proxy) => {
        //   proxy.on('error', (err) => console.log('代理错误:', err));
        // }
      }
    }
  }
})