<script setup>
useHead({
  script: [{ src: "/js/redirect.js" }],
});
</script>

<template>
  <v-app>
    <v-main>
      <slot />
    </v-main>
  </v-app>
</template>
