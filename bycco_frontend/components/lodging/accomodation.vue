<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { parse } from 'yaml'
import { v_required, v_length2 } from '@/composables/validators'

// api
const { $backend } = useNuxtApp()

// i18n
const { t, locale } = useI18n()
const ts = {
  intro: 'Select which accomodation you want',
  extra: 'Normally the reservation is for 6 nights, from 7-Apr until 13-Apr.  You can optionally add 1 night before and/or after.',
  deviation: 'Specify any special requirements in the remarks field.'
}

// communication with manager
const emit = defineEmits(['changeStep', 'updateLodging'])
defineExpose({ setup })

// datamodel
const accomodation = ref("")
const common = ref([])
const daybefore = ref(false)
const dayafter = ref(false)
const formvalid = ref(false)
const nextday = ref(null)
const prevday = ref(null)
const remarks = ref("")
const roomtypes = ref([])

function next() {
  updateLodging()
  emit('changeStep', 5)
}

function prev() {
  updateLodging()
  emit('changeStep', 3)
}

async function parseYaml(group, name) {
  try {
    const yamlcontent = await readBucket(group, name)
    if (!yamlcontent) {
      return null
    }
    return parse(yamlcontent)
  }
  catch (error) {
    console.error('cannot parse yaml', yamlcontent)
  }
}


async function processCommon() {
  common.value = await parseYaml("data", "common.yaml")
  roomtypes.value = []
  common.value.roomtypes.forEach((rt) => {
    roomtypes.value.push({
      title: common.value.i18n[rt][locale.value],
      value: rt,
    })
  })
  const sd = new Date(common.value.period.startdate)
  const ed = new Date(common.value.period.enddate)
  prevday.value = new Date(sd)
  prevday.value.setDate(sd.getDate() - 1)
  nextday.value = new Date(ed)
  nextday.value.setDate(ed.getDate() + 1)
  console.log('date', prevday.value, nextday.value)
}

async function readBucket(group, name) {
  try {
    const reply = await $backend('filestore', 'anon_get_file', {
      group,
      name,
    })
    return reply.data
  }
  catch (error) {
    console.error('failed to fetch file from bucket')
    return null
  }
}


function setup(l) {
  console.log('setup accomodation', l)
  accomodation.value = l.accomodation
  daybefore.value = !!l.daybefore
  dayafter.value = !!l.dayafter
  remarks.value = l.remarks
}

function updateLodging() {
  emit('updateLodging', {
    accomodation: accomodation.value,
    daybefore: daybefore.value,
    dayafter: dayafter.value,
    remarks: remarks.value,
  })
}

onMounted(() => {
  processCommon()
})


</script>

<template>
  <div>
    <h2>{{ t("Accomodation") }}</h2>
    <v-form v-model="formvalid">
      <div class="mt-2 mb-2">
        {{ t(ts.intro) }}
        <v-radio-group v-model="accomodation" :rules="[v_required]">
          <v-radio v-for="rt in roomtypes" :key="rt" :label="rt.title" :value="rt.value" />
        </v-radio-group>
      </div>
      <div class="mt-2 mb-2">
        {{ t(ts.extra) }}
        <v-checkbox dense hide-details v-model="daybefore"
          :label="t('Arrival date') + ': ' + prevday" />
        <v-checkbox dense hide-details v-model="dayafter"
          :label="t('Departure date') + ': ' + nextday" />
      </div>
      <div class="mt-2 mb-3">
        {{ t(ts.deviation) }}
        <br>
        <v-textarea v-model="remarks" :label="t('Remarks')" auto-grow />
      </div>
      <div class="mt-2">
        <v-btn color="primary" @click="prev" class="mr-2">
          {{ t("Back") }}
        </v-btn>
        <v-btn color="primary" :disabled="!formvalid" @click="next">
          {{ t("Continue") }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>
