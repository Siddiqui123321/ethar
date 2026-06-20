import React from 'react'
import api from '../api'

export default function Products(){
  const [products, setProducts] = React.useState([])
  const [form, setForm] = React.useState({name:'',sku:'',price:'',quantity:''})
  const [errors, setErrors] = React.useState([])
  const [message, setMessage] = React.useState('')

  React.useEffect(()=>{fetchList()},[])
  function fetchList(){
    api.products.list().then(r=>setProducts(r.data)).catch(()=>{})
  }

  function validateForm(){
    const errs = []
    if(!form.name || !form.name.trim()) errs.push('Name is required')
    if(!form.sku || !form.sku.trim()) errs.push('SKU is required')
    const price = parseFloat(form.price)
    if(Number.isNaN(price) || price < 0) errs.push('Price must be a non-negative number')
    const qty = parseInt(form.quantity || '0')
    if(Number.isNaN(qty) || qty < 0) errs.push('Quantity must be a non-negative integer')
    return errs
  }

  async function create(e){
    e.preventDefault()
    setMessage('')
    const errs = validateForm()
    if(errs.length){ setErrors(errs); return }
    setErrors([])
    const payload = {name: form.name.trim(), sku: form.sku.trim(), price: parseFloat(form.price), quantity: parseInt(form.quantity || '0')}
    try{
      await api.products.create(payload)
      setMessage('Product added')
      setForm({name:'',sku:'',price:'',quantity:''})
      fetchList()
    }catch(err){
      setErrors([err.response?.data?.detail || err.message || 'Failed to create product'])
    }
  }

  function remove(id){
    if(!confirm('Delete product?')) return
    api.products.del(id).then(()=>{setMessage('Product deleted');fetchList()}).catch(err=>setErrors([err.response?.data?.detail||err.message]))
  }

  return (
    <div>
      <h2>Products</h2>
      <form onSubmit={create} className="card">
        {message && <div style={{color:'green'}}>{message}</div>}
        {errors.length > 0 && <div style={{color:'red'}}>
          {errors.map((e,i)=><div key={i}>{e}</div>)}
        </div>}
        <input placeholder="Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} />
        <input placeholder="SKU" value={form.sku} onChange={e=>setForm({...form,sku:e.target.value})} />
        <input type="number" step="0.01" placeholder="Price" value={form.price} onChange={e=>setForm({...form,price:e.target.value})} />
        <input type="number" placeholder="Quantity" value={form.quantity} onChange={e=>setForm({...form,quantity:e.target.value})} />
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
