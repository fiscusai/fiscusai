'use client';
import { useState } from 'react';

export default function BIEmailPage() {
  const [to, setTo] = useState('ops@fiscus.ai');
  const [fromDate, setFromDate] = useState('2025-07-01');
  const [toDate, setToDate] = useState('2025-08-01');
  const [result, setResult] = useState<any>(null);
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  const send = async () => {
    const url = `${base}/bi/export/email?to=${encodeURIComponent(to)}&from_date=${fromDate}&to_date=${toDate}`;
    const r = await fetch(url, { method: 'POST' });
    setResult(await r.json());
  };

  return (
    <div className="p-6 grid gap-3 max-w-lg">
      <h1 className="text-xl font-semibold">BI Export — Email Gönder</h1>
      <label className="text-sm">Alıcı e‑posta</label>
      <input className="border rounded p-2" value={to} onChange={e=>setTo(e.target.value)} />
      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="text-sm">Başlangıç</label>
          <input type="date" className="border rounded p-2 w-full" value={fromDate} onChange={e=>setFromDate(e.target.value)} />
        </div>
        <div>
          <label className="text-sm">Bitiş</label>
          <input type="date" className="border rounded p-2 w-full" value={toDate} onChange={e=>setToDate(e.target.value)} />
        </div>
      </div>
      <button onClick={send} className="px-3 py-2 border rounded bg-black text-white">Gönder</button>
      {result && <pre className="p-2 bg-gray-50 border rounded text-xs overflow-auto">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
