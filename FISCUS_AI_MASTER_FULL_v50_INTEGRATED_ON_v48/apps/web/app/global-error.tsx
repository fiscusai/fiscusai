
'use client';
export default function GlobalError({ error, reset }: { error: Error & { digest?: string }, reset: () => void }) {
  return (
    <html>
      <body>
        <div style={{padding:20}}>
          <h1>Bir şeyler ters gitti</h1>
          <p style={{opacity:.7}}>{error?.message || 'Bilinmeyen hata'}</p>
          <button onClick={reset} style={{padding:'8px 12px', border:'1px solid #ddd'}}>Tekrar dene</button>
        </div>
      </body>
    </html>
  );
}
