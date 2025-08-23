'use client';
import { useEffect, useState } from 'react';

export const metadata = { title: "Admin • Audit Log | FISCUS AI" };

type Row = { id:number; ts:string; actor:string; role:string; action:string; target:string; meta:string };

export default function Page() {
  const [items, setItems] = useState<Row[]>([]);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(20);
  const [actor, setActor] = useState('');
  const [action, setAction] = useState('');
  const [q, setQ] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [msg, setMsg] = useState('');

  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const token = typeof window !== 'undefined' ? localStorage.getItem('api_token') : null;

  async function load() {
    setMsg('');
    try {
      const p = new URLSearchParams();
      p.set('page', String(page));
      p.set('size', String(size));
      if (actor) p.set('actor', actor);
      if (q) p.set('q', q);
      if (action) p.set('action', action);
      if (start) p.set('start', start);
      if (end) p.set('end', end);
      const r = await fetch(`${api}/admin/audit?${p.toString()}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!r.ok) throw new Error('Yetki veya API hatası');
      const j = await r.json();
      setItems(j.items || []);
    } catch (e:any) {
      setMsg(e.message || 'Hata');
    }
  }

  useEffect(() => { load(); /* eslint-disable-next-line */ }, [page, size]);

  return (
    <section className="prose max-w-5xl py-8">
      <h1>Admin • Audit Log</h1>
      <button className="border px-3 py-1 rounded" onClick={()=>{
        const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const p = new URLSearchParams();
        if (actor) p.set('actor', actor);
      if (q) p.set('q', q);
        if (action) p.set('action', action);
        if (start) p.set('start', start);
        if (end) p.set('end', end);
        window.open(`${api}/admin/audit/export?${p.toString()}`, '_blank');
      }}>CSV indir</button>
      <div className="flex flex-wrap gap-2 items-end">
        <div><label>Actor<br/><input className="border px-2 py-1" value={actor} onChange={e=>setActor(e.target.value)} /></label></div>
        <div><label>Action<br/><input className="border px-2 py-1" value={action} onChange={e=>setAction(e.target.value)} /></label></div>
        <div><label>Start (ISO)<br/><input className="border px-2 py-1" placeholder="2025-08-01T00:00:00" value={start} onChange={e=>setStart(e.target.value)} /></label></div>
        <div><label>End (ISO)<br/><input className="border px-2 py-1" placeholder="2025-08-31T23:59:59" value={end} onChange={e=>setEnd(e.target.value)} /></label></div>
        <button className="border px-3 py-1 rounded" onClick={()=>{setPage(1);load();}}>Filtrele</button>
        <div><label>Search (q)<br/><input className="border px-2 py-1" value={q} onChange={e=>setQ(e.target.value)} /></label></div>
        <button className="border px-3 py-1 rounded" onClick={()=>{
          const p = new URLSearchParams(); if (actor) p.set('actor', actor); if (action) p.set('action', action); if (start) p.set('start', start); if (end) p.set('end', end); if (q) p.set('q', q);
          const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
          window.open(`${api}/admin/audit/export?`+p.toString(), '_blank');
        }}>CSV indir</button>
      </div>

      {msg && <p className="text-sm text-gray-600">{msg}</p>}

      <div className="overflow-auto">
        <table className="min-w-full text-sm border mt-4">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-2 py-1 text-left">TS</th>
              <th className="border px-2 py-1 text-left">Actor</th>
              <th className="border px-2 py-1 text-left">Role</th>
              <th className="border px-2 py-1 text-left">Action</th>
              <th className="border px-2 py-1 text-left">Target</th>
              <th className="border px-2 py-1 text-left">Meta</th>
            </tr>
          </thead>
          <tbody>
            {items.map((r) => (
              <tr key={r.id}>
                <td className="border px-2 py-1 whitespace-nowrap">{r.ts}</td>
                <td className="border px-2 py-1">{r.actor}</td>
                <td className="border px-2 py-1">{r.role}</td>
                <td className="border px-2 py-1">{r.action}</td>
                <td className="border px-2 py-1">{r.target}</td>
                <td className="border px-2 py-1">{r.meta}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-2 mt-3">
        <button className="border px-2 py-1 rounded" onClick={()=>setPage(p=>Math.max(1,p-1))}>‹ Prev</button>
        <span>Page {page}</span>
        <button className="border px-2 py-1 rounded" onClick={()=>setPage(p=>p+1)}>Next ›</button>
        <select className="border px-2 py-1" value={size} onChange={e=>setSize(parseInt(e.target.value,10))}>
          {[10,20,50,100].map(n=> <option key={n} value={n}>{n}/page</option>)}
        </select>
      </div>
    </section>
  );
}