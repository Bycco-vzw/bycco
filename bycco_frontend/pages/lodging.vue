<script setup>
import { useI18n } from "vue-i18n"
const { t } = useI18n()
</script>

<template>
  <v-container>
    <h1>{{ t('Lodging') }}</h1>
    Hotel Floreal
  </v-container>
</template>