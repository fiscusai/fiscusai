export default function Page(){
  return (
    <main className="min-h-screen">
      <section className="relative overflow-hidden bg-mermer">
        <div className="absolute inset-0 opacity-20" style={{backgroundImage:"url(/textures/marble.jpg)", backgroundSize:"cover"}} />
        <div className="relative max-w-6xl mx-auto px-6 py-28 text-center">
          <h1 className="font-display text-5xl md:text-6xl text-fiscus">FISCUS AI — Akıllı Muhasebe, Roma Disipliniyle</h1>
          <p className="mt-6 text-lg text-fiscus/80">Fatura, gelir–gider, banka entegrasyonu ve AI içgörüleri tek platformda.</p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <a href="/(dashboard)" className="px-6 py-3 rounded-md border border-altin hover:shadow-soft">Kontrol Paneli</a>
            <a href="/pricing" className="px-6 py-3 rounded-md bg-fiscus text-mermer hover:opacity-90">Planları Gör</a>
          </div>
        </div>
      </section>
    </main>
  )
}
