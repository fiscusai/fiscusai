import type { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = process.env.NEXT_PUBLIC_SITE_URL || 'https://fiscus.ai'
  return [
    { url: `${base}/`, changeFrequency: 'weekly', priority: 1.0 },
    { url: `${base}/pricing`, changeFrequency: 'monthly', priority: 0.8 },
    { url: `${base}/login`, changeFrequency: 'yearly', priority: 0.5 },
    { url: `${base}/register`, changeFrequency: 'yearly', priority: 0.5 },
  ]
}
