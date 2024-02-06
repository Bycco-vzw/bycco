<script setup>
import { ref } from "vue";

const drawer = ref(false);

async function goto(section) {
  const url = `/mgmt/${section}`
  console.log('going to', url)
  navigateTo(url)
}
</script>

<template>
  <VApp>
    <VNavigationDrawer v-model="drawer" color="deep-purple darken-1" dark>
      <!-- <VToolbar title="Menu" color="deep-purple darken-3" dark /> -->
      <VList>
        <VListItem @click="goto('overview')" title="Overview" />
        <VListItem @click="goto('reservations')" title="Reservations" />
        <!-- <VListItem @click="goto('rooms')" title="Rooms" />
        <VListItem @click="goto('enrollments')" title="Enrollments" />
        <VListItem @click="goto('payments')" title="Payment Requests" />
        <VListItem @click="goto('attendees')" title="Attendees" /> -->
        <VListItem @click="goto('logout')" title="Logout" />
      </VList>
    </VNavigationDrawer>
    <VAppBar color="deep-purple darken-1" dark>
      <VAppBarNavIcon @click="drawer = !drawer" />
      <VAppBarTitle> Management Bycco </VAppBarTitle>
    </VAppBar>
    <VMain>
      <slot />
    </VMain>
  </VApp>
</template>
