'use client';
import { useEffect, useState } from 'react';

type Match = { id: string; tx_id: string; invoice_id: string };

export default function ReconcilePage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [matches, setMatches] = useState<Match[]>([]);
  const [txId, setTx] = useState('');
  const [invId, setInv] = useState('');

  const load = async () => {
    const r = await fetch(`${base}/reconcile/matched`).then(r=>r.json()).catch(()=>[]);
    setMatches(r || []);
  };
  useEffect(()=>{ load(); }, []);

  const create = async () => {
    await fetch(`${base}/reconcile/manual`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ tx_id: txId, invoice_id: invId }) });
    setTx(''); setInv(''); load();
  };
  const update = async (id: string) => {
    const tx = prompt('Yeni tx_id?', '');
    const inv = prompt('Yeni invoice_id?', '');
    if (!tx || !inv) return;
    await fetch(`${base}/reconcile/manual/${id}`, { method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ tx_id: tx, invoice_id: inv }) });
    load();
  };
  const remove = async (id: string) => {
    await fetch(`${base}/reconcile/manual/${id}`, { method:'DELETE' });
    load();
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Banka Mutabakatı</h1>
      <div className="grid grid-cols-3 gap-2 max-w-2xl">
        <input value={txId} onChange={e=>setTx(e.target.value)} placeholder="tx_id" className="border rounded p-2" />
        <input value={invId} onChange={e=>setInv(e.target.value)} placeholder="invoice_id" className="border rounded p-2" />
        <button onClick={create} className="px-3 py-2 border rounded bg-black text-white">Eşleştir</button>
      </div>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">tx_id</th>
          <th className="p-2 text-left">invoice_id</th>
          <th className="p-2"></th>
        </tr></thead>
        <tbody>
          {matches.map(m => (
            <tr key={m.id} className="border-t">
              <td className="p-2">{m.tx_id}</td>
              <td className="p-2">{m.invoice_id}</td>
              <td className="p-2 text-right">
                <div className="flex gap-2 justify-end">
                  <button onClick={()=>update(m.id)} className="px-2 py-1 border rounded">Düzenle</button>
                  <button onClick={()=>remove(m.id)} className="px-2 py-1 border rounded">Sil</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
