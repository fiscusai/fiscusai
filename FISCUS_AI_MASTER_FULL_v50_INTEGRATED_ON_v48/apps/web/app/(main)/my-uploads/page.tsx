'use client';
import { useEffect, useState } from 'react';

export const metadata = { title: "Yüklemelerim | FISCUS AI" };

type Item = { key:string; mime:string; size:number; created_at:string; status:string };

export default function Page() {
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const token = typeof window !== 'undefined' ? localStorage.getItem('api_token') : null;

  const [items, setItems] = useState<Item[]>([]);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(20);
  const [q, setQ] = useState('');
  const [mime, setMime] = useState('');
  const [sizeMin, setSizeMin] = useState('');
  const [sizeMax, setSizeMax] = useState('');
  const [sort, setSort] = useState<'created_at'|'size'|'mime'|'key'>('created_at');
  const [order, setOrder] = useState<'asc'|'desc'>('desc');
  const [meta, setMeta] = useState({total_pages:1, total_items:0});

  async function load() {
    const p = new URLSearchParams();
    p.set('page', String(page));
    p.set('size', String(size));
    if (q) p.set('q', q);
    if (mime) p.set('mime', mime);
    if (sizeMin) p.set('size_min', sizeMin);
    if (sizeMax) p.set('size_max', sizeMax);
    p.set('sort', sort);
    p.set('order', order);

    const r = await fetch(`${api}/files/mine?${p.toString()}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    const j = await r.json();
    setItems(j.items || []);
    setMeta({ total_pages: j.total_pages || 1, total_items: j.total_items || 0 });
  }

  useEffect(()=>{ load(); /* eslint-disable-next-line */ }, [page, size, sort, order]);

  return (
    <section className="prose max-w-5xl py-8">
      <h1>Yüklemelerim</h1>

      <div className="flex flex-wrap items-end gap-2">
        <div><label>Ara<br/><input className="border px-2 py-1" value={q} onChange={e=>setQ(e.target.value)} /></label></div>
        <div><label>MIME<br/><input className="border px-2 py-1" placeholder="application/pdf" value={mime} onChange={e=>setMime(e.target.value)} /></label></div>
        <div><label>Boyut min (B)<br/><input className="border px-2 py-1" value={sizeMin} onChange={e=>setSizeMin(e.target.value)} /></label></div>
        <div><label>Boyut max (B)<br/><input className="border px-2 py-1" value={sizeMax} onChange={e=>setSizeMax(e.target.value)} /></label></div>
        <div><label>Sırala<br/>
          <select className="border px-2 py-1" value={sort} onChange={e=>setSort(e.target.value as any)}>
            <option value="created_at">Tarih</option>
            <option value="size">Boyut</option>
            <option value="mime">MIME</option>
            <option value="key">Anahtar</option>
          </select></label></div>
        <div><label>Yön<br/>
          <select className="border px-2 py-1" value={order} onChange={e=>setOrder(e.target.value as any)}>
            <option value="desc">Desc</option>
            <option value="asc">Asc</option>
          </select></label></div>
        <button className="border px-3 py-1 rounded" onClick={()=>{ setPage(1); load(); }}>Uygula</button>
      </div>

      <div className="overflow-auto mt-4">
        <table className="min-w-full text-sm border">
          <thead><tr className="bg-gray-100">
            <th className="border px-2 py-1 text-left">Anahtar</th>
            <th className="border px-2 py-1 text-left">MIME</th>
            <th className="border px-2 py-1 text-left">Boyut (B)</th>
            <th className="border px-2 py-1 text-left">Tarih</th>
            <th className="border px-2 py-1 text-left">Durum</th>
            <th className="border px-2 py-1 text-left">İşlemler</th>
          </tr></thead>
          <tbody>
            {items.map((r)=> (
              <tr key={r.key}>
                <td className="border px-2 py-1"><code className="truncate">{r.key}</code></td>
                <td className="border px-2 py-1">{r.mime}</td>
                <td className="border px-2 py-1">{r.size}</td>
                <td className="border px-2 py-1 whitespace-nowrap">{new Date(r.created_at).toLocaleString()}</td>
                <td className="border px-2 py-1">{r.status}</td>
                <td className="border px-2 py-1">
                  <button className="text-xs underline" onClick={async()=>{
                    const r2 = await fetch(`${api}/files/download-url?key=${encodeURIComponent(r.key)}`, { headers: token? {Authorization:`Bearer ${token}`} : {} });
                    const j2 = await r2.json(); if (j2.url) window.open(j2.url, '_blank');
                  }}>İndir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center gap-2 mt-3">
        <button className="border px-2 py-1 rounded" onClick={()=>setPage(p=>Math.max(1,p-1))}>‹ Prev</button>
        <span>Sayfa {page} / {meta.total_pages} • Toplam {meta.total_items}</span>
        <button className="border px-2 py-1 rounded" onClick={()=>setPage(p=>p+1)}>Next ›</button>
        <select className="border px-2 py-1" value={size} onChange={e=>setSize(parseInt(e.target.value,10))}>
          {[10,20,50,100].map(n=> <option key={n} value={n}>{n}/page</option>)}
        </select>
      </div>
    </section>
  );
}
