<script setup>
import { useI18n } from "vue-i18n"
const { t } = useI18n()
</script>

<template>
  <v-container>
    <h1>{{ t('Enrollment') }}</h1>
    Inschrijving
  </v-container>
</template>