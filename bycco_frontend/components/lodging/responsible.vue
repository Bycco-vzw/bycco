<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { v_required, v_length2 } from '@/composables/validators'

// i18n
const { t } = useI18n()

// communication with manager
const emit = defineEmits(['changeStep', 'updateLodging'])
defineExpose({ setup })


// data model
const first_name = ref("")
const last_name = ref("")
const email = ref("")
const mobile = ref("")
const address = ref("")


function next() {
  console.log('clicked next')
  updateLodging()
  // emit('changeStep', 3)
}

function prev() {
  console.log('clicked prev')
  updateLodging()
  emit('changeStep', 1)
}

function updateLodging() {
  emit('updateLoging', {
    first_name: first_name, value,
    last_name: last_name.value,
    email: email.value,
    mobile: mobile.value,
    address: address.value,
  })
}

function setup(l) {
  console.log('setup responsible', l)
  first_name.value = l.first_name + ''
  last_name.value = l.last_name + ''
  email.value = l.email + ''
  mobile.value = l.mobile + ''
  address.value = l.address + ''
}

</script>
<template>
  <div>
    <h2>{{ t('Responsible of the reservation') }}</h2>
    <div class="my-2">
      {{ t("In order to make a reservation you need to provide the following elements:") }}
    </div>
    <v-form v-model="formvalid">
      <v-row>
        <v-col cols="12" sd="6">
          <v-text-field v-model="first_name" :label="t('First name')" :rules="[v_required, v_length2]"
            @update:modelValue="updateLogding" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-text-field :value="last_name" :label="t('Last name')" required :rules="rules_last_name"
            @input="updateLastName($event)" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-text-field :value="email" :label="t('Email address')" required :rules="rules_email"
            @input="updateEmail($event)" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-text-field :value="mobile" :label="t('Mobile phone')" required :rules="rules_mobile"
            @input="updateMobile($event)" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-textarea rows=3 :value="address" :label="t('Address')" required :rules="rules_address"
            @input="updateAddress($event)" />
        </v-col>
      </v-row>
    </v-form>
    <div class="mt-2">
      <v-btn color="primary" @click="prev" class="mr-2">
        {{ t('Back') }}
      </v-btn>
      <v-btn color="primary" :disabled="!formResponsible" @click="next">
        {{ t('Continue') }}
      </v-btn>
    </div>
  </div>
</template>

<!-- <script>
import { mapState } from 'vuex'
const step = 2
export default {
  name: 'LodgingResponsible',
  data() {
    return {
      formResponsible: false,
      rules_first_name: [
        v => !!v || this.t('First name is required'),
        v => v.length > 1 || this.t('Invalid value')
      ],
      rules_last_name: [
        v => !!v || this.t('Last name is required'),
        v => v.length > 1 || this.t('Invalid value')
      ],
      rules_email: [
        v => !!v || this.t('Email is required'),
        v => v.length > 5 || this.t('Invalid value'),
        v => v.indexOf('@') > 2 || this.t('Invalid value')
      ],
      rules_mobile: [
        v => !!v || this.t('Mobile phone is required'),
        v => v.length > 5 || this.t('Invalid value')
      ],
      rules_address: [
        v => !!v || this.t('Address is required'),
        v => v.length > 10 || this.t('Invalid value')
      ],
      t: {
        intro: 'Please provide the coordinates of the responsible of the accomdation. This must be an adult, present in the Foreal during the tournament. This adult may be staying in another room.'
      }
    }
  },
  computed: {
    ...mapState({
      address: state => state.lodging.address,
      email: state => state.lodging.email,
      first_name: state => state.lodging.first_name,
      last_name: state => state.lodging.last_name,
      mobile: state => state.lodging.mobile
    })
  },
  methods: {
    updateAddress(e) {
      this.$store.commit('lodging/updateAddress', e)
    },
    updateEmail(e) {
      this.$store.commit('lodging/updateEmail', e)
    },
    updateFirstName(e) {
      this.$store.commit('lodging/updateFirstName', e)
    },
    updateLastName(e) {
      this.$store.commit('lodging/updateLastName', e)
    },
    updateMobile(e) {
      this.$store.commit('lodging/updateMobile', e)
    },
    next() {
      this.$store.commit('lodging/updateStep', step + 1)
    }
  }
}
</script> -->
