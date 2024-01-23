<script setup>
import { useI18n } from 'vue-i18n'

// communication
const emit = defineEmits(['changeStep', 'updateEnrollment'])
defineExpose({ setup })
const { $backend } = useNuxtApp()

// i18n
const { t } = useI18n()

// datamodel member
const age_ok = ref(true)
const birthyear = ref(null)
const first_name = ref("")
const gender = ref(null)
const idbel = ref("")
const idclub = ref("")
const idfide = ref("")
const last_name = ref("")
const nationalitybel = ref("")
const nationalityfide = ref("")
const natstatus = ref("Unknown")
const ratingbel = ref(0)
const ratingfide = ref(0)

// datamodel the rest
const isPlayerFound = ref(false)
const errorcode = ref(null)
const step = 2


async function lookup_bel() {
  let member
  try {
    const reply = await $backend('enrollment', 'lookup_idbel', {
      idbel: idbel.value
    })
    console.log("member", reply.data)
    member = reply.data
  }
  catch (error) {
    console.error('lookup_bel failed', error)
    return
  }
  isPlayerFound.value = member.belfound
  age_ok.value = member.age_ok
  birthyear.value = member.birthyear
  first_name.value = member.first_name
  gender.value = member.gender
  idclub.value = member.idclub
  idfide.value = member.idfide + ''
  last_name.value = member.last_name
  nationalitybel.value = member.nationalitybel
  nationalityfide.value = member.nationalityfide
  natstatus.value = member.natstatus
  ratingbel.value = member.ratingbel
  ratingfide.value = member.ratingfide
  if (!isPlayerFound.value) {
    errorcode.value = "notfound"
  }
}

async function lookup_fide() {
  let member
  try {
    const reply = await $backend('enrollment', 'lookup_idfide', {
      idfide: idfide.value
    })
    console.log("member", reply.data)
    member = reply.data
  }
  catch (error) {
    console.error('lookup_fide failed', error)
    return
  }
  isPlayerFound.value = member.belfound
  age_ok.value = member.age_ok
  birthyear.value = member.birthyear
  first_name.value = member.first_name
  gender.value = member.gender
  idclub.value = member.idclub
  idbel.value = member.idfide + ''
  last_name.value = member.last_name
  nationalitybel.value = member.nationalitybel
  nationalityfide.value = member.nationalityfide
  natstatus.value = member.natstatus
  ratingbel.value = member.ratingbel
  ratingfide.value = member.ratingfide
  if (!isPlayerFound.value) {
    errorcode.value = "notfound"
  }
}


function next() {
  updateEnrollment()
  emit('changeStep', step + 1)
}

function prev() {
  updateEnrollment()
  emit('changeStep', step - 1)
}

function restart() {
  isPlayerFound.value = false
  errorcode.value = null
  idbel.value = ""
  idfide.value = ""
}

function setup(e) {
  console.log('setup idnumber', e)
  idbel.value = e.idbel
  idfide.value = e.idfide
  first_name.value = e.first_name + ''
  last_name.value = e.last_name + ''
  ratingbel.value = e.ratingbel + 0
  ratingfide.value = e.ratingfide + 0

}

function updateEnrollment() {
  emit('updateEnrollment', {
    first_name: first_name.value,
    last_name: last_name.value,
    idbel: idbel.value,
    idfide: idfide.value,
    ratingbel: ratingbel.value,
    ratingfide: ratingfide.value,
  })
}
</script>
<template>
  <div>

    <v-container>
      <v-row class="my-2">
        <h2>{{ $t('enrollvk.idn_title') }}</h2>
      </v-row>
      <v-row class="mt-2">
        <div>{{ $t('enrollvk.idn_beldescription') }}</div>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="idbel" :label="$t('enrollvk.idn_idbel')" required />
        </v-col>
        <v-col cols="12" md="6">
          <v-btn color="primary" @click="lookup_bel()">
            {{ $t('Lookup') }}
          </v-btn>
        </v-col>
      </v-row>
      <v-row class="mt-2">
        <div>{{ $t('enrollvk.idn_fidedescription') }}</div>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="idfide" :label="$t('enrollvk.idn_idfide')" required />
        </v-col>
        <v-col cols="12" md="6">
          <v-btn color="primary" @click="lookup_fide()">
            {{ $t('Lookup') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>


    <v-alert v-show="errorcode" type="error" class="mt-2" closable>
      <div v-show="errorcode == 'notfound'">
        <div>{{ $t('enrollvk.idn_notfound') }}</div>
      </div>
      <div v-show="errorcode == 'alreadyregistered'">
        {{ $t('enrollvk.idn_alreadyregistered') }}
      </div>
      <div v-show="errorcode == 'unknown'">
        {{ $t('UnknownError') }}
      </div>
    </v-alert>
    <div class="mt-4">
      <div v-show="isPlayerFound">
        {{ $t('enrollvk.idn_playerfound') }} {{ first_name }} {{ last_name }}
      </div>
      <div class="mt-2">
        <v-btn class="ml-2" @click="prev" color="primary">
          {{ $t('Back') }}
        </v-btn>
        <v-btn v-show="isPlayerFound" class="ml-2" color="primary" @click="next">
          {{ $t('Continue') }}
        </v-btn>
        <v-btn v-show="isPlayerFound" class="ml-2" @click="restart">
          {{ $t('Other player') }}
        </v-btn>
      </div>
    </div>
  </div>
</template>