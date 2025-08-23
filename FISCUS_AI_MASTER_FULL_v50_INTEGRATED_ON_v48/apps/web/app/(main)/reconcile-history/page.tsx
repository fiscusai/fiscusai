
'use client';
import { useEffect, useState } from 'react';

type Item = { ts:string; org:string; tx_id:string; invoice_id:string; type:string; amount:number; invoice_amount:number; diff_amount:number };

export default function ReconcileHistory() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [data, setData] = useState<{items:Item[]; total:number; page:number; page_size:number} | null>(null);
  const [page, setPage] = useState(1);

  const load = async (p=1) => {
    const r = await fetch(`${base}/reconcile/history/?page=${p}&page_size=50`);
    setData(await r.json());
  };

  useEffect(()=>{ load(page); }, [page]);

  return (
    <div className="p-6 grid gap-3">
      <h1 className="text-xl font-semibold">Mutabakat Geçmişi</h1>
      <div className="flex gap-2">
        <a className="px-3 py-2 border rounded" href={`${base}/reconcile/history/export.csv`}>CSV indir</a>
        <a className="px-3 py-2 border rounded" href={`${base}/reconcile/history/export.pdf`} target="_blank">PDF aç</a>
      </div>
      <div className="overflow-auto border rounded">
        <table className="w-full text-sm">
          <thead><tr className="bg-gray-100"><th className="p-2">Zaman</th><th className="p-2">Org</th><th className="p-2">Tx</th><th className="p-2">Fatura</th><th className="p-2">Tür</th><th className="p-2 text-right">Tutar</th><th className="p-2 text-right">Fatura</th><th className="p-2 text-right">Fark</th></tr></thead>
          <tbody>
            {data?.items?.map((it,i)=>(
              <tr key={i} className="border-t">
                <td className="p-2 whitespace-nowrap">{it.ts}</td>
                <td className="p-2">{it.org}</td>
                <td className="p-2">{it.tx_id}</td>
                <td className="p-2">{it.invoice_id}</td>
                <td className="p-2">{it.type}</td>
                <td className="p-2 text-right">{it.amount}</td>
                <td className="p-2 text-right">{it.invoice_amount}</td>
                <td className="p-2 text-right">{it.diff_amount}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center gap-2">
        <button className="px-3 py-2 border rounded" onClick={()=>setPage(Math.max(1,(page-1)))}>Önceki</button>
        <div className="text-sm">Sayfa {page} / {Math.max(1, Math.ceil((data?.total||0)/(data?.page_size||50)))}</div>
        <button className="px-3 py-2 border rounded" onClick={()=>setPage(page+1)}>Sonraki</button>
      </div>
    </div>
  );
}
