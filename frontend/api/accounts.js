import axios from "axios";

const prefix = "/api/v1/accounts";
export default {
  login: async function(options) {
    return await axios.post(`${prefix}/anon/login`, options);
  },
};
