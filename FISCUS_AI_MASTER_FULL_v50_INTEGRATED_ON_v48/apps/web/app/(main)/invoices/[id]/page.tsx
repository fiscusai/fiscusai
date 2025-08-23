'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

export default function EditInvoicePage() {
  const params = useParams();
  const id = params?.id as string;
  const [form, setForm] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    const fetchOne = async () => {
      try {
        const r = await fetch(`${api}/invoices`);
        const list = await r.json();
        const cur = list.find((x:any) => x.id === id);
        setForm(cur);
      } catch (e:any) { setError(e.message); } finally { setLoading(false); }
    };
    fetchOne();
  }, [id]);

  const onChange = (e: any) => {
    const { name, value } = e.target;
    setForm((prev:any) => ({ ...prev, [name]: name === 'amount' ? Number(value) : value }));
  };

  const save = async () => {
    try {
      const r = await fetch(`${api}/invoices/${id}`, {
        method: 'PUT',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(form),
      });
      if (!r.ok) throw new Error('Güncelleme başarısız');
      alert('Güncellendi');
    } catch (e:any) {
      alert(e.message);
    }
  };

  if (loading) return <div className="p-6">Yükleniyor…</div>;
  if (!form) return <div className="p-6">Bulunamadı</div>;
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Fatura Düzenle</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {['id','date','customer','status'].map((k) => (
          <div key={k} className="flex flex-col">
            <label className="text-sm mb-1">{k.toUpperCase()}</label>
            <input className="border rounded px-3 py-2" name={k} value={(form as any)[k]}
              onChange={onChange} />
          </div>
        ))}
        <div className="flex flex-col">
          <label className="text-sm mb-1">AMOUNT</label>
          <input type="number" className="border rounded px-3 py-2" name="amount" value={form.amount} onChange={onChange} />
        </div>
        <div className="flex flex-col">
          <label className="text-sm mb-1">VAT RATE</label>
          <input className="border rounded px-3 py-2" name="vat_rate" value={form.vat_rate} onChange={onChange} />
        </div>
      </div>
      <div className="mt-4">
        <button onClick={save} className="px-4 py-2 border rounded hover:shadow">Kaydet</button>
      </div>
    </div>
  );
}
