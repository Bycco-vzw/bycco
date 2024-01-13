<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

// i18n
const { t } = useI18n()
const ts = {
  overview: 'Overview of the lodging reservation',
  confirmation: 'Your request for a reservation is confirmed. We will inform you by e-mail about the next steps in the reservation process.',
  newreservation: 'If you want to make a new reservation, click the button below',
  noconfirmation: 'Something went wrong during the registration of your reservation.  Check your internet connection. You could try again and/or contact bycco at info@bycco.be .'
}

// communication with manager
const emit = defineEmits(['changeStep', 'updateLodging'])
defineExpose({ setup })

// datamodel
const lodging = ref({})
const confirmed = ref(false)
const noerror = ref(false)


function prev() {
  updateLodging()
  emit('changeStep', 5)
}

function setup(l) {
  console.log('setup meals', l)
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
    <div>{{ $t('Accomodation') }}: {{ lodging.accomodatione }}:
      {{ startdate }} {{ enddate }}</div>
    <div>
      {{ $t('Meals') }}:
      <span v-show="meals == 'no'">{{ $t('No meals') }}</span>
      <span v-show="meals == 'half'">{{ $t('Half boarding') }}</span>
      <!-- <span v-show="meals == 'full'">{{ $t('Full boarding') }}</span> -->
    </div>
    <h4 class="mt-2">
      {{ $t('Remarks') }}
    </h4>
    <div>{{ remarks }}</div>
    <div v-if="!confirmed || !noerror" class="mt-2">
      <v-btn color="primary" @click="confirm">
        {{ $t("Confirm") }}
      </v-btn>
      <v-btn color="primary" @click="prev">
        {{ $t("Back") }}
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

<!-- <script>
import { mapState } from 'vuex'

const step = 6

export default {
  name: 'LodgingConfirmation',

  data() {
    return {
      confirmed: false,
      noerror: true,
      period: {},
      t: {
        overview: 'Overview of the lodging reservation',
        confirmation: 'Your request for a reservation is confirmed. We will inform you by e-mail about the next steps in the reservation process.',
        newreservation: 'If you want to make a new reservation, click the button below',
        noconfirmation: 'Something went wrong during the registration of your reservation.  Check your internet connection. You could try again and/or contact bycco at info@bycco.be .'
      }
    }
  },

  computed: {
    ...mapState({
      address: state => state.lodging.address,
      daybefore: state => state.lodging.daybefore,
      dayafter: state => state.lodging.dayafter,
      email: state => state.lodging.email,
      first_name: state => state.lodging.first_name,
      guestlist: state => state.lodging.guestlist,
      last_name: state => state.lodging.last_name,
      lodging: state => state.lodging.lodging,
      meals: state => state.lodging.meals,
      mobile: state => state.lodging.mobile,
      remarks: state => state.lodging.remarks
    }),
    sdatevalue() {
      const d = new Date(this.period.startdate)
      return d.valueOf() - (this.daybefore ? 86400000 : 0)
    },
    edatevalue() {
      const d = new Date(this.period.enddate)
      return d.valueOf() + (this.dayafter ? 86400000 : 0)
    },
    startdate() {
      return (new Date(this.sdatevalue)).toLocaleDateString(
        this.$i18n.locale, { dateStyle: 'medium' })
    },
    enddate() {
      return (new Date(this.edatevalue)).toLocaleDateString(
        this.$i18n.locale, { dateStyle: 'medium' })
    }
  },

  methods: {
    confirm() {
      console.log('confirm locale:', this.$i18n.locale)
      this.$api.reservation
        .add_reservation({
          reservationin: {
            address: this.address,
            checkindate: (new Date(this.sdatevalue)).toISOString().slice(0, 10),
            checkoutdate: (new Date(this.edatevalue)).toISOString().slice(0, 10),
            email: this.email,
            first_name: this.first_name,
            guestlist: this.guestlist.slice(0, -1),
            last_name: this.last_name,
            locale: this.$i18n.locale,
            lodging: this.lodging,
            mobile: this.mobile,
            meals: this.meals,
            remarks: this.remarks
          }
        })
        .then(() => {
          this.confirmed = true
          this.noerror = true
        }, (data) => {
          this.noerror = false
          console.error(data)
        })
    },
    prev() {
      this.$store.commit('lodging/updateStep', step - 1)
    },
    restart() {
      this.confirmed = false
      this.$store.commit('lodging/restart')
    }
  }
}
</script> -->
