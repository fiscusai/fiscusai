from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io, qrcode
from datetime import datetime

def format_currency(x, currency='TRY'):
    try:
        return f"{x:,.2f} {currency}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return f"{x} {currency}"

def build_invoice_pdf(invoice: dict, company: dict):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, (height - 20*mm), company.get("name", "FISCUS AI"))
    c.setFont("Helvetica", 9)
    c.drawString(20*mm, (height - 26*mm), f"Adres: {company.get('address','Roma Cad. 1, İstanbul')}")
    c.drawString(20*mm, (height - 31*mm), f"IBAN: {company.get('iban','TR00 0000 0000 0000 0000 0000 00')}")
    c.drawRightString((width - 20*mm), (height - 20*mm), f"FATURA #{invoice.get('number','-')}")
    c.drawRightString((width - 20*mm), (height - 26*mm), f"Tarih: {invoice.get('date','-')}")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, (height - 45*mm), "Müşteri")
    c.setFont("Helvetica", 9)
    cust = invoice.get("customer_info", {})
    c.drawString(20*mm, (height - 51*mm), f"{cust.get('name','-')}")
    c.drawString(20*mm, (height - 56*mm), f"Vergi No: {cust.get('tax_id','-')}")
    c.drawString(20*mm, (height - 61*mm), f"E-Posta: {cust.get('email','-')}")

    items = invoice.get("items", [])
    data = [["Açıklama", "Miktar", "Birim Fiyat", "Tutar", "KDV"]]
    for it in items:
        qty = it.get("qty", 1)
        price = it.get("price", 0.0)
        total = qty * price
        vat = total * (it.get("vat_rate", 0.2))
        data.append([
            it.get("desc", "-"),
            f"{qty}",
            format_currency(price),
            format_currency(total),
            format_currency(vat),
        ])
    table = Table(data, colWidths=[80*mm, 20*mm, 30*mm, 30*mm, 30*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (1,1), (-1,-1), "RIGHT"),
        ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
        ("FONT", (0,1), (-1,-1), "Helvetica", 9),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    table.wrapOn(c, 20*mm, height - 150*mm)
    table.drawOn(c, 20*mm, height - 150*mm)

    subtotal = sum((it.get("qty",1)*it.get("price",0.0)) for it in items)
    vat_total = sum(((it.get("qty",1)*it.get("price",0.0)) * it.get("vat_rate",0.2)) for it in items)
    discount = invoice.get("discount", 0.0)
    shipping = invoice.get("shipping", 0.0)
    grand = subtotal + vat_total + shipping - discount

    y = height - 160*mm - 10*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 25*mm, y, "Ara Toplam: " + format_currency(subtotal))
    y -= 6*mm
    c.drawRightString(width - 25*mm, y, "KDV Toplam: " + format_currency(vat_total))
    y -= 6*mm
    c.drawRightString(width - 25*mm, y, "İskonto: " + format_currency(discount))
    y -= 6*mm
    c.drawRightString(width - 25*mm, y, "Kargo: " + format_currency(shipping))
    y -= 8*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 25*mm, y, "GENEL TOPLAM: " + format_currency(grand))

    qr_data = invoice.get("payment_url", "https://fiscus.ai/pay/" + invoice.get("number","-"))
    qr_img = qrcode.make(qr_data)
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format="PNG")
    qr_buf.seek(0)
    c.drawInlineImage(qr_buf, 20*mm, 20*mm, 30*mm, 30*mm)

    c.setFont("Helvetica", 8)
    c.drawString(60*mm, 25*mm, "Ödeme için lütfen üstte yer alan IBAN bilgilerini kullanın.")
    c.drawString(60*mm, 20*mm, "Bu belge e‑fatura standartlarına uygun örnek formatta üretilmiştir.")

    c.setFont("Helvetica", 7)
    c.setFillColor(colors.grey)
    c.drawRightString(width - 10*mm, 10*mm, f"FISCUS AI • {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
