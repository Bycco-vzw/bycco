<script setup>
import { ref } from "vue"
import { useI18n } from "vue-i18n"
import { v_required, v_length2 } from "@/composables/validators"

// i18n
const { t } = useI18n()

// communication with manager
const emit = defineEmits(["changeStep", "updateStay"])
defineExpose({ setup })

// datamodel
const common = ref(null)
const guestlist = ref([])
const stay = ref({})
const remarks = ref("")
const formvalid = ref(false)
const errmsg = ref(null)

// methods

function deleteGuest(ix) {
  guestlist.value.splice(ix, 1)
}

function next() {
  if (!validateStay()) return
  updateStay()
  emit("changeStep", 5)
}

function prev() {
  updateStay()
  emit("changeStep", 3)
}

function set_guestlist() {
  let maxpers = 1
  common.value.rooms.forEach((r) => {
    if (stay.value.accomodation == r.name) {
      maxpers = r.maxpers
    }
  })
  console.log("maxpers", maxpers, stay.value.accomodation)
  guestlist.value = []
  stay.value.guestlist.forEach((g, ix) => {
    if (ix < maxpers) {
      guestlist.value.push(g)
    }
  })
  for (let i = guestlist.value.length; i < maxpers; i++) {
    guestlist.value.push({
      first_name: "",
      last_name: "",
      birthdate: "",
      player: false,
    })
  }
  console.log("guestlist", guestlist.value)
}

async function setup(stay_, common_) {
  console.log("setup guests", stay_, common_)
  stay.value = stay_
  common.value = common_
  set_guestlist()
  remarks.value = stay_.remarks || "" + ""
}

function updateStay() {
  let gl = []
  guestlist.value.forEach((g) => {
    if (g.first_name && g.last_name) {
      gl.push(g)
    }
  })
  console.log("guestlist without empty", gl)
  emit("updateStay", {
    guestlist: gl,
    remarks: remarks.value,
  })
}

function validateStay() {
  formvalid.value = true
  guestlist.value.forEach((g, ix) => {
    if (g.first_name && g.last_name) {
      if (!g.birthdate) {
        formvalid.value = false
        errmsg.value = "Invalid birthdate"
      }
    }
  })
  return formvalid.value
}
</script>

<template>
  <div>
    <h2>{{ t("stay.guest_2") }}</h2>
    <div class="mt-2 mb-3">
      {{ t("stay.guest_detail") }}
    </div>
    <div class="mt-2 pb-3">
      <b>
        {{ t("stay.guest_requester") }}
      </b>
    </div>
    <v-form class="pt-2">
      <v-row v-for="(g, ix) in guestlist" :key="ix">
        <v-col cols="12" sm="6" md="3">
          <v-text-field dense v-model="g.first_name" :label="t('First name')" />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field dense v-model="g.last_name" :label="t('Last name')" />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            dense
            v-model="g.birthdate"
            :label="t('Birth date')"
            type="date"
          />
        </v-col>
      </v-row>
      <v-alert v-show="!formvalid && errmsg" :text="errmsg" outlined type="error" />
      <div v-show="guestlist.length > 1">
        <h3 class="mt-3">
          {{ t("Participants") }}
        </h3>
        <div>
          {{ t("stay.guest_part") }}
        </div>
        <div v-for="(g, ix) in guestlist" :key="'a' + ix">
          <v-checkbox
            v-show="g.last_name.length"
            dense
            hide-details
            v-model="g.player"
            :label="`${g.first_name} ${g.last_name} `"
          />
        </div>
      </div>
      <div>
        <div class="mt-3 mb-3">
          {{ t("stay.guest_deviation") }}
          <br />
          <v-textarea v-model="remarks" :label="t('Remarks')" auto-grow />
        </div>
        <div class="mt-2">
          <v-btn color="primary" @click="prev" class="mr-2">
            {{ t("Back") }}
          </v-btn>
          <v-btn color="primary" @click="next">
            {{ t("Continue") }}
          </v-btn>
        </div>
      </div>
    </v-form>
  </div>
</template>

<style scoped>
.v-input--selection-controls.top8 {
  margin-top: 8px;
}
</style>
