'use client';
import { useState } from 'react';

const perms = [
  { action: 'invoice:create', admin: true, accountant: true, user: false },
  { action: 'invoice:update', admin: true, accountant: true, user: false },
  { action: 'invoice:delete', admin: true, accountant: false, user: false },
  { action: 'export:bi', admin: true, accountant: true, user: false },
  { action: 'settings:access', admin: true, accountant: false, user: false },
];

export default function RBACPage() {
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">İzin Matrisi (Demo)</h1>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">Aksiyon</th>
          <th className="p-2">Admin</th>
          <th className="p-2">Accountant</th>
          <th className="p-2">User</th>
        </tr></thead>
        <tbody>
          {perms.map(p => (
            <tr key={p.action} className="border-t">
              <td className="p-2">{p.action}</td>
              <td className="p-2 text-center">{p.admin ? '✓' : '—'}</td>
              <td className="p-2 text-center">{p.accountant ? '✓' : '—'}</td>
              <td className="p-2 text-center">{p.user ? '✓' : '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
