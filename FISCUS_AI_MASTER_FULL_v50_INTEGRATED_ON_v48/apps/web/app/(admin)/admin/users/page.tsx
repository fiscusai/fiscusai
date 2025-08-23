'use client';
import { useEffect, useState } from 'react';

export const metadata = { title: "Admin • Users | FISCUS AI" };

type Row = { id:number; sub:string; role:string; ts:string };

export default function Page() {
  const [items, setItems] = useState<Row[]>([]);
  const [sub, setSub] = useState('');
  const [role, setRole] = useState('uploader');
  const [msg, setMsg] = useState('');
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const token = typeof window !== 'undefined' ? localStorage.getItem('api_token') : null;

  async function load() {
    setMsg('');
    try {
      const r = await fetch(`${api}/admin/users`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
      if (!r.ok) throw new Error('Yetki veya API hatası');
      const j = await r.json();
      setItems(j);
    } catch (e:any) {
      setMsg(e.message || 'Hata');
    }
  }
  async function save() {
    setMsg('Kaydediliyor...');
    try {
      const r = await fetch(`${api}/admin/users?sub=${encodeURIComponent(sub)}&role=${encodeURIComponent(role)}`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!r.ok) throw new Error('Kayıt başarısız');
      setSub(''); setRole('uploader');
      await load();
      setMsg('Kaydedildi');
    } catch (e:any) {
      setMsg(e.message || 'Hata');
    }
  }
  async function del(s: string) {
    setMsg('Siliniyor...');
    try {
      const r = await fetch(`${api}/admin/users?sub=${encodeURIComponent(s)}`, {
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

  useEffect(()=>{ load(); }, []);

  return (
    <section className="prose max-w-4xl py-8">
      <h1>Admin • Users</h1>
      {msg && <p className="text-sm text-gray-600">{msg}</p>}
      <div className="flex gap-2 items-end">
        <div><label>Kullanıcı (sub)<br/><input className="border px-2 py-1" value={sub} onChange={e=>setSub(e.target.value)} placeholder="email@example.com" /></label></div>
        <div><label>Rol<br/>
          <select className="border px-2 py-1" value={role} onChange={e=>setRole(e.target.value)}>
            <option value="uploader">uploader</option>
            <option value="admin">admin</option>
          </select>
        </label></div>
        <button className="border px-3 py-1 rounded" onClick={save} disabled={!sub}>Kaydet</button>
      </div>

      <table className="min-w-full text-sm border mt-4">
        <thead><tr className="bg-gray-100">
          <th className="border px-2 py-1 text-left">sub</th>
          <th className="border px-2 py-1 text-left">role</th>
          <th className="border px-2 py-1 text-left">ts</th>
          <th className="border px-2 py-1">işlem</th>
        </tr></thead>
        <tbody>
          {items.map(r => (
            <tr key={r.id}>
              <td className="border px-2 py-1">{r.sub}</td>
              <td className="border px-2 py-1">{r.role}</td>
              <td className="border px-2 py-1">{r.ts}</td>
              <td className="border px-2 py-1 text-center">
                <button className="text-xs underline" onClick={()=>del(r.sub)}>Sil</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}