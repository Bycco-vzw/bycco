<script setup>
import { ref, computed, onMounted } from "vue"
import { useI18n } from "vue-i18n"
import { parse } from "yaml"
import { v_required, v_length2 } from "@/composables/validators"

// api
const { $backend } = useNuxtApp()

// i18n
const { t, locale } = useI18n()
const ts = {
  intro: "Select which accomodation you want",
  extra:
    "Normally the reservation is for 6 nights, from 7/4/2024 until 13/4/2024.  You can optionally add 1 night before and/or after.",
  deviation: "Specify any special requirements in the remarks field.",
}

// communication with manager
const emit = defineEmits(["changeStep", "updateStay"])
defineExpose({ setup })

// datamodel
const accomodation = ref("")
const common = ref(null)
const daybefore = ref(false)
const dayafter = ref(false)
const formvalid = ref(false)
const startday = computed(() => {
  if (!common.value) return null
  return new Date(common.value.trndates.startdate)
})
const startprevday = computed(() => {
  if (!common.value) return null
  let sd = new Date(common.value.trndates.startdate)
  sd.setDate(sd.getDate() - 1)
  return sd
})
const endday = computed(() => {
  if (!common.value) return null
  return new Date(common.value.trndates.enddate)
})
const endnextday = computed(() => {
  if (!common.value) return null
  let ed = new Date(common.value.trndates.enddate)
  ed.setDate(ed.getDate() + 1)
  return ed
})
const remarks = ref("")
const roomtypes = ref([])

function next() {
  updateStay()
  emit("changeStep", 5)
}

function prev() {
  updateStay()
  emit("changeStep", 3)
}

async function parseYaml(group, name) {
  try {
    const yamlcontent = await readBucket(group, name)
    if (!yamlcontent) {
      return null
    }
    return parse(yamlcontent)
  } catch (error) {
    console.error("cannot parse yaml", yamlcontent)
  }
}

async function processCommon() {
  console.log("process Common")
  common.value = await parseYaml("data", "common.yml")
  console.log("common", common.value)
  roomtypes.value = []
  common.value.roomtypes.forEach((rt) => {
    roomtypes.value.push({
      title: common.value.i18n[rt][locale.value],
      value: rt,
    })
  })
}

async function readBucket(group, name) {
  try {
    const reply = await $backend("filestore", "anon_get_file", {
      group,
      name,
    })
    return reply.data
  } catch (error) {
    console.error("failed to fetch file from bucket")
    return null
  }
}

async function setup(l) {
  console.log("setup accomodation", l)
  await processCommon()
  console.log("zzzz")
  accomodation.value = l.accomodation
  daybefore.value = !!l.daybefore
  dayafter.value = !!l.dayafter
  remarks.value = l.remarks
}

function updateStay() {
  let description
  roomtypes.value.forEach((x) => {
    if (x.value == accomodation.value) {
      description = x.title
    }
  })
  emit("updateStay", {
    accomodation: accomodation.value,
    daybefore: daybefore.value,
    dayafter: dayafter.value,
    remarks: remarks.value,
    checkindate: daybefore.value ? startprevday.value : startday.value,
    checkoutdate: dayafter.value ? endnextday.value : endday.value,
    acc_description: description,
  })
}
</script>

<template>
  <div>
    <h2>{{ t("stay.intro_accom") }}</h2>
    <v-form v-model="formvalid">
      <div class="mt-2 mb-2">
        {{ t(ts.intro) }}
        <v-radio-group v-model="accomodation" :rules="[v_required]">
          <v-radio
            v-for="rt in roomtypes"
            :key="rt"
            :label="rt.title"
            :value="rt.value"
          />
        </v-radio-group>
      </div>
      <div class="mt-2 mb-2">
        {{ t("stay.acc_normal") }}
        {{ t("stay.acc_from") }} {{ Intl.DateTimeFormat(locale.value).format(startday) }}
        {{ t("stay.acc_to") }} {{ Intl.DateTimeFormat(locale.value).format(endday) }}
      </div>
      <div class="mt-2">
        {{ t("stay.acc_changedate") }}
        <v-checkbox
          dense
          hide-details
          v-model="daybefore"
          :label="
            t('Arrival date') +
            ': ' +
            Intl.DateTimeFormat(locale.value).format(startprevday)
          "
        />
        <v-checkbox
          dense
          hide-details
          v-model="dayafter"
          :label="
            t('Departure date') +
            ': ' +
            Intl.DateTimeFormat(locale.value).format(endnextday)
          "
        />
      </div>
      <div class="mt-2 mb-3">
        {{ t(ts.deviation) }}
        <br />
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
