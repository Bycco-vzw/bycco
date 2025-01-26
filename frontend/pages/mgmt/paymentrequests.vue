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
  { title: 'PR nr', value: 'number' },
  { title: 'Type', value: 'reason' },
  { title: 'Last Name', value: 'last_name' },
  { title: 'First Name', value: 'first_name' },
  { title: 'Total price', value: 'totalprice' },
  { title: 'Send date', value: 'sentdate' },
  { title: 'Message', value: 'paymessage' },
  { title: 'Actions', value: 'action', sortable: false }
]
const prqs = ref([])
const search = ref("")

definePageMeta({
  layout: 'mgmt',
})

async function checkAuth() {
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
  console.log('token received', reply.data)
  mgmtstore.updateToken(reply.data)
}

function editPaymentRequest(item) {
  router.push('/mgmt/paymentrequest_edit/?id=' + item.id)
}

async function getPaymentRequests() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("payment", "mgmt_get_paymentrequests", {
      token: token.value
    })
  }
  catch (error) {
    console.error('getting paymentrequests', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Getting payment requests failed')
    }
    prqs.value = []
    return
  }
  finally {
    showLoading(false)
  }
  prqs.value = reply.data
  console.log('prqs', prqs.value)
}

function gotoLinked(item) {
  if (item.reason == "lodging") {
    router.push('/mgmt/reservation_edit/?id=' + item.id)
  }
}


async function refresh() {
  await getPaymentRequests()
}

async function send_prs() {
  showLoading(true)
  try {
    const reply = await $backend("payment", "mgmt_email_prs", {
      token: token.value
    })
  }
  catch (error) {
    console.error('getting paymentrequests', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Getting payment requests failed')
    }
    return
  }
  finally {
    showLoading(false)
  }
  await getPaymentRequests()
}

async function send_pr(item) {
  showLoading(true)
  try {
    const reply = await $backend("payment", "mgmt_email_pr", {
      token: token.value,
      id: item.id,
    })
  }
  catch (error) {
    console.error('getting paymentrequests', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Getting payment requests failed')
    }
    return
  }
  finally {
    showLoading(false)
  }
  await getPaymentRequests()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getPaymentRequests()
})

</script>


<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Payment Requests 2025</h1>
    <v-data-table :headers="headers" :items="prqs" class="elevation-1" :sort-by="['name']"
      :search="search" :items-per-page-options="[50, 150, -1]" items-per-page="50">
      <template #top>
        <v-card color="grey-lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field v-model="search" label="Search" class="mx-4" append-icon="mdi-magnify"
                hide_details />
              <v-spacer />
              <v-tooltip bottom>
                <template #activator="{ on }">
                  <v-btn fab outlined color="deep-purple" v-on="on" @click="send_prs()">
                    <v-icon>mdi-send</v-icon>
                  </v-btn>
                </template>
                Send virgin payment requests
              </v-tooltip>
              &nbsp;
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
      <template #item.action="{ item }">
        <v-tooltip location="bottom">
          Linked object
          <template #activator="{ props }">
            <v-icon small class="mr-2" v-bind="props" @click="gotoLinked(item)">
              mdi-link
            </v-icon>
          </template>
        </v-tooltip>
        <v-tooltip location="bottom">
          Send
          <template #activator="{ props }">
            <v-icon small class="mr-2" v-bind="props" @click="send_pr(item)">
              mdi-send
            </v-icon>
          </template>
        </v-tooltip>
        <v-tooltip location="bottom">
          Edit
          <template #activator="{ props }">
            <v-icon small class="mr-2" v-bind="props" @click="editPaymentRequest(item)">
              mdi-pencil
            </v-icon>
          </template>
        </v-tooltip>
      </template>
      <template #no-data>
        No paymentrequests found.
      </template>
    </v-data-table>
  </v-container>
</template>


<style>
.lightgreyrow {
  color: #ddd;
}
</style>
