import { createI18n } from 'vue-i18n'
import nl from "@/lang/nl.json"
import fr from "@/lang/fr.json"
import de from "@/lang/de.json"
import en from "@/lang/en.json"

export default defineNuxtPlugin(({ vueApp }) => {
  const i18n = createI18n({
    legacy: false,
    globalInjection: true,
    locale: 'nl',
    messages: {
      nl,
      fr,
      de,
      en,
    }
  })
  vueApp.use(i18n)
})