'use client';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
export default function RedirectPage() {
  const r = useRouter();
  useEffect(()=>{ r.replace('/(main)/customers_v2'); }, [r]);
  return null;
}
