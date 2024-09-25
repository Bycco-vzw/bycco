<script setup>
import { ref } from "vue"
import { parse } from "yaml"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()
const router = useRouter()
const route = useRoute()

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
const assignment = ref({
  roomtype: "",
  roomnr: "",
  modroomtype: null,
})
const idreservation = route.query.id
const newguest = ref({})
const roomtypes = ref([])
const roomnrs = ref([])
const rsv = ref({ payment_id: "" })

definePageMeta({
  layout: "mgmt",
})

function addGuest() {
  rsv.value.guestlist.push({
    last_name: newguest.value.last_name,
    first_name: newguest.value.first_name,
    birthdate: newguest.value.birthdate,
    player: newguest.value.player || false,
  })
  newguest.value = {}
}

function back() {
  router.go(-1)
}

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

async function confirm_assignment() {
  // let reply
  // showLoading(true)
  // try {
  //   reply = await $backend("stay", "mgmt_assign_room", {
  //     id: idreservation,
  //     roomnr: assignment.value.roomnr,
  //     token: mgmttoken.value,
  //   })
  //   readReservation(reply.data)
  // } catch (error) {
  //   console.error("getting assigning room", error)
  //   if (error.code == 401) {
  //     router.push("/mgmt")
  //   } else {
  //     showSnackbar("Assigning room failed: " + error.detail)
  //   }
  //   return
  // } finally {
  //   showLoading(false)
  // }
  // showSnackbar("Room number assigned OK")
}

async function create_pr() {
  // let reply
  // showLoading(true)
  // try {
  //   reply = await $backend("payment", "mgmt_create_stay_pr", {
  //     id: idreservation,
  //     token: mgmttoken.value,
  //   })
  // } catch (error) {
  //   console.error("creating payment request", error)
  //   if (error.code === 401) {
  //     router.push("/mgmt")
  //   } else {
  //     showSnackbar("Creating paymentrequesr failed: " + error.detail)
  //   }
  //   return
  // } finally {
  //   showLoading(false)
  // }
  // router.push("/mgmt/paymentrequest_edit?id=" + reply.data)
}

function deleteGuest(ix) {
  rsv.value.guestlist.splice(ix, 1)
}

async function delete_pr() {
  // let reply
  // if (confirm("Are you sure to delete the linked payment request")) {
  //   showLoading(true)
  //   try {
  //     reply = await $backend("payment", "mgmt_delete_stay_pr", {
  //       id: idreservation,
  //       token: mgmttoken.value,
  //     })
  //   } catch (error) {
  //     console.error("deleting linked payment request", error)
  //     if (error.code === 401) {
  //       router.push("/mgmt")
  //     } else {
  //       showSnackbar("Deleting Paymentrequest failed" + error.detail)
  //     }
  //     return
  //   } finally {
  //     showLoading(false)
  //   }
  //   await getReservation()
  // }
}

async function deleteAssignment(ix) {
  // let reply
  // showLoading(true)
  // try {
  //   reply = await $backend("stay", "mgmt_unassign_room", {
  //     id: idreservation,
  //     roomnr: rsv.value.assignments[ix].roomnr,
  //     token: mgmttoken.value,
  //   })
  //   readReservation(reply.data)
  // } catch (error) {
  //   console.error("getting unassigning room", error)
  //   if (error.code === 401) {
  //     router.push("/mgmt")
  //   } else {
  //     showSnackbar("Assigning room failed" + error.detail)
  //   }
  // } finally {
  //   showLoading(false)
  // }
}

async function getReservation() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("stay", "mgmt_get_reservation", {
      id: idreservation,
      token: token.value,
    })
    readReservation(reply.data)
  } catch (error) {
    console.error("getting reservation failed", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Getting reservation failed")
    }
  } finally {
    showLoading(false)
  }
}

async function gotoPaymentrequest(id) {
  // console.log("going to payment request", id)
  // router.push("/mgmt/paymentrequest_edit?id=" + id)
}

function readReservation(reservation) {
  rsv.value = { ...reservation }
  assignment.value = { roomtype: "", roomnr: "" }
}

async function get_free_rooms() {
  // let reply
  // showLoading(true)
  // try {
  //   reply = await $backend("stay", "mgmt_get_free_rooms", {
  //     roomtype: assignment.value.roomtype,
  //   })
  // } catch (error) {
  //   console.error("getting free rooms", error.response)
  // } finally {
  //   showLoading(false)
  // }
  // const rooms = reply.data
  // console.log("returned rooms", rooms)
}

async function parseYaml(group, name) {
  let yamlcontent
  try {
    yamlcontent = await readBucket(group, name)
    if (!yamlcontent) {
      return null
    }
    return parse(yamlcontent)
  } catch (error) {
    console.error("cannot parse yaml", error)
  }
}

async function processCommon() {
  const cm = await parseYaml("data", "common.yml")
  // roomtypes.value = []
  // cm.mgmtroomtypes.forEach((rt) => {
  //   roomtypes.value.push({
  //     title: cm.i18n[rt].nl,
  //     value: rt,
  //   })
  // })
}

async function readBucket(group, name) {
  try {
    const reply = await $backend("filestore", "anon_get_file", {
      group,
      name,
    })
    return reply.data
  } catch (error) {
    console.error("failed to fetch file from bucket")
    return null
  }
}

async function roomtypeSelected() {
  // let reply
  // showLoading(true)
  // try {
  //   reply = await $backend("stay", "mgmt_get_free_rooms", {
  //     token: mgmttoken.value,
  //     roomtype: assignment.value.roomtype,
  //   })
  // } catch (error) {
  //   console.error("getting free rooms", error.response)
  //   showSnackbar("Cannot get room numbers")
  //   return
  // } finally {
  //   showLoading(false)
  // }
  // const rooms = reply.data
  // roomnrs.value = Array.from(Object.keys(rooms), (x) => rooms[x].number)
}

async function saveGuestlist() {
  let reply
  showLoading(true)
  try {
    await $backend("stay", "mgmt_update_reservation", {
      id: idreservation,
      reservation: {
        guestlist: rsv.value.guestlist,
      },
      token: token.value,
    })
  } catch (error) {
    console.error("getting getReservations", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Saving reservation failed: " + error.detail)
    }
    return
  } finally {
    showLoading(false)
  }
  console.log("save successful")
  showSnackbar("Reservation saved")
}

async function saveProperties() {
  let reply
  showLoading(true)
  try {
    await $backend("stay", "mgmt_update_reservation", {
      id: idreservation,
      reservation: {
        address: rsv.value.address,
        bycco_remarks: rsv.value.bycco_remarks,
        checkindate: rsv.value.checkindate,
        checkoutdate: rsv.value.checkoutdate,
        email: rsv.value.email,
        enabled: rsv.value.enabled,
        first_name: rsv.value.first_name,
        last_name: rsv.value.last_name,
        locale: rsv.value.locale,
        stay: rsv.value.stay,
        meals: rsv.value.meals,
        mobile: rsv.value.mobile,
        organizers: rsv.value.organizers,
        remarks: rsv.value.remarks,
      },
      token: mgmttoken.value,
    })
  } catch (error) {
    console.error("getting getReservations", error)
    if (error.code === 401) {
      router.push("/mgmt")
    } else {
      showSnackbar("Saving reservation failed: " + error.detail)
    }
    return
  } finally {
    showLoading(false)
  }
  console.log("save successful")
  showSnackbar("Reservation saved")
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await processCommon()
  await checkAuth()
  await getReservation()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />

    <v-row class="my-2">
      <h2>Edit Reservation {{ rsv.number }}: {{ rsv.last_name }} {{ rsv.first_name }}</h2>
      <v-spacer />
      <v-tooltip bottom>
        <template #activator="{ on }">
          <v-btn outlined fab color="deep-purple" @click="back()">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </template>
        <span>Go Back</span>
      </v-tooltip>
    </v-row>

    <v-card class="my-3">
      <v-card-title> Properties </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="rsv.last_name" label="Last name" />
            <v-text-field v-model="rsv.first_name" label="First name" />
            <v-textarea v-model="rsv.address" label="Address" />
            <v-textarea v-model="rsv.bycco_remarks" label="Remarks from Bycco" />
            <v-text-field v-model="rsv.checkindate" label="Checkin Date" />
            <v-text-field v-model="rsv.checkoutdate" label="Checkout Date" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-switch v-model="rsv.enabled" label="Enabled" color="deep-purple" />
            <p>Reservation created: {{ rsv._creationtime }}</p>
            <p>Reservation modified: {{ rsv._modificationtime }}</p>
            <v-text-field v-model="rsv.email" label="E-mail" />
            <v-text-field v-model="rsv.mobile" label="Mobile" />
            <v-textarea v-model="rsv.remarks" label="Customer Remarks" />
            <v-text-field v-model="rsv.locale" label="Language" />
            <v-text-field v-model="rsv.stay" label="Requested accomodation" />
            <v-text-field v-model="rsv.meals" label="Requested meals" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="saveProperties"> Save </v-btn>
      </v-card-actions>
    </v-card>

    <v-card class="my-3">
      <v-card-title>Guest List</v-card-title>
      <v-card-text>
        <v-row v-for="(g, ix) in rsv.guestlist" :key="ix" class="mt-2">
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="g.first_name" dense label="First name" />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="g.last_name" dense label="Last name" />
          </v-col>
          <v-col cols="12" sm="6" md="2">
            <v-text-field v-model="g.birthdate" dense label="Birthdate" />
          </v-col>
          <v-col cols="6" sm="3" md="2">
            <v-checkbox v-model="g.player" dense label="player" />
          </v-col>
          <v-col cols="6" sm="3" md="2">
            <v-btn fab small dark color="deep-purple" @click="deleteGuest(ix)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <h4>New guest</h4>
        <v-row class="mt-2">
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="newguest.first_name" dense label="First name" />
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-text-field v-model="newguest.last_name" dense label="Last name" />
          </v-col>
          <v-col cols="12" sm="6" md="2">
            <v-text-field v-model="newguest.birthdate" dense label="Birthdate" />
          </v-col>
          <v-col cols="6" sm="3" md="2">
            <v-checkbox v-model="newguest.player" dense label="player" />
          </v-col>
          <v-col cols="6" sm="3" md="2">
            <v-btn fab small dark color="deep-purple" @click="addGuest">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="saveGuestlist"> Save </v-btn>
      </v-card-actions>
    </v-card>

    <v-card class="my-3">
      <v-card-title>Assignment of room</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="3">
            <v-select
              v-model="assignment.roomtype"
              :items="roomtypes"
              label="Select roomtype"
              @update:model-value="roomtypeSelected"
            />
          </v-col>
          <v-col cols="3">
            <v-select
              v-model="assignment.roomnr"
              :items="roomnrs"
              label="Select room number"
              :disabled="!assignment.roomtype.length"
            />
          </v-col>
          <v-col cols="3">
            <v-btn :disabled="!assignment.roomnr.length" @click="confirm_assignment">
              confirm
            </v-btn>
          </v-col>
        </v-row>
        <h4>Existing Assignments</h4>
        <div v-for="(a, ix) in rsv.assignments" :key="ix">
          {{ a.roomnr }} {{ a.roomtype }} &nbsp;&nbsp;&nbsp;
          <v-btn @click="deleteAssignment(ix)"> Delete </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title class="mt-2"> Payment Request </v-card-title>
      <v-card-actions>
        <v-btn v-if="!rsv.payment_id" @click="create_pr"> Create </v-btn>
        <v-btn v-if="rsv.payment_id" @click="gotoPaymentrequest(rsv.payment_id)">
          Show
        </v-btn>
        <v-btn v-if="rsv.payment_id" @click="delete_pr"> Delete </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<style scoped>
.bordermd {
  border: 1px solid grey;
}

.v-input--checkbox {
  margin-top: 0;
}
</style>
