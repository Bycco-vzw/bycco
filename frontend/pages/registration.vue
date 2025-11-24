<script setup>
import { ref, computed } from "vue"
import { useI18n } from "vue-i18n"

// communication with stepped children
const { $backend } = useNuxtApp()
const step = ref(1)
const refintro = ref(null)
const refidnumber = ref(null)
const refdetails = ref(null)
const refphoto = ref(null)
const refnat = ref(null)
const refconfirmation = ref(null)


// data model
const registration = ref({})
const common = ref(null)
const status = ref("closed")
const { t } = useI18n()

function calcStatus() {
  let now = new Date()
  let opendate = new Date(common.value.trndates.regopen)
  let closedate = new Date(common.value.trndates.regclose)
  console.log(opendate, closedate, now)
  if (opendate.valueOf() > now.valueOf()) {
    status.value = "notyetopen"
    return
  }
  if (closedate.valueOf() < now.valueOf()) {
    status.value = "closed"
  } else {
    status.value = "open"
  }
}

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

async function readCommon() {
  try {
    const reply = await $backend("stay", "get_common", {})
    common.value = reply.data
  } catch (error) {
    console.error("failed to fetch common", error)
    return null
  }
}

onMounted(async () => {
  await readCommon()
  calcStatus()
})

</script>

<template>
  <v-container fluid>
    <h1 class="my-2">
      {{ t("reg.tool") }} {{ t("BYC 2026") }}
    </h1>
    <div class v-if="status == 'closed'">      
      {{ t("reg.reg_closed") }}
    </div>
    <div class="my-2" v-if="status == 'notyetopen'">
      {{ t("reg.reg_notstarted") }}
    </div>    
    <div  class="my-2" v-if="status == 'open'">
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>1</v-chip>
          {{ t("reh.intro") }}
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
          {{ t("reg.idnumber") }}
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
          {{ t("reg.details") }}
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
          {{ t("reg.photo") }}
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
          {{ t("reg.nationality") }}
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
          {{ t("reg.confirmation") }}
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
