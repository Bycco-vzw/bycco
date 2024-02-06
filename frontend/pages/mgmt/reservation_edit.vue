<script setup>
import { ref } from 'vue'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()
const route = useRoute()
const router = useRouter()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// stores
const mgmtstore = useMgmtTokenStore()
const { token: mgmttoken } = storeToRefs(mgmtstore)
const personstore = usePersonStore();
const { person } = storeToRefs(personstore)

// datamodel
const rsv = ref({ payment_id: "" })
const search = ref("")
const assignment = ref({
  roomtype: '',
  roomnumber: '',
  modroomtype: null
})
const dialogDelete = ref(false)
const idreservation = route.query.id
const newguest = ref({})
const period = ref({})
const roomtypes = ref([])
const roomnumbers = ref([])

definePageMeta({
  layout: 'mgmt',
})

function addGuest() {
  rsv.value.guestlist.push({
    last_name: newguest.value.last_name,
    first_name: newguest.value.first_name,
    birthday: newguest.value.birthday,
    player: newguest.value.player
  })
  newguest.value = {}
}

function back() {
  router.go(-1)
}

async function checkAuth() {
  console.log('checking if auth is already set', mgmttoken.value)
  if (mgmttoken.value) return
  if (person.value.credentials.length === 0) {
    navigateTo('/mgmt')
    return
  }
  if (!person.value.email.endsWith('@bycco.be')) {
    navigateTo('/mgmt')
    return
  }
  let reply
  showLoading(true)
  // now login using the Google auth token
  try {
    reply = await $backend("accounts", "login", {
      logintype: 'google',
      token: person.value.credentials,
      username: null,
      password: null,
    })
  }
  catch (error) {
    navigateTo('/mgmt')
  }
  finally {
    showLoading(false)
  }
  mgmtstore.updateToken(reply.data)
}

async function confirm_assignment() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("lodging", "mgmt_assign_room", {
      id: idreservation,
      roomnumber: assignment.value.roomnumber,
      token: mgmttoken.value
    })
    readReservation(resp.data)
  }
  catch (error) {
    console.error('getting assigning room', resp)
    if (error.code === 401) {
      await navigateTo('/mgmt')
    } else {
      showSnackbar('Assigning room failed' + error.detail)
    }
  }
  finally {
    showLoading(false)
  }
}

async function create_pr() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("lodging", "create_pr", {
      id: this.$route.query.id,
      token: mgmttoken.value
    })
  }
  catch (error) {
    console.error('creating payment request', error)
    if (error.code === 401) {
      await navigateTo('/mgmt')
    } else {
      showSnackbar('Creating paymentrequesr failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  await navigateTo('/mgmt/paymentrequestedit?id=' + resp.data)
}

function deleteGuest(ix) {
  rsv.value.guestlist.splice(ix, 1)
}

async function delete_pr() {
  let reply
  if (confirm('Are you sure to delete the linked payment request')) {
    showLoading(true)
    try {
      reply = await $backend("lodging", "delete_pr", {
        id: idreservation,
        token: mgmttoken.value
      })
    }
    catch (error) {
      console.error('deleting linked payment request', error)
      if (error.code === 401) {
        await navigateTo('/mgmt')
      } else {
        showSnackbar('Deleting Paymentrequest failed' + error.detail)
      }
      return
    }
    finally {
      showLoading(false)
    }
    await getReservation()
  }
}

async function deleteAssignment(ix) {
  let reply
  showLoading(true)
  try {
    reply = await $backend("lodging", "unassign_room", {
      id: idreservation,
      roomnumber: rsv.value.assignments[ix].roomnr,
      token: mgmttoken.value
    })
    readReservation(reply.data)
  } catch (error) {
    console.error('getting unassigning room', error)
    if (error.code === 401) {
      await navigateTo('/mgmt')
    }
    else {
      showSnackbar('Assigning room failed' + error.detail)
    }
  }
}

async function getReservation() {
  let reply
  showLoading(true)
  try {
    reply = await $backend('lodging', "mgmt_get_reservation", {
      id: idreservation,
      token: mgmttoken.value
    })
    rsv.value = reply.data
  }
  catch (error) {
    console.error('getting reservation failed', error)
    if (error.code === 401) {
      navigateTo('/mgmt')
    }
    else {
      showSnackbar('Getting reservation failed')
    }
  }
  finally {
    showLoading(false)
  }
}

async function gotoPaymentrequest(id) {
  console.log('going to payment request', id)
  await navigateTo('/mgmt/paymentrequest_edit?id=' + id)
}

function readReservation(reservation) {
  rsv.value = { ...reservation }
  assignment.value = { roomtype: '', roomnumber: '' }
}

async function roomtypeSelected() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("lodging", "get_free_rooms", {
      roomtype: assignment.value.roomtype
    })
  }
  catch (error) {
    console.error('getting free rooms', error.response)
  }
  finally {
    showLoading(false)
  }
  const rooms = reply.data
  console.log('returned rooms', rooms)
  // roomnumbers.value = Array.from(Object.keys(rooms), x => rooms[x].number)
}

async function saveGuestlist() {
  let reply
  showLoading(true)
  try {
    await $backend("lodging", "mgmt_update_reservation", {
      id: idreservation,
      reservation: {
        guestlist: rsv.value.guestlist
      },
      token: mgmttoken.value
    })
  }
  catch (error) {
    console.error('getting getReservations', error)
    if (error.code === 401) {
      await navigateTo('/mgmt')
    }
    else {
      showSnackbar('Saving reservation failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  console.log('save successful')
  showSnackbar('Reservation saved')
}


async function saveProperties() {
  let reply
  showLoading(true)
  try {
    await $backend("lodging", "mgmt_update_reservation", {
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
        lodging: rsv.value.lodging,
        meals: rsv.value.meals,
        mobile: rsv.value.mobile,
        organizers: rsv.value.organizers,
        remarks: rsv.value.remarks
      },
      token: mgmttoken.value
    })
  }
  catch (error) {
    console.error('getting getReservations', error)
    if (error.code === 401) {
      await navigateTo('/mgmt')
    }
    else {
      showSnackbar('Saving reservation failed: ' + error.detail)
    }
    return
  }
  finally {
    showLoading(false)
  }
  console.log('save successful')
  showSnackbar('Reservation saved')
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
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
      <v-card-title>
        Properties
      </v-card-title>
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
            <v-text-field v-model="rsv.lodging" label="Requested accomodation" />
            <v-text-field v-model="rsv.meals" label="Requested meals" />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="saveProperties">
          Save
        </v-btn>
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
            <v-text-field v-model="g.birthday" dense label="Birthdate" />
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
            <v-text-field v-model="newguest.birthday" dense label="Birthdate" />
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
        <v-btn @click="saveGuestlist">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card class="my-3">
      <v-card-title>Assignment of room</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="3">
            <v-select v-model="assignment.roomtype" :items="roomtypes" label="Select roomtype"
              @change="roomtypeSelected" />
          </v-col>
          <v-col cols="3">
            <v-select v-model="assignment.roomnumber" :items="roomnumbers" label="Select room number"
              :disabled="!assignment.roomtype.length" />
          </v-col>
          <v-col cols="3">
            <v-btn :disabled="!assignment.roomnumber.length" @click="confirm_assignment">
              confirm
            </v-btn>
          </v-col>
        </v-row>
        <h4>Existing Assignments</h4>
        <div v-for="(a, ix) in rsv.assignments" :key="ix">
          {{ a.roomnr }} {{ a.roomtype }} &nbsp;&nbsp;&nbsp;
          <v-btn @click="deleteAssignment(ix)">
            Delete
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title class="mt-2">
        Payment Request
      </v-card-title>
      <v-card-actions>
        <v-btn v-if="!rsv.payment_id" @click="create_pr">
          Create
        </v-btn>
        <v-btn v-if="rsv.payment_id" @click="gotoPaymentrequest(rsv.payment_id)">
          Show
        </v-btn>
        <v-btn v-if="rsv.payment_id" @click="delete_pr">
          Delete
        </v-btn>
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