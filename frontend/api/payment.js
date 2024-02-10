import axios from 'axios'

const prefix = '/api/v1/payment'

export default {
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
  mgmt_email_pr: async function (options) {
    const { token, id, prq } = options
    return await axios.post(`${prefix}/email_pr/${id}`, prq, {
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
  mgmt_update_lodging_pr: async function (options) {
    const { token, id, prq } = options
    return await axios.put(`${prefix}/lodging_pr/${id}`, prq, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
}
