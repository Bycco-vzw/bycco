import axios from 'axios'

const prefix = '/api/v1/participant'

export default {
  get_participants_vk: async function () {
    return await axios.get(`${prefix}/vk`)
  },
  mgmt_import_enrollments_vk: async function (options) {
    const { token } = options
    return await axios.post(`${prefix}/import/enrollments/vk`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  }
}