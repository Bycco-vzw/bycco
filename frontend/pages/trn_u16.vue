<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDisplay } from 'vuetify'

const { t } = useI18n()
const { xs } = useDisplay()

const tournament = {
  json_file: "bjk_u16.json",
  category: "U16"
}
const { $backend } = useNuxtApp()

const swartrn = ref({})
const tab = ref(0)

async function getTournament(name) {
  let reply
  try {
    reply = await $backend("filestore", "anon_get_file", {
      group: "trn",
      name,
    })
    console.log('getTournament success', reply.data)
  } catch (error) {
    console.log('error', error)
    return
  }
  finally {
    console.log()
  }
  swartrn.value = processSwarJson(reply.data, xs.value, t)
}


onMounted(() => {
  getTournament(tournament.json_file)
})

</script>

<template>
  <v-container class="mt-1">
    <h1>{{ t('BYC 2024') }} {{ tournament.category }}</h1>
    <v-tabs v-model="tab" show>
      <v-tab>{{ t('Standings') }}</v-tab>
      <v-tab>{{ t('Pairings') }}</v-tab>
      <v-tab>Live</v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item>
        <v-data-table :items="swartrn.standings" :headers="swartrn.st_headers" :items-per-page="50"
          :hide-default-footer="true" mobile-breakpoint="0" density="compact" />
      </v-window-item>
      <v-window-item>
        <div v-for="p in swartrn.sortpairings" :key="p.rnr" class="my-2">
          <h2>{{ t('Round') }} {{ p.rnr }}</h2>
          <v-data-table :items="p.games" :headers="swartrn.pr_headers" :items-per-page="50"
            :hide-default-footer="true" mobile-breakpoint="0" density="compact" />
        </div>
      </v-window-item>
      <v-window-item>
        <a href="https://view.livechesscloud.com#3ed77562-6a33-4f0b-a315-1c1b4db61598"
          target="live">Live Games</a>
      </v-window-item>
    </v-window>
  </v-container>
</template>