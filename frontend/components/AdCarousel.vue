<script setup>
import { ref } from 'vue'

const current = ref(0)
const interval = 6
const items = [
  { src: '/img/frame_archery.png', name: 'archery' },
  { src: '/img/frame_chessconsult.png', name: 'chessconsult' },
  { src: '/img/frame_talistro.png', name: 'talistro' },
  { src: '/img/frame_chronos.png', name: 'chronos' },
  { src: '/img/frame_tusk.png', name: 'tusk' },
]

function setupCarousel() {
  let secCarousel = Math.floor((new Date() / 1000) % (
    interval * items.length));
  current.value = Math.floor(secCarousel / items.length);
  if (current.value == items.length) current.value = 0;
}

onMounted(() => setupCarousel())
</script>

<template>
  <div>
    <v-card class="my-2 mx-auto" max-width="400">
      <v-card-title>Gold Sponsor:</v-card-title>
      <v-card-text>
        <a href="http://www.truegen.be" target="_blank">
          <img src='/img/frame_truegen.png'>
        </a>
      </v-card-text>
    </v-card>
    <v-carousel :show-arrows="false" hide-delimiters :value="current" height="170"
      class="adcarousel mb-2" :interval="interval * 1000" cycle continuous>
      <v-carousel-item v-for="item in items" :key="item.name" :src="item.src">
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<script>
export default {

  mounted() {

  }
}
</script>

<style scoped>
.adcarousel.v-carousel {
  width: 360px;
  max-width: 95%;
  margin-left: auto;
  margin-right: auto;
}
</style>
