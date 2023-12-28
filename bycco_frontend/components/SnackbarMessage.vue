<script setup>
import { VSnackbar, VBtn } from 'vuetify/components';
const errortext = ref("")
const visible = ref(false)
function showSnackbar(txt){
  errortext.value = txt
  visible.value = true
}
function hideSnackbar(){
  visible.value = false
}
defineExpose({showSnackbar})
</script>
<template>
  <VSnackbar v-model="visible" timeout="6000">
    {{ errortext }}
    <template v-slot:actions>
      <VBtn color="green-lighten-2" variant="text" @click="hideSnackbar" icon="mdi-close" />
    </template>
  </VSnackbar> 
</template>
