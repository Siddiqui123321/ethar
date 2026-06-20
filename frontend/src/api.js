import axios from 'axios'

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000')

const client = axios.create({ baseURL: API_URL })

export default {
  products: {
    list: () => client.get('/products/'),
    create: (p) => client.post('/products/', p),
    get: (id) => client.get(`/products/${id}`),
    update: (id, data) => client.put(`/products/${id}`, data),
    del: (id) => client.delete(`/products/${id}`),
  },
  customers: {
    list: () => client.get('/customers/'),
    create: (c) => client.post('/customers/', c),
    get: (id) => client.get(`/customers/${id}`),
    del: (id) => client.delete(`/customers/${id}`),
  },
  orders: {
    list: () => client.get('/orders/'),
    create: (o) => client.post('/orders/', o),
    get: (id) => client.get(`/orders/${id}`),
    del: (id) => client.delete(`/orders/${id}`),
  }
}
