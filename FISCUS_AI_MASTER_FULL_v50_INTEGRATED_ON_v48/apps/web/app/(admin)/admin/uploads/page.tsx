'use client';
import { useEffect, useState } from 'react';

export const metadata = { title: "Admin • Son Yüklemeler | FISCUS AI" };

export default function Page() {
  const [items, setItems] = useState<string[]>([]);
  const [msg, setMsg] = useState<string>('');

  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const token = typeof window !== 'undefined' ? localStorage.getItem('api_token') : null;

  async function load() {
    setMsg('');
    try {
      const r = await fetch(`${api}/admin/uploads/recent`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!r.ok) throw new Error('Yetki veya API hatası');
      const j = await r.json();
      setItems(j.items || []);
    } catch (e:any) {
      setMsg(e.message || 'Hata');
    }
  }

  async function del(key: string) {
    setMsg('Siliniyor...');
    try {
      const r = await fetch(`${api}/admin/uploads?key=${encodeURIComponent(key)}`, {
        method: 'DELETE',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!r.ok) throw new Error('Silme başarısız');
      await load();
      setMsg('Silindi');
    } catch (e:any) {
      setMsg(e.message || 'Hata');
    }
  }

  async function rescan(key: string) {
    setMsg('Yeniden taranıyor...');
    try {
      const r = await fetch(`${api}/admin/uploads/rescan?key=${encodeURIComponent(key)}`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!r.ok) throw new Error('Tarama başarısız');
      setMsg('Tarama tetiklendi');
    } catch (e:any) {
      setMsg(e.message || 'Hata');
    }
  }

  useEffect(() => { load(); }, []);

  return (
    <section className="prose max-w-3xl py-8">
      <h1>Admin • Son Yüklemeler</h1>
      {msg && <p className="text-sm text-gray-600">{msg}</p>}
      {!items.length && <p>Kayıt yok.</p>}
      <ul className="space-y-2">
        {items.map((k,i) => (
          <li key={i} className="border rounded p-3">
            <div className="flex items-center justify-between">
              <code className="truncate">{k}</code>
              <div className="flex gap-2">
                <button className="text-xs underline" onClick={() => rescan(k)}>Tekrar Tara</button>
                <button className="text-xs underline" onClick={() => del(k)}>Sil</button>
              </div>
            </div>
          </li>
        ))}
      </ul>
      <button className="mt-4 text-xs underline" onClick={load}>Yenile</button>
    </section>
  );
}