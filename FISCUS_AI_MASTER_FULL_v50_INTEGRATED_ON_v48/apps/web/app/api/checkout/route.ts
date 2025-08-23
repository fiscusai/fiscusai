import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
export async function POST(req: NextRequest){
  const { priceKey } = await req.json()
  const secret = process.env.STRIPE_SECRET_KEY || ''
  const price = process.env[priceKey] || ''
  if(!secret || !price) return NextResponse.json({ error:'Stripe config missing' }, { status: 400 })
  const stripe = new Stripe(secret, { apiVersion: '2024-06-20' } as any)
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    line_items: [{ price, quantity: 1 }],
    success_url: req.nextUrl.origin + '/(dashboard)',
    cancel_url: req.nextUrl.origin + '/pricing'
  })
  return NextResponse.json({ url: session.url })
}
