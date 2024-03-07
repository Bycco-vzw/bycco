<script setup>
import { ref } from 'vue'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()
const router = useRouter()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// stores
const mgmtstore = useMgmtTokenStore()
const { token } = storeToRefs(mgmtstore)
const personstore = usePersonStore();
const { person } = storeToRefs(personstore)

// datamodel
const participants = ref([])
const search = ref("")
const headers = [
  { title: 'Last Name', value: 'last_name' },
  { title: 'First Name', value: 'first_name' },
  { title: 'Category', value: 'category' },
  { title: 'ID Bel', value: 'idbel' },
  { title: 'ID Fide', value: 'idfide' },
]

definePageMeta({
  layout: 'mgmt',
})


async function checkAuth() {
  console.log('checking if auth is already set', token.value)
  if (token.value) return
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
    console.log('cannot login', error)
    router.push('/mgmt')
    return
  }
  finally {
    showLoading(false)
  }
  console.log('mgmttoken received', reply.data)
  mgmtstore.updateToken(reply.data)
}


async function importEnrollments() {
  let reply, xls
  showLoading(true)
  try {
    reply = await $backend("participant", "mgmt_import_enrollments_vk", {
      token: token.value
    })
  }
  catch (error) {
    console.log('download error', error)
    showSnackbar('Failed to import enrollments: ' + error.detail)
  }
  finally {
    showLoading(false)
  }
}

async function getParticipants() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('participant', "get_participants_vk")
    participants.value = reply.data
  }
  catch (error) {
    console.error('getting participants failed', error)
    showSnackbar('Getting participants failed')
    return
  }
  finally {
    showLoading(false)
  }
}

// function gotoPaymentRequest(item) {
//   router.push('/mgmt/paymentrequest_edit?id=' + item.payment_id)
// }

function lightgreyRow(item) {
  if (!item.enabled) {
    return 'lightgreyrow'
  }
}

async function refresh() {
  await getParticipants()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getParticipants()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Management Particpants VK202</h1>
    <v-data-table :headers="headers" :items="participants" :item-class="lightgreyRow"
      :items-per-page-options="[150, -1]" class="elevation-1"
      :sort-by="[{ key: 'last_name', order: 'asc' }]" :search="search">
      <template #top>
        <v-card color="bg-grey-lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field v-model="search" label="Search" class="mx-4" append-icon="mdi-magnify"
                hide_details />
              <v-spacer />
              <v-tooltip location="bottom">
                Import Enrollments
                <template #activator="{ props }">
                  <v-btn fab outlined color="deep-purple-lighten-1" v-bind="props"
                    @click="importEnrollments()">
                    <v-icon>mdi-import</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              &nbsp;
              <v-tooltip location="bottom">
                Refresh

                <template #activator="{ props }">
                  <v-btn fab outlined color="deep-purple-lighten-1" v-bind="props"
                    @click="refresh()">
                    <v-icon>mdi-refresh</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </v-row>
          </v-card-title>
        </v-card>
      </template>

      <template #no-data>
        No participants found.
      </template>
    </v-data-table>
  </v-container>
</template>