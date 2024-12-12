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
const reg = ref({ representative: {}, payment_id: "" })

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
    reply = await $backend("registration", "mgmt_get_registration_bjk", {
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
    await $backend("registration", "mgmt_update_registration_bjk", {
      id: idregistration,
      reg: {
        first_name: reg.value.first_name,
        last_name: reg.value.last_name,
        idbel: reg.value.idbel,
        idfide: reg.value.idfide,
        category: reg.value.category,
        gender: reg.value.gender,
        birthyear: reg.value.birthyear,
        locale: reg.value.locale,
        confirmed: reg.value.confirmed,
        remarks: reg.value.remarks,
        enabled: reg.value.enabled,
        ratingbel: reg.value.ratingbel,
        ratingfide: reg.value.ratingfide,
        emailplayer: reg.value.emailplayer,
        mobileplayer: reg.value.mobileplayer,
        representative: {
          fullnameparent: reg.value.representative.fullnameparent,
          emailparent: reg.value.representative.emailparent,
          mobileparent: reg.value.representative.mobileparent,
          fullnameattendant: reg.value.representative.fullnameattendant,
          emailattendant: reg.value.representative.emailattendant,
          mobileattendant: reg.value.representative.mobileattendant,
        },
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
            <v-text-field v-model="reg.idbel" label="ID Bel" />
            <v-text-field v-model="reg.idfide" label="ID Fide" />
            <v-text-field v-model="reg.category" label="Category" />
            <v-text-field v-model="reg.gender" label="Gender" />
            <v-textarea v-model="reg.birthyear" label="Birthyear" />
            <v-text-field v-model="reg.locale" label="Locale" />
            <v-text-field v-model="reg.confirmed" label="Confirmed" />
            <v-textarea v-model="reg.remarks" label="Remarks from Bycco" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-switch v-model="reg.enabled" label="Enabled" color="deep-purple" />
            <v-text-field v-model="reg.ratingbel" label="Rating BEL" />
            <v-text-field v-model="reg.ratingfide" label="Rating FIDE" />
            <v-text-field v-model="reg.emailplayer" label="E-mail player" />
            <v-text-field v-model="reg.mobileplayer" label="Mobile player" />
            <v-text-field
              v-model="reg.representative.fullnameparent"
              label="Full name parent"
            />
            <v-text-field
              v-model="reg.representative.emailparent"
              label="E-mail parent"
            />
            <v-text-field v-model="reg.representative.mobileparent" label="GSM parent" />
            <v-text-field
              v-model="reg.representative.fullnameattendant"
              label="Full name attendant"
            />
            <v-text-field
              v-model="reg.representative.emailattendant"
              label="E-mail attendant"
            />
            <v-text-field
              v-model="reg.representative.mobileattendant"
              label="GSM attendant"
            />
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
