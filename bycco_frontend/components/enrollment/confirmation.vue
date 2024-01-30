<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'

const runtimeConfig = useRuntimeConfig()

// communication
const emit = defineEmits(['changeStep', 'restart'])
defineExpose({ setup })
const { $backend } = useNuxtApp()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// i18n
const { t } = useI18n()

// datamodel member
const birthyear = ref(null)
const category = ref("")
const first_name = ref("")
const gender = ref(null)
const idsub = ref("")
const last_name = ref("")
const nationalityfide = ref("")
const photourl = computed(() => `${runtimeConfig.public.apiUrl}api/v1/enrollment/photo/${idsub.value}`)
const isConfirmed = ref(false)

const step = 6

async function confirm() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("enrollment", "confirm_enrollment", {
      idsub: idsub.value
    })
  }
  catch (error) {
    console.error('confirmation failed', error)
    showSnackbar('Confirmation failed')
    return
  }
  finally {
    showLoading(false)
  }
  isConfirmed.value = true
}

function prev() {
  emit('changeStep', step - 1)
}

function restart() {
  isConfirmed.value = false
  emit('restart')
}

function setup(e) {
  console.log('setup confirmation', e)
  birthyear.value = e.birthyear
  category.value = e.category
  gender.value = e.gender
  idsub.value = e.idsub
  first_name.value = e.first_name
  nationalityfide.value = e.nationalityfide
  last_name.value = e.last_name
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
})

</script>
<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <v-row class="my-2">
      <h2>{{ $t('enrollvk.cfm_title') }}</h2>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4" lg="3">
        <v-img :src="photourl" width="160" />
      </v-col>
      <v-col cols="12" sm="4" lg="3">
        <div>
          {{ t('Full name') }}: <b>{{ last_name }}, {{ first_name }}</b>
        </div>
        <div>
          {{ t('Birthyear') }}: <b>{{ birthyear }}</b>
        </div>
        <div>
          {{ t('FIDE nationality') }}: <b>{{ nationalityfide }}</b>
        </div>
        <div>
          {{ t('Gender') }}: <b>{{ gender }}</b>
        </div>
        <div>
          {{ t('Category') }}: <b>{{ category }}</b>
        </div>
      </v-col>
    </v-row>
    <v-row class="my-4" v-show="!isConfirmed">
      <v-btn class="ml-2" @click="prev" color="primary">
        {{ $t('Back') }}
      </v-btn>
      <v-btn class="ml-2" @click="confirm" color="primary">
        {{ $t('enrollvk.cfm_confirm') }}
      </v-btn>
    </v-row>
    <v-row class="my-2" v-show="isConfirmed">
      <v-alert :text="t('enrollvk.cfm_confirmed')" type="success" />
    </v-row>
    <hr />
    <v-row v-show="isConfirmed" class="my-4">
      <h3>{{ t('Payment') }}</h3>
    </v-row>
    <v-row v-show="isConfirmed" class="my-4">
      {{ t('enrollvk.cfm_paymentinstructions') }}
    </v-row>
    <hr />
    <v-row v-show="isConfirmed" class="mt-6">
      <v-btn class="ml-2" @click="restart">
        {{ $t('enrollvk.cfm_new') }}
      </v-btn>
    </v-row>
  </v-container>
</template>