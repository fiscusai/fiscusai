
'use client';
import { useEffect, useState } from 'react';

type Report = { [k: string]: any };

export default function CspReportsPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [items, setItems] = useState<Report[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [domain, setDomain] = useState('');
  const [limit, setLimit] = useState(200);

  const load = async () => {
    const q = new URLSearchParams();
    if (domain) q.append('domain', domain);
    if (limit) q.append('limit', String(limit));
    const r = await fetch(`${base}/csp/reports?${q.toString()}`);
    const j = await r.json();
    setItems(j.items || []);
    const s = await fetch(`${base}/csp/stats`).then(r=>r.json());
    setStats(s);
  };
  useEffect(()=>{ load(); }, []);

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">CSP Raporları</h1>
      <div className="grid md:grid-cols-3 gap-2 items-end">
        <label className="text-sm">Domain
          <input className="border rounded p-2 w-full" value={domain} onChange={e=>setDomain(e.target.value)} />
        </label>
        <label className="text-sm">Limit
          <input type="number" className="border rounded p-2 w-full" value={limit} onChange={e=>setLimit(parseInt(e.target.value||'0'))} />
        </label>
        <button onClick={load} className="px-3 py-2 border rounded">Yükle</button>
      </div>

      {stats && (
        <div className="p-3 border rounded">
          <div className="font-medium mb-2">En çok ihlal edilen 10 direktif</div>
          <ul className="list-disc pl-5 text-sm">
            {(stats.top||[]).map((x:any)=> <li key={x[0]}>{x[0]}: {x[1]}</li>)}
          </ul>
          <div className="text-xs opacity-70 mt-1">Toplam: {stats.total}</div>
        </div>
      )}

      <div className="overflow-auto border rounded text-sm">
        <table className="w-full">
          <thead><tr className="bg-gray-100">
            <th className="p-2 text-left">Document</th>
            <th className="p-2 text-left">Violated</th>
            <th className="p-2 text-left">Blocked URI</th>
            <th className="p-2 text-left">Referrer</th>
          </tr></thead>
          <tbody>
            {items.map((r, idx)=> (
              <tr key={idx} className="border-t">
                <td className="p-2">{r['document-uri']}</td>
                <td className="p-2">{r['violated-directive']}</td>
                <td className="p-2">{r['blocked-uri']}</td>
                <td className="p-2">{r['referrer']}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
