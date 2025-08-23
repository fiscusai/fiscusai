import { useEffect, useState } from 'react';

type Status = { ok: boolean, version?: string, queue_depth?: number, uptime?: number };

export default function StatusPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [data, setData] = useState<Status|null>(null);

  useEffect(()=>{
    (async ()=>{
      try {
        const [v, q, u] = await Promise.all([
          fetch(`${base}/status/version`).then(r=>r.json()).catch(()=>({})),
          fetch(`${base}/status/queue-depth`).then(r=>r.json()).catch(()=>({})),
          fetch(`${base}/status/uptime`).then(r=>r.json()).catch(()=>({}))
        ]);
        setData({ ok: true, version: v?.version, queue_depth: q?.depth, uptime: u?.uptime });
      } catch { setData({ ok:false }); }
    })();
  }, []);

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Sistem Durumu</h1>
      <div className="grid sm:grid-cols-3 gap-3">
        <div className="border rounded p-3"><div className="text-sm opacity-60">Sürüm</div><div className="text-lg">{data?.version ?? '—'}</div></div>
        <div className="border rounded p-3"><div className="text-sm opacity-60">Kuyruk Derinliği</div><div className="text-lg">{data?.queue_depth ?? '—'}</div></div>
        <div className="border rounded p-3"><div className="text-sm opacity-60">Uptime (sn)</div><div className="text-lg">{data?.uptime ?? '—'}</div></div>
      </div>
    </div>
  );
}
