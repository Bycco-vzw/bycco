<template>
  <div>
    <h2>{{ $t("Accomodation") }}</h2>
    <v-form v-model="formAccomodation">
      <div class="mt-2 mb-2">
        {{ $t(t.intro) }}
        <v-radio-group :value="lodging" required :rules="[lodging_validator]" @change="updateLodging">
          <v-radio
            v-for="rt in roomtypes"
            :key="rt"
            :label="i18n[rt][$i18n.locale]"
            :value="rt"
          />
        </v-radio-group>
      </div>
      <div class="mt-2 mb-2">
        {{ $t(t.extra) }}
        <v-checkbox
          dense
          hide-details
          :value="daybefore"
          :label="$t('Arrival date') + ': ' + prevday"
          @change="updateDaybefore"
        />
        <v-checkbox
          dense
          hide-details
          :value="dayafter"
          :label="$t('Departure date') + ': ' + nextday"
          @change="updateDayafter"
        />
      </div>
      <div class="mt-2 mb-3">
        {{ $t(t.deviation) }}
        <br>
        <v-textarea
          :value="remarks"
          :label="$t('Remarks')"
          auto-grow
          @input="updateRemarks($event)"
        />
      </div>
      <div class="mt-2">
        <v-btn color="primary" :disabled="!formAccomodation" @click="next">
          {{ $t("Continue") }}
        </v-btn>
        <v-btn color="primary" @click="prev">
          {{ $t("Back") }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>

import { mapState } from 'vuex'

const step = 4

export default {
  name: 'LodgingAccomodation',

  data () {
    return {
      formAccomodation: false,
      roomtypes: {},
      period: {},
      i18n: {},
      t: {
        intro: 'Select which accomodation you want',
        extra: 'Normally the reservation is for 6 nights, from 19-Feb until 25-Feb.  You can optionally add 1 night before and/or after.',
        deviation: 'Specify any special requirements in the remarks field.'
      }
    }
  },

  async fetch () {
    const common = await this.$content('common').fetch()
    this.roomtypes = common.roomtypes
    this.period = common.period
    this.i18n = common.i18n
  },

  computed: {
    ...mapState({
      lodging: state => state.lodging.lodging,
      dayafter: state => state.lodging.dayafter,
      daybefore: state => state.lodging.daybefore,
      remarks: state => state.lodging.remarks
    }),
    prevday () {
      const s = new Date(this.period.startdate)
      return (new Date(s.valueOf() - 86400000)).toLocaleDateString(this.$i18n.locale, { dateStyle: 'medium' })
    },
    nextday () {
      const e = new Date(this.period.enddate)
      return (new Date(e.valueOf() + 86400000)).toLocaleDateString(this.$i18n.locale, { dateStyle: 'medium' })
    }
  },

  mounted () {
    console.log('roomtypes', this.roomtypes)
  },

  methods: {
    lodging_validator (v) {
      return !!v || this.$t('Lodging must be chosen')
    },
    next () {
      this.$store.commit('lodging/updateStep', step + 1)
    },
    prev () {
      this.$store.commit('lodging/updateStep', step - 1)
    },
    updateLodging (e) {
      this.$store.commit('lodging/updateLodging', e)
    },
    updateDaybefore () {
      this.$store.commit('lodging/updateDaybefore')
    },
    updateDayafter () {
      this.$store.commit('lodging/updateDayafter')
    },
    updateRemarks (e) {
      this.$store.commit('lodging/updateRemarks', e)
    }
  }
}
</script>
