<script setup>
import { ref } from 'vue'
const drawer = ref(false)
</script>


<template>
  <v-app>
    <v-navigation-drawer v-cloak v-model="drawer" app class="bg-blue-grey-darken-1 text white">
      <TheSidebar />
    </v-navigation-drawer>
    <v-app-bar color="blue-grey-darken-1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title>
        Bycco
      </v-app-bar-title>
    </v-app-bar>
    <v-main>
      <slot />
      <hr />
      <!-- <TheCarousel />>  -->
    </v-main>

    <TheFooter />
  </v-app>
</template>
  
<style scoped>
a {
  text-decoration: none;
  color: black;
}

a.copyright {
  color: white;
}

a:link,
a:hover {
  text-decoration: none;
}

a:hover {
  font-weight: 700;
}

footer div {
  margin: auto;
}

.footer2 {
  margin-bottom: 50px;
}
</style>
