import React from 'react'
import api from '../api'

export default function Products(){
  const [products, setProducts] = React.useState([])
  const [form, setForm] = React.useState({name:'',sku:'',price:0,quantity:0})

  React.useEffect(()=>{fetchList()},[])
  function fetchList(){
    api.products.list().then(r=>setProducts(r.data)).catch(()=>{})
  }

  function create(e){
    e.preventDefault()
    api.products.create(form).then(()=>{setForm({name:'',sku:'',price:0,quantity:0});fetchList()}).catch(err=>alert(err.response?.data?.detail||err.message))
  }

  function remove(id){
    if(!confirm('Delete product?')) return
    api.products.del(id).then(()=>fetchList()).catch(err=>alert(err.response?.data?.detail||err.message))
  }

  return (
    <div>
      <h2>Products</h2>
      <form onSubmit={create} className="card">
        <input placeholder="Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} />
        <input placeholder="SKU" value={form.sku} onChange={e=>setForm({...form,sku:e.target.value})} />
        <input type="number" placeholder="Price" value={form.price} onChange={e=>setForm({...form,price:parseFloat(e.target.value)})} />
        <input type="number" placeholder="Quantity" value={form.quantity} onChange={e=>setForm({...form,quantity:parseInt(e.target.value||0)})} />
        <button type="submit">Add</button>
      </form>

      <div className="list">
        {products.map(p=> (
          <div key={p.id} className="card">
            <strong>{p.name}</strong> — {p.sku} — ${p.price} — {p.quantity} in stock
            <div style={{float:'right'}}>
              <button onClick={()=>remove(p.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
