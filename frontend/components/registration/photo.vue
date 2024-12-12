<script setup>
import { ref, computed } from "vue"
import { useI18n } from "vue-i18n"
import VueCropper from "vue-cropperjs"
import "cropperjs/dist/cropper.css"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"

// communication
const emit = defineEmits(["changeStep", "updateRegistration"])
defineExpose({ setup })
const { $backend } = useNuxtApp()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// i18n
const { t } = useI18n()

// datamodel member
const first_name = ref("")
const last_name = ref("")
const idsub = ref("")
const photo = ref(null)
const photosrc = ref(null)

// datamodel the rest
const step = 4
async function uploadPhoto() {
  let reply
  showLoading(true)
  photo.value = photosrc.value.getCroppedCanvas({ width: 160 }).toDataURL()
  console.log("uploading idsub", idsub, idsub.value)
  try {
    reply = await $backend("registration", "upload_photo", {
      photo: photo.value,
      idsub: idsub.value,
    })
    emit("changeStep", step + 1)
  } catch (error) {
    showSnackbar(error.message)
  } finally {
    showLoading(false)
  }
}

function handleFile(event) {
  const reader = new FileReader()
  reader.onload = (event) => {
    photosrc.value.replace(event.target.result)
  }
  console.log("file", event)
  reader.readAsDataURL(event)
}

function next() {
  uploadPhoto()
}

function prev() {
  emit("changeStep", step - 1)
}

function setup(e) {
  console.log("setup photo1", e.first_name)
  first_name.value = e.first_name
  last_name.value = e.last_name
  idsub.value = e.idsub
}

function tValidator(f) {
  // returns a new function that translates the outcome of a validator
  function tf(v) {
    let s = f(v)
    if (typeof s === "string" || s instanceof String) {
      return t(s)
    } else {
      return s
    }
  }
  return tf
}

function updateRegistration() {
  emit("updateRegistration", {})
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
})
</script>
<template>
  <v-form>
    <v-container>
      <SnackbarMessage ref="refsnackbar" />
      <ProgressLoading ref="refloading" />
      <h2>{{ $t("Photo") }}</h2>
      <div class="my-2">{{ $t("enroll.pho_browse") }}</div>
      <v-file-input label="Badge" v-model="photo" @update:modelValue="handleFile" />
      <div>{{ $t("enroll.pho_crop") }}</div>
      <vue-cropper
        ref="photosrc"
        :view-mode="2"
        drag-mode="crop"
        :auto-crop-area="0.5"
        :background="true"
        src=""
        alt=" "
        :aspect-ratio="0.8"
        preview="#photoresult"
        :img-style="{ height: '400px' }"
      />
      <h4 class="mt-2">{{ $t("enroll.pho_result") }}</h4>
      <div id="photoresult" ref="photoresult" class="photoresult" />
      <div class="mt-2">
        <v-btn class="ml-2" @click="prev" color="primary">
          {{ $t("Back") }}
        </v-btn>
        <v-btn class="ml-2" color="primary" @click="next">
          {{ $t("Continue") }}
        </v-btn>
      </div>
    </v-container>
  </v-form>
</template>

<style>
.dropbox {
  width: 100%;
  background-color: aliceblue;
}

.photosrc {
  overflow: hidden;
  width: 100%;
  height: 400px;
  border: 1px dashed #808080;
  background-color: #d3d3d3;
}

.photoresult {
  overflow: hidden;
  position: relative;
  text-align: center;
  width: 160px;
  height: 200px;
}
</style>
