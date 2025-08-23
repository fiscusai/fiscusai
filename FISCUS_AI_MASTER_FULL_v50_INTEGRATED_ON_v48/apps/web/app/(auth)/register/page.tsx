'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiBase } from '@/lib/authClient';

export default function RegisterPage() {
  const [email, setEmail] = useState('demo@fiscus.ai');
  const [password, setPassword] = useState('demo123');
  const [name, setName] = useState('Demo Kullanıcı');
  const [msg, setMsg] = useState<string | null>(null);
  const router = useRouter();

  const submit = async () => {
    setMsg(null);
    const base = await apiBase();
    const r = await fetch(`${base}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name })
    });
    if (!r.ok) {
      setMsg('Kayıt başarısız');
      return;
    }
    setMsg('Kayıt başarılı, girişe yönlendiriliyorsunuz...');
    setTimeout(()=>router.replace('/(auth)/login'), 800);
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-sm border p-6 rounded bg-white">
        <h1 className="text-xl font-semibold mb-4">Kayıt Ol</h1>
        <div className="grid gap-3">
          <input value={name} onChange={e=>setName(e.target.value)} placeholder="Ad Soyad" className="border rounded p-2"/>
          <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="E-posta" className="border rounded p-2"/>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Şifre" className="border rounded p-2"/>
          {msg && <div className="text-sm">{msg}</div>}
          <button onClick={submit} className="px-4 py-2 bg-black text-white rounded">Kayıt Ol</button>
        </div>
      </div>
    </div>
  );
}
