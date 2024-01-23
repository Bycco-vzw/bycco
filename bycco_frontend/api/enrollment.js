import axios from 'axios'

const prefix = '/api/v1/enrollment'

export default {
  lookup_idbel: async function (options) {
    const { idbel } = options
    return await axios.get(`${prefix}/idbel/${idbel}`)
  },
  lookup_idfide: async function (options) {
    const { idfide } = options
    return await axios.get(`${prefix}/idfide/${idfide}`)
  },
}