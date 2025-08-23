'use client'
import { useState } from 'react'
import CompanySwitcher from '../../components/CompanySwitcher'
export default function Dashboard(){
  const [ctx,setCtx]=useState<{id:number,role:string}>({id:0,role:'viewer'})
  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-3xl">Kontrol Paneli</h1>
        <CompanySwitcher onChange={(id, role)=>setCtx({id,role: role||'viewer'})} />
      </div>
      <div className="grid md:grid-cols-3 gap-4 mt-6">
        <div className="p-4 border border-altin rounded-md bg-white/70">Nakit Akışı</div>
        <div className="p-4 border border-altin rounded-md bg-white/70">Alacaklar (A/R)</div>
        <div className="p-4 border border-altin rounded-md bg-white/70">Borçlar (A/P)</div>
      </div>
      <div className="mt-6 text-sm opacity-70">Seçili şirket: {ctx.id || '—'} · Rol: {ctx.role}</div>
    </div>
  )
}
