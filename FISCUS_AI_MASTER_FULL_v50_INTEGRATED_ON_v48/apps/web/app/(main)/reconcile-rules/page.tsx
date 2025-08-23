'use client';
import { apiFetch } from '@/lib/apiClient';
import { useEffect, useState } from 'react';

type Preview = { rules: string[]; tolerance_days: number; matched: number; unmatched: number };

export default function ReconcileRulesPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [rules, setRules] = useState<string>('Aurea,Legera');
  const [tol, setTol] = useState<number>(5);
  const [preview, setPreview] = useState<Preview|null>(null);
  const [current, setCurrent] = useState<Preview|null>(null);

  useEffect(()=>{
    // mevcut kural setini çek
    (async () => {
      const r = await fetch(`${base}/reconcile/rules`).then(r=>r.json());
      setRules((r.desc_rules||[]).join(','));
      setTol(r.tolerance_days || 5);
      setCurrent({ rules: r.desc_rules||[], tolerance_days: r.tolerance_days||5, matched:0, unmatched:0 });
    })();
  }, []);

  const doPreview = async () => {
    const params = new URLSearchParams();
    for (const r of rules.split(',').map(s=>s.trim()).filter(Boolean)) params.append('desc_rule', r);
    params.append('tolerance', String(tol));
    const res = await fetch(`${base}/reconcile/rules/preview?${params.toString()}`);
    setPreview(await res.json());
  };

  const doApply = async () => {
    const list = rules.split(',').map(s=>s.trim()).filter(Boolean);
    await apiFetch(`/reconcile/rules`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({"desc_rules": list, "tolerance_days": tol})
    });
    setCurrent({ rules: list, tolerance_days: tol, matched: preview?.matched || 0, unmatched: preview?.unmatched || 0 });
    alert('Kurallar kaydedildi.');
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Banka Mutabakat Kuralları</h1>
      {current && (
        <div className="p-3 border rounded bg-gray-50 text-sm">
          <div className="font-medium mb-1">Mevcut Kurallar</div>
          <div>Kurallar: {current.rules.join(', ') || '—'}</div>
          <div>Tolerans: {current.tolerance_days} gün</div>
        </div>
      )}
      <div className="grid gap-2 max-w-xl">
        <label className="text-sm">Açıklama Kuralları (virgülle ayırın)</label>
        <input className="border rounded p-2" value={rules} onChange={e=>setRules(e.target.value)} />
        <label className="text-sm">Tolerans (gün)</label>
        <input type="number" className="border rounded p-2" value={tol} onChange={e=>setTol(parseInt(e.target.value||'0'))} />
        <div className="flex gap-2">
          <button onClick={doPreview} className="px-3 py-2 border rounded">Önizle</button>
          <button onClick={doApply} className="px-3 py-2 border rounded bg-black text-white">Kaydet</button>
        </div>
      </div>
      {preview && (
        <div className="grid md:grid-cols-2 gap-4">
          <div className="p-3 border rounded">
            <div className="font-medium">Eşleşen Kayıtlar</div>
            <div className="text-2xl">{preview.matched}</div>
          </div>
          <div className="p-3 border rounded">
            <div className="font-medium">Eşleşmeyen Kayıtlar</div>
            <div className="text-2xl">{preview.unmatched}</div>
          </div>
        </div>
      )}
    </div>
  );
}
