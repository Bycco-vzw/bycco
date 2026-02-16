import axios from "axios"

const prefix = "/api/v1/guest"

export default {
  mgmt_read_csv: async function (options) {
    const { token, idbel, cat } = options
    return await axios.post(
      `${prefix}/read_csv`,
      {},
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    )
  },
}
