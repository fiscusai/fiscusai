import tr from '../locales/tr.json';
import en from '../locales/en.json';

export type Lang = 'tr' | 'en';

export function getLang(): Lang {
  if (typeof window === 'undefined') return 'tr';
  const stored = window.localStorage.getItem('lang');
  if (stored === 'en' || stored === 'tr') return stored;
  const nav = (navigator?.language || 'tr').toLowerCase();
  return nav.startsWith('en') ? 'en' : 'tr';
}

export function t(key: string, lang?: Lang): string {
  const l = lang || getLang();
  const dict = l === 'en' ? en : tr;
  return (dict as any)[key] || key;
}