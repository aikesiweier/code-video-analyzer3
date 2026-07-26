import apiClient from './index'

export function getReport(taskId) {
  return apiClient.get(`/report/${taskId}`).then(res => res.data)
}