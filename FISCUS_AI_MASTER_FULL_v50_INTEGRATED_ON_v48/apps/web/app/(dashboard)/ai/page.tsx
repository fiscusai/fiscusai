'use client'
import { useEffect, useState } from 'react'
import CompanySwitcher from '../../../components/CompanySwitcher'
import { API, authHeaders } from '../../../lib/sdk'
type FItem = { period:string; cash:number }
export default function AIPage(){
  const [summary,setSummary]=useState(''); const [anoms,setAnoms]=useState<any[]>([]); const [forecast,setForecast]=useState<FItem[]>([])
  const [companyId,setCompanyId]=useState<number>(0)
  const call=async(path:string,id:number)=>{ const headers:any = await authHeaders(); headers['X-Company-Id']=String(id); const res=await fetch(API+path,{method:'POST', headers}); return await res.json() }
  useEffect(()=>{ if(!companyId) return; (async()=>{ const s = await call('/ai/summarize', companyId); setSummary(s.summary); const a = await call('/ai/anomaly', companyId); setAnoms(a.anomalies||[]); const f = await call('/ai/forecast', companyId); setForecast(f.forecast||[]) })() },[companyId])
  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="flex items-center justify-between mb-4"><h1 className="font-display text-3xl">AI Paneli</h1><CompanySwitcher onChange={(id)=>setCompanyId(id)} /></div>
      <div className="mb-6 p-4 border border-altin rounded-md bg-white/70"><div className="font-semibold mb-2">Özet</div><div>{summary || 'Veri bekleniyor...'}</div></div>
      <div className="mb-6 p-4 border border-altin rounded-md bg-white/70"><div className="font-semibold mb-2">Aykırı Harcamalar</div>{anoms.length===0 ? <div>—</div> : <ul className="list-disc pl-6">{anoms.map((x:any)=>(<li key={x.id}>#{x.id} → ₺{x.amount} · {x.reason}</li>))}</ul>}</div>
      <div className="p-4 border border-altin rounded-md bg-white/70"><div className="font-semibold mb-2">Nakit Akışı Tahmini (3 dönem)</div><div className="flex gap-3">{forecast.map(f=>(<div key={f.period} className="p-3 border rounded-md">{f.period}: ₺{f.cash.toLocaleString('tr-TR')}</div>))}</div></div>
    </div>
  )
}
