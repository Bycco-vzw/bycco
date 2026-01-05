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

definePageMeta({
  layout: "mgmt",
})

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

async function download_registrations() {
  let reply, xls
  showLoading(true)
  try {
    reply = await $backend("registration", "mgmt_xls_registrations", {
      token: token.value,
    })
    console.log("xls reply", reply)
    xls = reply.data.xls64
  } catch (error) {
    console.log("download error", error)
    showSnackbar("Download error: " + error.detail)
  } finally {
    showLoading(false)
  }
  const link = document.createElement("a")
  link.download = "registrations_bjk26.xlsx"
  link.href = "data:application/excel;base64," + xls
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  showSnackbar("Downloading registrations successful")
}

async function download_participants() {
  let reply, xls
  showLoading(true)
  try {
    reply = await $backend("participant", "mgmt_xls_participants", {
      token: token.value,
    })
    console.log("xls reply", reply)
    xls = reply.data.xls64
  } catch (error) {
    console.log("download error", error)
    showSnackbar("Download error: " + error.detail)
  } finally {
    showLoading(false)
  }
  const link = document.createElement("a")
  link.download = "participants_bjk26.xlsx"
  link.href = "data:application/excel;base64," + xls
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  showSnackbar("Downloading participants successful")
}


onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Downloads BJK 2026</h1>
    <h3>Registrations</h3>
    <v-btn @click="download_registrations">Download registrations</v-btn>
    <h3>Participants</h3>
    <v-btn @click="download_participants">Download participants</v-btn>

  </v-container>
</template>
