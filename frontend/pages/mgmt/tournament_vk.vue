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
const trn_experts = ref({
  name: "vkexpert.json"
})
const trn_open = ref({
  name: "vkopen.json"
})
const trn_seniors = ref({
  name: "vksenior.json"
})

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

async function handleFile(event) {
  console.log("event", event)
  const reader = new FileReader()
  // reader.onload = (event) => {
  //   trn.content = event.target.result
  // }
  reader.readAsDataURL(event[0])
}

async function upload_trn(t) {
  let reply
  console.log("uploading ", t)
  showLoading(true)
  try {
    reply = await $backend("tournament", "mgmt_upload_json", {
      token: token.value,
      trn: {
        name: trn.fname,
        jsoncontent: trn.jsoncontent,
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
    <h1>Upload JSON files VK2024</h1>
    <h3>Experts</h3>
    <v-file-input label="Badge" v-model="trn_experts.file" @update:modelValue="handleFile" />
    <v-btn @click="upload_trn(trn_experts)">Upload</v-btn>

  </v-container>
</template>