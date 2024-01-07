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
const formvalid = ref(false)


function next() {
  updateLodging()
  emit('changeStep', 3)
}

function prev() {
  updateLodging()
  emit('changeStep', 1)
}

function setup(l) {
  console.log('setup responsible', l)
  first_name.value = l.first_name || '' + ''
  last_name.value = l.last_name || '' + ''
  email.value = l.email || '' + ''
  mobile.value = l.mobile || '' + ''
  address.value = l.address || '' + ''
}

function tValidator(f) {
  // returns a new function that translates the outcome of a validator
  function tf(v) {
    let s = f(v)
    if (typeof (s) === "string" || s instanceof String) {
      return t(s)
    }
    else {
      return s
    }
  }
  return tf
}

function updateLodging() {
  emit('updateLodging', {
    first_name: first_name.value,
    last_name: last_name.value,
    email: email.value,
    mobile: mobile.value,
    address: address.value,
  })
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
          <v-text-field v-model="first_name" :label="t('First name')"
            :rules="[tValidator(v_required), tValidator(v_length2)]" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-text-field v-model="last_name" :label="t('Last name')" :rules="[v_required]" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-text-field v-model="email" :label="t('Email address')" :rules="[v_required]" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-text-field v-model="mobile" :label="t('Mobile phone')" :rules="[v_required]" />
        </v-col>
        <v-col cols="12" sd="6">
          <v-textarea rows=3 v-model="address" :label="t('Address')" :rules="[v_required]" />
        </v-col>
      </v-row>
    </v-form>
    <div class="mt-2">
      <v-btn color="primary" @click="prev" class="mr-2">
        {{ t('Back') }}
      </v-btn>
      <v-btn color="primary" :disabled="!formvalid" @click="next">
        {{ t('Continue') }}
      </v-btn>
    </div>
  </div>
</template>

