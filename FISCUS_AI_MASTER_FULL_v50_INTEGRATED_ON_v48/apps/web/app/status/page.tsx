import { fetchServer } from '@/lib/fetcher';

export const revalidate = 30;

export default async function StatusPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const health = await fetchServer(`${base}/health`, 30).catch(()=>({ok:false}));
  const deep = await fetchServer(`${base}/health/deep`, 30).catch(()=>({}));
  const ver = await fetchServer(`${base}/status/version`, 30).catch(()=>({version:'unknown'}));

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-xl font-semibold">Sistem Durumu</h1>
      <div className="grid md:grid-cols-3 gap-3">
        <div className="p-4 border rounded"><div className="text-xs opacity-70">API</div><div className="text-lg">{health.ok ? 'UP' : 'DOWN'}</div></div>
        <div className="p-4 border rounded"><div className="text-xs opacity-70">Uptime</div><div className="text-lg">{deep.uptime ?? '—'}</div></div>
        <div className="p-4 border rounded"><div className="text-xs opacity-70">Sürüm</div><div className="text-lg">{ver.version}</div></div>
      </div>
    </div>
  );
}
