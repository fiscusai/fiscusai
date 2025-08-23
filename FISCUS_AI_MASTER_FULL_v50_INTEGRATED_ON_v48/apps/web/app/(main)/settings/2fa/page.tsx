'use client';
import { useEffect, useState } from 'react';

export default function TwoFASettings() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [status, setStatus] = useState<any>(null);
  const [secret, setSecret] = useState<string>('');
  const [uri, setUri] = useState<string>('');
  const [code, setCode] = useState<string>('');

  const load = async () => {
    const r = await fetch(`${base}/2fa/status`);
    setStatus(await r.json());
  };
  useEffect(()=>{ load(); }, []);

  const enable = async () => {
    const r = await fetch(`${base}/2fa/enable`, { method: 'POST' });
    const j = await r.json();
    setSecret(j.secret); setUri(j.otpauth_uri);
  };

  const verify = async () => {
    const r = await fetch(`${base}/2fa/verify?code=${encodeURIComponent(code)}`, { method: 'POST' });
    const j = await r.json();
    alert(j.ok ? '2FA etkinleştirildi' : 'Kod hatalı');
    await load();
  };

  return (
    <div className="p-6 grid gap-4 max-w-xl">
      <h1 className="text-xl font-semibold">İki Aşamalı Doğrulama (TOTP)</h1>
      {status && <div className="text-sm">Durum: <b>{status.enabled ? 'Aktif' : 'Pasif'}</b></div>}
      <button onClick={enable} className="px-3 py-2 border rounded">Kurulum başlat</button>
      {secret && (
        <div className="grid gap-2">
          <div className="text-sm">Secret: <code>{secret}</code></div>
          <div className="text-sm break-words">otpauth URI: <code>{uri}</code></div>
          <label className="text-sm">Uygulamadaki kodu girin</label>
          <input className="border rounded p-2" value={code} onChange={e=>setCode(e.target.value)} />
          <button onClick={verify} className="px-3 py-2 border rounded bg-black text-white">Doğrula</button>
        </div>
      )}
    </div>
  );
}
