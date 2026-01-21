import axios from 'axios'
import { useConfigStore } from '@/store/config'
import { useLogStore } from '@/store/log'

const configStore = useConfigStore()
const logStore = useLogStore()

const apiClient = axios.create({
  baseURL: configStore.apiBaseUrl,
  timeout: 60000, // 60秒超时
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    logStore.addLog({
      level: 'info',
      message: `API Request: ${config.method?.toUpperCase()} ${config.url}`,
      details: { params: config.params, data: config.data },
    })
    return config
  },
  (error) => {
    logStore.addLog({
      level: 'error',
      message: `API Request Error: ${error.message}`,
      details: { error },
    })
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    logStore.addLog({
      level: 'info',
      message: `API Response: ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`,
      details: { data: response.data },
    })
    return response
  },
  (error) => {
    logStore.addLog({
      level: 'error',
      message: `API Response Error: ${error.message}`,
      details: { error, response: error.response?.data },
    })
    return Promise.reject(error)
  }
)

export default apiClient