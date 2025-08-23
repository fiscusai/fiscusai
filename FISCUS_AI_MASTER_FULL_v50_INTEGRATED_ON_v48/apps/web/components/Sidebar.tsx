'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const items = [
  { href: '/dashboard', label: 'Gösterge Paneli' },
  { href: '/invoices', label: 'Faturalar' },
  { href: '/customers', label: 'Müşteriler' },
  { href: '/reports', label: 'Raporlar' },
  { href: '/ai', label: 'AI Paneli' },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="w-64 shrink-0 border-r border-zinc-200 bg-white/70 backdrop-blur-sm">
      <div className="p-4 font-serif text-xl tracking-widest">FISCUS AI</div>
      <nav className="flex flex-col">
        {items.map(i => (
          <Link key={i.href} href={i.href} className={`px-4 py-2 hover:bg-zinc-50 ${pathname === i.href ? 'text-amber-700 font-medium' : 'text-zinc-700'}`}>
            {i.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
