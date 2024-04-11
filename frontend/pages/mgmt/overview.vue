<script setup>
import { onMounted } from 'vue'
import { usePersonStore } from "@/store/person";
import { storeToRefs } from "pinia";


const config = useRuntimeConfig()
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

let checkinlaunched = false
let checkinsuccess = false

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

async function checkin() {
  checkinlaunched = true
  const data = {
    user: person.value.user,
    email: person.value.email,
    branch: config.public.repo_branch,
  }
  let reply = await fetch(config.public.statamic_url + '/python/checkin', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  checkinlaunched = false
  checkinsuccess = true
}

async function checkout() {
  checkoutlaunched = true
  const data = {
    user: person.value.user,
    email: person.value.email,
    branch: config.public.repo_branch,
  }
  const reply = await fetch(config.public.statamic_url + '/python/checkout', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  checkoutlaunched = false
  checkoutsuccess = true
}

function openCollections() {
  const stUrl = config.public.statamic_url
  window.open(`${stUrl}/cp/collections`, '_statamic')
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
