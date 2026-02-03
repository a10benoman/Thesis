import axios from 'axios'

const base = (import.meta.env.VITE_API_BASE as string) || 'http://localhost:8000'
const api = axios.create({ baseURL: base })

export async function listProducts() {
  const r = await api.get('/products/')
  return r.data
}

export async function createProduct(payload: { sku: string; name: string }) {
  const r = await api.post('/products/', payload)
  return r.data
}

export async function createMovement(product_id: number, type: string, quantity: number) {
  const r = await api.post('/movements/', null, { params: { product_id, type, quantity } })
  return r.data
}
