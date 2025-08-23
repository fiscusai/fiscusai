import { NextResponse } from 'next/server'
export async function POST(){
  const resp = NextResponse.json({ ok:true })
  resp.cookies.set('access_token','',{ httpOnly:true, expires:new Date(0), path:'/' })
  resp.cookies.set('refresh_token','',{ httpOnly:true, expires:new Date(0), path:'/' })
  return resp
}
