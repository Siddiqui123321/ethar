import React from 'react'
import api from '../api'

export default function Customers(){
  const [customers, setCustomers] = React.useState([])
  const [form, setForm] = React.useState({full_name:'',email:'',phone:''})
  const [errors, setErrors] = React.useState([])
  const [message, setMessage] = React.useState('')

  React.useEffect(()=>{fetchList()},[])
  function fetchList(){
    api.customers.list().then(r=>setCustomers(r.data)).catch(()=>{})
  }

  function validate(){
    const errs = []
    if(!form.full_name || !form.full_name.trim()) errs.push('Full name is required')
    const emailRe = /^\S+@\S+\.\S+$/
    if(!form.email || !emailRe.test(form.email)) errs.push('Valid email is required')
    return errs
  }

  async function create(e){
    e.preventDefault()
    setMessage('')
    const errs = validate()
    if(errs.length){ setErrors(errs); return }
    setErrors([])
    try{
      await api.customers.create(form)
      setMessage('Customer added')
      setForm({full_name:'',email:'',phone:''})
      fetchList()
    }catch(err){
      setErrors([err.response?.data?.detail||err.message])
    }
  }

  function remove(id){
    if(!confirm('Delete customer?')) return
    api.customers.del(id).then(()=>{setMessage('Customer deleted');fetchList()}).catch(err=>setErrors([err.response?.data?.detail||err.message]))
  }

  return (
    <div>
      <h2>Customers</h2>
      <form onSubmit={create} className="card">
        {message && <div style={{color:'green'}}>{message}</div>}
        {errors.length > 0 && <div style={{color:'red'}}>{errors.map((e,i)=><div key={i}>{e}</div>)}</div>}
        <input placeholder="Full name" value={form.full_name} onChange={e=>setForm({...form,full_name:e.target.value})} />
        <input placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} />
        <input placeholder="Phone" value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})} />
        <button type="submit">Add</button>
      </form>

      <div className="list">
        {customers.map(c=> (
          <div key={c.id} className="card">
            <strong>{c.full_name}</strong> — {c.email} — {c.phone}
            <div style={{float:'right'}}>
              <button onClick={()=>remove(c.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
