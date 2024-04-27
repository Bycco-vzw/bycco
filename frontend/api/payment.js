import axios from 'axios'

const prefix = '/api/v1/payment'

export default {
  // lodging
  mgmt_create_lodging_pr: async function (options) {
    const { token, id } = options
    return await axios.post(`${prefix}/lodging_pr/${id}`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_delete_lodging_pr: async function (options) {
    const { token, id } = options
    return await axios.delete(`${prefix}/lodging_pr/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_update_lodging_pr: async function (options) {
    const { token, id, prq } = options
    return await axios.put(`${prefix}/lodging_pr/${id}`, prq, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },

  // particpant vk
  mgmt_create_participant_vk_pr: async function (options) {
    const { token, id } = options
    return await axios.post(`${prefix}/participant_vk_pr/${id}`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_create_participants_vk_pr: async function (options) {
    const { token } = options
    return await axios.post(`${prefix}/participant_vk_pr`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_delete_participant_vk_pr: async function (options) {
    const { token, id } = options
    return await axios.delete(`${prefix}/participant_vk_pr/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_update_participant_vk_pr: async function (options) {
    const { token, id, prq } = options
    return await axios.put(`${prefix}/participant_vk_pr/${id}`, prq, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },

  // particpant bjk
  mgmt_create_participant_bjk_pr: async function (options) {
    const { token, id } = options
    return await axios.post(`${prefix}/participant_bjk_pr/${id}`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_create_participants_bjk_pr: async function (options) {
    const { token } = options
    return await axios.post(`${prefix}/participant_bjk_pr`, {}, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_delete_participant_bjk_pr: async function (options) {
    const { token, id } = options
    return await axios.delete(`${prefix}/participant_bjk_pr/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_update_participant_bjk_pr: async function (options) {
    console.log('calling api update pr bjk', options)
    const { token, id, prq } = options
    return await axios.put(`${prefix}/participant_bjk_pr/${id}`, prq, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },


  // general
  mgmt_email_pr: async function (options) {
    const { token, id, prq } = options
    return await axios.post(`${prefix}/email_pr/${id}`, prq, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_email_prs: async function (options) {
    const { token, id, prq } = options
    return await axios.post(`${prefix}/email_pr`, null, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_paymentrequests: async function (options) {
    const { token } = options
    return await axios.get(`${prefix}/pr`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_paymentrequest: async function (options) {
    const { token, id } = options
    return await axios.get(`${prefix}/pr/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
}
