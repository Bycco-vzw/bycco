import axios from 'axios'

const prefix = '/api/v1/lodging'
export default {
  make_reservation: async function (options) {
    const { lodgingIn } = options
    return await axios.post(`${prefix}/cmd/make_reservation`, lodgingIn)
  },
}
