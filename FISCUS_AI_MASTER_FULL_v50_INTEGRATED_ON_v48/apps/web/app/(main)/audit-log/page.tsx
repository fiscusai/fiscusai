'use client';
import { useEffect, useState } from 'react';

export default function AuditLogPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [lines, setLines] = useState<string[]>([]);
  const [n, setN] = useState<number>(100);

  const load = async () => {
    const r = await fetch(`${base}/audit/tail?n=${n}`);
    const j = await r.json();
    setLines(j);
  };
  useEffect(()=>{ load(); }, [n]);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-semibold">Audit Log</h1>
        <div className="flex items-center gap-2">
          <span className="text-sm">Satır:</span>
          <input type="number" className="border rounded p-1 w-24" value={n} onChange={e=>setN(parseInt(e.target.value||'0'))} />
          <button onClick={load} className="px-3 py-2 border rounded">Yenile</button>
        </div>
      </div>
      <pre className="p-3 border rounded bg-gray-50 text-xs overflow-auto" style={{maxHeight: '60vh'}}>
{lines.join('\n')}
      </pre>
    </div>
  );
}
