import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Upload contract
export const uploadContract = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

// Get clauses
export const getClauses = async (clauseType = null, search = null) => {
  const params = {}
  if (clauseType) params.clause_type = clauseType
  if (search) params.search = search
  
  const response = await api.get('/api/clauses', { params })
  return response.data
}

// Get single clause
export const getClause = async (clauseId) => {
  const response = await api.get(`/api/clauses/${clauseId}`)
  return response.data
}

// Get comparison
export const getComparison = async () => {
  const response = await api.get('/api/comparison')
  return response.data
}

// Get risks
export const getRisks = async () => {
  const response = await api.get('/api/risks')
  return response.data
}

// Get time frames
export const getTimeFrames = async () => {
  const response = await api.get('/api/time-frames')
  return response.data
}
