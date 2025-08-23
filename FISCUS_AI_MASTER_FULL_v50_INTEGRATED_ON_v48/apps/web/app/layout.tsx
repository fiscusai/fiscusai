export const metadata = { manifest: '/site.webmanifest',   title: "FISCUS AI", description: "Akıllı Muhasebe, Roma Disipliniyle." , openGraph: { title: 'FISCUS AI', description: 'Akıllı Muhasebe, Roma Disipliniyle.', type: 'website' }, twitter: { card: 'summary_large_image', title: 'FISCUS AI', description: 'Akıllı Muhasebe, Roma Disipliniyle.' } };

import Analytics from '@/components/Analytics';
import ServiceWorker from '@/components/ServiceWorker';
import LanguageSwitcher from '@/components/LanguageSwitcher';
import CookieConsent from '@/components/CookieConsent';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
<head>
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous"/>
        <link rel="preload" as="image" href="/og.png"/>
      </head>
      <body className="min-h-screen bg-[#F2F2F0] text-[#2D2D2D]">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <header className="flex items-center justify-between">
            <div className="font-serif text-2xl">FISCUS AI</div>
            <nav className="space-x-4">
              <a href="/pricing">Fiyatlandırma</a>
              <a href="/about">Hakkımızda</a>
              <a href="/auth/login" className="border px-3 py-1 rounded">Giriş</a>
            <LanguageSwitcher /></nav>
          </header>
          <main>{children}</main>
          <footer className="mt-16 text-sm text-gray-600">© {new Date().getFullYear()} FISCUS AI</footer>
        </div>
        <Analytics />
              <ServiceWorker />
      </body>
    </html>
  );
}
