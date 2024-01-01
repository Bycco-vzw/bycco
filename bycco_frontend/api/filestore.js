import axios from 'axios'

const prefix = '/api/v1/filestore'
export default {
  anon_get_file: async function (options) {
    const { group, name } = options
    return await axios.get(`${prefix}/anon/file`, {
      params: { group, name },
    })
  },
  anon_get_filelist: async function (options) {
    const { group } = options
    return await axios.get(`${prefix}/anon/files`, {
      params: { group },
    })
  },
}
