import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

console.log(process.env.DEBUG)
// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode` in the current working directory.
  const env = loadEnv(mode, process.cwd(), '')
  
  console.log('Environment variables:', env.VITE_DEBUG)
  
  return {
    plugins: [react()],
    server: {
      ...(env.VITE_DEBUG === 'true' && {
        proxy: {
          '/api': {
            target: 'http://localhost:8000',
            changeOrigin: true,
            secure: false,
          }
        }
      })
    }
  }
})
