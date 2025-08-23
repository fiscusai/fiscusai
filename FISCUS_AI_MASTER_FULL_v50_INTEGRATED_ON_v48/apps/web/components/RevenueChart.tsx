'use client';
import { Line } from 'react-chartjs-2';
import { Chart, LineElement, LinearScale, CategoryScale, PointElement, Tooltip, Legend } from 'chart.js';
Chart.register(LineElement, LinearScale, CategoryScale, PointElement, Tooltip, Legend);

export default function RevenueChart({ labels, data }: { labels: string[]; data: number[] }) {
  const cfg = {
    labels,
    datasets: [
      {
        label: 'Gelir',
        data,
        fill: false,
      },
    ],
  };
  const opts = {
    responsive: true,
    maintainAspectRatio: false,
  };
  return <div style={{height: 260}}><Line data={cfg} options={opts as any} /></div>;
}
