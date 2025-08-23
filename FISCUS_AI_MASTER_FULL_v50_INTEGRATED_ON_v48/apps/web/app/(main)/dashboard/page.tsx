'use client';
import { useEffect, useState } from 'react';
import { apiGet } from '@/lib/fetcher';
import KpiCard from '@/components/KpiCard';
import RevenueChart from '@/components/RevenueChart';

export default function DashboardPage() {
  const labels = ['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu'];
  const data = [12000, 18000, 15000, 22000, 24000, 26000, 28000, 30000];
  return (
    <div className="space-y-6">
      <h1 className="font-serif text-3xl tracking-wide">Gösterge Paneli</h1>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <KpiCard title="Aylık Gelir" value="₺30.000" hint="+%6 artış" />
        <KpiCard title="Bekleyen Tahsilat" value="₺59.500" />
        <KpiCard title="Giderler" value="₺18.900" />
        <KpiCard title="KDV" value="₺5.760" />
      </div>
      <div className="rounded-lg border border-zinc-200 bg-white p-4">
        <div className="mb-3 text-sm text-zinc-600">Gelir Trendi</div>
        <RevenueChart labels={labels} data={data} />
      </div>
    </div>
  );
}

// ISR example usage
