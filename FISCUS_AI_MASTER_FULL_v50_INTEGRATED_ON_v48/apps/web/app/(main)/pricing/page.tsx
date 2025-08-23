'use client';
import { useState } from 'react';

const plans = [
  { key: 'basic', name: 'Basic', price: '₺0', features: ['Sınırlı faturalar', 'Temel raporlar'] },
  { key: 'pro', name: 'Pro', price: '₺399/ay', features: ['Sınırsız faturalar', 'AI önerileri', 'Öncelikli destek'] },
  { key: 'enterprise', name: 'Enterprise', price: 'İletişime geçin', features: ['Çok kiracılı', 'SSO', 'Özel SLA'] },
];

export default function PricingPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [email, setEmail] = useState('demo@example.com');
  const [resp, setResp] = useState<any>(null);

  const checkout = async (plan: string) => {
    const r = await fetch(`${base}/payments/checkout`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan, interval: 'monthly', email })
    });
    const j = await r.json();
    setResp(j);
    if (j.payment_url) window.open(j.payment_url, '_blank');
  };

  return (
    <div className="p-6 grid gap-6">
      <h1 className="text-2xl font-semibold">Fiyatlandırma</h1>
      <div className="max-w-md">
        <label className="text-sm">E-posta</label>
        <input className="w-full p-2 border rounded" value={email} onChange={e=>setEmail(e.target.value)} />
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        {plans.map(p => (
          <div key={p.key} className="p-4 border rounded bg-white flex flex-col">
            <div className="text-xl font-semibold">{p.name}</div>
            <div className="text-3xl mt-2">{p.price}</div>
            <ul className="mt-3 text-sm opacity-80 list-disc pl-5">
              {p.features.map(f => <li key={f}>{f}</li>)}
            </ul>
            <button onClick={()=>checkout(p.key)} className="mt-auto px-4 py-2 border rounded bg-black text-white">Satın Al</button>
          </div>
        ))}
      </div>
      {resp && (
        <div className="p-4 border rounded bg-white">
          <div className="font-medium mb-2">Ödeme Yanıtı</div>
          <pre className="text-sm overflow-auto">{JSON.stringify(resp, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
