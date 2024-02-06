<script setup>
import { ref } from 'vue'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()

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
const reservations = ref([])
const search = ref("")
const headers = [
  { title: 'Request nr', value: 'number' },
  { title: 'Last Name', value: 'last_name' },
  { title: 'First Name', value: 'first_name' },
  { title: 'Request room', value: 'lodging' },
  { title: '# guests', value: 'guestlist' },
  { title: 'room', value: 'room' },
  { title: 'Actions', value: 'action', sortable: false }
]
const xls = ref(null)

definePageMeta({
  layout: 'mgmt',
})


async function checkAuth() {
  console.log('checking if auth is already set', token.value)
  if (token.value) return
  if (person.value.credentials.length === 0) {
    navigateTo('/mgmt')
    return
  }
  if (!person.value.email.endsWith('@bycco.be')) {
    navigateTo('/mgmt')
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
    navigateTo('/mgmt')
    return
  }
  finally {
    showLoading(false)
  }
  console.log('mgmttoken received', reply.data)
  mgmtstore.updateToken(reply.data)
}


async function downloadReservations() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("lodging", "xls_reservations", {
      authorization: 'Bearer ' + this.token
    })
    xls = resp.data.xls64
  }
  catch (error) {
    console.log('download error', error)
    showSnackbar('Download error: ' + error.detail)
  }
  finally {
    showLoading(false)
  }
  const link = document.createElement('a')
  link.download = 'reservations.xlsx'
  link.href = 'data:aaplication/excel;base64,' + xls.value
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  showSnackbar('Downloading reservations successful')
}

async function editReservation(item) {
  await navigateTo('/mgmt/reservation_edit/?id=' + item.id)
}

async function getReservations() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('lodging', "mgmt_get_reservations", {
      token: token.value
    })
    reservations.value = reply.data
    reservations.value.forEach((r) => {
      const rooms = r.assignments ? Array.from(r.assignments, a => a.roomnr) : []
      r.room = rooms.join(',')
    })
    console.log('rsv', reservations.value)
  }
  catch (error) {
    console.error('getting reservations failed', error)
    if (error.code === 401) {
      await navigateTo('/mgmt')
    }
    else {
      showSnackbar('Getting reservations failed')
    }
  }
  finally {
    showLoading(false)
  }
}

async function gotoPaymentRequest(item) {
  await navigateTo('/mgmt/paymentrequest_edit?id=' + item.payment_id)
}

function lightgreyRow(item) {
  if (!item.enabled) {
    return 'lightgreyrow'
  }
}

async function refresh() {
  await getReservations()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getReservations()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Management Reservations</h1>
    <v-data-table :headers="headers" :items="reservations" :item-class="lightgreyRow"
      :footer-props="footerProps" class="elevation-1" :sort-by="['name', 'modified']"
      :search="search">
      <template #top>
        <v-card color="grey lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field v-model="search" label="Search" class="mx-4" append-icon="mdi-magnify"
                hide_details />
              <v-spacer />
              <v-tooltip bottom>
                <template #activator="{ on }">
                  <v-btn fab outlined color="deep-purple" v-on="on" @click="downloadReservations()">
                    <v-icon>mdi-download-multiple</v-icon>
                  </v-btn>
                </template>
                Download Reservations
              </v-tooltip>
              <v-tooltip bottom>
                <template #activator="{ on }">
                  <v-btn fab outlined color="deep-purple" v-on="on" @click="refresh()">
                    <v-icon>mdi-refresh</v-icon>
                  </v-btn>
                </template>
                Refresh
              </v-tooltip>
            </v-row>
          </v-card-title>
        </v-card>
      </template>
      <template #item._creationtime="{ item }">
        {{ (new Date(item._creationtime)).toLocaleDateString("en-GB", { dateStyle: 'medium' }) }}
      </template>
      <template #item.guestlist="{ item }">
        {{ item.guestlist.length }}
      </template>
      <template #item.payment_id="{ item }">
        <NuxtLink v-if="item.payment_id" :to="'/mgmt/paymentrequestedit?id=' + item.payment_id">
          link
        </NuxtLink>
      </template>
      <template #item.action="{ item }">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon small class="mr-2" v-on="on" @click="editReservation(item)">
              mdi-pencil
            </v-icon>
          </template>
          Edit Reservation
        </v-tooltip>
        <v-tooltip v-if="item.payment_id" bottom>
          <template #activator="{ on }">
            <v-icon small class="mr-2" v-on="on" @click="gotoPaymentRequest(item)">
              mdi-currency-eur
            </v-icon>
          </template>
          Show payment request
        </v-tooltip>
      </template>
      <template #no-data>
        No reservations found.
      </template>
    </v-data-table>
  </v-container>
</template>