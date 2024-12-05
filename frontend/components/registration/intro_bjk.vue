<script setup>
import { useI18n } from 'vue-i18n'

// communication with main tool page
const emit = defineEmits(['changeStep'])
defineExpose({ setup })

// i18n
const { t } = useI18n()

function next() {
  console.log('clicked next')
  emit('changeStep', 2)
}

function setup(l) {
  console.log('setup intro', l)
}

</script>
<template>
  <v-container>
    <v-row>
      <h2>Intro</h2>
    </v-row>
    <v-row>
      <div class="mt-2">
        {{ t('enroll.intro_intro') }}
        <ul>
          <li>{{ t('enroll.intro_needbelid') }}</li>
          <li>{{ t('enroll.intro_needphoto') }}</li>
        </ul>
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        {{ t('enroll.intro_noid') }}
      </div>
      <div class="mt-2">
        {{ t('enroll.intro_new') }}
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <v-btn color="primary" @click="next">
          {{ t("Continue") }}
        </v-btn>
      </div>
    </v-row>
  </v-container>
</template>