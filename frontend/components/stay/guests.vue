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
const guestlist = ref([])
const remarks = ref("")
const formvalid = ref(false)

// methods

function deleteGuest(ix) {
  guestlist.value.splice(ix, 1)
}

function next() {
  updateStay()
  emit("changeStep", 4)
}

function prev() {
  updateStay()
  emit("changeStep", 2)
}

function setup(l) {
  console.log("setup guests", l)
  guestlist.value = [...l.guestlist]
  lastguestempty()
  remarks.value = l.remarks || "" + ""
}

function lastguestempty() {
  const lastguest = guestlist.value[guestlist.value.length - 1]
  console.log("lastguest", lastguest)
  if (!lastguest || lastguest.first_name || lastguest.last_name) {
    guestlist.value.push({
      first_name: "",
      last_name: "",
      birthdate: "",
      player: false,
    })
  }
}

function updateStay() {
  guestlist.value.length--
  console.log("guestwithoutlast", guestlist.value)
  emit("updateStay", {
    guestlist: guestlist.value,
    remarks: remarks.value,
  })
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
    <v-form v-model="formvalid" class="pt-2">
      <v-row v-for="(g, ix) in guestlist" :key="ix">
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            dense
            v-model="g.first_name"
            :label="t('First name')"
            @update:focused="lastguestempty"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            dense
            v-model="g.last_name"
            :label="t('Last name')"
            @update:focused="lastguestempty"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field
            dense
            v-model="g.birthdate"
            :label="t('Birth date')"
            type="date"
          />
        </v-col>
        <v-col cols="4" sm="2" md="1">
          <v-btn fab small @click="deleteGuest(ix)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>
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
          <v-btn color="primary" :disabled="!formvalid" @click="next">
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
