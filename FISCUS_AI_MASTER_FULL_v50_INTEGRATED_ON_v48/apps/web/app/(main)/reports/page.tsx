import { fetchServer } from '@/lib/fetcher';
import { Bar } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
Chart.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export const revalidate = 300;

export default async function ReportsPage() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const summary = await fetchServer(`${base}/reports/summary`, 300);
  const trend = await fetchServer(`${base}/reports/revenue-trend`, 300);
  const data = trend.data || [];
  const labels = data.map((d:any)=>d.month);
  const values = data.map((d:any)=>d.total);

  return (
    <div className="p-6 grid gap-6">
      <h1 className="text-xl font-semibold">Raporlar</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-4 border rounded"><div className="text-xs opacity-70">Gelir</div><div className="text-lg font-semibold">{summary.revenue?.toLocaleString?.() ?? summary.revenue}</div></div>
        <div className="p-4 border rounded"><div className="text-xs opacity-70">Gider</div><div className="text-lg font-semibold">{summary.cost?.toLocaleString?.() ?? summary.cost}</div></div>
        <div className="p-4 border rounded"><div className="text-xs opacity-70">Nakit Akışı</div><div className="text-lg font-semibold">{summary.cashflow?.toLocaleString?.() ?? summary.cashflow}</div></div>
        <div className="p-4 border rounded"><div className="text-xs opacity-70">KDV (Alınan / Ödenen)</div><div className="text-lg font-semibold">{summary.vat_collected?.toLocaleString?.() ?? summary.vat_collected} / {summary.vat_paid?.toLocaleString?.() ?? summary.vat_paid}</div></div>
      </div>
      <div className="p-4 border rounded">
        <div className="mb-2 font-medium">Aylık Gelir Trendi</div>
        <Bar data={{ labels, datasets: [{ label: 'Gelir', data: values }] }} />
      </div>
    </div>
  );
}
