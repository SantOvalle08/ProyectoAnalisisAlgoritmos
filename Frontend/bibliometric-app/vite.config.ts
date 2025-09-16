import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // Alias de rutas para importaciones más limpias
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
      '@pages': fileURLToPath(new URL('./src/pages', import.meta.url)),
      '@hooks': fileURLToPath(new URL('./src/hooks', import.meta.url)),
      '@services': fileURLToPath(new URL('./src/services', import.meta.url)),
      '@types': fileURLToPath(new URL('./src/types', import.meta.url)),
      '@utils': fileURLToPath(new URL('./src/utils', import.meta.url)),
      '@styles': fileURLToPath(new URL('./src/styles', import.meta.url)),
      '@context': fileURLToPath(new URL('./src/context', import.meta.url)),
    },
  },

  // Configuración del servidor de desarrollo
  server: {
    port: 3000,
    host: true,
    open: true,
    cors: true,
    // Proxy para la API del backend
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },

  // Configuración de build para producción
  build: {
    target: 'esnext',
    outDir: 'dist',
    sourcemap: true,
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          // Separar dependencias grandes en chunks
          vendor: ['react', 'react-dom'],
          mui: ['@mui/material', '@mui/icons-material'],
          charts: ['recharts', 'd3', 'plotly.js'],
          router: ['react-router-dom'],
        },
      },
    },
    // Optimizaciones para archivos grandes
    chunkSizeWarningLimit: 1000,
  },

  // Optimizaciones de dependencias
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'axios',
      'recharts',
      '@mui/material',
      '@mui/icons-material',
      'react-router-dom',
      '@tanstack/react-query',
    ],
    exclude: ['plotly.js'],
  },

  // Variables de entorno
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version || '1.0.0'),
  },

  // Configuración CSS
  css: {
    modules: {
      localsConvention: 'camelCaseOnly',
    },
  },

  // Vista previa de producción
  preview: {
    port: 4173,
    host: true,
    cors: true,
  },
})
