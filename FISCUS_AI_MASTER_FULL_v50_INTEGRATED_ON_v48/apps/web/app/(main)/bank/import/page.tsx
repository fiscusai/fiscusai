'use client';
import { useState } from 'react';

export default function BankImportPage(){
  const [message, setMessage] = useState('');
  const upload = async () => {
    const el:any=document.getElementById('bankfile');
    if(!el||!el.files||el.files.length===0){ alert('Dosya seç'); return; }
    const f = el.files[0];
    const fd = new FormData();
    fd.append('file', f);
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
    const r = await fetch(`${base}/bank/import`,{
      method:'POST',
      headers:{ 'X-Token':'dev-bank-token' },
      body: fd
    });
    const j = await r.json();
    if(!r.ok){ setMessage('Hata: '+(j.detail||'bilinmeyen')); return; }
    setMessage(`Yüklendi: ${j.count} hareket — Gelen: ${j.total_in} / Giden: ${j.total_out}`);
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Banka Verisi İçe Aktar</h1>
      <input id="bankfile" type="file" className="mb-3" />
      <div><button onClick={upload} className="px-3 py-2 border rounded">Yükle</button></div>
      <div className="mt-3 text-sm opacity-80">{message}</div>
    </div>
  );
}
