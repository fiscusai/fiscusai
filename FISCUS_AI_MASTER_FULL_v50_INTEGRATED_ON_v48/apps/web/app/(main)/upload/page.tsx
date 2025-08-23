import PresignedUploader from '@/components/PresignedUploader';

export const metadata = { title: "Dosya Yükleme | FISCUS AI" };

export default function Page() {
  return (
    <section className="prose max-w-3xl py-8">
      <h1>Dosya Yükleme</h1>
      <p>Bu sayfa MinIO/S3'e ön imzalı yükleme yapar.</p>
      <PresignedUploader />
    <p>Birden fazla dosyayı seçebilir, ilerlemeyi canlı izleyebilirsiniz.</p></section>
  );
}