<script setup>
import { onMounted } from 'vue'
import { usePersonStore } from "@/store/person";
import { storeToRefs } from "pinia";


const config = useRuntimeConfig()
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

definePageMeta({
  layout: "mgmt",
})

useHead({
  title: 'Management Overview',
})


function checkAuth() {
  if (person.value.credentials.length === 0) {
    navigateTo('/mgmt')
  }
  if (!person.value.email.endsWith('@bycco.be')) {
    navigateTo('/mgmt')
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
      <li>Managing the <NuxtLink to="/mgmt/reservations">Reservations</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/pages">Pages</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/paymentrequests">Payment Requests</NuxtLink>
      </li>
    </ul>
    <h3>VK 2024</h3>
    <ul>
      <li>Managing the <NuxtLink to="/mgmt/enrollments_vk">Enrollments VK2024</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/participants_vk">Participants VK2024</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/tournament_vk">Tournaments VK 2024</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/attendee_vk">Attendees VK 2024</NuxtLink>
      </li>
    </ul>
    <h3>BJK 2024</h3>
    <ul>
      <li>Managing the <NuxtLink to="/mgmt/enrollments_bjk">Enrollments BJK2024</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/participants_bjk">Participants BJK2024</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/tournament_bjk">Tournaments BJK 2024</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/attendee_bjk">Attendees BJK 2024</NuxtLink>
      </li>
    </ul>
  </v-container>
</template>
