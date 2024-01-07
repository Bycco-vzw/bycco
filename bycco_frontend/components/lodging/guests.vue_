<template>
  <div>
    <h2>{{ $t("Guests") }}</h2>
    <div class="mt-2 mb-3">
      {{ $t(t.intro) }}
    </div>
    <div class="mt-2 pb-3">
      <b>
        {{ $t(t.requester) }}
      </b>
    </div>
    <v-form v-model="formGuests" class="pt-2">
      <v-row v-for="(g, ix) in guestlist" :key="ix">
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            dense
            :value="g.first_name"
            :label="$t('First name')"
            :rules="validateRules('first_name', ix)"
            @input="updateGuestsField($event, ix, 'first_name')"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            dense
            :value="g.last_name"
            :label="$t('Last name')"
            :rules="validateRules('last_name', ix)"
            @input="updateGuestsField($event, ix, 'last_name')"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-menu
            ref="menu"
            v-model="menu_birth[ix]"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template #activator="{ on }">
              <v-text-field
                dense
                :value="g.birthday"
                readonly
                :label="$t('Birth date')"
                prepend-icon="mdi-calendar-range"
                :rules="validateRules('birthday', ix)"
                v-on="on"
              />
            </template>
            <v-date-picker
              :value="g.birthday"
              @input="updateGuestsField($event, ix, 'birthday')"
            />
          </v-menu>
        </v-col>
        <v-col cols="4" sm="2" md="1">
          <v-btn fab small @click="deleteGuest(ix)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <div v-show="guestlist.length > 1">
        <h3 class="mt-3">
          {{ $t('Participants') }}
        </h3>
        <div>
          {{ $t(t.participants) }}
        </div>
        <div v-for="(g, ix) in guestlist" :key="'a'+ix">
          <v-checkbox
            v-show="g.last_name.length"
            dense
            hide-details
            :value="g.player"
            :label="`${ g.first_name } ${ g.last_name } `"
            @change="updateGuestsField($event, ix, 'player')"
          />
        </div>
      </div>
      <div>
        <div class="mt-3 mb-3">
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
          <v-btn color="primary" :disabled="!formGuests" @click="next">
            {{ $t("Continue") }}
          </v-btn>
          <v-btn color="primary" @click="prev">
            {{ $t("Back") }}
          </v-btn>
        </div>
        </v-row>
      </div>
    </v-form>
  </div>
</template>

<script>
import { mapState } from 'vuex'

const step = 3

export default {
  name: 'LodgingGuests',
  data () {
    return {
      formGuests: false,
      t: {
        intro: 'Provide for any guest, the name, first name, birthday. Indicate if a guest intends to particpatte to the tournament.',
        requester: "Don't forget to mention the details of requester, in case he/she stays in this lodging.",
        deviation: 'As a default all guests stay the full period in the accomodation.  If this it not the case, please provide the any deviation form the default in the remarks field below.',
        participants: 'Indicate which guests will participate in the tournament'
      },
      menu_birth: [],
      renderGuests: true
    }
  },
  computed: {
    ...mapState({
      guestlist: state => state.lodging.guestlist,
      remarks: state => state.lodging.remarks
    })
  },
  methods: {
    deleteGuest (ix) {
      this.$store.commit('lodging/deleteGuest', ix)
    },
    next () {
      this.$store.commit('lodging/updateStep', step + 1)
    },
    prev () {
      this.$store.commit('lodging/updateStep', step - 1)
    },
    updateGuestsField (value, ix, field) {
      if (field === 'birthday') {
        this.menu_birth[ix] = false
      }
      this.$store.commit('lodging/updateGuestsField', {
        value,
        ix,
        field
      })
    },
    updateRemarks (value) {
      this.$store.commit('lodging/updateRemarks', value)
    },
    validateRules (field, ix) {
      const debug = this.guestlist.length === 3
      if (debug) { console.log('field', field, ix) }
      if (ix === this.guestlist.length - 1) {
        if (debug) { console.log('return true function') }
        return [() => true]
      }
      const g = this.guestlist[ix]
      if (debug) { console.log('field', g[field], ix) }
      return [
        () => !!g[field] || this.$t(`${field} is required`),
        () => g[field].length > 1 || this.$t('Invalid value')
      ]
    }

  }
}
</script>

<style scoped>
.v-input--selection-controls.top8 {
  margin-top: 8px;
}
</style>
