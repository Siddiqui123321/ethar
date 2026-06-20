import React from 'react'
import api from '../api'

export default function Customers(){
  const [customers, setCustomers] = React.useState([])
  const [form, setForm] = React.useState({full_name:'',email:'',phone:''})

  React.useEffect(()=>{fetchList()},[])
  function fetchList(){
    api.customers.list().then(r=>setCustomers(r.data)).catch(()=>{})
  }

  function create(e){
    e.preventDefault()
    api.customers.create(form).then(()=>{setForm({full_name:'',email:'',phone:''});fetchList()}).catch(err=>alert(err.response?.data?.detail||err.message))
  }

  function remove(id){
    if(!confirm('Delete customer?')) return
    api.customers.del(id).then(()=>fetchList()).catch(err=>alert(err.response?.data?.detail||err.message))
  }

  return (
    <div>
      <h2>Customers</h2>
      <form onSubmit={create} className="card">
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
