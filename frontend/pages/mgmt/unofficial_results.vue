<script setup>
import { ref } from "vue"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()
const router = useRouter()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// stores
const mgmtstore = useMgmtTokenStore()
const { token } = storeToRefs(mgmtstore)
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

// datamodel
const round = ref(1)
const category = ref(null)
const dlg_unofficial = ref(false)
const game = ref({})
const games = ref([])
const act_result = ref("")
const p_headers = [
  { title: "Board", value: "boardnr" },
  { title: "White", value: "white" },
  { title: "Black", value: "black" },
  { title: "Unof. Result", value: "unofficial_result" },
  { title: "Action", value: "action", sortable: false },
]

definePageMeta({
  layout: "mgmt",
})

async function checkAuth() {
  console.log("checking if auth is already set", token.value)
  if (token.value) return
  if (person.value.credentials.length === 0) {
    router.push("/mgmt")
    return
  }
  if (!person.value.email.endsWith("@bycco.be")) {
    router.push("/mgmt")
    return
  }
  let reply
  showLoading(true)
  // now login using the Google auth token
  try {
    reply = await $backend("accounts", "login", {
      logintype: "google",
      token: person.value.credentials,
      username: null,
      password: null,
    })
  } catch (error) {
    console.log("cannot login", error)
    router.push("/mgmt")
    return
  } finally {
    showLoading(false)
  }
  console.log("mgmttoken received", reply.data)
  mgmtstore.updateToken(reply.data)
}

async function editResult(item) {
  console.log("editResult", item)
  game.value = item
  dlg_unofficial.value = true
  act_result.value = item.uo_result + ""
}
async function getJsonFile() {
  let reply
  if (!category.value || !round.value) {
    sortpairings.value = []
    return
  }
  const name = `bjk_${category.value.toLowerCase()}.json`
  showLoading(true)
  try {
    reply = await $backend("filestore", "anon_get_file", {
      group: "trn",
      name,
    })
    console.log("getJsonFile success", reply.data)
  } catch (error) {
    console.log("error", error)
    showSnackbar("Cannot get json file: " + error.detail)
    return
  } finally {
    showLoading(false)
  }
  readSwarJson(reply.data)
}

function readSwarJson(swarjson) {
  console.log("readSwarJson", swarjson)
  games.value = []
  const players = swarjson.Swar.Player
  players.forEach((p) => {
    if (!p.RoundArray) return
    console.log("player", p)
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

async function saveUnofficial() {
  let reply
  console.log("saveUnofficial", act_result.value)
  try {
    console.log(round.value)
    console.log(game.value.boardnr)
    console.log(act_result.value)
    reply = await $backend("tournament", "mgmt_set_unofficial_result", {
      token: token.value,
      ur: {
        name: `bjk_${category.value.toLowerCase()}.json`,
        round: round.value,
        boardnr: game.value.boardnr,
        unofficial_result: act_result.value,
      },
    })
    console.log(2)
    game.value.unofficial_result = act_result.value
    showSnackbar("Unofficial result saved")
  } catch (error) {
    console.log("error")
    showSnackbar("Cannot save unofficial result ")
  } finally {
    showLoading(false)
    dlg_unofficial.value = false
  }
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Entry for unoffical results BJK 2025</h1>
    <v-row>
      <v-col cols="6">
        <v-select
          label="Category"
          v-model="category"
          :items="['U8', 'U10', 'U12', 'U14', 'U16', 'U18', 'U20']"
          @update:modelValue="getJsonFile"
        />
      </v-col>
      <v-col cols="6">
        <v-select
          label="Round"
          v-model="round"
          :items="[1, 2, 3, 4, 5, 6, 7, 8, 9]"
          @update:modelValue="getJsonFile"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-data-table :items="games" :headers="p_headers" density="compact">
        <template v-slot:item.action="{ item }">
          <v-icon class="me-2" size="small" @click="editResult(item)">
            mdi-pencil
          </v-icon>
        </template>
      </v-data-table>
    </v-row>
  </v-container>
  <v-dialog v-model="dlg_unofficial" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h5">Enter unofficial result</span>
      </v-card-title>
      <v-card-text>
        White: {{ game.white }}<br />
        Black: {{ game.black }}<br />
        <v-select
          label="Unofficial Result"
          v-model="act_result"
          :items="['', '1-0', '0-1', '½-½']"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="purple-darken-1" variant="text" @click="dlg_unofficial = false">
          Cancel
        </v-btn>
        <v-btn color="purple-darken-1" variant="text" @click="saveUnofficial">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
