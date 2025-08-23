'use client';
import { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const [ok, setOk] = useState<boolean>(false);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const t = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (!t) {
      router.replace('/(auth)/login?next=' + encodeURIComponent(pathname || '/(main)/dashboard'));
    } else {
      setOk(true);
    }
  }, [pathname]);

  if (!ok) return null;
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">{children}</div>
    </div>
  );
}
