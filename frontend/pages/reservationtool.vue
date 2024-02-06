<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { trndates } from '@/util/constants'

// communication with stepped children
const step = ref(1)
const refintro = ref(null)
const refresponsible = ref(null)
const refguests = ref(null)
const refaccomodation = ref(null)
const refmeals = ref(null)
const refconfirmation = ref(null)


// data model
const lodging = ref({ guestlist: [] })
const too_early = computed(() => {
  return new Date() < trndates.lodging_start
})

// i18n
const { t } = useI18n()

function changeStep(s) {
  console.log('receive update step', s)
  step.value = s
  switch (s) {
    case 1:
      refintro.value.setup(lodging.value)
      break
    case 2:
      refresponsible.value.setup(lodging.value)
      break
    case 3:
      refguests.value.setup(lodging.value)
      break
    case 4:
      refaccomodation.value.setup(lodging.value)
      break
    case 5:
      refmeals.value.setup(lodging.value)
      break
    case 6:
      refconfirmation.value.setup(lodging.value)
      break
  }
}

function updateLodging(l) {
  console.log('tool lodging updated', l)
  Object.assign(lodging.value, l)
}

</script>

<template>
  <v-container fluid>
    <h1 class="my-2">
      {{ t('Reservation tool') }}
    </h1>
    <div v-if="too_early">
      {{ t('Reservation for lodging not started yet') }}
    </div>
    <div v-if="!too_early">
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>1</v-chip>
          Intro
        </v-card-title>
        <v-card-text v-show="step == 1">
          <Lodging-Intro ref="refintro" @change-step="changeStep" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>2</v-chip>
          {{ t('Responsible of the reservation') }}
        </v-card-title>
        <v-card-text v-show="step == 2">
          <Lodging-Responsible ref="refresponsible" @change-step="changeStep"
            @update-lodging="updateLodging" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>3</v-chip>
          {{ t('Guest list') }}
        </v-card-title>
        <v-card-text v-show="step == 3">
          <Lodging-Guests ref="refguests" @change-step="changeStep" @update-lodging="updateLodging" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>4</v-chip>
          {{ t('Accomodation') }}
        </v-card-title>
        <v-card-text v-show="step == 4">
          <Lodging-Accomodation ref="refaccomodation" @change-step="changeStep"
            @update-lodging="updateLodging" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>5</v-chip>
          {{ t('Meals') }}
        </v-card-title>
        <v-card-text v-show="step == 5">
          <Lodging-Meals ref="refmeals" @change-step="changeStep" @update-lodging="updateLodging" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>6</v-chip>
          {{ t('Confirmation') }}
        </v-card-title>
        <v-card-text v-show="step == 6">
          <Lodging-Confirmation ref="refconfirmation" @change-step="changeStep"
            @update-lodging="updateLodging" />
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