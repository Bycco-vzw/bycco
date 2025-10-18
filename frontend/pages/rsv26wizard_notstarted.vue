<script setup>
import { useI18n } from "vue-i18n"

// data model
const { t } = useI18n()
</script>

<template>
  <v-container>
    <h1 class="my-2">
      {{ t("stay.res_tool") }}
    </h1>
    <div>
      {{ t("stay.res_notstarted") }}
    </div>
  </v-container>
</template>

<style scoped>
.bottomline {
  border-bottom: 1px solid #aaa;
}
</style>
