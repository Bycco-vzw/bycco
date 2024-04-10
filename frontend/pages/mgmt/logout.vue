<script setup>
import { usePersonStore } from "@/store/person"
import { useMgmtTokenStore } from "@/store/mgmttoken"

const personstore = usePersonStore();
const mgmttokenstore = useMgmtTokenStore()

useHead({
  title: 'Management Logout',
})

definePageMeta({
  layout: 'mgmt',
})

function logout() {
  personstore.updatePerson({
    credentials: "",
    user: "",
    email: "",
  })
  mgmttokenstore.updateToken(null)
  document.cookie = `g_state=;path=/;expires=Thu, 01 Jan 1970 00:00:01 GMT`;
  navigateTo('/mgmt')
}

</script>
<template>
  <v-container>
    <h1>Logout</h1>
    <VBtn @click="logout">Logout</VBtn>
  </v-container>
</template>