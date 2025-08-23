'use client'
import { useEffect, useState } from 'react'
import CompanySwitcher from '../../../components/CompanySwitcher'
import { API, authHeaders } from '../../../lib/sdk'
type Invoice = { id:number; number:string; issue_date:string; due_date:string; customer_id:number; subtotal:number; tax:number; total:number; status:string }
export default function InvoicesPage(){
  const [items,setItems]=useState<Invoice[]>([]), [status,setStatus]=useState(''), [q,setQ]=useState('')
  const [modalOpen,setModalOpen]=useState(false), [role,setRole]=useState('viewer'), [companyId,setCompanyId]=useState<number>(0)
  const [form,setForm]=useState<any>({ number:'', issue_date:'', due_date:'', customer_id:1, subtotal:0, tax:0, total:0, status:'draft' })
  const load=async(id:number)=>{ if(!id) return; const headers:any = await authHeaders(); headers['X-Company-Id']=String(id); const url = new URL(API + '/invoices'); if(status) url.searchParams.set('status', status); if(q) url.searchParams.set('q', q); const res = await fetch(url.toString(), { headers }); if(res.ok){ setItems(await res.json()) } }
  useEffect(()=>{ if(companyId) load(companyId) },[companyId])
  const submit=async(e:any)=>{ e.preventDefault(); const headers:any = await authHeaders(); headers['Content-Type']='application/json'; headers['X-Company-Id']=String(companyId); const res = await fetch(API + '/invoices', { method:'POST', headers, body: JSON.stringify(form)}); if(res.ok){ setModalOpen(false); await load(companyId); } else { alert('Yetki hatası (rol?)') } }
  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="flex items-center justify-between mb-4">
        <h1 className="font-display text-3xl">Faturalar</h1>
        <CompanySwitcher onChange={(id, r)=>{ setCompanyId(id); setRole(r||'viewer') }} />
      </div>
      <div className="flex gap-2 mb-4">
        <select className="border p-2 rounded-md" value={status} onChange={e=>setStatus(e.target.value)}>
          <option value="">Tümü</option><option value="draft">Taslak</option><option value="sent">Gönderildi</option><option value="paid">Ödendi</option><option value="overdue">Gecikmiş</option>
        </select>
        <input className="border p-2 rounded-md" placeholder="Ara (No)" value={q} onChange={e=>setQ(e.target.value)} />
        <button onClick={()=>load(companyId)} className="px-4 py-2 border border-altin rounded-md">Yenile</button>
        <button disabled={role==='viewer'} onClick={()=>setModalOpen(true)} className={`px-4 py-2 rounded-md ${role==='viewer'?'opacity-50 cursor-not-allowed border':'bg-fiscus text-mermer'}`}>{role==='viewer'?'Sadece görüntüleme':'Yeni Fatura'}</button>
      </div>
      <div className="overflow-auto rounded-md border border-altin">
        <table className="min-w-full bg-white/80">
          <thead className="sticky top-0 bg-mermer">
            <tr><th className="text-left p-3">No</th><th className="text-left p-3">Tarih</th><th className="text-left p-3">Vade</th><th className="text-left p-3">Müşteri</th><th className="text-right p-3">Toplam</th><th className="text-left p-3">Durum</th><th className="p-3">Aksiyon</th></tr>
          </thead>
          <tbody>{items.map(i=>(
            <tr key={i.id} className="border-t">
              <td className="p-3">{i.number}</td><td className="p-3">{i.issue_date}</td><td className="p-3">{i.due_date}</td>
              <td className="p-3">#{i.customer_id}</td><td className="p-3 text-right">₺{i.total.toLocaleString('tr-TR')}</td><td className="p-3">{i.status}</td>
              <td className="p-3">
                <a className="underline" href={`${API}/invoices/${i.id}/export?format=pdf`} target="_blank">PDF</a>{" | "}
                <a className="underline" href={`${API}/invoices/${i.id}/export?format=xlsx`} target="_blank">Excel</a>{" | "}
                <a className="underline" href={`${API}/invoices/${i.id}/export?format=xml`} target="_blank">XML</a>
              </td>
            </tr>))}
          </tbody>
        </table>
      </div>
      {modalOpen && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center">
          <form onSubmit={submit} className="bg-white p-6 rounded-md w-[520px] space-y-3 border border-altin">
            <h2 className="font-display text-2xl mb-2">Yeni Fatura</h2>
            <input className="w-full border p-2 rounded-md" placeholder="Fatura No" value={form.number} onChange={e=>setForm({...form, number:e.target.value})} />
            <div className="grid grid-cols-2 gap-2">
              <input className="border p-2 rounded-md" type="date" value={form.issue_date} onChange={e=>setForm({...form, issue_date:e.target.value})} />
              <input className="border p-2 rounded-md" type="date" value={form.due_date} onChange={e=>setForm({...form, due_date:e.target.value})} />
            </div>
            <div className="grid grid-cols-3 gap-2">
              <input className="border p-2 rounded-md" placeholder="Müşteri ID" type="number" value={form.customer_id} onChange={e=>setForm({...form, customer_id:Number(e.target.value)})} />
              <input className="border p-2 rounded-md" placeholder="Ara Toplam" type="number" value={form.subtotal} onChange={e=>setForm({...form, subtotal:Number(e.target.value)})} />
              <input className="border p-2 rounded-md" placeholder="KDV" type="number" value={form.tax} onChange={e=>setForm({...form, tax:Number(e.target.value)})} />
            </div>
            <input className="border p-2 rounded-md w-full" placeholder="Toplam" type="number" value={form.total} onChange={e=>setForm({...form, total:Number(e.target.value)})} />
            <select className="border p-2 rounded-md w-full" value={form.status} onChange={e=>setForm({...form, status:e.target.value})}>
              <option value="draft">Taslak</option><option value="sent">Gönderildi</option><option value="paid">Ödendi</option><option value="overdue">Gecikmiş</option>
            </select>
            <div className="flex gap-2 justify-end pt-2"><button type="button" className="px-4 py-2" onClick={()=>setModalOpen(false)}>Vazgeç</button><button className="px-4 py-2 border border-altin rounded-md">Kaydet</button></div>
          </form>
        </div>
      )}
    </div>
  )
}
