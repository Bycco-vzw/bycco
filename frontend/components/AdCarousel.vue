<script setup>
import { ref } from "vue"

const current = ref(0)
const interval = 6
const items = [
  { src: "/img/frame_archery.png", name: "archery" },
  { src: "/img/frame_chessconsult.png", name: "chessconsult" },
  { src: "/img/frame_talistro.png", name: "talistro" },
  { src: "/img/frame_chronos.png", name: "chronos" },
  { src: "/img/frame_cvwarehouse.png", name: "cvwarehouse" },
  { src: "/img/frame_dgt.png", name: "dgt" },
  { src: "/img/frame_floreal.png", name: "floreal" },
  { src: "/img/frame_standaardboekhandel.png", name: "standaardboekhandel" },
  { src: "/img/frame_thinkerspublishing.png", name: "thinkerspublishing" },
]

function setupCarousel() {
  let secCarousel = Math.floor((new Date() / 1000) % (interval * items.length))
  current.value = Math.floor(secCarousel / items.length)
  if (current.value == items.length) current.value = 0
}

onMounted(() => setupCarousel())
</script>

<template>
  <div class="my-2">
    <v-carousel
      :show-arrows="false"
      hide-delimiters
      :value="current"
      height="170"
      class="adcarousel mb-2"
      :interval="interval * 1000"
      cycle
      continuous
    >
      <v-carousel-item v-for="item in items" :key="item.name" :src="item.src">
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<style scoped>
.adcarousel.v-carousel {
  width: 360px;
  max-width: 95%;
  margin-left: auto;
  margin-right: auto;
}
</style>
