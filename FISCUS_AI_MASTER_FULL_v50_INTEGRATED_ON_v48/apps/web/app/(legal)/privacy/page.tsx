import { t } from '@/lib/t';
export const metadata = { title: "Privacy Policy | FISCUS AI" };

export default function Page() {
  return (
    <>
      <section className="prose max-w-3xl py-8">
  <h1>{t('legal.privacy.title')}</h1>
  <h2>Controller</h2>
<p>{t('legal.privacy.section1')}</p>
<h2>Data We Collect</h2>
<p>Account data, usage data, logs, and optional billing information.</p>
<h2>Purpose of Processing</h2>
<p>To provide and improve services, ensure security, meet legal obligations.</p>
<h2>Data Sharing</h2>
<p>Shared with processors and authorities where required by law.</p>
<h2>Your Rights</h2>
<p>Access, rectification, erasure, objection, portability (as applicable).</p>
<h2>Contact</h2>
<p>privacy@fiscus.ai</p>
</section>
    </>
  );
}