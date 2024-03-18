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
const idparticipant = route.query.id
const par = ref({ payment_id: "" })

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


async function create_pr() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("payment", "mgmt_create_participantbjk_pr", {
      id: idparticipant,
      token: mgmttoken.value
    })
  }
  catch (error) {
    console.error('creating payment request', error)
    if (error.code === 401) {
      router.push('/mgmt')
    } else {
      showSnackbar('Creating paymentrequesr failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  router.push('/mgmt/paymentrequest_edit?id=' + reply.data)
}

async function delete_pr() {
  let reply
  if (confirm('Are you sure to delete the linked payment request')) {
    showLoading(true)
    try {
      reply = await $backend("payment", "mgmt_delete_participantbjk_pr", {
        id: idparticipant,
        token: mgmttoken.value
      })
    }
    catch (error) {
      console.error('deleting linked payment request', error)
      if (error.code === 401) {
        router.push('/mgmt')
      } else {
        showSnackbar('Deleting Paymentrequest failed' + error.detail)
      }
      return
    }
    finally {
      showLoading(false)
    }
    await getReservation()
  }
}

async function getParticipant() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('participant', "mgmt_get_participant_bjk", {
      id: idparticipant,
      token: mgmttoken.value
    })
    readParticipant(reply.data)
  }
  catch (error) {
    console.error('getting participant failed', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Getting participant failed')
    }
  }
  finally {
    showLoading(false)
  }
}

async function gotoPaymentrequest(id) {
  console.log('going to payment request', id)
  router.push('/mgmt/paymentrequest_edit?id=' + id)
}

function readParticipant(participant) {
  par.value = { ...participant }
}


async function saveParticipant() {
  let reply
  showLoading(true)
  try {
    await $backend("participant", "mgmt_update_participant_bjk", {
      id: idreservation,
      participant: {},
      token: mgmttoken.value
    })
  }
  catch (error) {
    console.error('getting getParticipant', error)
    if (error.code == 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Saving participant failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  console.log('save successful')
  showSnackbar('Participant saved')
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getParticipant()
})

</script>

<template>
  <v-container>

    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />

    <v-row class="my-2">
      <h2>Edit Participant {{ par.idbel }}: {{ par.last_name }} {{ par.first_name }}</h2>
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
            <v-text-field v-model="par.last_name" label="Last name" />
            <v-text-field v-model="par.first_name" label="First name" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="par.ratingbel" label="ELO BEL" />
            <v-text-field v-model="par.ratingfide" label="ELO FIDE" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="saveParticipant">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>


    <v-card>
      <v-card-title class="mt-2">
        Payment Request
      </v-card-title>
      <v-card-actions>
        <v-btn v-if="!par.payment_id" @click="create_pr">
          Create
        </v-btn>
        <v-btn v-if="par.payment_id" @click="gotoPaymentrequest(par.payment_id)">
          Show
        </v-btn>
        <v-btn v-if="par.payment_id" @click="delete_pr">
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>

  </v-container>
</template>

<style scoped>
.bordermd {
  border: 1px solid grey;
}

.v-input--checkbox {
  margin-top: 0;
}
</style>