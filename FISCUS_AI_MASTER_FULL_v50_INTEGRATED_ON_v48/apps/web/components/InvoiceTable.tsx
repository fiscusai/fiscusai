'use client';
import { useEffect, useState } from 'react';

type Invoice = {
  id: string;
  number: string;
  customer: string;
  date: string;
  due_date: string;
  total: number;
  status: string;
};

export default function InvoiceTable() {
  const [rows, setRows] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const base = process.env.NEXT_PUBLIC_API_URL;
        const url = (base ? base.replace(/\/$/, '') : '') + '/invoices';
        const r = await fetch(url || '/api/health-proxy');
        if (r.ok && url) {
          const js = await r.json();
          setRows(js);
        } else {
          // fallback demo rows if API yoksa
          setRows([
            {id:'1', number:'INV-LOCAL-001', customer:'Demo Ltd', date:'2025-07-01', due_date:'2025-07-31', total:12000, status:'unpaid'},
          ]);
        }
      } catch (e) {
        setRows([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div>Yükleniyor...</div>;

  return (
    <div className="overflow-auto rounded-lg border border-zinc-200">
      <table className="min-w-full bg-white">
        <thead className="sticky top-0 bg-zinc-50 text-left text-xs uppercase tracking-wide text-zinc-500">
          <tr>
            <th className="px-3 py-2">No</th>
            <th className="px-3 py-2">Müşteri</th>
            <th className="px-3 py-2">Tarih</th>
            <th className="px-3 py-2">Vade</th>
            <th className="px-3 py-2">Tutar</th>
            <th className="px-3 py-2">Durum</th>
          </tr>
        </thead>
        <tbody className="text-sm">
          {rows.map(r => (
            <tr key={r.id} className="border-t border-zinc-100">
              <td className="px-3 py-2">{r.number}</td>
              <td className="px-3 py-2">{r.customer}</td>
              <td className="px-3 py-2">{r.date}</td>
              <td className="px-3 py-2">{r.due_date}</td>
              <td className="px-3 py-2">{r.total.toLocaleString('tr-TR', {style:'currency', currency:'TRY'})}</td>
              <td className="px-3 py-2">{r.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
