'use client';
import { useEffect, useState } from 'react';
import InvoiceForm from '@/components/InvoiceForm';
import { downloadCSV, downloadJSON } from '@/components/exportUtils';
type Invoice = { id?: string; number?: string; customer?: string; date?: string; total?: number; vat?: number; };

export default function InvoicesClientPage() {
  const [items, setItems] = useState<Invoice[]>([]);
  const [editing, setEditing] = useState<Invoice|undefined>(undefined);
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const load = async () => { const r = await fetch(`${base}/invoices/`); setItems(await r.json()); };
  useEffect(()=>{ load(); }, []);
  const onSaved = async () => { setEditing(undefined); await load(); };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-semibold">Faturalar (Gelişmiş)</h1>
        <div className="flex gap-2">
          <button onClick={()=>downloadCSV('invoices.csv', items)} className="px-3 py-2 border rounded">CSV</button>
          <button onClick={()=>downloadJSON('invoices.json', items)} className="px-3 py-2 border rounded">JSON</button>
          <button onClick={()=>setEditing({})} className="px-3 py-2 border rounded bg-black text-white">Yeni Fatura</button>
        </div>
      </div>
      {editing && <InvoiceForm initial={editing} onSaved={onSaved} />}
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">No</th><th className="p-2 text-left">Müşteri</th>
          <th className="p-2 text-left">Tarih</th><th className="p-2 text-right">Tutar</th><th className="p-2 text-right">KDV</th><th className="p-2 text-right">PDF</th>
        </tr></thead>
        <tbody>
        <tbody>
          {items.map((it, i)=>(
            <tr key={it.id || i} className="border-t">
              <td className="p-2">{it.number}</td><td className="p-2">{it.customer}</td>
              <td className="p-2">{it.date}</td><td className="p-2 text-right">{it.total}</td><td className="p-2 text-right">{it.vat}</td>
            <td className="p-2 text-right">
                <a href={(it.id ? `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/exports/invoice-v3/${it.id}.pdf` 
                               : `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/exports/invoice-v3/${it.number}.pdf`)} 
                   target="_blank" className="underline">PDF</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
