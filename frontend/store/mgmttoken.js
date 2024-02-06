// stores/mgmttoken.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useMgmtTokenStore = defineStore("mgmttoken", () => {
  const token = ref(null);
  function updateToken(newtoken) {
    token.value = newtoken;
  }
  function startup() {
    if (!token.value) {
      token.value = window.localStorage.getItem("idtoken");
    }
  }
  return { token, updateToken, startup };
});
