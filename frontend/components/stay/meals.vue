<script setup>
import { ref } from "vue"
import { useI18n } from "vue-i18n"
import { v_required } from "@/composables/validators"

// i18n
const { t } = useI18n()
const ts = {
  intro: "Select which meals you want",
  deviation:
    "Normally the first meal is dinner at arrival day and the last meal is breakfast at departure day. Specify any special food wishes (vegetarian, gluten free, ...) or deviations from the normal meal scheme in the remarks field.",
  // full: 'Full boarding',
  half: "Half boarding",
  no: "No meals",
  breakfast: "Breakfast",
}

// communication with manager
const emit = defineEmits(["changeStep", "updateStay"])
defineExpose({ setup })

// datamodel
const common = ref(null)
const stay = ref(null)
const meals = ref("")
const remarks = ref("")
const breakfast = ref(false)
const formvalid = ref(false)

function next() {
  updateStay()
  emit("changeStep", 6)
}

function prev() {
  updateStay()
  emit("changeStep", 4)
}

function set_meals() {
  common.value.rooms.forEach((r) => {
    if (r.name == stay.value.accomodation) {
      breakfast.value = !!r.breakfast
    }
  })
  if (!stay.value.meals) {
    meals.value = breakfast.value ? "breakfast" : "half"
  } else {
    meals.value = stay.value.meals + ""
  }
}

function setup(stay_, common_) {
  console.log("setup meals", stay_, common_)
  common.value = common_
  stay.value = stay_
  set_meals()
  remarks.value = stay_.remarks ? stay_.remarks + "" : ""
}

function updateStay() {
  emit("updateStay", {
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
          <v-radio :label="$t(ts.no)" value="no" v-if="!breakfast" />
          <v-radio :label="$t(ts.breakfast)" value="no" v-if="breakfast" />
          <v-radio :label="$t(ts.half)" value="half" />
          <!-- <v-radio :label="$t(t.full)" value="full" /> -->
        </v-radio-group>
      </div>
      <div class="mt-2 mb-3">
        {{ $t(ts.deviation) }}
        <br />
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
