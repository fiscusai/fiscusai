import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
export function middleware(req: NextRequest) {
  const access = req.cookies.get('access_token')?.value
  if (req.nextUrl.pathname.startsWith('/(dashboard)')) {
    if (!access) {
      const url = req.nextUrl.clone(); url.pathname = '/(auth)/login'
      return NextResponse.redirect(url)
    }
  }
  return NextResponse.next()
}
