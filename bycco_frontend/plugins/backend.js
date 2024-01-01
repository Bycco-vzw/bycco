import axios from 'axios'
import filestore from '@/api/filestore'

axios.defaults.withCredentials = true

const error_messages = {
  401: 'Authentication required',
  403: 'Permission denied',
  404: 'Not found',
  500: 'General server error',
  503: 'Could not connect to database server',
  600: 'Connection issue: server unreachable',
  700: 'You triggered a bug.  Please inform the webmaster.',
  Forbidden: 'Permission denied',
  WrongUsernamePasswordCombination:
    'Wrong combination of username and password',
}

axios.interceptors.response.use(
  (response) => {
    return Promise.resolve({
      data: response.data,
      headers: response.headers,
    })
  },
  (error) => {
    if (error.response) {
      const detail = error.response.data.detail
      console.warn('Axios', error.response.status, detail, error.request)
      console.log('detail', detail)
      console.log('status code', error.response.status)
      return Promise.reject({
        code: error.response.status,
        headers: error.response.headers,
        message: detail
          ? error_messages[detail]
          : error_messages[error.response.status],
      })
    }
    if (error.request) {
      console.warn('Axios', 'No response received', error.request)
      return Promise.reject({
        code: 600,
        message: error_messages[600],
      })
    }
    console.warn('Axios', 'No request sent', error.message)
    return Promise.reject({
      code: 700,
      message: error_messages[700],
    })
  },
)

const factories = {
  filestore,
}

export default defineNuxtPlugin((nuxtApp) => {
  const runtimeConfig = useRuntimeConfig()
  axios.defaults.baseURL = runtimeConfig.public.apiUrl
  return {
    provide: {
      backend: async function (fact, method, options) {
        const f = factories[fact][method]
        if (!f) {
          console.log('$backend method not existing', fact, method)
        }
        return await f(options)
      },
    },
  }
})
