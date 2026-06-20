import React from 'react'
import api from '../api'

export default function Dashboard(){
  const [products, setProducts] = React.useState([])
  const [customers, setCustomers] = React.useState([])
  const [orders, setOrders] = React.useState([])

  React.useEffect(()=>{load()},[])
  function load(){
    api.products.list().then(r=>setProducts(r.data)).catch(()=>{})
    api.customers.list().then(r=>setCustomers(r.data)).catch(()=>{})
    api.orders.list().then(r=>setOrders(r.data)).catch(()=>{})
  }

  const lowStock = products.filter(p=>p.quantity <= 5)

  return (
    <div>
      <h2>Dashboard</h2>
      <div className="card">
        <div>Total products: {products.length}</div>
        <div>Total customers: {customers.length}</div>
        <div>Total orders: {orders.length}</div>
      </div>

      <h3>Low stock products</h3>
      <div className="list">
        {lowStock.map(p=> <div key={p.id} className="card">{p.name} — {p.quantity}</div>)}
      </div>
    </div>
  )
}
