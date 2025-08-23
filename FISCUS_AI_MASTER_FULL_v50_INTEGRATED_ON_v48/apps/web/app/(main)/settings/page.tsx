'use client';
import { hasRole } from '@/lib/useAuth';
import { useEffect, useState } from 'react';

export default function SettingsPage() {
  const [allowed, setAllowed] = useState(false);
  useEffect(() => { setAllowed(hasRole(['admin'])); }, []);

  if (!allowed) {
    return <div className="p-6"><h1 className="text-xl font-semibold">Ayarlar</h1><p>Bu sayfa sadece yöneticiler içindir.</p></div>;
  }

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Ayarlar (Admin)</h1>
      <section className="p-4 border rounded">
        <div className="font-medium mb-2">Sistem</div>
        <button className="px-3 py-2 border rounded">Yedek Al</button>
        <button className="px-3 py-2 border rounded">Veritabanını Optimize Et</button>
      </section>
      <section className="p-4 border rounded">
        <div className="font-medium mb-2">Kullanıcı Yetkileri</div>
        <button className="px-3 py-2 border rounded">Yeni Kullanıcı Ekle</button>
      </section>
    </div>
  );
}
