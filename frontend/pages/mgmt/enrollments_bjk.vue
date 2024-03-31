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
  { title: 'Comfirmed', value: 'confirmed' },
  { title: 'Actions', value: 'action', sortable: false },
]
const enrs = ref([])
const enr = ref({})
const search = ref("")
const editdialog = ref(false)

definePageMeta({
  layout: 'mgmt',
})

async function checkAuth() {
  console.log('checking if auth is already set', token.value)
  if (token.value) return
  if (person.value.credentials.length === 0) {
    console.log('person credentals not set')
    console.log('pushing to /mgmt')
    router.push('/mgmt')
    console.log('pushing done')
    return
  }
  if (!person.value.email.endsWith('@bycco.be')) {
    console.log('person credentals not ending with bycco.be')
    console.log('pushing to /mgmt')
    router.push('/mgmt')
    console.log('pushing done')
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
    console.log('pushing to /mgmt')
    router.push('/mgmt')
    console.log('pushing done')
    return
  }
  finally {
    showLoading(false)
  }
  mgmtstore.updateToken(reply.data)
}

async function editEnrollment(item) {
  await getEnrollment(item.id)
  editdialog.value = true
}


async function getEnrollment(id) {
  let reply
  showLoading(true)
  try {
    reply = await $backend('enrollment', "mgmt_get_enrollment_bjk", {
      id: id,
      token: token.value
    })
    enr.value = reply.data
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


async function getEnrollments() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('enrollment', "get_enrollments_bjk")
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

async function save() {
  showLoading(true)
  try {
    await $backend("enrollment", "mgmt_update_enrollment_bjk", {
      id: enr.value.id,
      enr: {
        enabled: enr.value.enabled
      },
      token: token.value
    })
    editdialog.value = false
    enrs.value.forEach((e) => {
      if (e.id == enr.value.id) {
        e.enabled = enr.value.enabled
      }
    })
  }
  catch (error) {
    console.error('update enrollment', error)
    if (error.code === 401) {
      showSnackbar('Credentials expired, you need to login again')
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
  showSnackbar('Enrollment saved')
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
    <h1>Management Enrollments BJK2024</h1>
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
      <template v-slot:item.last_name="{ item }">
        <span :class="{ disabled: !item.enabled }">
          {{ item.last_name }}
        </span>
      </template>
      <template v-slot:item.first_name="{ item }">
        <span :class="{ disabled: !item.enabled }">
          {{ item.first_name }}
        </span>
      </template>
      <template v-slot:item.category="{ item }">
        <span :class="{ disabled: !item.enabled }">
          {{ item.category }}
        </span>
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
    <VDialog v-model="editdialog" width="20em">
      <VCard>
        <VCardTitle>
          {{ $t('Edit') }}: {{ enr.last_name }} {{ enr.first_name }}
          <VDivider />
        </VCardTitle>
        <VCardText>
          <v-switch v-model="enr.enabled" label="Enabled" color="deep-purple" />
          Last name: <b>{{ enr.last_name }}</b><br />
          First name: <b>{{ enr.first_name }}</b><br />
          Confirmed: <b>{{ enr.confirmed }}</b><br />
          Confirmation email: <b>{{ enr.confirmation_email }}</b><br />
          Category: <b>{{ enr.category }}</b><br />
          ID BEL: <b>{{ enr.idbel }}</b><br />
          ID FIDE: <b>{{ enr.idfide }}</b><br />
          Chess title <b>{{ enr.chesstitle }}</b><br />
          Nationality FIDE: <b>{{ enr.nationalityfide }}</b>
        </VCardText>
        <VCardActions>
          <VSpacer />
          <VBtn @click="save">Save</VBtn>
          <VBtn @click="editdialog = false">Cancel</VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </v-container>
</template>

<style scoped>
.disabled {
  color: rgb(186, 185, 185);
}
</style>