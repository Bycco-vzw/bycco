<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

// communication with main tool page
const emit = defineEmits(['changeStep'])
defineExpose({ setup })

// i18n
const { t } = useI18n()

// datamodel
const gdpr_ok = ref(false)
const step = 5


function next() {
  console.log('clicked next')
  emit('changeStep', step + 1)
}

function prev() {
  console.log('clicked prev')
  emit('changeStep', step - 1)
}

function setup(l) {
  console.log('setup gdpr', l)
}

</script>
<template>
  <v-container>
    <v-row>
      <h2>{{ t('enrollvk.gdpr_title') }}</h2>
    </v-row>
    <v-row>
      <div class="mt-2">
        <ul>
          <li>{{ t('enrollvk.gdpr_1') }}</li>
          <li>{{ t('enrollvk.gdpr_2') }}</li>
          <li>{{ t('enrollvk.gdpr_3') }}</li>
          <li>{{ t('enrollvk.gdpr_4') }}</li>
          <li>{{ t('enrollvk.gdpr_5') }}</li>
          <li>{{ t('enrollvk.gdpr_6') }}</li>
        </ul>
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <VCheckbox :label="t('enrollvk.gdpr_agree')" v-model="gdpr_ok" />
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <v-btn class="ml-2" @click="prev" color="primary">
          {{ $t('Back') }}
        </v-btn>
        <v-btn :disabled="!gdpr_ok" class="ml-2" color="primary" @click="next">
          {{ $t('Continue') }}
        </v-btn>
      </div>
    </v-row>
  </v-container>
</template>