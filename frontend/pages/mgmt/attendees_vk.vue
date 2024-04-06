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
const pwzersonstore = usePersonStore();
const { person } = storeToRefs(personstore)

// datamodel
const attendees = ref([])
const att = ref()
const search = ref("")
const headers = [
  { title: 'Last Name', value: 'last_name', sortable: true },
  { title: 'First Name', value: 'first_name', sortable: true },
  { title: 'Category', value: 'category', sortable: true },
  { title: 'Actions', value: 'action' },
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


async function create_att() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("attendee", "mgmt_create_attendee_vk", {
      token: token.value,
      attendee: att.value
    })
  }
  catch (error) {
    console.error('creating all pr failed', error)
    if (error.code === 401) {
      router.push('/mgmt')
    } else {
      showSnackbar('Creating paymentrequests failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  await getParticipants()
}

function edit_att(item) {
}

async function get_attendees() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('attendee', "get_attendees_vk")
    attendees.value = reply.data
  }
  catch (error) {
    console.error('getting attendees failed', error)
    showSnackbar('Getting attendess failed')
    return
  }
  finally {
    showLoading(false)
  }
}


async function refresh() {
  await get_attendees()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await get_attendees()
})

</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Management Attendees VK2024</h1>
    <v-data-table :headers="headers" :items="attendees" :items-per-page-options="[20, 50, -1]"
      items-per-page="20" class="elevation-1" :sort-by="[{ key: 'last_name', order: 'asc' }]"
      :search="search">
      <template #top>
        <v-card color="bg-grey-lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field v-model="search" label="Search" class="mx-4" append-icon="mdi-magnify"
                hide_details />
              <v-spacer />
              <v-tooltip location="bottom">
                Create new attendee
                <template #activator="{ props }">
                  <v-btn fab outlined color="deep-purple-lighten-1" v-bind="props"
                    @click="create_att()">
                    <v-icon>mdi-plus</v-icon>
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
      <template #item.action="{ item }">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon small class="mr-2" v-on="on" @click="edit_attendee(item)">
              mdi-pencil
            </v-icon>
          </template>
          Edit Attendee
        </v-tooltip>
      </template>
      <template #no-data>
        No attendees found.
      </template>
    </v-data-table>
    <VDialog v-model="editdialog" width="30em">
      <VCard>
        <VCardTitle>
          {{ $t('Edit') }}: {{ att.last_name }} {{ att.first_name }}
          <VDivider />
        </VCardTitle>
        <VCardText>
          <v-switch v-model="att.enabled" label="Enabled" color="deep-purple" />
          Last name: <b>{{ att.last_name }}</b><br />
          First name: <b>{{ att.first_name }}</b><br />
          Category: <b>{{ att.category }}</b><br />
          ID BEL: <b>{{ att.idbel }}</b><br />
          ID FIDE: <b>{{ att.idfide }}</b><br />
        </VCardText>
        <VCardActions>
          <VSpacer />
          <VBtn @click="edit_save">Save</VBtn>
          <VBtn @click="editdialog = false">Cancel</VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </v-container>
</template>