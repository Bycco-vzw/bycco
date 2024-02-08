import axios from 'axios'

const prefix = '/api/v1/paymentrequest'

export default {
  mgmt_create_lodging_pr: async function (options) {
    const { token, id } = options
    return await axios.post(`${prefix}/lodging_pr/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
}
