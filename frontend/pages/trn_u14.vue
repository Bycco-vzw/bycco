<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDisplay } from 'vuetify'

const { t } = useI18n()
const { xs } = useDisplay()

const tournament = {
  json_file: "bjk_u14.json",
  category: "U14"
}

const { $backend } = useNuxtApp()

const swartrn = ref({})
const tab = ref(0)
const games = ref([])
const round = ref(1)

const uo_headers = [
  { title: t("Board"), value: "boardnr" },
  { title: t("White"), value: "white" },
  { title: t("Black"), value: "black" },
  { title: t("Result"), value: "unofficial_result" },
]

async function getTournament() {
  let reply
  try {
    reply = await $backend("filestore", "anon_get_file", {
      group: "trn",
      name: tournament.json_file,
    })
  } catch (error) {
    console.log("error", error)
    return
  } finally {
    console.log()
  }
  swartrn.value = processSwarJson(reply.data, xs.value, t)
  getUnofficialGames(reply.data)
}

function getUnofficialGames(swarjson) {
  games.value = []
  const players = swarjson.Swar.Player
  players.forEach((p) => {
    if (!p.RoundArray) return
    p.RoundArray.forEach((r) => {
      if (r.RoundNr != round.value) return
      if (r.Color == "White") {
        games.value.push({
          white: p.Name,
          black: r.OpponentName,
          unofficial_result: r.UnofficialResult ? r.UnofficialResult : "",
          boardnr: parseInt(r.Tabel),
        })
      }
    })
  })
  games.value.sort((x, y) => x.boardnr - y.boardnr)
}

onMounted(() => {
  getTournament()
  setInterval(getTournament, 60000)
})
</script>

<template>
  <v-container class="mt-1">
    <h1>{{ t("BYC 2025") }} {{ tournament.category }}</h1>
    <v-tabs v-model="tab" show>
      <v-tab>{{ t("Standings") }}</v-tab>
      <v-tab>{{ t("Pairings") }}</v-tab>
      <v-tab>Live</v-tab>
      <v-tab>{{ t("Unofficial results") }}</v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item>
        <v-data-table
          :items="swartrn.standings"
          :headers="swartrn.st_headers"
          :items-per-page="50"
          mobile-breakpoint="0"
          density="compact"
        />
      </v-window-item>
      <v-window-item>
        <div v-for="p in swartrn.sortpairings" :key="p.rnr" class="my-2">
          <h2>{{ t("Round") }} {{ p.rnr }}</h2>
          <v-data-table
            :items="p.games"
            :headers="swartrn.pr_headers"
            :items-per-page="50"
            mobile-breakpoint="0"
            density="compact"
          />
        </div>
      </v-window-item>
      <v-window-item>
        <a
          href="https://view.livechesscloud.com/#c2fb0603-ec59-4803-b172-cbc9664ddf41"
          target="live"
          >Live Games</a
        >
      </v-window-item>
      <v-window-item>
        <h2>{{ t("Unofficial results") }}</h2>
        <div>
          {{ t("uo_explanation") }}
        </div>
        <v-select v-model="round" label="Round" :items="[1, 2, 3, 4, 5, 6, 7, 8, 9]" max-width="10em" 
         @update:modelValue="getTournament"  />
        <v-data-table
          :items="games"
          :headers="uo_headers"
          :items-per-page="50"
          mobile-breakpoint="0"
          density="compact"
        </v-data-table>
      </v-window-item>
    </v-window>
  </v-container>
</template>
