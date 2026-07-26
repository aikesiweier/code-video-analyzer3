import apiClient from './index'

export function register(data) {
  return apiClient.post('/register', data).then(res => res.data)
}

export function login(data) {
  return apiClient.post('/login', data).then(res => res.data)
}

export function getMe() {
  return apiClient.get('/me').then(res => res.data)
}