<script setup>
import { ref } from "vue"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
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
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

// datamodel
const participants = ref([])
const search = ref("")
const headers = [
  { title: "Last Name", value: "last_name", sortable: true },
  { title: "First Name", value: "first_name", sortable: true },
  { title: "Category", value: "category", sortable: true },
  { title: "ID Bel", value: "idbel" },
  { title: "ID Fide", value: "idfide" },
  { title: "Elo BEL", value: "ratingbel", sortable: true },
  { title: "Elo FIDE", value: "ratingfide", sortable: true },
  { title: "Actions", value: "action" },
]
const idbel = ref("")
const category = ref("U8")
const showAddParticipant = ref(false)

definePageMeta({
  layout: "mgmt",
})

function addParticipant() {
  showAddParticipant.value = true
}

async function checkAuth() {
  console.log("checking if auth is already set", token.value)
  if (token.value) return
  if (person.value.credentials.length === 0) {
    router.push("/mgmt")
    return
  }
  if (!person.value.email.endsWith("@bycco.be")) {
    router.push("/mgmt")
    return
  }
  let reply
  showLoading(true)
  // now login using the Google auth token
  try {
    reply = await $backend("accounts", "login", {
      logintype: "google",
      token: person.value.credentials,
      username: null,
      password: null,
    })
  } catch (error) {
    console.log("cannot login", error)
    router.push("/mgmt")
    return
  } finally {
    showLoading(false)
  }
  console.log("mgmttoken received", reply.data)
  mgmtstore.updateToken(reply.data)
}

async function doAddParticipant() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("participant", "mgmt_add_participant_bjk", {
      token: token.value,
      idbel: idbel.value,
      cat: category.value,
    })
    showAddParticipant.value = false
    showSnackbar("Participant added")
  } catch (error) {
    console.error("adding participant failed", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Adding participant failed: " + error.detail)
    }
    return
  } finally {
    showLoading(false)
  }
  await getParticipants()
}

async function create_prs() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("payment", "mgmt_create_participants_bjk_pr", {
      token: token.value,
    })
  } catch (error) {
    console.error("creating all pr failed", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Creating paymentrequests failed: " + error.detail)
    }
    return
  } finally {
    showLoading(false)
  }
  await getParticipants()
}

function editParticipant(item) {
  router.push("/mgmt/participant_edit?id=" + item.id)
}

async function getParticipants() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("participant", "get_participants_bjk", {})
    participants.value = reply.data
  } catch (error) {
    console.error("getting participants failed", error)
    showSnackbar("Getting participants failed")
    return
  } finally {
    showLoading(false)
  }
}

function gotoPaymentRequest(item) {
  router.push("/mgmt/paymentrequest_edit?id=" + item.payment_id)
}

async function importEnrollments() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("participant", "mgmt_import_enrollments_bjk", {
      token: token.value,
    })
  } catch (error) {
    console.log("import error", error)
    if (error.code == 401) {
      router.push("/mgmt")
      return
    }
    showSnackbar("Failed to import enrollments: " + error.detail)
  } finally {
    showLoading(false)
  }
}

function lightgreyRow(item) {
  if (!item.enabled) {
    return "lightgreyrow"
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
    <h1>Management Particpants BJK2025</h1>
    <div v-if="showAddParticipant" class="mb-3">
      <h4>Adding a participant</h4>
      <v-text-field label="ID BEL" v-model="idbel" />
      <v-text-field label="Category" v-model="category" />
      <v-btn @click="doAddParticipant">Add</v-btn>
    </div>
    <v-data-table
      :headers="headers"
      :items="participants"
      :item-class="lightgreyRow"
      :items-per-page-options="[150, -1]"
      items-per-page="150"
      class="elevation-1"
      :sort-by="[{ key: 'last_name', order: 'asc' }]"
      :search="search"
    >
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
      <template #top>
        <v-card color="bg-grey-lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field
                v-model="search"
                label="Search"
                class="mx-4"
                append-icon="mdi-magnify"
                hide_details
              />
              <v-spacer />
              <v-tooltip location="bottom">
                Import Registrations
                <template #activator="{ props }">
                  <v-btn
                    fab
                    outlined
                    color="deep-purple-lighten-1"
                    v-bind="props"
                    @click="importEnrollments()"
                  >
                    <v-icon>mdi-import</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              &nbsp;
              <v-tooltip location="bottom">
                Create payment requests
                <template #activator="{ props }">
                  <v-btn
                    fab
                    outlined
                    color="deep-purple-lighten-1"
                    v-bind="props"
                    @click="create_prs()"
                  >
                    <v-icon>mdi-currency-eur</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              &nbsp;
              <v-tooltip location="bottom">
                Add participant
                <template #activator="{ props }">
                  <v-btn
                    fab
                    outlined
                    color="deep-purple-lighten-1"
                    v-bind="props"
                    @click="addParticipant()"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              &nbsp;
              <v-tooltip location="bottom">
                Refresh
                <template #activator="{ props }">
                  <v-btn
                    fab
                    outlined
                    color="deep-purple-lighten-1"
                    v-bind="props"
                    @click="refresh()"
                  >
                    <v-icon>mdi-refresh</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </v-row>
          </v-card-title>
        </v-card>
      </template>
      <template #item.payment_id="{ item }">
        <NuxtLink
          v-if="item.payment_id"
          :to="'/mgmt/paymentrequestedit?id=' + item.payment_id"
        >
          link
        </NuxtLink>
      </template>
      <template #item.action="{ item }">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon small class="mr-2" v-on="on" @click="editParticipant(item)">
              mdi-pencil
            </v-icon>
          </template>
          Edit Participant
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
      <template #no-data> No participants found. </template>
    </v-data-table>
  </v-container>
</template>

<style scoped>
.disabled {
  color: rgb(186, 185, 185);
}
</style>
