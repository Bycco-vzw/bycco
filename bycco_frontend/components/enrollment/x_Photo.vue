<template>
  <div>
    <h2>{{ $t('Photo') }}</h2>
    <h4 class="mt-2">
      {{ $t('Select photo') }}
    </h4>
    <div>{{ $t('SubPhoto1') }}</div>
    <div class="my-1">
      <file-pond
        ref="pond"
        accepted-file-types="image/jpeg, image/png"
        :label-idle="labelIdle"
        class-name="dropbox"
        @addfile="handleFile"
      />
    </div>
    <div class="photosrc">
      <vue-cropper
        ref="photosrc"
        :view-mode="2"
        drag-mode="crop"
        :auto-crop-area="0.5"
        :background="true"
        src=""
        alt="Source Image"
        :aspect-ratio="0.8"
        preview="#photoresult"
        :img-style="{height: '400px'}"
      />
    </div>
    <h4 class="mt-2">
      {{ $t('Resulting photo') }}
    </h4>
    <div>{{ $t('SubPhoto3') }}</div>
    <div id="photoresult" ref="photoresult" class="photoresult" />
    <div class="mt-2">
      <v-btn color="primary" @click="doCrop">
        {{ $t('Continue') }}
      </v-btn>
      <v-btn @click="prev">
        {{ $t('Back') }}
      </v-btn>
    </div>
  </div>
</template>

<script>
import VueCropper from 'vue-cropperjs'
import vueFilePond from 'vue-filepond'
import 'cropperjs/dist/cropper.css'
import 'filepond/dist/filepond.min.css'

import { mapState } from 'vuex'

const FilePond = vueFilePond()

export default {

  components: {
    VueCropper,
    FilePond
  },

  computed: {
    labelIdle () {
      return '<span class="filepond--label-action">' + this.$t('SubPhoto2') + '</span>'
    },
    ...mapState({
      step: state => state.enrollment.step,
      enrollment: state => state.enrollment.enrollment,
      photo: state => state.enrollment.photo
    })
  },

  watch: {
    photo (nv) {
      const self = this
      if (!nv || !nv.length) {
        self.$refs.pond.removeFiles()
        self.$refs.photosrc.destroy()
      }
    }
  },

  mounted () {
    this.$root.$on('reset', () => {
      console.log('resetting photo')
      this.$refs.photoresult.innerHTML = ''
      this.$store.commit('enrollment/updatePhoto', null)
    })
  },

  methods: {

    doCrop () {
      const self = this
      this.$store.commit('enrollment/updatePhoto', self.$refs.photosrc.getCroppedCanvas({ width: 160 }).toDataURL())
      if (!this.photo.length) {
        this.$store.commit('enrollment/updateStep', 5)
        return
      }
      this.$api.enrollment.upload_photo({
        photo: this.photo,
        idsub: this.enrollment.idsub
      }).then(
        function () {
          this.$store.commit('enrollment/updateStep', 5)
        }.bind(this),
        function (err) {
          console.log('upload failed', err)
        }
      )
    },

    handleFile (err, file) {
      if (err) {
        console.error('Nasty', err)
      }
      const reader = new FileReader()
      const self = this
      reader.onload = (event) => {
        self.$refs.photosrc.replace(event.target.result)
      }
      reader.readAsDataURL(file.file)
    },

    prev () {
      this.$store.commit('enrollment/updateStep', 3)
    }

  }

}
</script>

<style>
.dropbox {
  width: 100%;
}
.photosrc{
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
