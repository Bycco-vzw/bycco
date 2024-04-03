<script setup>
import { ref, onMounted } from 'vue'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'

import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person";
import { storeToRefs } from "pinia";

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
const { token } = storeToRefs(mgmtstore)
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

// model
let checkinlaunched = false
let checkinsuccess = false
const instance = ref("bycco1")

definePageMeta({
  layout: "mgmt",
})

useHead({
  title: 'Pages',
  // we need google script to load because we might redirect internally
  // to index in case we fail the authentication
  script: [
    { src: 'https://accounts.google.com/gsi/client', async: true, defer: true }
  ]
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
    console.log('failed login redirecting to /mgmt')
    mgmtstore.updateToken(null)
    router.push('/mgmt')
  }
  finally {
    showLoading(false)
  }
  mgmtstore.updateToken(reply.data)
}


async function checkin() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("page", "checkin", {
      instance: instance.value,
      token: token.value,
    })
  }
  catch (error) {
    console.error('failed', error)
    showSnackbar("Error while copying content to Statamic")
    // mgmtstore.updateToken(null)
    // router.push('/mgmt')
    return
  }
  finally {
    showLoading(false)
  }
  showSnackbar("Content copied to Statamic")
  mgmtstore.updateToken(reply.data)
}


async function checkout() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("page", "checkout", {
      instance: instance.value,
      token: token.value,
    })
  }
  catch (error) {
    console.error('failed', error)
    showSnackbar("Error while copying content to operational site")
    // mgmtstore.updateToken(null)
    // router.push('/mgmt')
    return
  }
  finally {
    showLoading(false)
  }
  showSnackbar("Content copied to operational site")
  mgmtstore.updateToken(reply.data)
}



function openPageCollection() {
  const hostname = "st1"
  window.open(`https://${hostname}.bycco.be/cp/collections/pages`, '_statamic')
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  checkAuth()
})
</script>


<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />

    <h1>Management Pages</h1>
    <p>Here you can modify the pages of the Bycco website</p>
    <p>We use a tool called Statamic</p>
    <p>In order to make changes to a page, you have the following steps</p>
    <ul>
      <li>Copy the content of the operational website to Statamic.</li>
      <v-btn variant="tonal" @click="checkin">copy</v-btn><br><br>
      <li>Open the Statamic tool (it opens in a separate browser tab/window)</li>
      <v-btn variant="tonal" @click="openPageCollection">open Statamic</v-btn><br><br>
      <li>Modify the pages in the statamic tool</li><br>
      <li>Close the Statamic tab/window </li><br>
      <li>Copy the modified content in Statamic to the operational site</li>
      <v-btn variant="tonal" @click="checkout">copy</v-btn><br><br>
    </ul>
    <br>
    <P>
      When opening the Statamic tool for the first time, you will need to provide a
      username + password.
    </P>
    <ul>
      <li><b>username:</b> info@bycco.be</li>
      <li><b>password:</b> jeugd2024</li>

    </ul>
  </v-container>
</template>
