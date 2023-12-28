<script setup>
const { locale, setLocale } = useI18n()
const localePath = useLocalePath()

</script>

<template>
  <div>
    <v-toolbar dark text class="blue-grey">
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
      <v-list-item to="/" :title=" $t('Home')" prepend-icon="home" / >
      </v-list-item>
      <v-list-group no-action>
        <template #activator="{ props }">
          <v-list-item :title=" $t('Tournament')" />
        </template>
        <v-list-item to="/enrollment" :title="$t('Enrollment')" />
        <v-list-item to="/participants" :title="$t('Participants')" />>
        <v-list-item to="/toernooireglement" :title="$t('Tournament Rules')" />
        <v-list-item to="/live" title="Live" />
        <v-list-item to="/pgn" title="PGN" />
      </v-list-group>
      <!-- <v-list-group no-action>
        <template #activator>
          <v-list-item-content>
            <v-list-item-title>Info</v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item to="/huishoudreglement">
          <v-list-item-content>
            {{ $t('Internal Regulations') }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/covid">
          <v-list-item-content>
            Covid 19
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
      <v-list-group no-action>
        <template #activator>
          <v-list-item-content>
            <v-list-item-title>{{ $t('Lodging') }}</v-list-item-title>
          </v-list-item-content>
        </template>
        <v-list-item to="/verblijf">
          <v-list-item-content>
            {{ $t('Lodging') }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/restaurant">
          <v-list-item-content>
            {{ $t('Catering') }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/toewijzingverblijf">
          <v-list-item-content>
            {{ $t('Reservation') }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/lodging">
          <v-list-item-content>
            {{ $t('Reservation wizard') }}
          </v-list-item-content>
        </v-list-item>
      </v-list-group> -->
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
