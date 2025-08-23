'use client';
import { useState } from 'react';

export default function BIReportsPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [org, setOrg] = useState('');
  const [cust, setCust] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');

  const downloadZip = () => {
    const u = new URL(`${base}/exports/bi/invoices.zip`);
    if (org) u.searchParams.set('org_id', org);
    if (cust) u.searchParams.set('customer', cust);
    if (start) u.searchParams.set('start', start);
    if (end) u.searchParams.set('end', end);
    window.location.href = u.toString();
  };

  return (
    <div className="p-6 grid gap-3 max-w-xl">
      <h1 className="text-xl font-semibold">BI Export (ZIP)</h1>
      <input className="border p-2 rounded" placeholder="Org ID (örn. ORG-ALPHA)" value={org} onChange={e=>setOrg(e.target.value)} />
      <input className="border p-2 rounded" placeholder="Müşteri Adı (parça eşleşir)" value={cust} onChange={e=>setCust(e.target.value)} />
      <div className="grid grid-cols-2 gap-2">
        <input type="date" className="border p-2 rounded" value={start} onChange={e=>setStart(e.target.value)} />
        <input type="date" className="border p-2 rounded" value={end} onChange={e=>setEnd(e.target.value)} />
      </div>
      <button onClick={downloadZip} className="px-4 py-2 border rounded bg-black text-white">ZIP İndir</button>
    </div>
  );
}
