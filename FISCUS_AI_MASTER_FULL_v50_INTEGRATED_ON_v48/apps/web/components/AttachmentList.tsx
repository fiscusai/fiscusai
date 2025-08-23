'use client';
import { useEffect, useState } from 'react';

export default function AttachmentList({ invoiceId }: { invoiceId: string }) {
  const [items, setItems] = useState<{filename:string;content_type:string}[]>([]);
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  const load = async () => {
    const r = await fetch(`${base}/attachments/${invoiceId}`);
    const j = await r.json();
    setItems(j);
  };
  useEffect(()=>{ load(); }, [invoiceId]);

  const onUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const form = new FormData();
    form.append('file', f);
    const res = await fetch(`${base}/attachments/${invoiceId}`, { method: 'POST', body: form });
    if (!res.ok) alert('Yükleme hatası');
    await load();
  };

  return (
    <div className="mt-2">
      <div className="flex items-center gap-2 mb-2">
        <input type="file" onChange={onUpload} />
      </div>
      {items.length === 0 && <div className="text-sm opacity-70">Henüz ek yok</div>}
      <ul className="space-y-1">
        {items.map((it, idx) => (
          <li key={idx}>
            <a className="text-blue-600 underline" href={`${base}/attachments/file/${encodeURIComponent(it.filename)}`} target="_blank">
              {it.filename}
            </a> <span className="text-xs opacity-60">({it.content_type})</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
