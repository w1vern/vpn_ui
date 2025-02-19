// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  modules: [
    "@primevue/nuxt-module",
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss'
  ],
  primevue: {
    options: {
      theme: {
       
      },
    },
  },
  tailwindcss: {
    // Options
  }
});
