'use client';
import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js';
Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export default function AIPanel() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const [anoms, setAnoms] = useState<any>({outliers:[], duplicates:[]});
  const [forecast, setForecast] = useState<any>({history:[], forecast:[]});

  useEffect(()=>{
    (async ()=>{
      const a = await fetch(`${base}/ai_adv/anomalies`).then(r=>r.json());
      setAnoms(a);
      const f = await fetch(`${base}/ai_adv/cashflow_forecast?months=3`).then(r=>r.json());
      setForecast(f);
    })();
  }, []);

  return (
    <div className="p-6 grid gap-6">
      <h1 className="text-xl font-semibold">AI Paneli</h1>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="border rounded p-3">
          <div className="font-medium mb-1">Anomaliler</div>
          <div className="text-sm opacity-70 mb-2">Aykırı değerler ve mükerrer fatura numaraları</div>
          <div className="text-sm">
            <div className="font-medium">Outliers</div>
            <ul className="list-disc ml-5">
              {anoms.outliers?.map((o:any,i:number)=>(
                <li key={i}>#{o.number} — {o.total?.toLocaleString()} (z={o.z?.toFixed(2)})</li>
              ))}
            </ul>
            <div className="font-medium mt-2">Duplicates</div>
            <ul className="list-disc ml-5">
              {anoms.duplicates?.map((d:any,i:number)=>(
                <li key={i}>#{d.number}</li>
              ))}
            </ul>
          </div>
        </div>
        <div className="border rounded p-3">
          <div className="font-medium mb-1">Nakit Akışı Tahmini (3 Ay)</div>
          <Line data={{
            labels: [
              ...forecast.history?.map((h:any)=>h.month),
              ...forecast.forecast?.map((f:any)=>`+${f.month_index}`)
            ],
            datasets: [
              { label: 'Geçmiş', data: forecast.history?.map((h:any)=>h.cashflow) || [] },
              { label: 'Tahmin', data: (
                (forecast.history?.map((_:any)=>null) || []).concat(forecast.forecast?.map((f:any)=>f.cashflow) || [])
              ) }
            ]
          }} />
        </div>
      </div>
    </div>
  );
}
