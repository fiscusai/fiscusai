'use client';
import { useEffect, useState } from 'react';
import { getLang } from '@/lib/t';

export default function LanguageSwitcher() {
  const [lang, setLang] = useState<'tr'|'en'>(getLang());

  useEffect(() => {
    // Başlangıçta localStorage ile senkronize et
    const current = getLang();
    if (current !== lang) setLang(current);
  }, []);

  function change(l: 'tr'|'en') {
    try {
      window.localStorage.setItem('lang', l);
      setLang(l);
      // Sayfayı yenileyelim ki metinler anında güncellensin
      window.location.reload();
    } catch (_) {}
  }

  return (
    <div className="inline-flex items-center gap-2 text-sm">
      <button
        onClick={() => change('tr')}
        className={`px-2 py-1 rounded ${lang==='tr' ? 'border' : 'opacity-70'}`}
        aria-pressed={lang==='tr'}
      >
        TR
      </button>
      <button
        onClick={() => change('en')}
        className={`px-2 py-1 rounded ${lang==='en' ? 'border' : 'opacity-70'}`}
        aria-pressed={lang==='en'}
      >
        EN
      </button>
    </div>
  );
}