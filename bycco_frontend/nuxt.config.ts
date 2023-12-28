import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: '/css/bycco.css',
        },
      ],
    },
  },
  build: {
    transpile: ['vuetify'],
  },
  css: [
    'vuetify/lib/styles/main.sass',
    '@mdi/font/css/materialdesignicons.min.css',
  ],
  experimental: {
    payloadExtraction: false,
  },
  i18n: {
    defaultLocale: "nl",
    lazy: true,
    locales: [
      { code: "nl", file: "nl.js" },
      { code: "fr", file: "fr.js" },
      { code: "de", file: "de.js" },
      { code: "en", file: "en.js" },
    ],
    langDir: "lang/",  
    strategy: "prefix",
    vueI18n: './i18n.config.ts',
  },    
  modules: ['@nuxtjs/i18n', '@pinia/nuxt'],
  nitro: {
    prerender: {
      crawlLinks: false,
      failOnError: false,
    },
  },
  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL || 'http://localhost:8000/',
      statamicurl: process.env.STATAMIC_URL || 'http://localhost:8000/',
      repo_branch: 'master',
    },
  },
  vite: {
    vue: {
      template: {
        transformAssetUrls
      }
    }
  }
})
