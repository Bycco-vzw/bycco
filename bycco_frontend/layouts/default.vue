<script setup>
import { ref } from 'vue'
// import TheSidebar from '@/components/TheSidebar.vue'
// import TheCarousel from '@/components/TheCarousel.vue'
// import TheFooter from '@/components/TheFooter.vue'
import TheTopbar from '@/components/TheTopbar.vue'
const drawer = ref(false)
</script>


<template>
  <v-app> 
    <!-- <v-navigation-drawer v-cloak v-model="drawer" app class="bg-blue-grey-darken-1 text white">
      <TheSidebar />
    </v-navigation-drawer> -->
    <TheTopbar />
    <v-main>
      <slot />
      <!-- <TheCarousel />>  -->
      <hr />
    </v-main>
    <v-footer>The Footer</v-footer>
    <!-- <TheFooter />        -->
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
