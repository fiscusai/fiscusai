'use client'
import { useEffect, useState } from 'react'
import { API, authHeaders } from '../lib/sdk'
export default function CompanySwitcher({ onChange }:{ onChange:(id:number, role?:string)=>void }){
  const [companies,setCompanies]=useState<{company_id:number,role:string}[]>([])
  const [sel,setSel]=useState<string>('')
  useEffect(()=>{(async()=>{
    const headers = await authHeaders()
    const me = await (await fetch(API+'/auth/me',{ headers })).json()
    setCompanies(me.companies||[])
    const saved = localStorage.getItem('companyId') || (me.companies?.[0]?.company_id?.toString() || '')
    const role = me.companies?.find((c:any)=>c.company_id.toString()===saved)?.role || 'viewer'
    setSel(saved); if(saved) onChange(Number(saved), role)
  })()},[])
  return (
    <select className="border p-2 rounded-md" value={sel} onChange={(e)=>{
      const id=e.target.value; setSel(id); localStorage.setItem('companyId', id)
      const role = companies.find(c=>c.company_id.toString()===id)?.role || 'viewer'; onChange(Number(id), role)
    }}>
      {companies.map(c=>(<option key={c.company_id} value={c.company_id}>{c.company_id} · {c.role}</option>))}
    </select>
  )
}
