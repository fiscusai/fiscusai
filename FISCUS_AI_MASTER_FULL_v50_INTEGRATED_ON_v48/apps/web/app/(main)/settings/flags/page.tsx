'use client';
import { useEffect, useState } from 'react';

function isAdmin(): boolean {
  try {
    const s = localStorage.getItem('fiscus_auth');
    if (!s) return false;
    const obj = JSON.parse(s);
    return obj?.role === 'admin';
  } catch { return false; }
}

export default function FlagsPage() {
  const [flags, setFlags] = useState<Record<string, boolean>>({});
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  useEffect(()=>{
    (async ()=>{
      const j = await fetch(`${base}/flags/`).then(r=>r.json());
      setFlags(j);
    })();
  }, []);

  if (!isAdmin()) return <div className="p-6">Bu sayfa yalnızca admin içindir.</div>;

  const toggle = (k: string) => setFlags(prev => ({...prev, [k]: !prev[k]}));
  const save = async () => {
    await fetch(`${base}/flags/`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(flags)});
    alert('Kaydedildi');
  };

  return (
    <div className="p-6 grid gap-4 max-w-xl">
      <h1 className="text-xl font-semibold">Feature Flags</h1>
      {Object.keys(flags).length === 0 && <div>Yükleniyor…</div>}
      {Object.entries(flags).map(([k,v]) => (
        <label key={k} className="flex items-center justify-between border p-2 rounded">
          <span>{k}</span>
          <input type="checkbox" checked={!!v} onChange={()=>toggle(k)} />
        </label>
      ))}
      <button onClick={save} className="px-4 py-2 border rounded bg-black text-white">Kaydet</button>
    </div>
  );
}
