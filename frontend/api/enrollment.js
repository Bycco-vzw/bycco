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
  create_enrollment_vk: async function (options) {
    const { enrollmentVkIn } = options
    return await axios.post(`${prefix}/vk`, enrollmentVkIn)
  },
  create_enrollment_bjk: async function (options) {
    const { enrollmentIn } = options
    return await axios.post(`${prefix}/bjk`, enrollmentIn)
  },
  confirm_enrollment: async function (options) {
    const { idsub } = options
    return await axios.post(`${prefix}/confirm/${idsub}`)
  },
  upload_photo: async function (options) {
    const { idsub, photo } = options
    return await axios.post(`${prefix}/photo/${idsub}`, { photo })
  },
  get_enrollments_vk: async function () {
    return await axios.get(`${prefix}/vk`)
  },
  get_enrollments_bjk: async function () {
    return await axios.get(`${prefix}/bjk`)
  },
  mgmt_update_enrollment_vk: async function (options) {
    return await axios.post(`${prefix}/vk`)
  }
}