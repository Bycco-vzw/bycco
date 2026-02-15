<script setup>
import { ref, computed, onMounted } from "vue"
import { useI18n } from "vue-i18n"
import { useDisplay } from "vuetify"

// communication
const { $backend } = useNuxtApp()
const { t } = useI18n()
const { xs, sm } = useDisplay()
const tab = ref(0)

// data model
const common = ref(null)
const stheaders_smartphone = ["rank", "name", "elo", "gender", "points"]  
const stheaders_tablet = ["rank", "name", "elo", "idbel", "points", "gender",  "clubname"]  
const stheaders_pc = []  
const tournament = {
  json_file: "bjk_u8.json",
  category: "U8",
}
const swartrn = ref({})
const games = ref([])
const round = ref(1)
const uo_headers = [
  { title: t("Board"), value: "boardnr" },
  { title: t("White"), value: "white" },
  { title: t("Black"), value: "black" },
  { title: t("Result"), value: "unofficial_result" },
]
const st_headers = computed(() => {
  let dsp = stheaders_pc
  if (xs.value) {
    dsp =  stheaders_smartphone
  }
  if (sm.value)  {
    dsp = stheaders_tablet
  }
  if (!dsp.length) return swartrn.value.st_headers
  if (!swartrn.value.st_headers) return []
  return swartrn.value.st_headers.filter((x) => dsp.includes(x.value))
})

// routines

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
  swartrn.value = processSwarJson(reply.data, t)
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

async function readCommon() {
  console.log('readCommon')
  try {
    const reply = await $backend("stay", "get_common", {})
    common.value = reply.data
  } catch (error) {
    console.error("failed to fetch common", error)
    return null
  }
}

async function setUnRound(){
  let uround = -1
  let now = new Date()
  console.log("common", common.value)
  for (const [rix, ds] of Object.entries(common.value.rounds)) {
    let d = new Date(ds)
    if (now.getTime() > d.getTime()) {
      uround = rix
    }
  }
  if (uround != -1) {
    console.log("fetching trn round", uround)
    round.value = uround
    await getTournament()
  }
}

onMounted(async () => {
  await readCommon()
  await getTournament()
  setInterval(getTournament, 60000)
  await setUnRound()
})

</script>

<template>
  <v-container class="mt-1">
    <h1>{{ t("BYC 2026") }} {{ tournament.category }}</h1>
    <v-tabs v-model="tab" show>
      <v-tab>{{ t("Standings") }}</v-tab>
      <v-tab>{{ t("Pairings") }}</v-tab>
      <!-- <v-tab>Live</v-tab> -->
      <v-tab>{{ t("Unofficial results") }}</v-tab>
    </v-tabs>
    <v-window v-model="tab"  :touch="false">
      <v-window-item>
        <v-data-table
          :items="swartrn.standings"
          :headers="st_headers"
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
      <!-- <v-window-item>
          <a
          href="https://view.livechesscloud.com#3ac8ec22-aa23-4cea-b576-153b63be4aa2 "
          target="live"
          >Live Games</a
        >
      </v-window-item> -->
      <v-window-item>
        <h2>{{ t("Unofficial results") }}</h2>
        <div style="font-size: 0.7rem;" class="mb-2">
          {{ t("uo_explanation") }}
        </div>
        <div>{{ t("Round") }}: {{ round }}</div>
        <v-data-table
          :items="games"
          :headers="uo_headers"
          :items-per-page="50"
          mobile-breakpoint="0"
          density="compact">
        </v-data-table>
      </v-window-item>
    </v-window>
  </v-container>
</template>
