import React from 'react'
import Products from './pages/Products'
import Customers from './pages/Customers'
import Orders from './pages/Orders'
import Dashboard from './pages/Dashboard'

export default function App(){
  const [view, setView] = React.useState('dashboard')
  return (
    <div className="container">
      <header>
        <h1>Inventory & Orders</h1>
        <nav>
          <button onClick={()=>setView('dashboard')}>Dashboard</button>
          <button onClick={()=>setView('products')}>Products</button>
          <button onClick={()=>setView('customers')}>Customers</button>
          <button onClick={()=>setView('orders')}>Orders</button>
        </nav>
      </header>
      <main>
        {view === 'dashboard' && <Dashboard />}
        {view === 'products' && <Products />}
        {view === 'customers' && <Customers />}
        {view === 'orders' && <Orders />}
      </main>
    </div>
  )
}
