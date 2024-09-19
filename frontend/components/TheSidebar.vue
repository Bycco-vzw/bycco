<script setup>
import { useI18n } from "vue-i18n"
const { t, locale } = useI18n()

function setLocale(l) {
  console.log("setting locale", l)
  locale.value = l
}

function livegames_vk() {
  window.open(
    "https://lichess.org/broadcast/flemish-championship-2024--closed/round-1/YKpRRcUf",
    "_live"
  )
}

function rules_bjk() {
  window.open(
    "https://drive.google.com/file/d/1U7VycNN8ObdzqptAt1TrpIWJDPZoEo-q/view",
    "_rules"
  )
}
</script>

<template>
  <div>
    <v-toolbar dark text class="bg-blue-grey">
      <v-list>
        <v-list-item title="Menu" />
      </v-list>
    </v-toolbar>
    <div class="bm-blue-grey-darken-1">
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('nl')"
        >NL</v-btn
      >
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('fr')"
        >FR</v-btn
      >
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('de')"
        >DE</v-btn
      >
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('en')"
        >EN</v-btn
      >
    </div>
    <v-list nav class="bm-blue-grey-darken-1">
      <v-list-item to="/" :title="t('Home')" />

      <v-list-group no-action>
        <template #activator="{ props }">
          <v-list-item v-bind="props" :title="t('BYC 2025')" />
        </template>
        <v-list-item to="schedule" :title="t('Game schedule')" />
        <!-- <v-list-item @click="rules_bjk" :title="t('Tournament Rules')" />
        <v-list-item to="/trn_u8" title="U8" />
        <v-list-item to="/trn_u10" title="U10" />
        <v-list-item to="/trn_u12" title="U12" />
        <v-list-item to="/trn_u14" title="U14" />
        <v-list-item to="/trn_u16" title="U16" />
        <v-list-item to="/trn_u18" title="U18" />
        <v-list-item to="/trn_u20" title="U20" /> -->
      </v-list-group>
      <v-list-group no-action>
        <template #activator="{ props }">
          <v-list-item v-bind="props" title="Info" />
        </template>
        <v-list-item to="/stay" :title="t('stay.stay')" />
        <v-list-item to="/catering" :title="t('stay.catering')" />
        <v-list-item to="/reservation" :title="t('stay.reservation')" />
        <!-- <v-list-item @click="livegames_" title="Live" /> -->
      </v-list-group>
    </v-list>
  </div>
</template>

<style scoped>
.btn-language.v-btn {
  min-width: 0;
  color: white;
}

.v-list-group--active.primary--text {
  color: white !important;
}

.menucell {
  width: 60px;
}

.left72 {
  padding-left: 72px;
}
</style>
