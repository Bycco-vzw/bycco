<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { trndates } from '@/util/constants'

// communication with stepped children
const step = ref(1)
const refintro = ref(null)
const refresponsible = ref(null)

// data model
const lodging = ref({})
const too_early = computed(() => {
  return new Date() < trndates.lodging_start
})

// i18n
const { t } = useI18n()

function changeStep(s) {
  console.log('receive update step', s)
  switch (s) {
    case 1:
      refintro.value.setup(lodging.value)
      break
    case 2:
      refresponsible.value.setup(lodging.value)
      break
  }
}

function updateLodging(l) {
  Object.assign(lodging.value, l)
}


</script>

<template>
  <v-container fluid>
    <h1 class="my-2">
      {{ $t('Reservation tool') }}
    </h1>
    <div v-if="too_early">
      {{ $t('Reservation for lodging not started yet') }}
    </div>
    <div v-if="!too_early">
      <v-stepper v-model="step">
        <v-stepper-header>
          <v-stepper-item title="Intro" :value="1" />
        </v-stepper-header>
        <v-stepper-window direction="vertical" v-show="step == 1">
          <v-stepper-window-item :value="1">
            <Lodging-Intro ref="refintro" />
          </v-stepper-window-item>
        </v-stepper-window>
        <v-stepper-header>
          <v-stepper-item title="Responsible" :value="2" />
        </v-stepper-header>
        <v-stepper-window direction="vertical" v-show="step == 1">
          <v-stepper-window-item :value="1">
            <Lodging-Responsible ref="refresponsible" />
          </v-stepper-window-item>
        </v-stepper-window>



        <!-- <v-stepper-step :complete="step > 2" step="2">
            {{ $t('Step') }} 2
          </v-stepper-step>
          <v-stepper-content step="2">
            <Lodging-Responsible />
          </v-stepper-content>

          <v-stepper-step :complete="step > 3" step="2">
            {{ $t('Step') }} 3
          </v-stepper-step>
          <v-stepper-content step="3">
            <Lodging-Guests />
          </v-stepper-content>

          <v-stepper-step :complete="step > 4" step="4">
            {{ $t('Step') }} 4
          </v-stepper-step>
          <v-stepper-content step="4">
            <Lodging-Accomodation />
          </v-stepper-content>

          <v-stepper-step :complete="step > 5" step="5">
            {{ $t('Step') }} 5
          </v-stepper-step>
          <v-stepper-content step="5">
            <Lodging-Meals />
          </v-stepper-content>

          <v-stepper-step :complete="confirmed" step="6">
            {{ $t('Step') }} 6
          </v-stepper-step>
          <v-stepper-content step="6">
            <Lodging-Confirmation />
          </v-stepper-content> -->
      </v-stepper>
    </div>
  </v-container>
</template>