<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { v_required, v_length2 } from '@/composables/validators'
import { categories } from '@/util/constants'

import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'

// communication
const emit = defineEmits(['changeStep', 'updateEnrollment'])
defineExpose({ setup })
const { $backend } = useNuxtApp()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// i18n
const { t, locale } = useI18n()

// datamodel member
const birthyear = ref(0)
const category = ref("20")
const emailplayer = ref("")
const emailparent = ref("")
const emailattendant = ref("")
const first_name = ref("")
const fullnameparent = ref("")
const fullnameattendant = ref("")
const idbel = ref("")
const idfide = ref("")
const idsub = ref("")
const isParentPresent = ref(false)
const last_name = ref("")
const mobileplayer = ref("")
const mobileparent = ref("")
const mobileattendant = ref("")
const nationalityfide = ref("")

// datamodel the rest
const step = 3
const errorcode = ref(false)
const apicat = computed(() => {
  if ([8, 10, 12, 14, 16, 18, 20].includes(category.value)) {
    return "U" + category.value
  }
  else return category.value
})
const catitems = computed(() => {
  const cs = []
  categories.forEach((c) => {
    if (c.year <= birthyear.value) { cs.push(c) }
  })
  return cs
})
const isAdult = computed(() => {
  birthyear.value < categories[1].year
})
const formvalid = ref(false)

async function next() {
  if (!validate_form()) {
    formvalid.value = false
    return
  }
  formvalid.valid = true
  let reply
  showLoading(true)
  try {
    reply = await $backend("enrollment", "create_enrollment_bjk", {
      enrollmentIn: {
        category: apicat.value,
        emailattendant: emailattendant.value,
        emailparent: emailparent.value,
        emailplayer: emailplayer.value,
        fullnameattendant: fullnameattendant.value,
        fullnameparent: fullnameparent.value,
        idbel: idbel.value,
        idfide: idfide.value,
        idsub: idsub.value,
        locale: locale.value,
        mobileattendant: mobileattendant.value,
        mobileparent: mobileparent.value,
        mobileplayer: mobileplayer.value,
      }
    })
  }
  catch (error) {
    console.error('error', error)
    showSnackbar(error.message)
    return
  }
  finally {
    showLoading(false)
  }
  idsub.value = reply.data
  updateEnrollment()
  emit('changeStep', step + 1)
}

function prev() {
  updateEnrollment()
  emit('changeStep', step - 1)
}

function setup(e) {
  console.log('setup details', e)
  birthyear.value = e.birthyear
  category.value = e.category
  emailattendant.value = e.emailattendant || ""
  emailparent.value = e.emailparent || ""
  emailplayer.value = e.emailplayer || ""
  first_name.value = e.first_name
  fullnameattendant.value = e.fullnameattendant || ""
  fullnameparent.value = e.fullnameparent || ""
  idbel.value = e.idbel
  idfide.value = e.idfide
  idsub.value = e.idsub
  last_name.value = e.last_name
  mobileplayer.value = e.mobileplayer || ""
  nationalityfide.value = e.nationalityfide
  if (!category.value) {
    categories.forEach((c) => {
      if (c.year <= birthyear.value)
        category.value = c.value
    })
  }
}

function updateEnrollment() {
  emit('updateEnrollment', {
    category: category.value,
    emailplayer: emailplayer.value,
    idsub: idsub.value,
    mobileplayer: mobileplayer.value,
  })
}

function validate_form() {
  errorcode.value = false
  if (isAdult.value) {
    if (emailplayer.value.length < 2 && mobileplayer.value.length < 2) {
      errorcode.value = "playerdetailsnotvalid"
      return false
    }
  }
  else {
    if (isParentPresent.value) {
      if (fullnameparent.value.length < 2 || emailparent.value.length < 2 ||
        mobileparent.value.length < 2) {
        errorcode.value = "parentdetailsnotvalid"
        return false
      }
    }
    else {
      if (fullnameattendant.value.length < 2 || emailattendant.value.length < 2 ||
        mobileattendant.value.length < 2) {
        errorcode.value = "attendantdetailsnotvalid"
        return false
      }
    }
  }
  return true
}


onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
})

</script>
<template>
  <v-form v-model="formvalid">
    <v-container>
      <SnackbarMessage ref="refsnackbar" />
      <ProgressLoading ref="refloading" />
      <v-row class="mt-2">
        <h2>{{ $t('enrollvk.det_title') }}</h2>
      </v-row>
      <v-row>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('First name') }}: <b>{{ first_name }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('Last name') }}: <b>{{ last_name }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('Birthyear') }}: <b>{{ birthyear }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('FIDE nationality') }}: <b>{{ nationalityfide }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            {{ $t('Gender') }}: <b>{{ gender }}</b>
          </div>
        </v-col>
      </v-row>
      <v-row>

        <h3 class="my-2">{{ $t('enroll.det_more') }}</h3>
        <p class="my-2">{{ $t('enroll.det_requiredinfo') }}</p>
      </v-row>
      <v-row>
        <v-col cols="12" md="6" class="pa-1">
          <h4>{{ $t('Info participant') }}</h4>
          <v-select v-model="category" :label="$t('Category')" :items="catitems" />
          <v-text-field v-model="emailplayer" :label="$t('Email player')" />
          <v-text-field v-model="mobileplayer" :label="$t('GSM player')" />
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <h4>{{ $t('Info about parent') }}</h4>
          <v-checkbox v-model="isParentPresent" :label="$t('A parent is present at site')" />
          <v-text-field v-model="fullnameparent" :label="$t('Full name')" />
          <v-text-field v-model="emailparent" :label="$t('Email parent')" />
          <v-text-field v-model="mobileparent" :label="$t('GSM parent')" />
        </v-col>
        <v-col cols="12" md="6" class="pa-1" v-show="!isParentPresent">
          <h4>{{ $t('Info about attendant on site') }}</h4>
          <div>
            <v-text-field v-model="fullnameattendant" :label="$t('Full name')" />
            <v-text-field v-model="emailattendant" :label="$t('Email')" />
            <v-text-field v-model="mobileattendant" :label="$t('GSM number')" />
          </div>
        </v-col>
      </v-row>
      <v-alert v-show="errorcode" type="error" class="mt-2" closable>
        <div v-show="errorcode == 'playerdetailsnotvalid'">
          <div>{{ t('enroll.det_playerdetailsnotvalid') }}</div>
        </div>
        <div v-show="errorcode == 'parentdetailsnotvalid'">
          <div>{{ t('enroll.det_parentdetailsnotvalid') }}</div>
        </div>
        <div v-show="errorcode == 'attendantdetailsnotvalid'">
          <div>{{ t('enroll.det_attendantdetailsnotvalid') }}</div>
        </div>
      </v-alert>
      <v-row class="mt-4">
        <div class="mt-2">
          <v-btn class="ml-2" @click="prev" color="primary">
            {{ $t('Back') }}
          </v-btn>
          <v-btn class="ml-2" color="primary" @click="next">
            {{ $t('Continue') }}
          </v-btn>
        </div>
      </v-row>
    </v-container>
  </v-form>
</template>