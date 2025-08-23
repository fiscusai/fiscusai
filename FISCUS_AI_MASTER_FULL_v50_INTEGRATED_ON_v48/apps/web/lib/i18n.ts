import tr from '../messages/tr.json'
import en from '../messages/en.json'

export type Locale = 'tr' | 'en'

const dict = { tr, en } as const

export function t(key: keyof typeof tr, locale: Locale = 'tr') {
  return (dict[locale] as any)[key] ?? key
}
