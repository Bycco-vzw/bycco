<script setup>
import { ref } from "vue"

const router = useRouter()
const drawer = ref(false);

async function goto(section) {
  const url = `/mgmt/${section}`
  router.push(url)
}

useHead({
  script: [
    { src: 'https://accounts.google.com/gsi/client', defer: true }
  ],
})


</script>
<script>
</script>
<template>
  <VApp>
    <VNavigationDrawer v-model="drawer" color="deep-purple darken-1" dark>
      <VToolbar title="BYCCO Mgmt" color="deep-purple darken-3" dark />
      <v-list>
        <v-list-item @click="goto('overview')" title="Overview" />
        <v-list-item @click="goto('pages')" title="Pages" />
        <v-list-item @click="goto('reservations')" title="Reservations" />
        <v-list-item @click="goto('paymentrequests')" title="Payment Requests" />
        <v-list-group no-action>
          <template #activator="{ props }">
            <v-list-item v-bind="props" title="VK 2024" />
          </template>
          <v-list-item @click="goto('enrollments_vk')" title="Enrollments" />
          <v-list-item @click="goto('participants_vk')" title="Participants" />
          <v-list-item @click="goto('tournament_vk')" title="Tournaments" />
          <v-list-item @click="goto('attendee_vk')" title="Attendees" />
        </v-list-group>
        <v-list-group no-action>
          <template #activator="{ props }">
            <v-list-item v-bind="props" title="BJK 2024" />
          </template>
          <v-list-item @click="goto('enrollments_bjk')" title="Enrollments" />
          <v-list-item @click="goto('participants_bjk')" title="Participants" />
          <v-list-item @click="goto('tournament_bjk')" title="Tournaments" />
          <v-list-item @click="goto('attendee_bjk')" title="Attendees" />
        </v-list-group>
        <v-list-item @click="goto('logout')" title="Logout" />
      </v-list>
    </VNavigationDrawer>
    <VAppBar color="deep-purple darken-1" dark>
      <VAppBarNavIcon @click="drawer = !drawer" />
      <VAppBarTitle>Management Bycco </VAppBarTitle>
    </VAppBar>
    <VMain>
      <slot />
    </VMain>
  </VApp>
</template>
