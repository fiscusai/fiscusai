import { fetchServer } from '@/lib/fetcher';

type Expense = { id?: string; date?: string; category?: string; amount?: number; vat?: number; };
export const revalidate = 120;

export default async function ExpensesPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const items: Expense[] = await fetchServer(`${base}/expenses/`, 120);
  const total = items.reduce((s, x) => s + (x.amount || 0), 0);
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-semibold">Giderler</h1>
      </div>
      <div className="mb-2 text-sm opacity-80">Toplam: {total.toLocaleString?.() ?? total}</div>
      <table className="w-full border">
        <thead><tr className="bg-gray-100">
          <th className="p-2 text-left">ID</th>
          <th className="p-2 text-left">Tarih</th>
          <th className="p-2 text-left">Kategori</th>
          <th className="p-2 text-right">Tutar</th>
          <th className="p-2 text-right">KDV</th>
        </tr></thead>
        <tbody>
          {items.map((it, idx) => (
            <tr key={it.id || idx} className="border-t">
              <td className="p-2">{it.id}</td>
              <td className="p-2">{it.date}</td>
              <td className="p-2">{it.category}</td>
              <td className="p-2 text-right">{it.amount?.toLocaleString?.() ?? it.amount}</td>
              <td className="p-2 text-right">{it.vat?.toLocaleString?.() ?? it.vat}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
