import axios from "axios"

const prefix = "/api/v1/registration"

export default {
  lookup_idbel: async function (options) {
    const { idbel } = options
    return await axios.get(`${prefix}/idbel/${idbel}`)
  },
  lookup_idfide: async function (options) {
    const { idfide } = options
    return await axios.get(`${prefix}/idfide/${idfide}`)
  },
  create_registration: async function (options) {
    const { registrationIn } = options
    return await axios.post(`${prefix}/bjk`, registrationIn)
  },
  confirm_registration: async function (options) {
    const { idsub } = options
    return await axios.post(`${prefix}/confirm/${idsub}`)
  },
  upload_photo: async function (options) {
    const { idsub, photo } = options
    return await axios.post(`${prefix}/photo/${idsub}`, { photo })
  },
  get_registrations: async function () {
    return await axios.get(`${prefix}/bjk`)
  },
  mgmt_get_registration: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/bjk/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_update_registration: async function (options) {
    const { id, reg, token } = options
    return await axios.put(`${prefix}/bjk/${id}`, reg, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_xls_registrations: async function (options) {
    const { token } = options
    return await axios.get(`${prefix}/cmd/xls_registration`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },  
}
