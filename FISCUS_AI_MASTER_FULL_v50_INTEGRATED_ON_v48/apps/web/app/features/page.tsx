export default function Features() {
  const items = [
    {h:'Fatura & OCR', p:'E-fatura/e-arşiv ve AI tabanlı sınıflandırma'},
    {h:'Gelir–Gider', p:'Gerçek zamanlı grafikler, oran analizleri'},
    {h:'Raporlar', p:'KDV, nakit akışı, tahsilat günleri'},
    {h:'Banka Entegrasyonu', p:'Türkiye bankaları; mutabakat ve içe aktarma'},
    {h:'AI Paneli', p:'Özetleme, anomali tespiti, tahmin ve aksiyon'},
    {h:'KVKK & Güvenlik', p:'Şifreleme, log maskeleme, rol/izin matrisi'},
  ]
  return (
    <div className="mx-auto max-w-6xl px-4 py-12">
      <h1 className="font-serif text-3xl">Özellikler</h1>
      <div className="mt-8 grid gap-6 md:grid-cols-2">
        {items.map((x, i) => (
          <div key={i} className="rounded-lg border border-[#C9A54A]/40 bg-white p-5 shadow-sm">
            <h3 className="font-serif text-xl">{x.h}</h3>
            <p className="mt-2 text-sm text-[#2D2D2D]/75">{x.p}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
