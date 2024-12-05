<script setup>
import { ref } from "vue"
import { parse } from "yaml"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()
const router = useRouter()
const route = useRoute()

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
const idregistration = route.query.id
const reg = ref({ payment_id: "" })

definePageMeta({
  layout: "mgmt",
})

function back() {
  router.go(-1)
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

async function create_pr() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("payment", "mgmt_create_registration_pr", {
      id: idregistration,
      token: token.value,
    })
  } catch (error) {
    console.error("creating payment request", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Creating paymentrequesr failed: " + error.detail)
    }
    return
  } finally {
    showLoading(false)
  }
  router.push("/mgmt/paymentrequest_edit?id=" + reply.data)
}

async function delete_pr() {
  let reply
  if (confirm("Are you sure to delete the linked payment request")) {
    showLoading(true)
    try {
      reply = await $backend("payment", "mgmt_delete_stay_pr", {
        id: idregistration,
        token: token.value,
      })
    } catch (error) {
      console.error("deleting linked payment request", error)
      if (error.code === 401) {
        router.push("/mgmt")
      } else {
        showSnackbar("Deleting Paymentrequest failed" + error.detail)
      }
      return
    } finally {
      showLoading(false)
    }
    await getRegistration()
  }
}

async function getRegistration() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("registration", "mgmt_get_registration", {
      id: idregistration,
      token: token.value,
    })
    readRegistration(reply.data)
  } catch (error) {
    console.error("getting registration failed", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Getting registration failed")
    }
  } finally {
    showLoading(false)
  }
}

async function gotoPaymentrequest(id) {
  console.log("going to payment request", id)
  router.push("/mgmt/paymentrequest_edit?id=" + id)
}

function readRegistration(registration) {
  reg.value = { ...registration }
}

async function saveRegistration() {
  let reply
  showLoading(true)
  try {
    await $backend("stay", "mgmt_update_registration", {
      id: idregistration,
      registration: {
        address: reg.value.address,
        bycco_remarks: reg.value.bycco_remarks,
        checkindate: reg.value.checkindate,
        checkoutdate: reg.value.checkoutdate,
        email: reg.value.email,
        enabled: reg.value.enabled,
        first_name: reg.value.first_name,
        last_name: reg.value.last_name,
        locale: reg.value.locale,
        stay: reg.value.stay,
        meals: reg.value.meals,
        mobile: reg.value.mobile,
        organizers: reg.value.organizers,
        remarks: reg.value.remarks,
      },
      token: token.value,
    })
  } catch (error) {
    console.error("getting getRegistrations", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Saving registration failed: " + error.detail)
    }
    return
  } finally {
    showLoading(false)
  }
  console.log("save successful")
  showSnackbar("Registration saved")
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getRegistration()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />

    <v-row class="my-2">
      <h2>
        Edit Registration {{ reg.number }}: {{ reg.last_name }} {{ reg.first_name }}
      </h2>
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
      <v-card-title> Properties </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="reg.last_name" label="Last name" />
            <v-text-field v-model="reg.first_name" label="First name" />
            <v-textarea v-model="reg.address" label="Address" />
            <v-textarea v-model="reg.bycco_remarks" label="Remarks from Bycco" />
            <v-text-field v-model="reg.checkindate" label="Checkin Date" />
            <v-text-field v-model="reg.checkoutdate" label="Checkout Date" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-switch v-model="reg.enabled" label="Enabled" color="deep-purple" />
            <p>Registration created: {{ reg._creationtime }}</p>
            <p>Registration modified: {{ reg._modificationtime }}</p>
            <v-text-field v-model="reg.email" label="E-mail" />
            <v-text-field v-model="reg.mobile" label="Mobile" />
            <v-textarea v-model="reg.remarks" label="Customer Remarks" />
            <v-text-field v-model="reg.locale" label="Language" />
            <v-text-field v-model="reg.stay" label="Requested accomodation" />
            <v-text-field v-model="reg.meals" label="Requested meals" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="saveRegistration"> Save </v-btn>
      </v-card-actions>
    </v-card>

    <v-card>
      <v-card-title class="mt-2"> Payment Request </v-card-title>
      <v-card-actions>
        <v-btn v-if="!reg.payment_id" @click="create_pr"> Create </v-btn>
        <v-btn v-if="reg.payment_id" @click="gotoPaymentrequest(reg.payment_id)">
          Show
        </v-btn>
        <v-btn v-if="reg.payment_id" @click="delete_pr"> Delete </v-btn>
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
