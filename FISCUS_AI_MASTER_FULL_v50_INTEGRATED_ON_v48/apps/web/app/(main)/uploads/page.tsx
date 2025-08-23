'use client';
import { useState } from 'react';

export default function UploadsPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [status, setStatus] = useState<string>('');
  const [publicUrl, setPublicUrl] = useState<string>('');

  const onFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const presign = await fetch(`${base}/s3/presign-upload?filename=${encodeURIComponent(f.name)}&content_type=${encodeURIComponent(f.type||'application/octet-stream')}`).then(r=>r.json());
    const put = await fetch(presign.url, { method:'PUT', headers: presign.headers, body: f });
    setStatus(put.ok ? 'Yüklendi' : 'Hata: '+put.status);
    setPublicUrl(presign.public_url);
  };

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Dosya Yükleme (Presigned)</h1>
      <input type="file" onChange={onFile} className="border rounded p-2" />
      {status && <div className="text-sm">{status}</div>}
      {publicUrl && <div className="text-sm">Public URL: <a className="underline" href={publicUrl} target="_blank">{publicUrl}</a></div>}
    </div>
  );
}
