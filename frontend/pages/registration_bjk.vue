<script setup>
import { ref, computed } from "vue"
import { useI18n } from "vue-i18n"

// communication with stepped children
const step = ref(1)
const refintro = ref(null)
const refidnumber = ref(null)
const refdetails = ref(null)
const refphoto = ref(null)
const refnat = ref(null)
const refconfirmation = ref(null)
const today = new Date()

// cutoff after 23rd of February 2025
const cutoffdate = new Date(2025, 1, 24)
const active = cutoffdate.valueOf() > today.valueOf()

// data model
const registration = ref({})

// i18n
const { t } = useI18n()

function changeStep(s) {
  console.log("receive update step", s)
  step.value = s
  switch (s) {
    case 1:
      refintro.value.setup(registration.value)
      break
    case 2:
      refidnumber.value.setup(registration.value)
      break
    case 3:
      refdetails.value.setup(registration.value)
      break
    case 4:
      refphoto.value.setup(registration.value)
      break
    case 5:
      refnat.value.setup(registration.value)
      break
    case 6:
      refconfirmation.value.setup(registration.value)
      break
  }
}

function updateRegistration(l) {
  console.log("registration updated", l)
  Object.assign(registration.value, l)
}

function restart() {
  registration.value = {}
  step.value = 1
}
</script>

<template>
  <v-container fluid>
    <h1 class="my-2">{{ t("enroll.tool") }} {{ t("BYC 2025") }}</h1>
    <div v-if="!active">
      <p class="mt-5">Inschrijvingen afgesloten</p>
      <p class="mt-5">Enregistrements clôturés</p>
      <p class="mt-5">Registrations closed</p>
      <p class="mt-5">Anmeldungen geschlossen</p>
    </div>
    <div v-if="active">
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>1</v-chip>
          Intro
        </v-card-title>
        <v-card-text>
          <RegistrationIntro
            v-show="step == 1"
            ref="refintro"
            @change-step="changeStep"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>2</v-chip>
          {{ t("ID number") }}
        </v-card-title>
        <v-card-text>
          <RegistrationIdnumber
            v-show="step == 2"
            ref="refidnumber"
            @change-step="changeStep"
            @update-registration="updateRegistration"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>3</v-chip>
          {{ t("Details") }}
        </v-card-title>
        <v-card-text>
          <RegistrationDetails
            v-show="step == 3"
            ref="refdetails"
            @change-step="changeStep"
            @update-registration="updateRegistration"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>4</v-chip>
          {{ t("Photo") }}
        </v-card-title>
        <v-card-text v-show="step == 4">
          <RegistrationPhoto
            ref="refphoto"
            @change-step="changeStep"
            @update-registration="updateRegistration"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>5</v-chip>
          {{ t("Nationality") }}
        </v-card-title>
        <v-card-text>
          <RegistrationNationality
            v-show="step == 5"
            ref="refnat"
            @change-step="changeStep"
            @update-registration="updateRegistration"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>6</v-chip>
          {{ t("Confirmation") }}
        </v-card-title>
        <v-card-text>
          <RegistrationConfirmation
            v-show="step == 6"
            ref="refconfirmation"
            @change-step="changeStep"
            @restart="restart"
          />
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<style scoped>
.bottomline {
  border-bottom: 1px solid #aaa;
}
</style>
