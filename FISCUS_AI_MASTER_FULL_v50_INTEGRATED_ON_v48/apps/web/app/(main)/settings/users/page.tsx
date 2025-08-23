'use client';
import { useEffect, useState } from 'react';
import { apiFetch } from '@/lib/apiClient';

type User = { id: string; email: string; role: 'admin'|'accountant'|'user' };

export default function AdminUsersPage() {
  const [items, setItems] = useState<User[]>([]);

  const load = async () => {
    const j = await apiFetch('/users/');
    setItems(j);
  };
  useEffect(()=>{ load(); }, []);

  const changeRole = async (id: string, role: User['role']) => {
    await apiFetch(`/users/${id}/role`, {
      method: 'PUT',
      body: JSON.stringify({ role })
    });
    await load();
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Kullanıcı Yönetimi</h1>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">Email</th>
          <th className="p-2 text-left">Rol</th>
          <th className="p-2"></th>
        </tr></thead>
        <tbody>
          {items.map(u => (
            <tr key={u.id} className="border-t">
              <td className="p-2">{u.email}</td>
              <td className="p-2">{u.role}</td>
              <td className="p-2 text-right">
                <div className="flex gap-2 justify-end">
                  <button onClick={()=>changeRole(u.id,'user')} className="px-2 py-1 border rounded">User</button>
                  <button onClick={()=>changeRole(u.id,'accountant')} className="px-2 py-1 border rounded">Accountant</button>
                  <button onClick={()=>changeRole(u.id,'admin')} className="px-2 py-1 border rounded">Admin</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
