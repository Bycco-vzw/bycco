<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { v_required, v_length2 } from '@/composables/validators'

// i18n
const { t } = useI18n()
const ts = {
  intro: 'Provide for any guest, the name, first name, birthdate. Indicate if a guest intends to particpatte to the tournament.',
  requester: "Don't forget to mention the details of requester, in case he/she stays in this lodging.",
  deviation: 'As a default all guests stay the full period in the accomodation.  If this it not the case, please provide the any deviation form the default in the remarks field below.',
  participants: 'Indicate which guests will participate in the tournament'
}

// communication with manager
const emit = defineEmits(['changeStep', 'updateLodging'])
defineExpose({ setup })

// datamodel
const guestlist = ref([])
const remarks = ref("")
const formvalid = ref(false)
const menu_birth = ref([])
const renderGuests = ref(true)


// methods


function deleteGuest(ix) {
  guestlist.value.splice(ix, 1)
}

function next() {
  updateLodging()
  emit('changeStep', 4)
}

function prev() {
  updateLodging()
  emit('changeStep', 2)
}

function setup(l) {
  console.log('setup guests', l)
  guestlist.value = [...l.guestlist]
  lastguestempty()
  remarks.value = l.remarks || '' + ''
}

function lastguestempty() {
  const lastguest = guestlist.value[guestlist.value.length - 1]
  console.log('lastguest', lastguest)
  if (!lastguest || lastguest.first_name || lastguest.last_name) {
    guestlist.value.push({
      first_name: '',
      last_name: '',
      birthdate: '',
      player: false,
    })
  }
}

function updateLodging() {
  guestlist.value.length--
  console.log('guestwithoutlast', guestlist.value)
  emit('updateLodging', {
    guestlist: guestlist.value,
    remarks: remarks.value,
  })
}


</script>

<template>
  <div>
    <h2>{{ t("Guests") }}</h2>
    <div class="mt-2 mb-3">
      {{ t(ts.intro) }}
    </div>
    <div class="mt-2 pb-3">
      <b>
        {{ t(ts.requester) }}
      </b>
    </div>
    <v-form v-model="formvalid" class="pt-2">
      <v-row v-for="(g, ix) in guestlist" :key="ix">
        <v-col cols="12" sm="6" md="3">
          <v-text-field dense v-model="g.first_name" :label="t('First name')"
            @update:focused="lastguestempty" />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field dense v-model="g.last_name" :label="t('Last name')"
            @update:focused="lastguestempty" />
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-text-field dense v-model="g.birthdate" :label="t('Birth date')" type="date" />
        </v-col>
        <v-col cols="4" sm="2" md="1">
          <v-btn fab small @click="deleteGuest(ix)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <div v-show="guestlist.length > 1">
        <h3 class="mt-3">
          {{ t('Participants') }}
        </h3>
        <div>
          {{ t(ts.participants) }}
        </div>
        <div v-for="(g, ix) in guestlist" :key="'a' + ix">
          <v-checkbox v-show="g.last_name.length" dense hide-details v-model="g.player"
            :label="`${g.first_name} ${g.last_name} `" />
        </div>
      </div>
      <div>
        <div class="mt-3 mb-3">
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
      </div>
    </v-form>
  </div>
</template>


<style scoped>
.v-input--selection-controls.top8 {
  margin-top: 8px;
}
</style>
