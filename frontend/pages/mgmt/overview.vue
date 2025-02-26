<script setup>
import { onMounted } from "vue"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

const config = useRuntimeConfig()
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

definePageMeta({
  layout: "mgmt",
})

useHead({
  title: "Management Overview",
})

function checkAuth() {
  if (person.value.credentials.length === 0) {
    navigateTo("/mgmt")
  }
  if (!person.value.email.endsWith("@bycco.be")) {
    navigateTo("/mgmt")
  }
}

onMounted(() => {
  checkAuth()
})
</script>

<template>
  <v-container class="markdowncontent">
    <h1>Overview</h1>
    <ul>
      <li>
        Managing the
        <NuxtLink to="/mgmt/reservations">Reservations for stay Floreal 2025</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/pages">Pages</NuxtLink></li>
      <li>
        Managing the <NuxtLink to="/mgmt/paymentrequests">Payment Requests</NuxtLink>
      </li>
      <li>
        Managing the
        <NuxtLink to="/mgmt/registrations_bjk">Registrations BJK 2025</NuxtLink>
      </li>
      <li>
        Managing the <NuxtLink to="/mgmt/participants_bjk">Participants BJK2025</NuxtLink>
      </li>
      <li>
        Uploading <NuxtLink to="/mgmt/tournament">SWAR JSON files for BJK 2025</NuxtLink>
      </li>
      <li>
        Entering unofficial <NuxtLink to="/mgmt/u_results">results for BJK 2025</NuxtLink>
      </li>
      <li>
        Managing the <NuxtLink to="/mgmt/attendee_bjk">Attendees BJK 2025</NuxtLink>
      </li>
    </ul>
  </v-container>
</template>
