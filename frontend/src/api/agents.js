import apiClient from './index'

export function listAgents() {
  return apiClient.get('/agents').then(res => res.data)
}

export function createAgent(data) {
  return apiClient.post('/agents', data).then(res => res.data)
}

export function getAgent(id) {
  return apiClient.get(`/agents/${id}`).then(res => res.data)
}

export function updateAgent(id, data) {
  return apiClient.put(`/agents/${id}`, data).then(res => res.data)
}

export function deleteAgent(id) {
  return apiClient.delete(`/agents/${id}`).then(res => res.data)
}