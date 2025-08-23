import { fetchServer } from '@/lib/fetcher';
type Customer = { id?: string; name?: string; email?: string; tax_id?: string; };
export const revalidate = 60;
export default async function CustomersV2Page() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const items: Customer[] = await fetchServer(`${base}/v2/customers`, 60);
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Müşteriler (V2)</h1>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">Ad</th>
          <th className="p-2 text-left">Email</th>
          <th className="p-2 text-left">Vergi No</th>
        </tr></thead>
        <tbody>
          {items.map((it, idx)=> (
            <tr key={it.id || idx} className="border-t">
              <td className="p-2">{it.name}</td>
              <td className="p-2">{it.email}</td>
              <td className="p-2">{it.tax_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
