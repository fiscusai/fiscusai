'use client';
import { useState } from 'react';

type UploadItem = {
  file: File;
  progress: number;
  status: 'idle' | 'signing' | 'uploading' | 'done' | 'error';
  key?: string;
  error?: string;
};

const MAX_MB = 20;
const ALLOWED = ['application/pdf','image/png','image/jpeg','image/webp'];

export default function PresignedUploader() {
  const [items, setItems] = useState<UploadItem[]>([]);

  function pickFiles(e: React.ChangeEvent<HTMLInputElement>) {
    const files = Array.from(e.target.files || []);
    const next: UploadItem[] = [];
    for (const f of files) {
      const mb = f.size / (1024*1024);
      if (mb > MAX_MB) {
        next.push({file: f, progress: 0, status: 'error', error: `Dosya çok büyük (${mb.toFixed(1)}MB > ${MAX_MB}MB)`});
        continue;
      }
      if (!ALLOWED.includes(f.type)) {
        next.push({file: f, progress: 0, status: 'error', error: `İzin verilmeyen tür: ${f.type || 'bilinmiyor'}`});
        continue;
      }
      next.push({file: f, progress: 0, status: 'idle'});
    }
    setItems(prev => [...prev, ...next]);
  }

  async function uploadOne(idx: number) {
    const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    setItems(curr => curr.map((it,i) => i===idx? {...it, status:'signing'} : it));
    const f = items[idx].file;
    try {
      const token = localStorage.getItem('api_token');
        const res = await fetch(`${api}/files/presign?filename=${encodeURIComponent(f.name)}&mime=${encodeURIComponent(f.type||'')}&size=${f.size}`);
      if (!res.ok) throw new Error('Ön imza alınamadı');
      const { post, key } = await res.json();

      setItems(curr => curr.map((it,i) => i===idx? {...it, status:'uploading'} : it));

      const form = new FormData();
      Object.entries(post.fields).forEach(([k,v]) => form.append(k, String(v)));
      form.append('file', f);

      const xhr = new XMLHttpRequest();
      const p = new Promise<void>((resolve, reject) => {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const pct = Math.round((e.loaded/e.total)*100);
            setItems(curr => curr.map((it,i) => i===idx? {...it, progress:pct} : it));
          }
        });
        xhr.onreadystatechange = () => {
          if (xhr.readyState === 4) {
            if (xhr.status >= 200 && xhr.status < 300) resolve();
            else reject(new Error('Yükleme hatası'));
          }
        };
        xhr.open('POST', post.url, true);
        xhr.send(form);
      });
      await p;

      setItems(curr => curr.map((it,i) => i===idx? {...it, progress:100, status:'done', key} : it));
    } catch (err: any) {
      setItems(curr => curr.map((it,i) => i===idx? {...it, status:'error', error: err?.message || 'Hata'} : it));
    }
  }

  async function uploadAll() {
    for (let i=0;i<items.length;i++) {
      if (items[i].status==='idle' || items[i].status==='error') {
        await uploadOne(i);
      }
    }
  }

  return (
    <div className="space-y-4">
      <div className="text-sm text-gray-600">
        İzin verilen türler: {ALLOWED.join(', ')} • Maks {MAX_MB}MB
      </div>
      <input type="file" multiple onChange={pickFiles} />
      <button className="border px-3 py-1 rounded" onClick={uploadAll} disabled={!items.length}>
        Tümünü Yükle
      </button>
      <ul className="space-y-2">
        {items.map((it, i) => (
          <li key={i} className="border rounded p-3">
            <div className="flex items-center justify-between">
              <div className="truncate">{it.file.name}</div>
              <div className="text-xs">{it.file.type || 'type?'} • {(it.file.size/1024/1024).toFixed(1)}MB</div>
            </div>
            <div className="h-2 bg-gray-200 rounded mt-2 overflow-hidden">
              <div className="h-2 bg-gray-700" style={{width: `${it.progress}%`}} />
            </div>
            <div className="mt-1 text-xs">
              Durum: {it.status}{it.key?` • ${it.key}`:''}{it.error?` • ${it.error}`:''}
            </div>
            {it.status!=='uploading' && it.status!=='done' && (
              <button className="mt-2 text-xs underline" onClick={() => uploadOne(i)}>Tek yükle</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}