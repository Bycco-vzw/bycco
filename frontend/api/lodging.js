import axios from 'axios'

const prefix = '/api/v1/lodging'
const roomprefix = '/api/v1/room'

export default {
  make_reservation: async function (options) {
    const { lodgingIn } = options
    return await axios.post(`${prefix}/cmd/make_reservation`, lodgingIn)
  },
  mgmt_assign_room: async function (options) {
    const { token, id, roomnr } = options
    return await axios.post(`${prefix}/cmd/assignroom/${id}/${roomnr}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_unassign_room: async function (options) {
    const { token, id, roomnr } = options
    return await axios.delete(`${prefix}/cmd/assignroom/${id}/${roomnr}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_reservations: async function (options) {
    const { token } = options
    return await axios.get(`${prefix}/reservation`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_reservation: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/reservation/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_update_reservation: async function (options) {
    const { id, token, reservation } = options
    return await axios.put(`${prefix}/reservation/${id}`, reservation, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  },
  mgmt_get_free_rooms: async function (options) {
    const { token, roomtype } = options
    return await axios.get(`${roomprefix}/freeroom/${roomtype}`, {
      headers: {
        Authorization: "Bearer " + token,
      }
    })
  }
}
