<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { v_required, v_length2 } from '@/composables/validators'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'

// communication
const emit = defineEmits(['changeStep', 'updateEnrollment'])
defineExpose({ setup })
const { $backend } = useNuxtApp()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// i18n
const { t, locale } = useI18n()

// datamodel member
const birthyear = ref(0)
const category = ref("VK")
const emailplayer = ref("")
const first_name = ref("")
const idbel = ref("")
const idfide = ref("")
const idsub = ref("")
const last_name = ref("")
const mobileplayer = ref("")
const nationalityfide = ref("")

// datamodel the rest
const step = 3
const formvalid = ref(false)

async function next() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("enrollment", "create_enrollment_vk", {
      enrollmentVkIn: {
        category: category.value,
        emailplayer: emailplayer.value,
        idbel: idbel.value,
        idfide: idfide.value,
        idsub: idsub.value,
        locale: locale.value,
        mobileplayer: mobileplayer.value,
      }
    })
  }
  catch (error) {
    console.error('error', error)
    showSnackbar(error.message)
    return
  }
  finally {
    showLoading(false)
  }
  idsub.value = reply.data
  updateEnrollment()
  emit('changeStep', step + 1)
}

function prev() {
  updateEnrollment()
  emit('changeStep', step - 1)
}

function setup(e) {
  console.log('setup details', e)
  birthyear.value = e.birthyear
  category.value = e.category
  emailplayer.value = e.emailplayer
  first_name.value = e.first_name
  idbel.value = e.idbel
  idfide.value = e.idfide
  idsub.value = e.idsub
  last_name.value = e.kast_name
  mobileplayer.value = e.mobileplayer
  nationalityfide.value = e.nationalityfide
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

function updateEnrollment() {
  emit('updateEnrollment', {
    category: category.value,
    emailplayer: emailplayer.value,
    idsub: idsub.value,
    mobileplayer: mobileplayer.value,
  })
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
})

</script>
<template>
  <v-form v-model="formvalid">
    <v-container>
      <SnackbarMessage ref="refsnackbar" />
      <ProgressLoading ref="refloading" />
      <v-row class="mt-2">
        <h2>{{ $t('enrollvk.det_title') }}</h2>
      </v-row>
      <v-row>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('First name') }}: <b>{{ first_name }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('Last name') }}: <b>{{ last_name }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('Birthyear') }}: <b>{{ birthyear }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('FIDE nationality') }}: <b>{{ nationalityfide }}</b>
          </div>
        </v-col>
      </v-row>
      <v-row>
        <h3 class="my-2">{{ $t('enrollvk.det_requiredinfo') }}</h3>
      </v-row>
      <v-row>
        <div class="my-2">{{ $t('enrollvk.det_details') }}</div>
      </v-row>
      <v-row>
        <h4 class="mt-2 mb-1">{{ $t('enrollvk.det_tournament') }}</h4>
      </v-row>
      <v-row class="mt-1">
        <VRadioGroup v-model="category" :rules="[tValidator(v_required)]">
          <VRadio label="Vlaams Kampioenschap 2024" value="VK"></VRadio>
          <VRadio :label="t('enrollvk.det_senioren')" value="SEN"></VRadio>
          <VRadio :label="t('enrollvk.det_experten')" value="EXP"></VRadio>
        </VRadioGroup>
      </v-row>
      <v-row>
        <div>{{ $t('enrollvk.det_expremark') }}</div>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <VTextField :label="t('Email')" v-model="emailplayer"
            :rules="[tValidator(v_required), tValidator(v_length2)]" />
        </v-col>
        <v-col cols="12" md="6">
          <VTextField :label="t('GSM number')" v-model="mobileplayer"
            :rules="[tValidator(v_required), tValidator(v_length2)]" />
        </v-col>
      </v-row>
      <v-row class="mt-4">
        <div class="mt-2">
          <v-btn class="ml-2" @click="prev" color="primary">
            {{ $t('Back') }}
          </v-btn>
          <v-btn :disabled="!formvalid" class="ml-2" color="primary" @click="next">
            {{ $t('Continue') }}
          </v-btn>
        </div>
      </v-row>
    </v-container>
  </v-form>
</template>