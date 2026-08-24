import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'
import basicSsl from '@vitejs/plugin-basic-ssl'

export default defineConfig({
  plugins: [
    react(),
    basicSsl(),
    VitePWA({
      registerType: 'autoUpdate',
      devOptions: { enabled: true },
      manifest: {
        name: 'API Corrección Formativa',
        short_name: 'CorrecciónIA',
        description: 'Entorno de Evaluación Formativa con IA',
        theme_color: '#0f111a',
        background_color: '#0f111a',
        display: 'standalone',
        icons: [
          {
            src: 'https://vitejs.dev/logo.svg',
            sizes: '192x192',
            type: 'image/svg+xml'
          }
        ]
      }
    })
  ],
  server: {
    https: true,
    port: 5173
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setup.js'
  }
})