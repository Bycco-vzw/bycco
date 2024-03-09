<script setup>
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()

function setLocale(l) {
  console.log('setting locale', l)
  locale.value = l
}


</script>

<template>
  <div>
    <v-toolbar dark text class="bg-blue-grey">
      <v-list>
        <v-list-item title="Menu" />
      </v-list>
    </v-toolbar>
    <v-divider />
    <div class="bm-blue-grey-darken-1">
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('nl')">NL</v-btn>
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('fr')">FR</v-btn>
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('de')">DE</v-btn>
      <v-btn variant="text" class="btn-language hover-darker" @click="setLocale('en')">EN</v-btn>
    </div>
    <v-list nav class="bm-blue-grey-darken-1">
      <v-list-item to="/" :title="t('Home')" />
      <v-list-group no-action>
        <template #activator="{ props }">
          <v-list-item v-bind="props" :title="t('Tournament')" />
        </template>
        <v-list-item to="/vk2024" title="Info" />
        <v-list-item to="/gameschedule" :title="t('Game schedule')" />
        <v-list-item to="/enrollmenttool" :title="t('Enrollment')" />
        <v-list-item to="/participants_vk" :title="t('Participants')" />
      </v-list-group>
      <v-list-group no-action>

        <template #activator="{ props }">
          <v-list-item v-bind="props" :title="t('Lodging')" />
        </template>
        <v-list-item to="/lodging" :title="t('Lodging') + ' 2024'" />
        <v-list-item to="/catering" :title="t('Catering')" />
        <v-list-item to="/reservation" :title="t('Reservation')" />
        <v-list-item to="/reservationtool" :title="t('Reservation tool')" />
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
