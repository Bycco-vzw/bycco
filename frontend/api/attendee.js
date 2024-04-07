import axios from 'axios'

const prefix = '/api/v1/attendee'

export default {
  mgmt_add_attendee_vk: async function (options) {
    const { attendee, token } = options
    return await axios.post(`${prefix}/vk`, attendee, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_attendees_vk: async function (options) {
    const { token } = options
    return await axios.get(`${prefix}/vk`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_attendee_vk: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/vk/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_update_attendee_vk: async function (options) {
    const { id, attendee, token } = options
    return await axios.put(`${prefix}/vk/${id}`, attendee, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
}