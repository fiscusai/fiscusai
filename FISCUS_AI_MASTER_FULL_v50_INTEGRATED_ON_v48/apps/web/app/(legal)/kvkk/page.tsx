import { t } from '@/lib/t';
export const metadata = { title: "KVKK Aydınlatma Metni | FISCUS AI" };

export default function Page() {
  return (
    <>
      <section className="prose max-w-3xl py-8">
  <h1>{t('legal.kvkk.title')}</h1>
  <h2>Veri Sorumlusu</h2>
<p>{t('legal.kvkk.section1')}</p>
<h2>Kişisel Verilerin İşlenme Amaçları</h2>
<p>Hizmetlerin sunulması, güvenlik, yasal yükümlülüklerin yerine getirilmesi.</p>
<h2>İşlenen Veri Kategorileri</h2>
<p>Kimlik, iletişim, işlem güvenliği, finans, müşteri işlem verileri.</p>
<h2>Aktarım</h2>
<p>Yasal yükümlülükler ve hizmet sağlayıcılarla sınırlı olarak aktarım yapılabilir.</p>
<h2>Haklarınız</h2>
<p>KVKK md.11 kapsamındaki tüm haklarınızı kullanabilirsiniz.</p>
<h2>İletişim</h2>
<p>kvkk@fiscus.ai üzerinden bize ulaşabilirsiniz.</p>
</section>
    </>
  );
}