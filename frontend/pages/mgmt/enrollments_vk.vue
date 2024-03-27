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
const headers = [
  { title: 'Last Name', value: 'last_name' },
  { title: 'First Name', value: 'first_name' },
  { title: 'Category', value: 'category' },
  { title: 'ID Bel', value: 'idbel' },
  { title: 'ID Fide', value: 'idfide' },
  { title: 'Enabled', value: 'enabled' },
  { title: 'Comfirmed', value: 'confirmed' },
  { title: 'Actions', value: 'action', sortable: false },
]
const enrs = ref([])
const search = ref("")

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

function editEnrollment(item) {
  router.push('/mgmt/enrollment_vk_edit/?id=' + item.id)
}

async function getEnrollments() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('enrollment', "get_enrollments_vk")
    enrs.value = reply.data
    console.log('enrs', enrs.value)
  }
  catch (error) {
    console.error('getting enrollments failed', error)
    showSnackbar('Getting enrollments failed')
    return
  }
  finally {
    showLoading(false)
  }
}

async function refresh() {
  await getEnrollments()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getEnrollments()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Management Enrollments VK2024</h1>
    <v-data-table :headers="headers" :items="enrs" class="elevation-1"
      :items-per-page-options="[50, 150, -1]" items-per-page="50"
      :sort-by="[{ key: 'last_name', order: 'asc' }]" :search="search">
      <template #top>
        <v-card color="grey-lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field v-model="search" label="Search" class="mx-4" append-icon="mdi-magnify"
                hide_details />
              <v-spacer />
              <v-tooltip location="bottom" text="Refresh">
                <template #activator="{ props }">
                  <v-btn fab outlined color="deep-purple" v-bind="props" @click="refresh()">
                    <v-icon>mdi-refresh</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </v-row>
          </v-card-title>
        </v-card>
      </template>
      <template #item.action="{ item }">
        <v-tooltip location="bottom">
          Edit
          <template #activator="{ props }">
            <v-icon small class="mr-2" v-bind="props" @click="editEnrollment(item)">
              mdi-pencil
            </v-icon>
          </template>
        </v-tooltip>
      </template>
      <template #no-data>
        No enrollments found.
      </template>
    </v-data-table>
  </v-container>
</template>