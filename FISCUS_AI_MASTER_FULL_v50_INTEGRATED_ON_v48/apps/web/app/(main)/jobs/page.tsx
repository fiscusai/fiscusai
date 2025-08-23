'use client';
import { useEffect, useState } from 'react';

export default function JobsPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [cron, setCron] = useState<{id:string,cron:string}[]>([]);
  const [hist, setHist] = useState<any[]>([]);
  const [id, setId] = useState('daily-report');
  const [spec, setSpec] = useState('0 9 * * *');

  const load = async () => {
    const s = await fetch(`${base}/jobs/scheduled`).then(r=>r.json());
    setCron(s.cron || []);
    const h = await fetch(`${base}/jobs/history?n=50`).then(r=>r.json());
    setHist(h.history || []);
  };

  useEffect(()=>{ load(); }, []);

  const schedule = async () => {
    await fetch(`${base}/jobs/schedule/cron?id=${encodeURIComponent(id)}&cron=${encodeURIComponent(spec)}`, { method:'POST' });
    await load();
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Zamanlanmış İşler</h1>
      <div className="flex gap-2">
        <input className="border p-2 rounded" placeholder="job id" value={id} onChange={e=>setId(e.target.value)} />
        <input className="border p-2 rounded" placeholder="0 9 * * *" value={spec} onChange={e=>setSpec(e.target.value)} />
        <button onClick={schedule} className="px-3 py-2 border rounded bg-black text-white">Kaydet</button>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="p-3 border rounded">
          <div className="font-medium mb-2">Aktif Cronlar</div>
          <pre className="text-xs bg-gray-50 p-2 rounded overflow-auto">{JSON.stringify(cron, null, 2)}</pre>
        </div>
        <div className="p-3 border rounded">
          <div className="font-medium mb-2">Son Çalışmalar</div>
          <pre className="text-xs bg-gray-50 p-2 rounded overflow-auto">{JSON.stringify(hist, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
}
