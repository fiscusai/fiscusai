export default function NotFound() {
  return (
    <div className="min-h-[50vh] flex items-center justify-center text-center p-10">
      <div>
        <h1 className="text-3xl font-bold">Sayfa bulunamadı (404)</h1>
        <p className="mt-2 opacity-70">Aradığınız sayfa kaldırılmış veya hiç var olmamış olabilir.</p>
      </div>
    </div>
  );
}
