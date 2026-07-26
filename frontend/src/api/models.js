import apiClient from './index'

export function listModels() {
  return apiClient.get('/models').then(res => res.data)
}

export function createModel(data) {
  return apiClient.post('/models', data).then(res => res.data)
}

export function updateModel(id, data) {
  return apiClient.put(`/models/${id}`, data).then(res => res.data)
}

export function deleteModel(id) {
  return apiClient.delete(`/models/${id}`).then(res => res.data)
}