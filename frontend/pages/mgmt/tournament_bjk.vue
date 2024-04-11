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
const trn_u8 = ref({
  name: "bjk_u8.json"
})
const trn_u10 = ref({
  name: "bjk_u10.json"
})
const trn_u12 = ref({
  name: "bjk_u12.json"
})
const trn_u14 = ref({
  name: "bjk_u14.json"
})
const trn_u16 = ref({
  name: "bjk_u16.json"
})
const trn_u18 = ref({
  name: "bjk_u18.json"
})
const trn_u20 = ref({
  name: "bjk_u20.json"
})
let activetrn = null


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

function upload_trn(t) {
  activetrn = t
  const reader = new FileReader()
  reader.onload = async (event) => {
    activetrn.jsoncontent = event.target.result
    await uploading()
  }
  reader.readAsDataURL(t.file[0])
}

async function uploading() {
  showLoading(true)
  try {
    const reply = await $backend("tournament", "mgmt_upload_json", {
      token: token.value,
      trn: {
        name: activetrn.name,
        jsoncontent: activetrn.jsoncontent,
      }
    })
  }
  catch (error) {
    console.error('uploading json failed', error)
    if (error.code === 401) {
      router.push('/mgmt')
    } else {
      showSnackbar('Uploading json file failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
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
    <h1>Upload JSON files BJK2024</h1>
    <h3>U8</h3>
    <v-file-input label="Json file" v-model="trn_u8.file" />
    <v-btn @click="upload_trn(trn_u8)">Upload</v-btn>
    <h3>U10</h3>
    <v-file-input label="Json file" v-model="trn_u10.file" />
    <v-btn @click="upload_trn(trn_u10)">Upload</v-btn>
    <h3>U12</h3>
    <v-file-input label="Json file" v-model="trn_u12.file" />
    <v-btn @click="upload_trn(trn_u12)">Upload</v-btn>
    <h3>U14</h3>
    <v-file-input label="Json file" v-model="trn_u14.file" />
    <v-btn @click="upload_trn(trn_u14)">Upload</v-btn>
    <h3>U16</h3>
    <v-file-input label="Json file" v-model="trn_u16.file" />
    <v-btn @click="upload_trn(trn_u16)">Upload</v-btn>
    <h3>U18</h3>
    <v-file-input label="Json file" v-model="trn_u18.file" />
    <v-btn @click="upload_trn(trn_u18)">Upload</v-btn>
    <h3>U20</h3>
    <v-file-input label="Json file" v-model="trn_u20.file" />
    <v-btn @click="upload_trn(trn_u20)">Upload</v-btn>


  </v-container>
</template>