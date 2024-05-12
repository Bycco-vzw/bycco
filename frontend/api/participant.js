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
  },
  mgmt_get_participant_vk: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/vk/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_update_participant_vk: async function (options) {
    const { id, participant, token } = options
    return await axios.put(`${prefix}/vk/${id}`, { participant }, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  get_participants_bjk: async function (options) {
    const { enabled } = options
    if (enabled) {
      return await axios.get(`${prefix}/bjk?enabled=1`)
    }
    else {
      return await axios.get(`${prefix}/bjk`)
    }
  },
  mgmt_import_enrollments_bjk: async function (options) {
    const { token } = options
    return await axios.post(`${prefix}/import/enrollments/bjk`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_participant_bjk: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/bjk/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_update_participant_bjk: async function (options) {
    const { id, participant, token } = options
    return await axios.put(`${prefix}/bjk/${id}`, participant, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_import_enrollments_bjk: async function (options) {
    const { token } = options
    return await axios.post(`${prefix}/import/enrollments/bjk`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  upload_photo_bjk: async function (options) {
    const { id, photo } = options
    return await axios.post(`${prefix}/photo/bjk/${id}`, { photo })
  },
}