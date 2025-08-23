'use client';
import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/apiClient';

type Customer = { id:string; name:string; email:string; tax_id:string };

export default function CustomersV2Client() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [items, setItems] = useState<Customer[]>([]);
  const [q, setQ] = useState('');
  const [sort, setSort] = useState('name:asc');

  const load = async () => {
    const url = `${base}/v2/customers/?q=${encodeURIComponent(q)}&sort=${encodeURIComponent(sort)}&page=1&page_size=20`;
    const r = await apiFetch(url);
    const j = await r.json();
    setItems(j.items || []);
  };
  useEffect(()=>{ load(); }, [q, sort]);

  return (
    <div className="p-6 grid gap-3">
      <div className="flex gap-2 items-center">
        <input className="border rounded p-2" placeholder="Ara..." value={q} onChange={e=>setQ(e.target.value)} />
        <select className="border rounded p-2" value={sort} onChange={e=>setSort(e.target.value)}>
          <option value="name:asc">Ad ↑</option>
          <option value="name:desc">Ad ↓</option>
          <option value="email:asc">Email ↑</option>
          <option value="email:desc">Email ↓</option>
        </select>
      </div>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">Ad</th><th className="p-2 text-left">Email</th><th className="p-2 text-left">Vergi No</th>
        </tr></thead>
        <tbody>
          {items.map((it)=> (
            <tr key={it.id} className="border-t">
              <td className="p-2">{it.name}</td>
              <td className="p-2">{it.email}</td>
              <td className="p-2">{it.tax_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
