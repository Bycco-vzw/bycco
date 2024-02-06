<script setup>
import { ref, watch } from 'vue'
import showdown from 'showdown'
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()

const mdConverter = new showdown.Converter()

const { $backend } = useNuxtApp()
const metadata = ref(null)
const pagetitle = ref("")
const pagecontent = ref("")

async function getContent() {
  try {
    const reply = await $backend('filestore', 'anon_get_file', {
      group: 'pages',
      name: 'enrollment.md'
    })
    metadata.value = useMarkdown(reply.data).metadata
    updateLocale(locale.value)
  }
  catch (error) {
    console.log('failed')
  }
}

function updateLocale(l) {
  console.log('updating locale', l)
  pagetitle.value = metadata.value["title_" + l]
  pagecontent.value = mdConverter.makeHtml(metadata.value["content_" + l])
}

watch(locale, (nl, ol) => updateLocale(nl))

onMounted(() => {
  getContent()
})

</script>

<template>
  <v-container>
    <h1>{{ pagetitle }}</h1>
    <div v-html="pagecontent" class="markdowncontent"></div>
  </v-container>
</template>