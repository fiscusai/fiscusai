import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const r = await fetch(`${api}/health`)
    const json = await r.json()
    res.status(200).json(json)
  } catch (e) {
    res.status(500).json({ ok: false, error: 'proxy_error' })
  }
}
