<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { v_required } from '@/composables/validators'

// i18n
const { t } = useI18n()
const ts = {
  intro: 'Select which meals you want',
  deviation: 'Normally the first meal is dinner at arrival day and the last meal is breakfast at departure day. Specify any special food wishes (vegetarian, gluten free, ...) or deviations from the normal meal scheme in the remarks field.',
  // full: 'Full boarding',
  half: 'Half boarding',
  no: 'No meals'
}

// communication with manager
const emit = defineEmits(['changeStep', 'updateLodging'])
defineExpose({ setup })

// datamodel
const meals = ref("")
const remarks = ref("")
const formvalid = ref(false)

function next() {
  updateLodging()
  emit('changeStep', 6)
}

function prev() {
  updateLodging()
  emit('changeStep', 4)
}

function setup(l) {
  console.log('setup meals', l)
  meals.value = l.meals ? l.meals + '' : 'half'
  remarks.value = l.remarks ? l.remarks + '' : ''
}

function updateLodging() {
  emit('updateLodging', {
    meals: meals.value,
    remarks: remarks.value,
  })
}


</script>

<template>
  <div>
    <v-form v-model="formvalid">
      <div class="mt-2 mb-2">
        {{ $t(ts.intro) }}
        <v-radio-group v-model="meals" :rules="[v_required]">
          <v-radio :label="$t(ts.no)" value="no" />
          <v-radio :label="$t(ts.half)" value="half" />
          <!-- <v-radio :label="$t(t.full)" value="full" /> -->
        </v-radio-group>
      </div>
      <div class="mt-2 mb-3">
        {{ $t(ts.deviation) }}
        <br>
        <v-textarea v-model="remarks" :label="$t('Remarks')" auto-grow />
      </div>
      <div class="mt-2">
        <v-btn color="primary" @click="prev" class="mr-2">
          {{ $t("Back") }}
        </v-btn>
        <v-btn color="primary" :disabled="!formvalid" @click="next">
          {{ $t("Continue") }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

