import React, { useEffect, useState } from 'react'
import { listProducts, createProduct, createMovement } from './api'

export default function App() {
  const [products, setProducts] = useState<any[]>([])
  const [sku, setSku] = useState('')
  const [name, setName] = useState('')

  useEffect(() => {
    refresh()
  }, [])

  async function refresh() {
    const p = await listProducts()
    setProducts(p)
  }

  async function onCreate(e: React.FormEvent) {
    e.preventDefault()
    await createProduct({ sku, name })
    setSku('')
    setName('')
    refresh()
  }

  async function onQuickSale(productId: number) {
    await createMovement(productId, 'OUT', 1)
    refresh()
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Inventory ML Demo</h1>

      <form onSubmit={onCreate} className="mb-4">
        <input placeholder="SKU" value={sku} onChange={(e) => setSku(e.target.value)} className="mr-2" />
        <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} className="mr-2" />
        <button type="submit">Create Product</button>
      </form>

      <h2 className="text-xl">Products</h2>
      <ul>
        {products.map((p) => (
          <li key={p.id} className="mb-2">
            {p.sku} - {p.name} <button onClick={() => onQuickSale(p.id)} className="ml-2">Sale -1</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
