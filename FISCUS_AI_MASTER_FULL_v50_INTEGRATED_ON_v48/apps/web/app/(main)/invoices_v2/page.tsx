
import { fetchServer } from '@/lib/fetcher';

export const revalidate = 30;

type Listing<T> = { items: T[]; total: number; page: number; page_size: number }
type Invoice = { id?: string; number?: string; customer?: string; date?: string; total?: number; vat?: number; };

export default async function InvoicesV2Page({ searchParams }: { searchParams: { q?: string; sort?: string; page?: string; page_size?: string }}) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const q = searchParams.q ?? '';
  const sort = searchParams.sort ?? 'date:desc';
  const page = searchParams.page ?? '1';
  const page_size = searchParams.page_size ?? '20';
  const url = `${base}/v2/invoices/?q=${encodeURIComponent(q)}&sort=${encodeURIComponent(sort)}&page=${page}&page_size=${page_size}`;
  const data = await fetchServer<Listing<Invoice>>(url, 30);
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Faturalar V2 (SSR)</h1>
      <div className="text-sm opacity-70 mb-2">Toplam: {data.total}</div>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">No</th><th className="p-2 text-left">Müşteri</th>
          <th className="p-2 text-left">Tarih</th><th className="p-2 text-right">Tutar</th><th className="p-2 text-right">KDV</th>
        </tr></thead>
        <tbody>
          {data.items.map((it, i)=>(
            <tr key={it.id || i} className="border-t">
              <td className="p-2">{it.number}</td>
              <td className="p-2">{it.customer}</td>
              <td className="p-2">{it.date}</td>
              <td className="p-2 text-right">{it.total}</td>
              <td className="p-2 text-right">{it.vat}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
