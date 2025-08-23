import { NextRequest, NextResponse } from 'next/server'
export async function POST(req: NextRequest){
  const body = await req.json()
  const api = process.env.NEXT_PUBLIC_API_BASE
  const res = await fetch(api + '/auth/login', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) })
  if(!res.ok) return new NextResponse('Unauthorized', { status: 401 })
  const data = await res.json()
  const resp = NextResponse.json({ ok:true })
  resp.cookies.set('access_token', data.access_token, { httpOnly:true, secure:true, sameSite:'strict', path:'/' })
  resp.cookies.set('refresh_token', data.refresh_token, { httpOnly:true, secure:true, sameSite:'strict', path:'/' })
  return resp
}
