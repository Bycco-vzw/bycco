<script setup>
import { ref } from "vue"
import { useI18n } from "vue-i18n"

// communication with main tool page
const emit = defineEmits(["changeStep"])
defineExpose({ setup })

// i18n
const { t } = useI18n()

function next() {
  console.log("clicked next")
  emit("changeStep", 2)
}

function setup(l) {
  console.log("setup intro", l)
}
</script>

<template>
  <div>
    <h2>Intro</h2>
    <div class="mt-2">
      {{ t("stay.intro_requirements") }}
      <ul>
        <li>{{ t("stay.intro_responsible") }}</li>
        <li>{{ t("stay.intro_guest") }}</li>
        <li>{{ t("stay.intro_participant") }}</li>
        <li>{{ t("stay.intro_accom") }}</li>
        <li>{{ t("stay.intro_meals") }}</li>
      </ul>
    </div>
    <div class="mt-2">
      {{ t("stay.intro_multiple") }}
    </div>
    <div class="mt-2">
      <v-btn color="primary" @click="next">
        {{ t("Continue") }}
      </v-btn>
    </div>
  </div>
</template>
