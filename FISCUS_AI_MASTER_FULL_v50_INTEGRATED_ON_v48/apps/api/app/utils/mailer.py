import os, smtplib, ssl, pathlib, json
from email.message import EmailMessage
from typing import Optional

def _write_dev_mail(subject: str, to: str, html: str):
    out_dir = os.getenv("MAIL_OUT_DIR", "/tmp/mail_out")
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    fname = pathlib.Path(out_dir) / f"mail_{to.replace('@','_')}.eml"
    data = f"Subject: {subject}\nTo: {to}\nContent-Type: text/html; charset=utf-8\n\n{html}"
    fname.write_text(data, encoding="utf-8")
    return str(fname)

def send_email(subject: str, to: str, html: str) -> str:
    provider = os.getenv("MAIL_PROVIDER", "dev").lower()
    if provider in ("", "dev"):
        return _write_dev_mail(subject, to, html)

    if provider == "smtp":
        host = os.getenv("SMTP_HOST")
        port = int(os.getenv("SMTP_PORT", "587"))
        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASS")
        use_tls = os.getenv("SMTP_TLS", "1") == "1"
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = os.getenv("MAIL_FROM", user or "no-reply@example.com")
        msg["To"] = to
        msg.set_content(html, subtype="html")
        if use_tls and port == 465:
            with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) as s:
                if user: s.login(user, password or "")
                s.send_message(msg)
        else:
            with smtplib.SMTP(host, port) as s:
                if use_tls: s.starttls(context=ssl.create_default_context())
                if user: s.login(user, password or "")
                s.send_message(msg)
        return "sent:smtp"

    if provider == "postmark":
        # Simple HTTP call using urllib to avoid extra deps
        import urllib.request, urllib.error
        api_key = os.getenv("POSTMARK_TOKEN")
        if not api_key:
            return _write_dev_mail(subject, to, html)
        body = json.dumps({
            "From": os.getenv("MAIL_FROM","no-reply@example.com"),
            "To": to,
            "Subject": subject,
            "HtmlBody": html
        }).encode("utf-8")
        req = urllib.request.Request("https://api.postmarkapp.com/email",
                                     data=body,
                                     headers={"Content-Type":"application/json","Accept":"application/json","X-Postmark-Server-Token":api_key})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return f"sent:postmark:{r.status}"
        except urllib.error.URLError as e:
            return f"error:postmark:{e}"

    if provider == "ses":
        # Boto3 usually handles SES, but to avoid dependency, fallback to dev mode if boto3 absent
        try:
            import boto3  # type: ignore
            ses = boto3.client("ses", region_name=os.getenv("SES_REGION","eu-central-1"))
            res = ses.send_email(
                Source=os.getenv("MAIL_FROM","no-reply@example.com"),
                Destination={"ToAddresses":[to]},
                Message={
                    "Subject":{"Data":subject, "Charset":"UTF-8"},
                    "Body":{"Html":{"Data":html, "Charset":"UTF-8"}}
                }
            )
            return f"sent:ses:{res.get('MessageId','')}"
        except Exception as e:
            return f"error:ses:{e}"

    return _write_dev_mail(subject, to, html)
