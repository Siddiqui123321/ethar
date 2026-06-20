import React from 'react'
import api from '../api'

export default function Orders(){
  const [orders, setOrders] = React.useState([])
  const [customers, setCustomers] = React.useState([])
  const [products, setProducts] = React.useState([])
  const [form, setForm] = React.useState({customer_id:'', items:[]})

  React.useEffect(()=>{fetchAll()},[])
  function fetchAll(){
    api.orders.list().then(r=>setOrders(r.data)).catch(()=>{})
    api.customers.list().then(r=>setCustomers(r.data)).catch(()=>{})
    api.products.list().then(r=>setProducts(r.data)).catch(()=>{})
  }

  function addItem(){
    setForm({...form, items: [...form.items, {product_id:'', quantity:1}]})
  }

  function updateItem(idx, key, value){
    const items = [...form.items]
    items[idx][key]=value
    setForm({...form, items})
  }

  function create(e){
    e.preventDefault()
    // coerce types
    const payload = {customer_id: parseInt(form.customer_id), items: form.items.map(i=>({product_id: parseInt(i.product_id), quantity: parseInt(i.quantity)}))}
    api.orders.create(payload).then(()=>{setForm({customer_id:'', items:[]});fetchAll()}).catch(err=>alert(err.response?.data?.detail||err.message))
  }

  return (
    <div>
      <h2>Orders</h2>
      <form onSubmit={create} className="card">
        <select value={form.customer_id} onChange={e=>setForm({...form, customer_id:e.target.value})}>
          <option value="">Select customer</option>
          {customers.map(c=> <option value={c.id} key={c.id}>{c.full_name}</option>)}
        </select>
        <div>
          <button type="button" onClick={addItem}>Add Item</button>
        </div>
        {form.items.map((it, idx)=> (
          <div key={idx} style={{marginTop:8}}>
            <select value={it.product_id} onChange={e=>updateItem(idx,'product_id', e.target.value)}>
              <option value="">Select product</option>
              {products.map(p=> <option value={p.id} key={p.id}>{p.name} ({p.quantity} available)</option>)}
            </select>
            <input type="number" value={it.quantity} onChange={e=>updateItem(idx,'quantity', e.target.value)} style={{width:80, marginLeft:8}} />
          </div>
        ))}
        <div style={{marginTop:8}}>
          <button type="submit">Create Order</button>
        </div>
      </form>

      <div className="list">
        {orders.map(o=> (
          <div key={o.id} className="card">
            <strong>Order #{o.id}</strong> — Customer {o.customer_id} — ${o.total_amount}
            <div>
              {o.items.map(it=> <div key={it.id}>{it.product_id} x{it.quantity} @ ${it.unit_price}</div>)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
