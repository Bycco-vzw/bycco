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

  modules: [
    '@pinia/nuxt',
    async (options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig',
        config => config.plugins.push(vuetify())
      )
    },
  ],

  nitro: {
    prerender: {
      crawlLinks: false,
      failOnError: true,
    }
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
  },

  devtools: {
    timeline: {
      enabled: true
    }
  }
})