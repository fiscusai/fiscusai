
export default function Pricing() {
  const plans = [
    {name:'Basic', price:'₺299/ay', features:['Fatura & Gider','Raporlar','İhracat (CSV/PDF)']},
    {name:'Pro', price:'₺799/ay', features:['AI İçgörüler','Banka Mutabakatı','Yetki/Log']},
    {name:'Enterprise', price:'İletişime geçin', features:['Çok-şirket','SLA & Destek','Özel entegrasyonlar']},
  ];
  return (
    <section className="max-w-5xl mx-auto px-6 py-16">
      <h2 className="text-3xl font-semibold text-center mb-8">Fiyatlandırma</h2>
      <div className="grid md:grid-cols-3 gap-6">
        {plans.map(p=> (
          <div key={p.name} className="border rounded-lg p-6 hover:shadow-lg transition relative">
            <div className="absolute inset-x-0 -top-[1px] h-[2px] bg-gradient-to-r from-yellow-600 via-yellow-400 to-yellow-600"></div>
            <div className="text-xl font-medium">{p.name}</div>
            <div className="text-2xl mt-2">{p.price}</div>
            <ul className="mt-4 space-y-1 text-sm opacity-80">
              {p.features.map(f=>(<li key={f}>• {f}</li>))}
            </ul>
            <a href="/(auth)/register" className="mt-6 inline-block px-4 py-2 border border-yellow-600 rounded">Seç</a>
          </div>
        ))}
      </div>
    </section>
  );
}
