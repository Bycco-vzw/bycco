<script setup>
import { ref, computed } from "vue"
import { useI18n } from "vue-i18n"

// communication with stepped children
const { $backend } = useNuxtApp()
const step = ref(1)
const refintro = ref(null)
const refresponsible = ref(null)
const refguests = ref(null)
const refaccomodation = ref(null)
const refmeals = ref(null)
const refconfirmation = ref(null)

// data model
const stay = ref({ guestlist: [] })
const common = ref(null)
const status = ref("closed")
const { t } = useI18n()

function calcStatus() {
  let now = new Date()
  let opendate = new Date(common.value.trndates.stayopen)
  let closedate = new Date(common.value.trndates.stayclose)
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
      refintro.value.setup(stay.value)
      break
    case 2:
      refresponsible.value.setup(stay.value)
      break
    case 3:
      refaccomodation.value.setup(stay.value, common.value)
      break
    case 4:
      refguests.value.setup(stay.value, common.value)
      break
    case 5:
      refmeals.value.setup(stay.value, common.value)
      break
    case 6:
      refconfirmation.value.setup(stay.value, common.value)
      break
  }
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

function updateStay(l) {
  console.log("tool stay updated", l)
  Object.assign(stay.value, l)
}

onMounted(async () => {
  await readCommon()
  calcStatus()
})
</script>

<template>
  <v-container>
    <h1 class="my-2">
      {{ t("stay.res_tool") }}
    </h1>
    <div class="my-2" v-if="status == 'closed'">
      {{ t("stay.res_closed") }}
    </div>
    <div class="my-2" v-if="status == 'notyetopen'">
      {{ t("stay.res_notstarted") }}
    </div>
    <div class="my-2" v-if="status == 'open'">
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>1</v-chip>
          Intro
        </v-card-title>
        <v-card-text v-show="step == 1">
          <Stay-Intro ref="refintro" @change-step="changeStep" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>2</v-chip>
          {{ t("Responsible of the reservation") }}
        </v-card-title>
        <v-card-text v-show="step == 2">
          <Stay-Responsible
            ref="refresponsible"
            @change-step="changeStep"
            @update-stay="updateStay"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>3</v-chip>
          {{ t("Accomodation") }}
        </v-card-title>
        <v-card-text v-show="step == 3">
          <Stay-Accomodation
            ref="refaccomodation"
            @change-step="changeStep"
            @update-stay="updateStay"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>4</v-chip>
          {{ t("Guest list") }}
        </v-card-title>
        <v-card-text v-show="step == 4">
          <Stay-Guests
            ref="refguests"
            @change-step="changeStep"
            @update-stay="updateStay"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>5</v-chip>
          {{ t("Meals") }}
        </v-card-title>
        <v-card-text v-show="step == 5">
          <Stay-Meals
            ref="refmeals"
            @change-step="changeStep"
            @update-stay="updateStay"
          />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>6</v-chip>
          {{ t("Confirmation") }}
        </v-card-title>
        <v-card-text v-show="step == 6">
          <Stay-Confirmation
            ref="refconfirmation"
            @change-step="changeStep"
            @update-stay="updateStay"
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
