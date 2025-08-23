'use client'
import { useEffect, useState } from 'react'
import CompanySwitcher from '../../../components/CompanySwitcher'
import { API, authHeaders } from '../../../lib/sdk'
type Customer = { id:number; name:string; email?:string|null; tax_no?:string|null }
export default function CustomersPage(){
  const [items,setItems]=useState<Customer[]>([]); const [q,setQ]=useState(''); const [form,setForm]=useState<any>({name:'', email:'', tax_no:''}); const [open,setOpen]=useState(false); const [companyId,setCompanyId]=useState<number>(0)
  const load=async(id:number)=>{ if(!id) return; const headers:any = await authHeaders(); headers['X-Company-Id']=String(id); const res=await fetch(API+'/customers',{ headers }); const data=await res.json(); setItems(data) }
  useEffect(()=>{ if(companyId) load(companyId) },[companyId])
  const submit=async(e:any)=>{ e.preventDefault(); const headers:any = await authHeaders(); headers['Content-Type']='application/json'; headers['X-Company-Id']=String(companyId); const res=await fetch(API+'/customers',{method:'POST', headers, body: JSON.stringify(form)}); if(res.ok){ setOpen(false); setForm({name:'',email:'',tax_no:''}); await load(companyId) } }
  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="flex items-center justify-between mb-4"><h1 className="font-display text-3xl">Müşteriler</h1><CompanySwitcher onChange={(id)=>setCompanyId(id)} /></div>
      <div className="flex gap-2 mb-3"><input className="border p-2 rounded-md" placeholder="Ara (isim)" value={q} onChange={e=>setQ(e.target.value)} /><button onClick={()=>setOpen(true)} className="px-4 py-2 bg-fiscus text-mermer rounded-md">Yeni Müşteri</button></div>
      <div className="grid md:grid-cols-2 gap-3">{items.filter(c=>c.name.toLowerCase().includes(q.toLowerCase())).map(c=>(<div key={c.id} className="p-4 border border-altin rounded-md bg-white/70"><div className="font-semibold">{c.name}</div><div className="text-sm opacity-80">{c.email || '—'} · {c.tax_no || '—'}</div></div>))}</div>
      {open && (<div className="fixed inset-0 bg-black/30 flex items-center justify-center"><form onSubmit={submit} className="bg-white p-6 rounded-md w-[420px] space-y-3 border border-altin"><h2 className="font-display text-2xl mb-2">Yeni Müşteri</h2><input className="w-full border p-2 rounded-md" placeholder="Ad" value={form.name} onChange={e=>setForm({...form, name:e.target.value})}/><input className="w-full border p-2 rounded-md" placeholder="E-posta" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/><input className="w-full border p-2 rounded-md" placeholder="Vergi No" value={form.tax_no} onChange={e=>setForm({...form, tax_no:e.target.value})}/><div className="flex gap-2 justify-end pt-2"><button type="button" className="px-4 py-2" onClick={()=>setOpen(false)}>Vazgeç</button><button className="px-4 py-2 border border-altin rounded-md">Kaydet</button></div></form></div>)}
    </div>
  )
}
