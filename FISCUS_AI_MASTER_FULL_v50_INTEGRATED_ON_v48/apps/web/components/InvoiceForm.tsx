'use client';
import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/apiClient';

type Invoice = { id?: string; number?: string; customer?: string; date?: string; total?: number; vat?: number; };

export default function InvoiceForm({ initial, onSaved }: { initial?: Invoice; onSaved?: () => void }) {
  const [form, setForm] = useState<Invoice>(initial || { date: new Date().toISOString().slice(0,10), vat: 0 });

  useEffect(() => { if (initial) setForm(initial); }, [initial]);

  const save = async () => {
    const isUpdate = !!form.id;
    if (isUpdate) {
      await apiFetch(`/v2/invoices/${form.id}`, { method: 'PUT', body: JSON.stringify(form) });
    } else {
      await apiFetch(`/v2/invoices/`, { method: 'POST', body: JSON.stringify(form) });
    }
    onSaved && onSaved();
  };

  return (
    <div className="p-4 border rounded-md bg-white">
      <div className="grid grid-cols-2 gap-3">
        <label className="flex flex-col text-sm">Fatura No
          <input className="input input-bordered p-2 border rounded" value={form.number || ''}
            onChange={e=>setForm({...form, number: e.target.value})} />
        </label>
        <label className="flex flex-col text-sm">Müşteri
          <input className="input input-bordered p-2 border rounded" value={form.customer || ''}
            onChange={e=>setForm({...form, customer: e.target.value})} />
        </label>
        <label className="flex flex-col text-sm">Tarih
          <input type="date" className="input input-bordered p-2 border rounded" value={form.date || ''}
            onChange={e=>setForm({...form, date: e.target.value})} />
        </label>
        <label className="flex flex-col text-sm">Tutar
          <input type="number" className="input input-bordered p-2 border rounded" value={form.total || 0}
            onChange={e=>setForm({...form, total: parseFloat(e.target.value)})} />
        </label>
        <label className="flex flex-col text-sm">KDV
          <input type="number" className="input input-bordered p-2 border rounded" value={form.vat || 0}
            onChange={e=>setForm({...form, vat: parseFloat(e.target.value)})} />
        </label>
      </div>
      <div className="mt-3 flex gap-2">
        <button onClick={save} className="px-4 py-2 border rounded bg-black text-white">Kaydet</button>
      </div>
    </div>
  );
}
