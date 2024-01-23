<template>
  <div>
    <h2>{{ $t('Details player') }}</h2>

    <v-layout row wrap>
      <v-flex xs12 sm6>
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
      </v-flex>
      <v-flex xs12 sm6>
        <div class="mt-2">
          <span>{{ $t('Gender') }}</span>:
          {{ enrollment.gender }}
        </div>
        <div class="mt-2">
          <span>{{ $t('FIDE Nationality') }}</span>:
          {{ enrollment.nationalityfide }}
        </div>
      </v-flex>
    </v-layout>

    <div class="mt-3">
      <h3 class="mt-3">
        {{ $t('Additional Fields') }}
      </h3>
      <div> {{ $t('Required information') }}</div>

      <v-layout row wrap>
        <v-flex xs12 sm6 md4>
          <h4>{{ $t('Info participant') }}</h4>
          <v-select v-model="category" :label="$t('Category')" :items="cats" />
          <v-text-field v-model="emailplayer" :label="$t('Email player')" />
          <v-text-field v-model="mobileplayer" :label="$t('GSM player')" />
        </v-flex>
        <v-flex xs12 sm6 md4>
          <h4>{{ $t('Info about parent') }}</h4>
          <v-text-field v-model="fullnameparent" :label="$t('Full name')" />
          <v-text-field v-model="emailparent" :label="$t('Email parent')" />
          <v-text-field v-model="mobileparent" :label="$t('GSM parent')" />
        </v-flex>
        <v-flex xs12 sm6 md4>
          <h4>{{ $t('Info about attendant on site') }}</h4>
          <v-checkbox v-model="isParentPresent" :label="$t('A parent is present at site')" />
          <div v-show="!isParentPresent">
            <v-text-field v-model="fullnameattendant" :label="$t('Full name')" />
            <v-text-field v-model="emailattendant" :label="$t('Email')" />
            <v-text-field v-model="mobileattendant" :label="$t('GSM number')" />
          </div>
        </v-flex>
      </v-layout>
    </div>

    <v-alert v-model="alert" type="error" class="mt-2" dismissible>
      <div v-show="errorcode == 'invalidfield'">
        {{ $t('SubDetail5') }}
      </div>
      <div v-show="errorcode == 'firewall'">
        {{ $t('SubDetail6') }}
      </div>
      <div v-show="errorcode == 'unknown'">
        {{ $t('UnknownError') }}
      </div>
    </v-alert>

    <div class="mt-2">
      <v-btn color="primary" @click="createEnrollment()">
        {{ $t('Continue') }}
      </v-btn>
      <v-btn v-t="'Back'" @click="prev" />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import { categories } from '@/util/const'

export default {

  data () {
    return {
      alert: false,
      errorcode: null,
      category_: null,
      emailplayer: '',
      mobileplayer: '',
      fullnameparent: '',
      emailparent: '',
      mobileparent: '',
      fullnameattendant: '',
      emailattendant: '',
      mobileattendant: '',
      isParentPresent: false
    }
  },

  computed: {
    adult () {
      return this.enrollment.birthyear < 2004
    },
    category: {
      set (val) {
        this.category_ = val
      },
      get () {
        return this.category_
      }
    },
    cats () {
      const cs = []
      categories.forEach((c) => {
        if (c.year <= this.enrollment.birthyear) { cs.push(c) }
      })
      return cs
    },
    ...mapState({
      step: state => state.enrollment.step,
      enrollment: state => state.enrollment.enrollment
    })
  },

  watch: {
    step () {
      if (this.step === 3) {
        if (!this.enrollment.category) {
          this.category = this.cats[this.cats.length - 1].value
        }
      }
    }
  },

  mounted () {
    this.$root.$on('reset', () => {
      this.emailplayer = ''
      this.mobileplayer = ''
      this.fullnameparent = ''
      this.emailparent = ''
      this.mobileparent = ''
      this.fullnameattendant = ''
      this.emailattendant = ''
      this.mobileattendant = ''
      this.isParentPresent = false
    })
  },

  methods: {

    createEnrollment () {
      this.alert = false
      this.errorcode = false
      if (this.adult) {
        this.errorcode = (
          this.emailplayer.length < 3 ||
          this.mobileplayer.length < 3
        )
          ? 'invalidfield'
          : null
      }
      if (!this.adult) {
        this.errorcode = (
          this.emailparent.length < 3 ||
          this.mobileparent.length < 3 ||
          this.fullnameparent.length < 3 ||
          (!this.isParentPresent && (
            this.emailattendant.length < 3 ||
            this.mobileattendant.length < 3 ||
            this.fullnameattendant.length < 3
          ))
        )
          ? 'invalidfield'
          : null
      }
      if (this.errorcode) {
        this.alert = true
        return
      }
      const self = this
      let subparam = {
        category: this.category,
        emailparent: this.emailparent || '',
        emailplayer: this.emailplayer || '',
        emailattendant: this.emailattendant || '',
        fullnameattendant: this.fullnameattendant || '',
        fullnameparent: this.fullnameparent || '',
        idbel: this.enrollment.idbel,
        locale: this.$i18n.locale,
        mobileattendant: this.mobileattendant || '',
        mobileparent: this.mobileparent || '',
        mobileplayer: this.mobileplayer || ''
      }
      this.$api.enrollment.create_enrollment({ enrollment: subparam }).then(
        function (data) {
          console.log('data', data)
          subparam = Object.assign(self.enrollment, subparam, { idsub: data.data })
          self.$store.commit('enrollment/updateEnrollment', subparam)
          self.$store.commit('enrollment/updateStep', 4)
        },
        function (data) {
          console.error('enrollment failed', data)
          self.errorcode = (data == 403) ? 'firewall' : 'unknown'
        }
      )
    },

    prev () {
      this.$store.commit('enrollment/updateStep', 2)
    }

  }

}

</script>

<style scoped>

</style>
