'use client'
import { useEffect, useState } from 'react'
import CompanySwitcher from '../../../components/CompanySwitcher'
import { API, authHeaders } from '../../../lib/sdk'
type Expense = { id:number; title:string; amount:number; date:string; category?:string|null }
export default function ExpensesPage(){
  const [items,setItems]=useState<Expense[]>([]); const [form,setForm]=useState<any>({title:'', amount:0, date:'', category:''})
  const [open,setOpen]=useState(false); const [cat,setCat]=useState(''); const [companyId,setCompanyId]=useState<number>(0)
  const load=async(id:number)=>{ if(!id) return; const headers:any = await authHeaders(); headers['X-Company-Id']=String(id); const res=await fetch(API+'/expenses',{ headers }); const data=await res.json(); setItems(data) }
  useEffect(()=>{ if(companyId) load(companyId) },[companyId])
  const submit=async(e:any)=>{ e.preventDefault(); const headers:any = await authHeaders(); headers['Content-Type']='application/json'; headers['X-Company-Id']=String(companyId); const res=await fetch(API+'/expenses',{method:'POST', headers, body: JSON.stringify(form)}); if(res.ok){ setOpen(false); setForm({title:'',amount:0,date:'',category:''}); await load(companyId) } }
  const importCSV=async(e:any)=>{ const file=e.target.files?.[0]; if(!file) return; const fd=new FormData(); fd.append('file', file); fd.append('amount_col','amount'); fd.append('title_col','title'); fd.append('date_col','date'); fd.append('category_col','category'); const headers:any = await authHeaders(); headers['X-Company-Id']=String(companyId); const res=await fetch(API+'/expenses/import',{method:'POST', headers, body: fd}); const data=await res.json(); alert('İçe aktarılan kayıt: '+data.created); await load(companyId) }
  const total = items.filter(i=>!cat || i.category===cat).reduce((s,i)=>s+i.amount,0)
  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="flex items-center justify-between mb-4">
        <h1 className="font-display text-3xl">Giderler</h1>
        <CompanySwitcher onChange={(id)=>setCompanyId(id)} />
      </div>
      <div className="flex gap-2 mb-3">
        <select className="border p-2 rounded-md" value={cat} onChange={e=>setCat(e.target.value)}>
          <option value="">Tüm Kategoriler</option>
          {[...new Set(items.map(i=>i.category || ''))].filter(Boolean).map(c=>(<option key={c} value={c}>{c}</option>))}
        </select>
        <button onClick={()=>setOpen(true)} className="px-4 py-2 bg-fiscus text-mermer rounded-md">Yeni Gider</button>
        <label className="px-4 py-2 border border-altin rounded-md cursor-pointer">
          CSV İçe Aktar <input type="file" accept=".csv" onChange={importCSV} hidden/>
        </label>
        <div className="ml-auto font-semibold">Toplam: ₺{total.toLocaleString('tr-TR')}</div>
      </div>
      <div className="overflow-auto rounded-md border border-altin">
        <table className="min-w-full bg-white/80">
          <thead className="sticky top-0 bg-mermer"><tr><th className="text-left p-3">Başlık</th><th className="text-left p-3">Tarih</th><th className="text-left p-3">Kategori</th><th className="text-right p-3">Tutar</th></tr></thead>
          <tbody>{items.filter(i=>!cat || i.category===cat).map(i=>(<tr key={i.id} className="border-t">
            <td className="p-3">{i.title}</td><td className="p-3">{i.date}</td><td className="p-3">{i.category || '—'}</td><td className="p-3 text-right">₺{i.amount.toLocaleString('tr-TR')}</td>
          </tr>))}</tbody>
        </table>
      </div>
      {open && (<div className="fixed inset-0 bg-black/30 flex items-center justify-center">
        <form onSubmit={submit} className="bg-white p-6 rounded-md w-[420px] space-y-3 border border-altin">
          <h2 className="font-display text-2xl mb-2">Yeni Gider</h2>
          <input className="w-full border p-2 rounded-md" placeholder="Başlık" value={form.title} onChange={e=>setForm({...form, title:e.target.value})}/>
          <div className="grid grid-cols-2 gap-2"><input className="border p-2 rounded-md" type="date" value={form.date} onChange={e=>setForm({...form, date:e.target.value})}/><input className="border p-2 rounded-md" placeholder="Kategori" value={form.category} onChange={e=>setForm({...form, category:e.target.value})}/></div>
          <input className="w-full border p-2 rounded-md" type="number" placeholder="Tutar" value={form.amount} onChange={e=>setForm({...form, amount:Number(e.target.value)})}/>
          <div className="flex gap-2 justify-end pt-2"><button type="button" className="px-4 py-2" onClick={()=>setOpen(false)}>Vazgeç</button><button className="px-4 py-2 border border-altin rounded-md">Kaydet</button></div>
        </form></div>)}
    </div>
  )
}
