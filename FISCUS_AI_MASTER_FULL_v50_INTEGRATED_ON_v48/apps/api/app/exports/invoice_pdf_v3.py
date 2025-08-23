from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
import io, qrcode
from fastapi import HTTPException

def _currency(v, sym='₺'):
    try:
        return f"{sym}{float(v):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return f"{sym}{v}"

def build_invoice_pdf_v3(invoice: dict, organization: dict) -> bytes:
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, h-20*mm, organization.get("name", "FISCUS AI"))
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, h-26*mm, organization.get("address", "Roma Cad. No:1, İstanbul"))
    c.drawString(20*mm, h-31*mm, f"VKN: {organization.get('vkn','0000000000')}  IBAN: {organization.get('iban','TR00 0000 0000 0000 0000 0000 00')}")

    # Invoice meta
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(w-20*mm, h-20*mm, f"FATURA #{invoice.get('number','—')}")
    c.setFont("Helvetica", 10)
    c.drawRightString(w-20*mm, h-26*mm, f"Tarih: {invoice.get('date','—')}")
    c.drawRightString(w-20*mm, h-31*mm, f"Müşteri: {invoice.get('customer','—')}")

    # Table header
    y = h-45*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, y, "Açıklama")
    c.drawRightString(w-110*mm, y, "Miktar")
    c.drawRightString(w-80*mm, y, "Birim")
    c.drawRightString(w-50*mm, y, "Birim Fiyat")
    c.drawRightString(w-20*mm, y, "Tutar")
    c.line(20*mm, y-2*mm, w-20*mm, y-2*mm)

    # Items
    y -= 8*mm
    c.setFont("Helvetica", 9)
    items = invoice.get("items") or [
        {"desc":"Hizmet", "qty":1, "unit":"adet", "price":invoice.get("total",0)}
    ]
    subtotal = 0.0
    for it in items:
        if y < 40*mm:
            # footer + page number
            c.setFont("Helvetica", 8)
            c.drawString(20*mm, 15*mm, "FISCUS AI — Akıllı Muhasebe, Roma Disipliniyle.")
            c.showPage()
            y = h-20*mm
        desc = it.get("desc","—")
        qty = float(it.get("qty",1))
        unit = it.get("unit","")
        price = float(it.get("price",0))
        total = qty*price
        subtotal += total
        c.drawString(20*mm, y, desc[:60])
        c.drawRightString(w-110*mm, y, f"{qty:.2f}")
        c.drawRightString(w-80*mm, y, unit)
        c.drawRightString(w-50*mm, y, _currency(price))
        c.drawRightString(w-20*mm, y, _currency(total))
        y -= 6*mm

    # Discounts/Shipping (optional)
    discount = float(invoice.get("discount", 0) or 0)
    shipping = float(invoice.get("shipping", 0) or 0)
    vat = float(invoice.get("vat", 0) or 0)
    currency = invoice.get("currency","₺")

    # Summary
    y -= 6*mm
    c.line(120*mm, y, w-20*mm, y)
    y -= 6*mm
    c.setFont("Helvetica", 10)
    c.drawRightString(w-50*mm, y, "Ara Toplam:")
    c.drawRightString(w-20*mm, y, _currency(subtotal, currency)); y -= 6*mm
    c.drawRightString(w-50*mm, y, "İskonto:")
    c.drawRightString(w-20*mm, y, _currency(-discount, currency)); y -= 6*mm
    c.drawRightString(w-50*mm, y, "Kargo:")
    c.drawRightString(w-20*mm, y, _currency(shipping, currency)); y -= 6*mm
    c.drawRightString(w-50*mm, y, "KDV:")
    c.drawRightString(w-20*mm, y, _currency(vat, currency)); y -= 6*mm
    grand = subtotal - discount + shipping + vat
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(w-50*mm, y, "GENEL TOPLAM:")
    c.drawRightString(w-20*mm, y, _currency(grand, currency)); y -= 10*mm

    # QR code (payment link mock)
    link = invoice.get("payment_link", "https://fiscus.ai/pay/mock")
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_w, img_h = img.size
    img_path = io.BytesIO()
    img.save(img_path, format="PNG")
    img_path.seek(0)
    c.drawInlineImage(img_path, 20*mm, y-20*mm, 20*mm, 20*mm)

    c.setFont("Helvetica", 8)
    c.drawString(45*mm, y-8*mm, "Ödeme için QR'ı tarayın veya bağlantıyı ziyaret edin.")
    c.drawString(20*mm, 15*mm, "FISCUS AI — Akıllı Muhasebe, Roma Disipliniyle.  |  fiscus.ai")

    c.showPage()
    c.save()
    return buf.getvalue()
