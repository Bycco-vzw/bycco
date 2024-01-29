<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import vueFilePond from 'vue-filepond'
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.esm.js'
import 'filepond/dist/filepond.min.css'
import VueCropper from 'vue-cropperjs'
import 'cropperjs/dist/cropper.css';
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'

// communication
const emit = defineEmits(['changeStep', 'updateEnrollment'])
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

const FilePond = vueFilePond(FilePondPluginFileValidateType)

async function uploadPhoto() {
  let reply
  showLoading(true)
  photo.value = photosrc.value.getCroppedCanvas({ width: 160 }).toDataURL()
  try {
    reply = await $backend("enrollment", "upload_photo", {
      photo: photo.value,
      idsub: idsub.value
    })
    emit('changeStep', step + 1)
  }
  catch (error) {
    showSnackbar(error.message)
  }
  finally {
    showLoading(false)
  }
}

function handleFile(err, file) {
  if (err) {
    console.error('Nasty', err)
    showSnackbar('Error reading file')
    return
  }
  const reader = new FileReader()
  const self = this
  reader.onload = (event) => {
    photosrc.value.replace(event.target.result)
  }
  reader.readAsDataURL(file.file)
}



function next() {
  uploadPhoto()
}

function prev() {
  emit('changeStep', step - 1)
}

function setup(e) {
  console.log('setup photo', e)
  first_name.value = e.first_name
  last_name.value = e.last_name
  idsub.value = e.idsub
}



function tValidator(f) {
  // returns a new function that translates the outcome of a validator
  function tf(v) {
    let s = f(v)
    if (typeof (s) === "string" || s instanceof String) {
      return t(s)
    }
    else {
      return s
    }
  }
  return tf
}

function updateEnrollment() {
  emit('updateEnrollment', {

  })
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
      <v-row class="mt-2">
        <h2>{{ $t('Photo') }}</h2>
      </v-row>
      <v-row class="my-2">
        <div class="my-2">{{ $t('enrollvk.pho_upload') }}</div>
      </v-row>
      <v-row class="my-2">
        <v-col cols="12">
          <div class="my-2">{{ $t('enrollvk.pho_dragbrowse') }}</div>
        </v-col>
        <v-col cols="12">
          <file-pond ref="pond" accepted-file-types="image/jpeg, image/png" :label-idle="labelIdle"
            class-name="dropbox" @addfile="handleFile" />
        </v-col>
      </v-row>
      <v-row class="my-2">
        <v-col cols="12">
          <div>{{ $t('enrollvk.pho_crop') }}</div>
        </v-col>
        <vue-cropper ref="photosrc" :view-mode="2" drag-mode="crop" :auto-crop-area="0.5"
          :background="true" src="" alt=" " :aspect-ratio="0.8" preview="#photoresult"
          :img-style="{ height: '400px' }" />
      </v-row>
      <v-row class="my-2">
        <h4>{{ $t('enrollvk.pho_result') }}</h4>
      </v-row>
      <v-row class="my-2">
        <div id="photoresult" ref="photoresult" class="photoresult" />
      </v-row>
      <v-row class="mt-4">
        <div>
          <v-btn class="ml-2" @click="prev" color="primary">
            {{ $t('Back') }}
          </v-btn>
          <v-btn class="ml-2" color="primary" @click="next">
            {{ $t('Continue') }}
          </v-btn>
        </div>
      </v-row>
    </v-container>
  </v-form>
</template>

<style>
.dropbox {
  width: 100%;
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