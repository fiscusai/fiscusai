import { NextRequest, NextResponse } from 'next/server'
export async function POST(req: NextRequest){
  const api = process.env.NEXT_PUBLIC_API_BASE
  const refresh = req.cookies.get('refresh_token')?.value
  if(!refresh) return new NextResponse('No refresh', { status: 401 })
  const res = await fetch(api + '/auth/refresh', { method:'POST', headers:{ Authorization: 'Bearer ' + refresh } })
  if(!res.ok) return new NextResponse('Refresh failed', { status: 401 })
  const data = await res.json()
  const resp = NextResponse.json({ ok:true })
  resp.cookies.set('access_token', data.access_token, { httpOnly:true, secure:true, sameSite:'strict', path:'/' })
  resp.cookies.set('refresh_token', data.refresh_token, { httpOnly:true, secure:true, sameSite:'strict', path:'/' })
  return resp
}
