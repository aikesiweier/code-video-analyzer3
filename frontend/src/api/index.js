import axios from 'axios'
import store from '../store'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 300000
})

// 请求拦截器：自动附加 token
apiClient.interceptors.request.use(config => {
  const token = store.state.token || localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => Promise.reject(error))

// 可选：响应拦截器，处理 401 等
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      store.commit('clearUser')
      // 跳转到登录页，可根据需要取消注释
      // window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient