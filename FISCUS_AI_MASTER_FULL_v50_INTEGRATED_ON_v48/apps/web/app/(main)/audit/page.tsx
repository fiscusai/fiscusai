
'use client';
import { useEffect, useMemo, useState } from 'react';
import { apiGet } from '@/lib/apiClient';

type AuditItem = { ts: string; event: string; data: any };

export default function AuditPage() {
  const [items, setItems] = useState<AuditItem[]>([]);
  const [auto, setAuto] = useState(false);
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [events, setEvents] = useState<string[]>([]);

  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  const fetchData = async () => {
    const params = new URLSearchParams();
    if (from) params.append('from', from);
    if (to) params.append('to', to);
    if (events.length) params.append('event', events.join(','));
    const data = await apiGet<{items:AuditItem[],total:number,page:number,page_size:number}>(`${base}/audit?${params.toString()}`);
    setItems(data?.items || []);
  };

  useEffect(()=>{ fetchData(); }, []);
  useEffect(()=>{
    if (!auto) return;
    const t = setInterval(fetchData, 5000);
    return ()=>clearInterval(t);
  }, [auto, from, to, events]);

  const eventOptions = useMemo(()=>{
    const set = new Set(items.map(i=>i.event));
    return Array.from(set);
  }, [items]);

  const downloadCSV = () => {
    const headers = ['ts','event','data'];
    const rows = items.map(i => [i.ts, i.event, JSON.stringify(i.data)]);
    const csv = [headers.join(','), ...rows.map(r=>r.map(x=>JSON.stringify(x)).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'audit.csv'; a.click();
    URL.revokeObjectURL(url);
  };

  const toggleEvent = (ev: string) => {
    setEvents(prev => prev.includes(ev) ? prev.filter(x=>x!==ev) : [...prev, ev]);
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Audit Log</h1>
      <div className="grid md:grid-cols-4 gap-3 items-end">
        <label className="text-sm">Başlangıç
          <input type="date" className="border rounded p-2 w-full" value={from} onChange={e=>setFrom(e.target.value)} />
        </label>
        <label className="text-sm">Bitiş
          <input type="date" className="border rounded p-2 w-full" value={to} onChange={e=>setTo(e.target.value)} />
        </label>
        <div>
          <div className="text-sm mb-1">Event Filtre</div>
          <div className="flex flex-wrap gap-2">
            {eventOptions.map(ev => (
              <button key={ev} onClick={()=>toggleEvent(ev)}
                className={`px-2 py-1 border rounded text-xs ${events.includes(ev) ? 'bg-black text-white' : ''}`}>
                {ev}
              </button>
            ))}
          </div>
        </div>
        <div className="flex gap-2">
          <button onClick={fetchData} className="px-3 py-2 border rounded">Uygula</button>
          <label className="flex gap-2 items-center text-sm border rounded px-3">
            <input type="checkbox" checked={auto} onChange={e=>setAuto(e.target.checked)} />
            Otomatik yenile (5sn)
          </label>
        </div>
      </div>
      <div className="flex gap-2">
        <button onClick={downloadCSV} className="px-3 py-2 border rounded">CSV indir</button>
      </div>
      <div className="overflow-auto border rounded text-sm">
        <table className="w-full">
          <thead><tr className="bg-gray-100">
            <th className="p-2 text-left">Zaman</th><th className="p-2 text-left">Event</th><th className="p-2 text-left">Veri</th>
          </tr></thead>
          <tbody>
            {items.map((it, idx)=>(
              <tr key={idx} className="border-t align-top">
                <td className="p-2 whitespace-nowrap">{it.ts}</td>
                <td className="p-2 whitespace-nowrap">{it.event}</td>
                <td className="p-2"><pre className="text-xs">{JSON.stringify(it.data, null, 2)}</pre></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
