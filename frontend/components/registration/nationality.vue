<script setup>
import { ref } from "vue"
import { useI18n } from "vue-i18n"

// communication with main tool page
const emit = defineEmits(["changeStep"])
defineExpose({ setup })

// i18n
const { t } = useI18n()

// datamodel
const gdpr_ok = ref(false)
const nat_ok = ref(false)
const natstatus = ref("")
const step = 5

function next() {
  console.log("clicked next")
  emit("changeStep", step + 1)
}

function prev() {
  console.log("clicked prev")
  emit("changeStep", step - 1)
}

function setup(l) {
  console.log("setup nat", l)
  if (l.nationalityfide == "BEL") {
    natstatus.value = "fidebelg"
  } else {
    if (!l.nationalityfide) {
      natstatus.value = "unknown"
    } else {
      natstatus.value = "nobelg"
    }
  }
}
</script>
<template>
  <v-container>
    <v-row>
      <h2>{{ t("Nationality") }}</h2>
    </v-row>
    <v-row>
      <div v-show="natstatus == 'fidebelg'">
        {{ t("enroll.nat_fidebelg", { email: "info@bycco.be" }) }}
      </div>
      <div v-show="natstatus == 'nobelg'">
        {{ t("enroll.nat_nobelg", { email: "info@bycco.be" }) }}
      </div>
      <div v-show="natstatus == 'unknown'">
        {{ t("enroll.nat_unknown", { email: "info@bycco.be" }) }}
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <VCheckbox :label="t('enroll.nat_agree')" v-model="nat_ok" />
      </div>
    </v-row>
    <v-row>
      <h2>{{ t("enroll.gdpr_title") }}</h2>
    </v-row>
    <v-row>
      <div class="mt-2">
        <ul>
          <li>{{ t("enroll.gdpr_1") }}</li>
          <li>{{ t("enroll.gdpr_2") }}</li>
          <li>{{ t("enroll.gdpr_3") }}</li>
          <li>{{ t("enroll.gdpr_4") }}</li>
          <li>{{ t("enroll.gdpr_5") }}</li>
          <li>{{ t("enroll.gdpr_6") }}</li>
        </ul>
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <VCheckbox :label="t('enroll.nat_agree')" v-model="gdpr_ok" />
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <v-btn class="ml-2" @click="prev" color="primary">
          {{ $t("Back") }}
        </v-btn>
        <v-btn :disabled="!gdpr_ok" class="ml-2" color="primary" @click="next">
          {{ $t("Continue") }}
        </v-btn>
      </div>
    </v-row>
  </v-container>
</template>
