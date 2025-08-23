
'use client';
import { useState } from 'react';

export default function AutoReconcile() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [daysTol, setDaysTol] = useState(5);
  const [amtTol, setAmtTol] = useState(1.0);
  const [data, setData] = useState<any>(null);
  const [autoApply, setAutoApply] = useState(true);

  const run = async () => {
    const payload = {
      transactions: [{ id:'T-100', date:'2025-08-05', amount:1000, description:'Aurea INV-1000 Ödeme' }],
      invoices: [{ id:'I-1000', number:'INV-1000', date:'2025-08-01', amount:1000, org:'ORG-ALPHA', customer:'Aurea' }],
      rules: { desc_rules:['Aurea','INV-'], tolerance_days: daysTol, amount_tolerance: amtTol }
    };
    const r = await fetch(`${base}/reconcile/auto/run`, { method:'POST', headers:{'Content-Type':'application/json','X-Org':'ORG-ALPHA','X-User-Role':'accountant'}, body: JSON.stringify(payload) });
    const j = await r.json(); setData(j);
    if (autoApply && j.matches?.length) {
      await fetch(`${base}/reconcile/auto/apply`, { method:'POST', headers:{'Content-Type':'application/json','X-Org':'ORG-ALPHA','X-User-Role':'accountant'}, body: JSON.stringify({ matches: j.matches }) });
    }
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Otomatik Mutabakat</h1>
      <div className="grid md:grid-cols-4 gap-3">
        <label className="text-sm">Tarih toleransı (gün)
          <input type="number" className="border rounded p-2 w-full" value={daysTol} onChange={e=>setDaysTol(parseInt(e.target.value||'0'))}/>
        </label>
        <label className="text-sm">Tutar toleransı
          <input type="number" step="0.01" className="border rounded p-2 w-full" value={amtTol} onChange={e=>setAmtTol(parseFloat(e.target.value||'0'))}/>
        </label>
        <label className="text-sm flex gap-2 items-center">
          <input type="checkbox" checked={autoApply} onChange={e=>setAutoApply(e.target.checked)}/> Eşleşmeleri otomatik uygula
        </label>
        <div className="flex items-end">
          <button onClick={run} className="px-3 py-2 border rounded bg-black text-white">Çalıştır</button>
        </div>
      </div>
      {data && (
        <div className="grid md:grid-cols-3 gap-3">
          <div className="p-3 border rounded"><div className="font-medium">Tam Eşleşen</div><pre className="text-xs">{JSON.stringify(data.matches,null,2)}</pre></div>
          <div className="p-3 border rounded"><div className="font-medium">Kısmi</div><pre className="text-xs">{JSON.stringify(data.partials,null,2)}</pre></div>
          <div className="p-3 border rounded"><div className="font-medium">Eşleşmeyen</div><pre className="text-xs">{JSON.stringify(data.unmatched,null,2)}</pre></div>
        </div>
      )}
    </div>
  );
}
