<script setup>
import { ref, watch } from "vue"
import showdown from "showdown"
import { useI18n } from "vue-i18n"
const { t, locale } = useI18n()

//  snackbar and loading widgets
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

const mdConverter = new showdown.Converter()

const { $backend } = useNuxtApp()
const metadata = ref(null)
const pagetitle = ref("")
const pagecontent = ref("")

async function getContent() {
  showLoading(true)
  try {
    const reply = await $backend("filestore", "anon_get_file", {
      group: "pages",
      name: "index.md",
    })
    metadata.value = useMarkdown(reply.data).metadata
    updateLocale(locale.value)
  } catch (error) {
    showSnackbar("Page loading error")
  } finally {
    showLoading(false)
  }
}

function updateLocale(l) {
  console.log("updating locale", l)
  if (process.client) {
    localStorage.setItem("locale", l)
  }
  locale.value = l
  pagetitle.value = metadata.value["title_" + l]
  pagecontent.value = mdConverter.makeHtml(metadata.value["content_" + l])
}

watch(locale, (nl, ol) => updateLocale(nl))

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  getContent()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>{{ pagetitle }}</h1>
    <div v-html="pagecontent" class="markdowncontent"></div>
  </v-container>
</template>

<style scoped>
h1:after {
  content: " ";
  display: block;
  border: 1px solid #aaa;
  margin-bottom: 1em;
}

ul {
  padding-left: 1rem;
}

.v-card-title {
  white-space: normal;
}
</style>
