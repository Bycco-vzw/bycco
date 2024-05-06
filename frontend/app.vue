<script setup>
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

function setLocale(l) {
  if (process.client) {
    localStorage.setItem("locale", l)
  }
  locale.value = l
}

if (process.client) {
  let _bl = (navigator.userLanguage || navigator.language).replace('-', '_')
  let browserlocale = _bl.split('_')[0];
  console.log('browserlocale', browserlocale)
  let storagelocale = localStorage.getItem("locale")
  console.log('storagelocale', storagelocale)
  if (!storagelocale) {
    storagelocale = browserlocale
  }
  setLocale(storagelocale)
}

</script>
<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>