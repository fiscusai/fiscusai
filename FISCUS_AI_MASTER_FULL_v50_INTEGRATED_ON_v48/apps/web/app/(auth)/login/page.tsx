'use client';
import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { apiBase, setTokens } from '@/lib/authClient';

export default function LoginPage() {
  const [email, setEmail] = useState('demo@fiscus.ai');
  const [password, setPassword] = useState('demo123');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get('next') || '/(main)/dashboard';

  const submit = async () => {
    setError(null);
    const base = await apiBase();
    const r = await fetch(`${base}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!r.ok) {
      setError('Giriş başarısız');
      return;
    }
    const j = await r.json();
    setTokens(j.access_token, j.refresh_token);
    router.replace(next);
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-sm border p-6 rounded bg-white">
        <h1 className="text-xl font-semibold mb-4">Giriş</h1>
        <div className="grid gap-3">
          <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="E-posta" className="border rounded p-2"/>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Şifre" className="border rounded p-2"/>
          {error && <div className="text-red-600 text-sm">{error}</div>}
          <button onClick={submit} className="px-4 py-2 bg-black text-white rounded">Giriş Yap</button>
        </div>
      </div>
    </div>
  );
}
