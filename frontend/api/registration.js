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
  create_registration_vk: async function (options) {
    const { registrationVkIn } = options
    return await axios.post(`${prefix}/vk`, registrationVkIn)
  },
  create_registration_bjk: async function (options) {
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
  get_registrations_vk: async function () {
    return await axios.get(`${prefix}/vk`)
  },
  get_registrations_vk: async function () {
    return await axios.get(`${prefix}/vk`)
  },
  get_registrations_bjk: async function () {
    return await axios.get(`${prefix}/bjk`)
  },
  mgmt_get_registration_bjk: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/bjk/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_get_registration_vk: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/vk/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_update_registration_bjk: async function (options) {
    const { id, reg, token } = options
    return await axios.put(`${prefix}/bjk/${id}`, reg, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_update_registration_vk: async function (options) {
    const { id, enr, token } = options
    return await axios.put(`${prefix}/vk/${id}`, enr, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
}
