import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname

  const match = path.match(/^\/([vrcpsgi])(\d+)(?:\/.*)?$/)

  if (match) {
    const newPath = `/${match[1]}/${match[2]}`
    return NextResponse.redirect(new URL(newPath, request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/(v|r|c|p|s|g|i)(\\d+)(/.*)?']
}