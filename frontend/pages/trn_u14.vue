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

const sb_headers = computed(() => {
  if (xs.value) {
    return sheaders.filter((x) => { return !x.small })
  }
  else {
    return sheaders
  }
})

const sheaders = [
  {
    title: 'Nr',
    sortable: false,
    value: 'rank'
  },
  {
    title: t('Name'),
    sortable: false,
    value: 'name'
  },
  {
    title: 'Elo',
    sortable: false,
    value: 'elo'
  },
  {
    title: t('Games'),
    sortable: false,
    small: true,
    value: 'ngames'
  },
  {
    title: t('Points'),
    sortable: false,
    value: 'points'
  },
  {
    title: "BC1",
    sortable: false,
    small: true,
    value: 'tb1'
  },
  {
    title: "Buch",
    sortable: false,
    small: true,
    value: 'tb2'
  },
  {
    title: "SB",
    sortable: false,
    small: true,
    value: 'tb3'
  },
  {
    title: "Prog",
    sortable: false,
    small: true,
    value: 'tb4'
  },
  {
    title: "DE",
    sortable: false,
    small: true,
    value: 'tb5'
  },
]
const gheaders = [
  {
    title: 'Nr',
    sortable: false,
    value: 'boardnr'
  },
  {
    title: 'Wit',
    sortable: false,
    value: 'white'
  },
  {
    title: 'Res.',
    sortable: false,
    value: 'result'
  },
  {
    title: 'Zwart',
    sortable: false,
    value: 'black'
  }
]

const tab = ref(0)
const trn = ref({})
let swartrn = null

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
  swartrn = reply.data
  processTournament()
}

function getWhiteResult(rescode) {
  switch (rescode) {
    case '1':
      return '1-0'
    case '0':
      return '0-1'
    case '½':
      return '½-½'
    case '1FF':
      return '1-0 FF'
    case '0ff':
      return '0-1 FF'
    case '-':
      return '-'
  }
}

function processTournament() {
  const standings = [], pairings = [], sortpairings = []
  const players = swartrn.Swar.Player
  console.log('players', players)
  players.forEach((p) => {
    standings[p.Ranking - 1] = {
      id: p.NationalId,
      rank: p.Ranking,
      name: p.Name,
      elo: p.FideElo,
      ngames: p.NbOfParts,
      points: parseFloat(p.Points),
      tb1: p.TieBreak[0].Points,
      tb2: p.TieBreak[1].Points,
      tb3: p.TieBreak[2].Points,
      tb4: p.TieBreak[3].Points,
      tb5: p.TieBreak[4].Points,
    }
    if (!p.RoundArray) p.RoundArray = []
    p.RoundArray.forEach((r) => {
      const rnr = r.RoundNr
      const pr = pairings[rnr] || {
        games: [],
        bye: null,
        absent: [],
        rnr
      }
      switch (r.Color) {
        case 'No Color':
          if (r.Tabel === 'BYE') {
            pr.bye = {
              white: p.Name,
              black: 'Bye',
              result: ''
            }
          }
          if (r.Tabel === 'Absent') {
            pr.absent.push({
              white: p.Name,
              black: 'Afwezig',
              result: ''
            })
          }
          break
        case 'White':
          let boardnr = parseInt(r.Tabel) - 1
          pr.games.push({
            white: p.Name,
            black: r.OpponentName,
            result: getWhiteResult(r.Result),
            boardnr: boardnr + 1,
          })
          break
      }
      pairings[rnr] = pr
    })
  })

  const maxround = pairings.length - 1
  pairings.forEach((p, ix) => {
    p.games.sort((x, y) => x.boardnr - y.boardnr)
    if (ix > 0) {
      sortpairings[maxround - ix] = {
        games: p.games,
        rnr: p.rnr
      }
      if (p.bye) {
        sortpairings[maxround - ix].games.push(p.bye)
      }
      if (p.absent) {
        sortpairings[maxround - ix].games.push(...p.absent)
      }
    }
  })
  trn.value = { standings, pairings, sortpairings }
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
        <v-data-table :items="trn.standings" :headers="sb_headers" :items-per-page="50"
          :hide-default-footer="true" mobile-breakpoint="0" density="compact" />
      </v-window-item>
      <v-window-item>
        <div v-for="p in trn.sortpairings" :key="p.rnr" class="my-2">
          <h2>Ronde {{ p.rnr }}</h2>
          <v-data-table :items="p.games" :headers="gheaders" :items-per-page="50"
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

<style scoped>
.person-photo {
  width: 160px;
}

.person-photo-sm {
  width: 120px;
}
</style>
