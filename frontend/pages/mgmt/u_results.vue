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
const round = ref(null)
const category = ref(null)
const trn_u8 = ref({
  name: "bjk_u8.json",
})
const trn_u10 = ref({
  name: "bjk_u10.json",
})
const trn_u12 = ref({
  name: "bjk_u12.json",
})
const trn_u14 = ref({
  name: "bjk_u14.json",
})
const trn_u16 = ref({
  name: "bjk_u16.json",
})
const trn_u18 = ref({
  name: "bjk_u18.json",
})
const trn_u20 = ref({
  name: "bjk_u20.json",
})
let activetrn = null

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

function readSwarJson(swarjson, t) {
  const pairings = [],
    sortpairings = []
  const players = swarjson.Swar.Player
  let st_headers = _st_headers
  players.forEach((p) => {
    if (!p.RoundArray) p.RoundArray = []
    p.RoundArray.forEach((r) => {
      const rnr = r.RoundNr
      const pr = pairings[rnr] || {
        games: [],
        bye: null,
        absent: [],
        rnr,
      }
      switch (r.Color) {
        case "No Color":
          if (r.Tabel === "BYE") {
            pr.bye = {
              white: p.Name,
              black: "Bye",
              result: "",
            }
          }
          if (r.Tabel === "Absent") {
            pr.absent.push({
              white: p.Name,
              black: t("Absent"),
              result: "",
            })
          }
          break
        case "White":
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
        rnr: p.rnr,
      }
      if (p.bye) {
        sortpairings[maxround - ix].games.push(p.bye)
      }
      if (p.absent) {
        sortpairings[maxround - ix].games.push(...p.absent)
      }
    }
  })
  st_headers.forEach((h) => {
    if (h.u_title) {
      h.title = t(h.u_title)
    }
  })
  pr_headers.forEach((h) => {
    if (h.u_title) {
      h.title = t(h.u_title)
    }
  })
  return sortpairings
}

function handleFile(f) {
  const reader = new FileReader()
  reader.onload = (event) => {
    activetrn.json = event.target.result
  }
  // reader.readAsDataURL(f)
}

async function getTournament(name) {
  let reply
  try {
    reply = await $backend("filestore", "anon_get_file", {
      group: "trn",
      name,
    })
    console.log("getTournament success", reply.data)
  } catch (error) {
    console.log("error", error)
    return
  } finally {
    console.log()
  }
  swartrn.value = processSwarJson(reply.data, xs.value, t)
}

function uploading(trn) {
  console.log("uploading", trn)
  activetrn = trn
  handleFile(trn.file)
}

async function uploadTrn() {
  showLoading(true)
  try {
    const reply = await $backend("tournament", "mgmt_upload_json", {
      token: token.value,
      trn: {
        name: activetrn.name,
        jsoncontent: activetrn.jsoncontent,
      },
    })
  } catch (error) {
    console.error("uploading json failed", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Uploading json file failed: " + error.detail)
    }
    return
  } finally {
    showLoading(false)
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
          v-model="category"
          :items="['U8', 'U10', 'U12', 'U14', 'U16', 'U18', 'U20']"
          @update:modelValue="getJsonFile"
        />
      </v-col>
      <v-col cols="6">
        <v-select
          v-model="round"
          :items="[1, 2, 3, 4, 5, 6, 7, 8, 9]"
          @update:modelValue="getJsonFile"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
