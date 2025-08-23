import io, zipfile, json, smtplib, os
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path

def generate_bi_zip(from_date: str, to_date: str) -> bytes:
    # This is a mock: create small csv/parquet-like placeholders.
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('readme.txt', f'FISCUS BI Export\nFrom: {from_date}\nTo: {to_date}\nGenerated: {datetime.utcnow().isoformat()}Z\n')
        z.writestr('invoices.csv', 'id,number,customer,total\nINV-1,INV-1,Aurea,1200\n')
        z.writestr('invoices.parquet', b'PAR1')  # placeholder header
    return buf.getvalue()

def send_email_with_zip(to_email: str, zip_bytes: bytes, subject: str = "FISCUS BI Export"):
    host = os.getenv("SMTP_HOST", "localhost")
    port = int(os.getenv("SMTP_PORT", "1025"))
    sender = os.getenv("SMTP_SENDER", "no-reply@fiscus.ai")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content("BI export zip dosyası ektedir.")
    msg.add_attachment(zip_bytes, maintype="application", subtype="zip", filename="bi_export.zip")

    with smtplib.SMTP(host, port) as s:
        s.send_message(msg)

def run_bi_export_and_email(to_email: str, from_date: str, to_date: str) -> dict:
    z = generate_bi_zip(from_date, to_date)
    send_email_with_zip(to_email, z)
    return {"ok": True, "emailed_to": to_email, "size": len(z)}
