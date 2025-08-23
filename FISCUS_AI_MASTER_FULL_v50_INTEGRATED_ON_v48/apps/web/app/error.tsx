'use client';
export default function GlobalError({ error, reset }: { error: Error & { digest?: string }, reset: () => void }) {
  return (
    <html>
      <body>
        <div className="min-h-[50vh] flex items-center justify-center text-center p-10">
          <div>
            <h1 className="text-3xl font-bold">Bir hata oluştu</h1>
            <p className="mt-2 opacity-70">{error?.message || 'Bilinmeyen hata'}</p>
            <button onClick={reset} className="mt-4 px-4 py-2 border rounded">Tekrar dene</button>
          </div>
        </div>
      </body>
    </html>
  );
}
