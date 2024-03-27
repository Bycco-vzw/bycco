<script setup>
import { ref } from 'vue'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()
const route = useRoute()
const router = useRouter()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// stores
const mgmtstore = useMgmtTokenStore()
const { token: mgmttoken } = storeToRefs(mgmtstore)
const personstore = usePersonStore();
const { person } = storeToRefs(personstore)

// datamodel
const idenr = route.query.id
const enr = ref({})

definePageMeta({
  layout: 'mgmt',
})


function back() {
  router.go(-1)
}

async function checkAuth() {
  console.log('checking if auth is already set', mgmttoken.value)
  if (mgmttoken.value) return
  if (person.value.credentials.length === 0) {
    router.push('/mgmt')
    return
  }
  if (!person.value.email.endsWith('@bycco.be')) {
    router.push('/mgmt')
    return
  }
  let reply
  showLoading(true)
  // now login using the Google auth token
  try {
    reply = await $backend("accounts", "login", {
      logintype: 'google',
      token: person.value.credentials,
      username: null,
      password: null,
    })
  }
  catch (error) {
    navigateTo('/mgmt')
  }
  finally {
    showLoading(false)
  }
  mgmtstore.updateToken(reply.data)
}

async function getEnrollment() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('enrollment', "mgmt_get_enrollment_vk", {
      id: idenr,
      token: mgmttoken.value
    })
    readEnrollment(reply.data)
  }
  catch (error) {
    console.error('getting enrollment failed', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Getting enrollment failed')
    }
  }
  finally {
    showLoading(false)
  }
}

function readEnrollment(enrollment) {
  enr.value = { ...enrollment }
}

async function saveEnrollment() {
  let reply
  showLoading(true)
  try {
    await $backend("enrollment", "mgmt_update_enrollment_vk", {
      id: idenr.value,
      enrollment: {
        enabled: enr.value.enabled
      },
      token: mgmttoken.value
    })
  }
  catch (error) {
    console.error('getting getEnrollment', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Saving enrollment failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  console.log('save successful')
  showSnackbar('Enrollment saved')
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getEnrollment()
})

</script>

<template>
  <v-container>

    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />

    <v-row class="my-2">
      <h2>Edit Enrollment: {{ enr.last_name }} {{ enr.first_name }}</h2>
      <v-spacer />
      <v-tooltip bottom>
        <template #activator="{ on }">
          <v-btn outlined fab color="deep-purple" @click="back()">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
    </v-row>

    <v-card class="my-3">
      <v-card-title>
        Properties
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <v-switch v-model="enr.enabled" label="Enabled" />
            Last name: <b>{{ enr.last_name }}</b><br />
            First name: <b>{{ enr.first_name }}</b><br />
            Confirmed: <b>{{ enr.confirmed }}</b><br />
            Confirmation email: <b>{{ enr.confirmation_email }}</b>
          </v-col>
          <v-col cols="12" sm="6">
            Category: <b>{{ enr.category }}</b><br />
            ID BEL: <b>{{ enr.idbel }}</b><br />
            ID FIDE: <b>{{ enr.idfide }}</b><br />
            Chess title <b>{{ enr.chesstitle }}</b><br />
            Nationality FIDE: <b>{{ enr.nationalityfide }}</b>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="saveEnrollment">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>

  </v-container>
</template>
