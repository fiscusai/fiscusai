'use client';
import { useState } from 'react';

export default function InvitePage() {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('user');
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  const sendInvite = async () => {
    const res = await fetch(`${base}/auth/invite`, {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ email, role })
    });
    if (!res.ok) { alert('Hata: ' + await res.text()); return; }
    alert('Davet gönderildi! (outbox klasörünü kontrol et)');
  };

  return (
    <div className="p-6 grid gap-3 max-w-md">
      <h1 className="text-xl font-semibold">Kullanıcı Davet Et</h1>
      <input className="border rounded p-2" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
      <select className="border rounded p-2" value={role} onChange={e=>setRole(e.target.value)}>
        <option value="user">User</option>
        <option value="accountant">Accountant</option>
        <option value="admin">Admin</option>
      </select>
      <button className="border rounded px-3 py-2" onClick={sendInvite}>Davet Gönder</button>
    </div>
  );
}
