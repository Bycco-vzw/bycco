<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

// i18n
const { t, locale } = useI18n()
const ts = {
  overview: 'Overview of the lodging reservation',
  confirmation: 'Your request for a reservation is confirmed. We will inform you by e-mail about the next steps in the reservation process.',
  newreservation: 'If you want to make a new reservation, click the button below',
  noconfirmation: 'Something went wrong during the registration of your reservation.  Check your internet connection. You could try again and/or contact bycco at info@bycco.be .'
}

// communication
const emit = defineEmits(['changeStep', 'updateLodging'])
defineExpose({ setup })
const { $backend } = useNuxtApp()

// datamodel
const lodging = ref({})
const confirmed = ref(false)
const noerror = ref(true)


function prev() {
  updateLodging()
  emit('changeStep', 5)
}

async function postConfirmation() {
  try {
    const reply = await $backend('lodging', 'make_reservation', {
      lodgingIn: {
        first_name: lodging.value.first_name,
        last_name: lodging.value.last_name,
        email: lodging.value.email,
        mobile: lodging.value.mobile,
        address: lodging.value.address,
        guestlist: lodging.value.guestlist,
        lodging: lodging.value.accomodation,
        locale: locale.value,
        checkindate: lodging.value.checkindate,
        checkoutdate: lodging.value.checkoutdate,
        meals: lodging.value.meals,
        remarks: lodging.value.remarks,
      }
    })
  }
  catch (error) {
    console.error('Failed', error)
  }
}

function setup(l) {
  console.log('setup confirmation', l)
  lodging.value = { ...l }
}

function updateLodging() {
  emit('updateLodging', lodging.value)
}

</script>?

<template>
  <div>
    <div class="mt-2 mb-2">
      {{ $t(ts.overview) }}
    </div>
    <h4 class="mt-2">
      Contact details:
    </h4>
    <div>
      {{ lodging.first_name }} {{ lodging.last_name }}<br>
      E-mail: {{ lodging.email }}<br>
      Tel: {{ lodging.mobile }}<br>
      {{ lodging.address }}
    </div>
    <h4 class="mt-2">
      {{ $t('Guests') }}
    </h4>
    <div v-for="(g, ix) in lodging.guestlist" :key="ix">
      <span v-if="g.last_name.length">
        {{ ix + 1 }}. {{ g.last_name }} {{ g.first_name }} {{ g.birthdate }}
        {{ g.player ? "player" : "" }}
      </span>
    </div>
    <div>{{ $t('Accomodation') }}: {{ lodging.acc_description }}:
      {{ Intl.DateTimeFormat(locale.value).format(lodging.checkindate) }}
      {{ Intl.DateTimeFormat(locale.value).format(lodging.checkoutdate) }}
    </div>
    <div>
      {{ $t('Meals') }}:
      <span v-show="lodging.meals == 'no'">{{ $t('No meals') }}</span>
      <span v-show="lodging.meals == 'half'">{{ $t('Half boarding') }}</span>
      <!-- <span v-show="meals == 'full'">{{ $t('Full boarding') }}</span> -->
    </div>
    <h4 class="mt-2">
      {{ $t('Remarks') }}
    </h4>
    <div>{{ lodging.remarks }}</div>
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

