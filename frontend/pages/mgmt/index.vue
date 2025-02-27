<script setup>
import { ref, onMounted } from "vue"
import * as jose from "jose"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// stores
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

// model
const authenticated = ref(false)

// google one tap
useOneTap({
  onSuccess: (resp) => {
    console.log("Success:", resp)
    const payload = jose.decodeJwt(resp.credential)
    personstore.updatePerson({
      credentials: resp.credential,
      user: payload.name,
      email: payload.email,
    })
    authenticated.value = true
  },
  onError: () => console.error("Error with One Tap Login"),
})

useHead({
  title: "Management Login",
})

definePageMeta({
  layout: "mgmt",
})

</script>

<template>
  <VContainer>
    <p>Management Bycco</p>
    <div v-if="!authenticated">
      <p>Waiting for authorization</p>
    </div>
    <ul v-if="authenticated">
      <li>Managing the <NuxtLink to="/mgmt/pages">Pages</NuxtLink></li>
      <li>Managing the <NuxtLink to="/mgmt/reservations">Stay Reservations</NuxtLink></li>
      <li>
        Managing the <NuxtLink to="/mgmt/paymentrequests">Payment Requests</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/registrations">Registrations</NuxtLink></li>
      <li>Managing the <NuxtLink to="/mgmt/participants">Participants</NuxtLink></li>
      <li>Uploading the <NuxtLink to="/mgmt/upload_json">SWAR JSON Files</Nuxtlink></li>
      <li>Editing the <NuxtLink to="/mgmt/unofficial_results">Unofficial Results</Nuxtlink></li>
    </ul>
  </VContainer>
</template>
