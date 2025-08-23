'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  const [ok, setOk] = useState(true);
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  useEffect(()=>{
    (async ()=>{
      try {
        const st = await fetch(`${base}/2fa/status`).then(r=>r.json());
        const isEnabled = !!st.enabled;
        const auth = JSON.parse(localStorage.getItem('fiscus_auth') || '{}');
        if (auth?.role === 'admin' && !isEnabled) setOk(false);
      } catch (e) { /* ignore */ }
    })();
  }, []);

  if (!ok) {
    return (
      <div className="p-6 grid gap-3">
        <div className="p-4 border rounded bg-yellow-50">
          Admin ayarlarına erişmek için 2FA etkin olmalı. Lütfen 2FA kurulumunu tamamlayın.
        </div>
        <Link className="px-4 py-2 border rounded bg-black text-white w-fit" href="/(main)/settings/2fa">2FA Ayarına Git</Link>
      </div>
    );
  }

  return <>{children}</>;
}
