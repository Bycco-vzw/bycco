<script setup>
import { ref } from "vue"
import { useI18n } from "vue-i18n"

// i18n
const { t, locale } = useI18n()
const ts = {
  overview: "Overview of the stay reservation",
  confirmation:
    "Your request for a reservation is confirmed. We will inform you by e-mail about the next steps in the reservation process.",
  newreservation: "If you want to make a new reservation, click the button below",
  noconfirmation:
    "Something went wrong during the registration of your reservation.  Check your internet connection. You could try again and/or contact bycco at info@bycco.be .",
}

// communication
const emit = defineEmits(["changeStep", "updateStay"])
defineExpose({ setup })
const { $backend } = useNuxtApp()

// datamodel
const stay = ref({})
const common = ref(null)
const confirmed = ref(false)
const noerror = ref(true)

function prev() {
  updateStay()
  emit("changeStep", 5)
}

async function postConfirmation() {
  try {
    const reply = await $backend("stay", "make_reservation", {
      stayIn: {
        first_name: stay.value.first_name,
        last_name: stay.value.last_name,
        email: stay.value.email,
        mobile: stay.value.mobile,
        address: stay.value.address,
        guestlist: stay.value.guestlist,
        stay: stay.value.accomodation,
        locale: locale.value,
        checkindate: stay.value.checkindate,
        checkoutdate: stay.value.checkoutdate,
        meals: stay.value.meals,
        remarks: stay.value.remarks,
      },
    })
    confirmed.value = true
  } catch (error) {
    console.error("Failed", error)
    noerror.value = false
  }
}

function restart() {
  confirmed.value = false
  noerror.value = true
  emit("updateStay", { guestlist: [] })
  emit("changeStep", 1)
}

function setup(stay_, common_) {
  console.log("setup confirmation", stay_, common_)
  common.value = common_
  stay.value = { ...stay_ }
}

function updateStay() {
  emit("updateStay", stay.value)
}
</script>
?

<template>
  <div>
    <div class="mt-2 mb-2">
      {{ $t(ts.overview) }}
    </div>
    <h4 class="mt-2">Contact details:</h4>
    <div>
      {{ stay.first_name }} {{ stay.last_name }}<br />
      E-mail: {{ stay.email }}<br />
      Tel: {{ stay.mobile }}<br />
      {{ stay.address }}
    </div>
    <h4 class="mt-2">
      {{ $t("Guests") }}
    </h4>
    <div v-for="(g, ix) in stay.guestlist" :key="ix">
      <span v-if="g.last_name.length">
        {{ ix + 1 }}. {{ g.last_name }} {{ g.first_name }} {{ g.birthdate }}
        {{ g.player ? "player" : "" }}
      </span>
    </div>
    <div>
      {{ $t("Accomodation") }}: {{ stay.acc_description }}:
      {{ Intl.DateTimeFormat(locale.value).format(stay.checkindate) }}
      {{ Intl.DateTimeFormat(locale.value).format(stay.checkoutdate) }}
    </div>
    <div>
      {{ $t("Meals") }}:
      <span v-show="stay.meals == 'no'">{{ $t("No meals") }}</span>
      <span v-show="stay.meals == 'half'">{{ $t("Half boarding") }}</span>
      <!-- <span v-show="meals == 'full'">{{ $t('Full boarding') }}</span> -->
    </div>
    <h4 class="mt-2">
      {{ $t("Remarks") }}
    </h4>
    <div>{{ stay.remarks }}</div>
    <div v-if="!confirmed || !noerror" class="mt-2">
      <v-btn color="primary" @click="prev" class="mr-2">
        {{ $t("Back") }}
      </v-btn>
      <v-btn color="primary" @click="postConfirmation">
        {{ $t("Confirm") }}
      </v-btn>
    </div>
    <div v-if="confirmed && noerror" class="pt-3">
      <v-alert type="success" class="my-4">
        {{ $t(ts.confirmation) }}
      </v-alert>
      <div class="mt-4">
        {{ $t(ts.newreservation) }}
      </div>
      <v-btn color="primary" @click="restart">
        {{ $t("New reservation") }}
      </v-btn>
    </div>
    <div v-if="!noerror" class="pt-3">
      <v-alert type="error">
        {{ $t("Request reservation not confirmed") }}
      </v-alert>
      <div>{{ $t(ts.noconfirmation) }}</div>
    </div>
  </div>
</template>
