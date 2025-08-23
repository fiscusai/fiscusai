'use client';
import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/apiClient';

type Invoice = { id:string; number:string; customer:string; date:string; total:number; vat:number };

export default function InvoicesV2Client() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [items, setItems] = useState<Invoice[]>([]);
  const [q, setQ] = useState('');
  const [sort, setSort] = useState('date:desc');

  const load = async () => {
    const url = `${base}/v2/invoices/?q=${encodeURIComponent(q)}&sort=${encodeURIComponent(sort)}&page=1&page_size=20`;
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
          <option value="date:desc">Tarih ↓</option>
          <option value="date:asc">Tarih ↑</option>
          <option value="total:desc">Tutar ↓</option>
          <option value="total:asc">Tutar ↑</option>
        </select>
      </div>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">No</th><th className="p-2 text-left">Müşteri</th>
          <th className="p-2 text-left">Tarih</th><th className="p-2 text-right">Tutar</th><th className="p-2 text-right">KDV</th>
        </tr></thead>
        <tbody>
          {items.map((it)=> (
            <tr key={it.id} className="border-t">
              <td className="p-2">{it.number}</td>
              <td className="p-2">{it.customer}</td>
              <td className="p-2">{it.date}</td>
              <td className="p-2 text-right">{it.total?.toLocaleString?.() ?? it.total}</td>
              <td className="p-2 text-right">{it.vat?.toLocaleString?.() ?? it.vat}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
