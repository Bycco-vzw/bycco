<script setup>
const localePath = useLocalePath()
const { locale, t: $t } = useI18n()

const props = defineProps({
  landing: String,
  drawer: Boolean,
})

function toggleDrawer() {

}

</script>

<template>
  <v-app-bar v-cloak dark app class="bm-blue-grey-darken-2" :class="{ landing: props.landing }">
    <v-app-bar-nav-icon @click="toggleDrawer" />
    <v-toolbar-items>
      <v-btn text large :to="localePath('index')">
        BYCCO
      </v-btn>
    </v-toolbar-items>
    <v-spacer />
    <v-toolbar-items class="hidden-sm-and-down">
      <!-- <v-btn text large href="/enrollment">
        {{ $t('Enrollment') }}
      </v-btn> -->
      <!-- <v-btn text large href="/lodging">
        {{ $t('Lodging') }}
      </v-btn> -->
      <!-- <v-btn text large href="/pairings/u20">
        {{ $t('Pairings') }}
      </v-btn> -->
    </v-toolbar-items>
  </v-app-bar>
</template>


<style scoped>
.landing.blue-grey.darken-2 {
  background-color: rgba(77, 94, 101, 0.4) !important;
}
</style>
