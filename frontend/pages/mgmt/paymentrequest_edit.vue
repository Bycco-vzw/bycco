<script setup>
import { ref } from 'vue'
import { parse } from 'yaml'
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
const assignment = ref({ roomtype: '', roomnumber: '' })
const dialogDelete = ref(false)
const idpaymentrequest = route.query.id
const newguest = ref({})
const period = ref({})
const roomtypes = ref([])
const roomnumbers = ref([])
const prq = ref({})

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

async function email() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("payment", "mgmt_email_pr", {
      id: idpaymentrequest,
      token: mgmttoken.value,
    })
  }
  catch (error) {
    console.error('email payment request failed', error)
    if (error.code == 401) {
      router.push('/mgmt')
    } else {
      showSnackbar('Email payment request failed: ' + error.detail)
    }
    return
  }
  finally {

  }
  await get_paymentrequest()
}

async function get_paymentrequest() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('payment', "mgmt_get_paymentrequest", {
      id: idpaymentrequest,
      token: mgmttoken.value
    })
    prq.value = reply.data
    prq.value.totalprice = prq.value.totalprice.toFixed(2)
  }
  catch (error) {
    console.error('getting payment request failed', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Getting paymentrequest failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
}

async function registerPayment() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("payment", "mgmt_update_lodging_pr", {
      id: idpaymentrequest,
      prq: {
        remarks: prq.value.remarks,
        paystatus: prq.value.paystatus,
        paydate: (new Date()).toISOString().substring(0, 10),
      },
      token: mgmttoken.value,
    })
    showSnackbar("Payment registered")
  }
  catch (error) {
    console.error('register payment failed', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Registering payment failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  await get_paymentrequest()
}

async function saveProperties() {
  let reply
  showLoading(true)
  try {
    switch (prq.value.reason) {
      case "lodging":
        reply = await $backend("payment", "mgmt_update_lodging_pr", {
          id: idpaymentrequest,
          prq: {
            address: prq.value.address,
            bycco_remarks: prq.value.bycco_remarks,
            checkindate: prq.value.checkindate,
            checkoutdate: prq.value.checkoutdate,
            email: prq.value.email,
            enabled: prq.value.enabled,
            first_name: prq.value.first_name,
            last_name: prq.value.last_name,
            locale: prq.value.locale,
            lodging: prq.value.lodging,
            meals: prq.value.meals,
            mobile: prq.value.mobile,
            organizers: prq.value.organizers,
            remarks: prq.value.remarks,
            reductionamount: prq.value.reductionamount,
            reductionpct: prq.value.reductionpct
          },
          token: mgmttoken.value,
        })
        break
      case "bjk2024":
        console.log("updating pr bjk2024")
        reply = await $backend("payment", "mgmt_update_participant_bjk_pr", {
          id: idpaymentrequest,
          prq: {
            address: prq.value.address,
            email: prq.value.email,
            enabled: prq.value.enabled,
            first_name: prq.value.first_name,
            last_name: prq.value.last_name,
            locale: prq.value.locale,
          },
          token: mgmttoken.value,
        })
        break
    }
    showSnackbar("PR saved")
  }
  catch (error) {
    console.error('saving pr failed', error)
    if (error.code === 401) {
      router.push('/mgmt')
    }
    else {
      showSnackbar('Saving pr failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  await get_paymentrequest()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await get_paymentrequest()
})

</script>

<template>
  <v-container>

    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />

    <v-row>
      <h2>Payment request {{ prq.number }}: {{ prq.last_name }} {{ prq.first_name }}</h2>
      <v-spacer />
      <v-tooltip bottom>
        <template #activator="{ on }">
          <v-btn slot="activator" outlined fab color="deep-purple" v-on="on" @click="back()">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template #activator="{ on }">
          <v-btn slot="activator" outlined fab color="deep-purple" v-on="on" @click="email()">
            <v-icon>mdi-email</v-icon>
          </v-btn>
        </template>
        <span>Email</span>
      </v-tooltip>
    </v-row>
    <v-card class="my-3">
      <v-card-title>
        Register payment
      </v-card-title>
      <v-card-text>
        <v-switch v-model="prq.paystatus" label="Paid" color="deep-purple" />
        <v-textarea v-model="prq.remarks" rows="2" label="Remarks" />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="registerPayment">
          Register Payment
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="my-3">
      <v-card-title>
        Properties
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <p>Reason: {{ prq.reason }}</p>
            <p>Email sent: {{ prq.sentdate }}</p>
            <v-text-field v-model="prq.last_name" label="Last name" />
            <v-text-field v-model="prq.first_name" label="First name" />
            <v-textarea v-model="prq.address" label="Address" />
          </v-col>
          <v-col cols="12" sm="6">
            <p>Total cost: <b>{{ prq.totalprice }} €</b></p>
            <p v-if="prq.reason == 'lodging'">Guests: {{ prq.guests }}</p>
            <v-text-field v-model="prq.email" label="E-mail" />
            <v-text-field v-model="prq.locale" label="Language" />
            <v-text-field v-model="prq.reductionamount" label="Reduction fixed amount" />
            <v-text-field v-model="prq.reductionpct" label="Reduction pct" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="saveProperties">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="my-3">
      <v-card-title>Details</v-card-title>
      <v-card-text>
        <v-row v-for="(d, ix) in prq.details" :key="ix" class="mt-2">
          <v-col cols="2" sm="2" md="1">
            {{ ix + 1 }}
          </v-col>
          <v-col cols="10" sm="10" md="5">
            {{ d.description }}
          </v-col>
          <v-col cols="4" sm="4" md="2" class="text-right">
            {{ d.unitprice }} {{ d.unitprice ? "€" : "" }}
          </v-col>
          <v-col cols="4" sm="4" md="2" class="text-right">
            {{ d.quantity }}
          </v-col>
          <v-col cols="4" sm="4" md="2" class="text-right">
            {{ d.totalprice }} €
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions />
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
