<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'


// communication with stepped children
const step = ref(1)
const refintro = ref(null)
const refidnumber = ref(null)
const refdetails = ref(null)
const refphoto = ref(null)
const refgdpr = ref(null)
const refconfirmation = ref(null)


// data model
const enrollment = ref({})


// i18n
const { t } = useI18n()

function changeStep(s) {
  console.log('receive update step', s)
  step.value = s
  switch (s) {
    case 1:
      refintro.value.setup(enrollment.value)
      break
    case 2:
      refidnumber.value.setup(enrollment.value)
      break
    case 3:
      refdetails.value.setup(enrollment.value)
      break
    case 4:
      refphoto.value.setup(enrollment.value)
      break
    case 5:
      refgdpr.value.setup(enrollment.value)
      break
    case 6:
      refconfirmation.value.setup(enrollment.value)
      break
  }
}

function updateEnrollment(l) {
  console.log('enrollment updated', l)
  Object.assign(enrollment.value, l)
}

function restart() {
  enrollment.value = {}
  step.value = 1
}

</script>

<template>
  <v-container fluid>
    <h1 class="my-2">
      {{ t('enrollvk.tool') }}
    </h1>
    <div>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>1</v-chip>
          Intro
        </v-card-title>
        <v-card-text>
          <EnrollmentIntro v-show="step == 1" ref="refintro" @change-step="changeStep" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>2</v-chip>
          {{ t('ID number') }}
        </v-card-title>
        <v-card-text>
          <EnrollmentIdnumber v-show="step == 2" ref="refidnumber" @change-step="changeStep"
            @update-enrollment="updateEnrollment" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>3</v-chip>
          {{ t('Details') }}
        </v-card-title>
        <v-card-text>
          <EnrollmentDetails v-show="step == 3" ref="refdetails" @change-step="changeStep"
            @update-enrollment="updateEnrollment" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>4</v-chip>
          {{ t('Photo') }}
        </v-card-title>
        <v-card-text v-show="step == 4">
          <EnrollmentPhoto ref="refphoto" @change-step="changeStep"
            @update-enrollment="updateEnrollment" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>5</v-chip>
          {{ t('GDPR') }}
        </v-card-title>
        <v-card-text>
          <EnrollmentGdpr v-show="step == 5" ref="refgdpr" @change-step="changeStep"
            @update-enrollment="updateEnrollment" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>6</v-chip>
          {{ t('Confirmation') }}
        </v-card-title>
        <v-card-text>
          <EnrollmentConfirmation v-show="step == 6" ref="refconfirmation" @change-step="changeStep"
            @restart="restart" />
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