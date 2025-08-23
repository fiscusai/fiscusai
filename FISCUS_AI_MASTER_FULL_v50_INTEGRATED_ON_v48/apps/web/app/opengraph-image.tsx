import { ImageResponse } from 'next/og'

export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image() {
  const title = 'FISCUS AI — Akıllı Muhasebe, Roma Disipliniyle'
  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg,#F2F2F0,#C9A54A)',
          color: '#2D2D2D',
          fontSize: 96,
          letterSpacing: -2,
          fontFamily: 'Cinzel, serif',
          textShadow: '0 2px 4px rgba(0,0,0,0.12)'
        }}
      >
        {title}
      </div>
    ),
    { ...size }
  )
}
