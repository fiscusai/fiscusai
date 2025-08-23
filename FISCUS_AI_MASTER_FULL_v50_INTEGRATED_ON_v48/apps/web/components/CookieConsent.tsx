'use client'
import { useEffect, useState } from 'react'
export default function CookieConsent(){
  const [open,setOpen]=useState(false)
  useEffect(()=>{ const v=localStorage.getItem('cookie-consent'); if(!v) setOpen(true) },[])
  if(!open) return null
  return (
    <div className="cookie-banner">
      <div className="flex items-center gap-3">
        <div><b>Çerezler</b> — deneyimi iyileştirmek için bazı çerezler kullanıyoruz.</div>
        <div className="ml-auto flex gap-2">
          <button className="px-3 py-1 border" onClick={()=>{localStorage.setItem('cookie-consent','reject'); setOpen(false)}}>Reddet</button>
          <button className="px-3 py-1 border" onClick={()=>{localStorage.setItem('cookie-consent','accept'); setOpen(false)}}>Kabul Et</button>
        </div>
      </div>
    </div>
  )
}
