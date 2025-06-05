import tailwindcss from "@tailwindcss/vite";
import svgLoader from 'vite-svg-loader'

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: false },
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/color-mode',
    '@nuxt/ui',
    '@nuxt/image',
    '@nuxt/fonts',
    '@nuxtjs/tailwindcss',
  ],
  runtimeConfig: {
    public: {
      baseURL: process.env.BASE_URL || 'http://localhost:5000/api'
    }
  },
  css: [
      '@/assets/css/main.css',
  ],
  vite: {
    plugins: [
      svgLoader(),
    ],
    server: {
      allowedHosts: []
    },
  },
  fonts: {
    google: {
      families: {
        'Open+Sans': [300, 400, 500, 600, 700, 800],
        'Inter': [100, 200, 300, 400, 500, 600, 700, 800, 900],
      },
    },
  },
  colorMode: {
    preference: 'system', // По умолчанию использовать системную тему
    fallback: 'light',    // Если системная тема недоступна — светлая
    classSuffix: '',      // Класс будет просто 'dark' или 'light'
  },
  ui: {
    prefix: 'Nuxt',
    theme: {
      colors: [
        'background',
        'text',
        'primary',
        'primaryHover',
        'neutral',
        'accent',
        'secondary',
        'success',
        'info',
        'warning',
          'error',
        'button',
        'border',
        'test'
      ]
    },
  }
})