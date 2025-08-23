
'use client';
import { useEffect, useState } from 'react';

export type Role = 'admin' | 'accountant' | 'user';
type Me = { email?: string; role?: Role };

export default function useAuth() {
  const [me, setMe] = useState<Me | null>(null);
  useEffect(()=>{
    const raw = localStorage.getItem('fiscus_auth');
    if (raw) {
      try { setMe(JSON.parse(raw)); } catch {}
    }
  }, []);
  const is = (r: Role) => me?.role === r;
  return { me, isAdmin: is('admin'), isAccountant: is('accountant'), isUser: is('user') };
}
