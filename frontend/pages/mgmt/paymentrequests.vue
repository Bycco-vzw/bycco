<script setup>
import { ref } from 'vue'
import ProgressLoading from '@/components/ProgressLoading.vue'
import SnackbarMessage from '@/components/SnackbarMessage.vue'
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()

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
const headers = [
  { title: 'PR nr', value: 'number' },
  { title: 'Reason', value: 'reason' },
  { title: 'Last Name', value: 'last_name' },
  { title: 'First Name', value: 'first_name' },
  { title: 'Total price', value: 'totalprice' },
  { title: 'Status', value: 'paystatus' },
  { title: 'Message', value: 'paymessage' },
  { title: 'Link', value: 'link_id' },
  { title: 'Actions', value: 'action', sortable: false }
]
const prqs = ref([])
const search = ref("")
const filter = ref({})
const footerProps = ref({
  itemsPerPageOptions: [150, -1]
})

function editPaymentRequest(item) {
  navigateTo('/mgmt/paymentrequest_edit/?id=' + item.id)
}

async function getPaymentRequests() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("paymentrequest", "get_paymentrequests", {
      token: mgmttoken.value
    })
  }
  catch (error) {
    console.error('getting paymentrequests', error)
    if (error.code === 401) {
      await navigateTo('/mgmt')
    }
    else {
      showSnackbar('Getting payment requests failed')
    }
  }
  finally {
    showLoading(true)
  }

  prqs.value = resp.data
  console.log('prqs', prqs.value)

}

async function refresh() {
  await getPaymentRequests()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getPaymentRequests()
})

</script>


<template>
  <v-container>
    <h1>Payment Requests</h1>
    <v-data-table :headers="headers" :items="prqs" item-class="lightgreyrow"
      :footer-props="footerProps" class="elevation-1" :sort-by="['name']" :search="search">
      <template #top>
        <v-card color="grey lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field v-model="search" label="Search" class="mx-4" append-icon="mdi-magnify"
                hide_details />
              <v-spacer />
              <v-tooltip bottom>
                <template #activator="{ on }">
                  <v-btn fab outlined color="deep-purple" v-on="on"
                    @click="downloadPaymentRequests()">
                    <v-icon>mdi-download-multiple</v-icon>
                  </v-btn>
                </template>
                Download Paymentrequests
              </v-tooltip>
              <v-tooltip bottom>
                <template #activator="{ on }">
                  <v-btn fab outlined color="deep-purple" v-on="on" @click="refresh()">
                    <v-icon>mdi-refresh</v-icon>
                  </v-btn>
                </template>
                Refresh
              </v-tooltip>
            </v-row>
          </v-card-title>
        </v-card>
      </template>
      <template #item.link_id="{ item }">
        <NuxtLink v-if="item.link_id" :to="'/mgmt/reservation_edit?id=' + item.link_id">
          link
        </NuxtLink>
      </template>
      <template #item.action="{ item }">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon small class="mr-2" v-on="on" @click="editPaymentRequest(item)">
              mdi-pencil
            </v-icon>
          </template>
          Edit Paymentrequests
        </v-tooltip>
      </template>
      <template #no-data>
        No paymentrequests found.
      </template>
    </v-data-table>
  </v-container>
</template>

<script>

export default {

  name: 'Paymentrequestlist',

  layout: 'mgmt',

  data() {
    return {
      filter: {},
      footerProps: {
        itemsPerPageOptions: [150, -1]
      },
      headers: [
        {
          text: 'PR nr', value: 'number'
        },
        {
          text: 'Reason', value: 'reason'
        },
        {
          text: 'Last Name', value: 'last_name'
        },
        {
          text: 'First Name', value: 'first_name'
        },
        {
          text: 'Total price', value: 'totalprice'
        },
        {
          text: 'Status', value: 'paystatus'
        },
        {
          text: 'Message', value: 'paymessage'
        },
        {
          text: 'Link', value: 'link_id'
        },
        {
          text: 'Actions', value: 'action', sortable: false
        }
      ],
      prqs: [],
      search: ''
    }
  },

  computed: {
    token() { return this.$store.state.token.value }
  },

  mounted() {
    this.getPaymentRequests()
  },

  methods: {

    downloadPaymentRequests() {
      alert('TODO')
    },

    editPaymentRequest(item) {
      this.$router.push('/mgmt/paymentrequestedit/?id=' + item.id)
    },

    async getPaymentRequests() {
      try {
        const resp = await this.$api.paymentrequest.get_paymentrequests({
          token: this.token
        })
        this.prqs = resp.data.paymentrequests
        console.log('prqs', this.prqs)
      } catch (error) {
        const resp = error.response
        console.error('getting paymentrequests', resp)
        if (resp.status === 401) {
          this.$router.push('/mgmt/login')
        } else {
          this.$root.$emit('snackbar', { text: 'Getting paymentrequests failed', reason: resp.data.detail })
        }
      }
    },

    async refresh() {
      await this.getPaymentRequests()
    }

  }

}
</script>

<style>
.lightgreyrow {
  color: #bbb;
}
</style>
