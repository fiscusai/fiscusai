import Image from 'next/image';

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      <Image
        src="/images/hero-marble.webp"
        alt="Marble"
        fill
        sizes="100vw"
        priority
        style={{ objectFit: 'cover', opacity: 0.25 }}
      />
      <div className="relative z-10 max-w-5xl mx-auto px-6 py-28">
        <h1 className="text-4xl md:text-6xl font-semibold tracking-tight">FISCUS AI</h1>
        <p className="mt-3 text-lg opacity-80">Akıllı Muhasebe, Roma Disipliniyle.</p>
        <div className="mt-6">
          <a className="px-5 py-3 border rounded bg-black text-white">Hemen Başla</a>
        </div>
      </div>
    </section>
  );
}

{/* Prefetch örneği */}
<link rel="prefetch" href="/pricing" />
<link rel="prefetch" href="/about" />
