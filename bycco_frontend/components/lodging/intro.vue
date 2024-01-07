<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'



// communication with main tool page
const emit = defineEmits(['changeStep'])
defineExpose({ setup })

// i18n
const { t } = useI18n()
const ts = {
  intro: 'In order to make a reservation you need to provide the following elements:',
  req1: 'the details of the adult responsible for the reservation',
  req2: 'the details of every guest',
  req3: 'which guests are participants to the tournament',
  req4: 'accomodation details, start date and end date',
  req5: 'the meals',
  multiple: 'The reservation is done per room.  If you want to book two rooms, you have to run this tools twice.'
}

function next() {
  console.log('clicked next')
  emit('changeStep', 2)
}

function setup(l) {
  console.log('setup intro', l)
}

</script>

<template>
  <div>
    <h2>Intro</h2>
    <div class="mt-2">
      {{ t(ts.intro) }}
      <ul>
        <li>{{ t(ts.req1) }}</li>
        <li>{{ t(ts.req2) }}</li>
        <li>{{ t(ts.req3) }}</li>
        <li>{{ t(ts.req4) }}</li>
        <li>{{ t(ts.req5) }}</li>
      </ul>
    </div>
    <div class="mt-2">
      {{ t(ts.multiple) }}
    </div>
    <div class="mt-2">
      <v-btn color="primary" @click="next">
        {{ t("Continue") }}
      </v-btn>
    </div>
  </div>
</template>


