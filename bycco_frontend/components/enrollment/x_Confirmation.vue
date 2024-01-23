<template>
  <div>
    <h2>{{ $t('Confirmation details') }}</h2>
    <v-layout row>
      <v-flex xs12 sm6 lg4 class="confirmationphoto">
        <img :src="photo">
      </v-flex>
      <v-flex xs12 sm6 lg4>
        <div class="mt-2">
          <span>{{ $t('Full name') }}</span>:
          {{ enrollment.first_name }} {{ enrollment.last_name }}
        </div>
        <div class="mt-2">
          <span>{{ $t('Birthyear') }}</span>:
          {{ enrollment.birthyear }}
        </div>
        <div class="mt-2">
          <span>{{ $t('ID Club') }}</span>:
          {{ enrollment.idclub }}
        </div>
        <div class="mt-2">
          <span>{{ $t('Nationality') }}</span>:
          {{ enrollment.nationalitybel }}
        </div>
        <div class="mt-2">
          <span>{{ $t('FIDE Nationality') }}</span>:
          {{ enrollment.nationalityfide }}
        </div>
        <div class="mt-2">
          <span>{{ $t('Can become Belgian champion') }}</span>:
          <span v-if="enrollment.natstatus == 'Fide Belg.'">{{ $t('Yes') }}</span>
          <span v-if="enrollment.natstatus == 'No Belg.'">{{ $t('No') }}</span>
          <span v-if="enrollment.natstatus == 'Unknown'">{{ $t('To be confirmed') }}</span>
        </div>
      </v-flex>
      <v-flex xs12 sm6 lg4>
        <div class="mt-2">
          <span>{{ $t('Gender') }}</span>:
          {{ enrollment.gender }}
        </div>
        <div class="mt-2">
          <span>{{ $t('Category') }}</span>:
          -{{ enrollment.category }}
        </div>
      </v-flex>
    </v-layout>
    <div v-show="!enrollment.confirmed" class="mt-2">
      <div>
        <v-btn color="primary" @click="confirm">
          {{ $t('Confirm') }}
        </v-btn>
      </div>
    </div>
    <div v-show="enrollment.confirmed" class="mt-2">
      <h3>{{ $t('Payment') }}</h3>
      <div>{{ $t('Your enrollment is confirmed') }}</div>
      <v-btn class="mt-2" @click="restart()">
        {{ $t('New registration') }}
      </v-btn>
    </div>
  </div>
</template>

<script>

import { mapState } from 'vuex'

export default {

  data() {
    return {
      errorcode: false,
      paymessage: ''
    }
  },

  computed: {
    ...mapState({
      step: state => state.enrollment.step,
      enrollment: state => state.enrollment.enrollment,
      photo: state => state.enrollment.photo
    })
  },

  methods: {
    confirm() {
      const self = this
      this.$api.enrollment.confirm_enrollment({
        idsub: this.enrollment.idsub
      }).then(
        function (data) {
          self.$store.commit('enrollment/updateEnrollment', { ...self.enrollment, confirmed: true })
        },
        function (data) {
          console.error('Error confirming', data)
        }
      )
    },
    restart() {
      this.$root.$emit('reset')
      this.$store.commit('enrollment/restart')
    }
  }
}
</script>

<style scoped>

</style>
