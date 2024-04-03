import axios from 'axios'

const prefix = '/api/v1/page'

export default {
  checkin: async function (options) {
    const { token, instance } = options
    return await axios.post(`${prefix}/checkin/${instance}`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  checkout: async function (options) {
    const { token, instance } = options
    return await axios.post(`${prefix}/checkout/${instance}`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
}
