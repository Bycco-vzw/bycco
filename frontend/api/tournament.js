import axios from 'axios'

const prefix = '/api/v1/tournament'

export default {
  // lodging
  mgmt_upload_jsonfile: async function (options) {
    const { token, trn } = options
    return await axios.post(`${prefix}/json`, trn, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
}
