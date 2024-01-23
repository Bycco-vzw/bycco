<template>
  <div>
    <h2>{{ $t('ID number') }}</h2>
    <div>{{ $t('SubId1') }}</div>
    <v-text-field v-model="idnumber" :label="$t('ID number')" required />
    <v-btn color="primary" @click="lookup()">
      {{ $t('Lookup ID number') }}
    </v-btn>
    <v-alert v-show="errorcode" type="error" class="mt-2">
      <div v-show="errorcode == 'notfound'">
        <div>{{ $t('SubId2') }}</div>
        <div>{{ $t('SubId3') }}</div>
      </div>
      <div v-show="errorcode == 'playeradult'">
        {{ $t('SubId4') }}
      </div>
      <div v-show="errorcode == 'alreadyregistered'">
        {{ $t('SubId5') }}
      </div>
      <div v-show="errorcode == 'unknown'">
        {{ $t('UnknownError') }}
      </div>
    </v-alert>
    <div class="mt-4">
      <div v-show="s.isPlayerFound">
        {{ $t('Player found:') }} {{ s.first_name }} {{ s.last_name }}
      </div>
      <div class="mt-2">
        <v-btn v-show="s.isPlayerFound" color="primary" @click="next">
          {{ $t('Continue') }}
        </v-btn>
        <v-btn v-show="s.isPlayerFound" class="ml-2" @click="restart">
          {{ $t('Other player') }}
        </v-btn>
        <v-btn class="ml-2" @click="prev">
          {{ $t('Back') }}
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>

import { categories } from '@/util/const'
import { mapState } from 'vuex'

export default {

  data () {
    return {
      errorcode: false,
      found: false,
      maxyear: categories[0].year,
      idnumber: ''
    }
  },

  computed: {
    ...mapState({
      s: state => state.enrollment.enrollment
    })
  },

  mounted () {
    this.$root.$on('reset', () => {
      this.idnumber = ''
    })
  },

  methods: {

    lookup () {
      const self = this
      this.errorcode = false
      const s = { ...this.enrollment }
      this.$api.enrollment.find_belplayer({
        idbel: this.idnumber
      }).then(
        function (reply) {
          const data = reply.data
          if (!data.belfound) {
            self.errorcode = 'notfound'
          }
          if (!data.age_ok) {
            self.errorcode = 'playeradult'
          }
          if (data.confirmed) {
            self.errorcode = 'alreadyregistered'
          }
          if (!self.errorcode) {
            s.birthyear = data.birthyear
            s.first_name = data.first_name
            s.gender = data.gender
            s.idbel = data.idbel
            s.idclub = data.idclub
            s.idfide = data.idfide
            s.isPlayerFound = true
            s.last_name = data.last_name
            s.nationalitybel = data.nationalitybel
            s.nationalityfide = data.nationalityfide
            s.natstatus = data.natstatus
            s.ratingbel = data.ratingbel
            s.ratingfide = data.ratingfide
            self.$store.commit('enrollment/updateEnrollment', s)
          }
        },
        function (data) {
          self.errorcode = 'unknown'
        }
      )
    },

    next () {
      this.$store.commit('enrollment/updateStep', 3)
    },

    prev () {
      this.$store.commit('enrollment/updateStep', 1)
    },

    restart () {
      this.$store.commit('enrollment/restart')
      this.errorcode = false
      this.idnumber = ''
    }

  }
}
</script>

<style scoped>

</style>
