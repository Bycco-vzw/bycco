<template>
  <div>
    <v-form v-model="formMeals">
      <h2>{{ $t("Meals") }}</h2>
      <div class="mt-2 mb-2">
        {{ $t(t.intro) }}
        <v-radio-group :value="meals" required :rules="rules_meals" @change="updateMeals($event)">
          <v-radio :label="$t(t.no)" value="no" />
          <v-radio :label="$t(t.half)" value="half" />
          <!-- <v-radio :label="$t(t.full)" value="full" /> -->
        </v-radio-group>
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
        <v-btn color="primary" :disabled="!formMeals" @click="next">
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

const step = 5

export default {
  name: 'LodgingMeals',
  data () {
    return {
      formMeals: false,
      rules_meals: [
        v => !!v || this.$t('meals must be selected')
      ],
      t: {
        intro: 'Select which meals you want',
        deviation: 'Normally the first meal is dinner at arrival day and the last meal is breakfast at departure day. Specify any special food wishes (vegetarian, gluten free, ...) or deviations from the normal meal scheme in the remarks field.',
        full: 'Full boarding',
        half: 'Half boarding',
        no: 'No meals'
      }
    }
  },
  computed: {
    ...mapState({
      meals: state => state.lodging.meals,
      remarks: state => state.lodging.remarks
    })
  },
  methods: {
    next () {
      this.$store.commit('lodging/updateStep', step + 1)
    },
    prev () {
      this.$store.commit('lodging/updateStep', step - 1)
    },
    updateMeals (e) {
      console.log('Setting meals', e)
      this.$store.commit('lodging/updateMeals', e)
    },
    updateRemarks (e) {
      this.$store.commit('lodging/updateRemarks', e)
    }
  }
}
</script>
