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
      <VToolbar title="BYCCO Mgmt" color="deep-purple darken-3" dark />
      <VList>
        <VListItem @click="goto('overview')" title="Overview" />
        <VListItem @click="goto('reservations')" title="Reservations" />
        <VListItem @click="goto('payments')" title="Payment Requests" />
        <VListItem @click="goto('enrollments_vk')" title="Enrollments VK2024" />
        <VListItem @click="goto('participants_vk')" title="Participants VK2024" />
        <VListItem @click="goto('enrollments_bjk')" title="Enrollments BJK2024" />
        <VListItem @click="goto('participants_bjk')" title="Participants BJK2024" />
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
