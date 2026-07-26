import apiClient from './index'

export function getHistory() {
  return apiClient.get('/history').then(res => res.data)
}