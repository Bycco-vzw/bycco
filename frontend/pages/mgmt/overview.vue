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
  // we need google script to load because we might redirect internally
  // to index in case we fail the authentication
  script: [
    { src: 'https://accounts.google.com/gsi/client', async: true, defer: true }
  ]
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
      <li>Managing the <NuxtLink to="/mgmt/paymentrequests">Payment Requests</NuxtLink>
      </li>
    </ul>
  </v-container>
</template>

