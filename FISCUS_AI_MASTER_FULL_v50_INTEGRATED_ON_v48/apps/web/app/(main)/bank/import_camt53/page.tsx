'use client';
import { useState } from 'react';

export default function ImportCAMT53Page() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  const onFile = async (e: any) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const fd = new FormData();
    fd.append('file', f);
    setLoading(true);
    try {
      const res = await fetch(`${base}/bank/import/camt53`, { method:'POST', body: fd });
      const j = await res.json();
      setResult(j);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">CAMT.053 İçe Aktarma</h1>
      <input type="file" accept=".xml,.camt,.camt53" onChange={onFile} />
      {loading && <div>Yükleniyor...</div>}
      {result && (
        <pre className="p-3 border rounded bg-gray-50 overflow-auto text-xs">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}
