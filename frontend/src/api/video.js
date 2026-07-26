import apiClient from './index'

export function uploadVideo(file) {
  const formData = new FormData()
  formData.append('file', file)
  return apiClient.post('/video/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }).then(res => res.data)
}

export function getTaskStatus(taskId) {
  return apiClient.get(`/video/status/${taskId}`).then(res => res.data)
}