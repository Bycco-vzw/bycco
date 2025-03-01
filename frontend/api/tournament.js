import axios from "axios"

const prefix = "/api/v1/tournament"

export default {
  // lodging
  mgmt_upload_json: async function (options) {
    const { token, trn } = options
    return await axios.post(`${prefix}/json`, trn, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_set_unofficial_result: async function (options) {
    const { token, ur } = options
    return await axios.post(`${prefix}/unofficial_result`, ur, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
}
