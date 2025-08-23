
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import io, os, qrcode
from datetime import datetime

def _qr_image(data: str):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=3, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio

def render_invoice_pdf(invoice: dict, company: dict | None = None):
    """
    invoice: { id, number, date, customer, items:[{name,qty,price,vat_rate}], total, vat, iban, organization_id }
    company: { name, address, iban, phone, email }
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4

    # Header
    c.setFillColorRGB(0.18,0.18,0.18)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(25*mm, (H-25*mm), "FISCUS AI")
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(25*mm, (H-30*mm), "Akıllı Muhasebe, Roma Disipliniyle.")
    c.setFillColorRGB(0,0,0)

    # Invoice Meta
    y = H - 45*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25*mm, y, "E-FATURA")
    c.setFont("Helvetica", 10)
    y -= 6*mm
    c.drawString(25*mm, y, f"Fatura No: {invoice.get('number') or invoice.get('id')}")
    y -= 6*mm
    c.drawString(25*mm, y, f"Tarih: {invoice.get('date')}")
    y -= 6*mm
    c.drawString(25*mm, y, f"Organizasyon: {invoice.get('organization_id','-')}")

    # Company / Customer blocks
    left_y = y - 12*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(25*mm, left_y, "Satıcı")
    c.setFont("Helvetica", 9)
    left_y -= 5*mm
    comp = company or {"name":"Fiscus AI Ltd.","address":"Roma Cad. 7, İstanbul","iban": invoice.get("iban","TR00 0000 0000 0000 0000 0000 00")}
    c.drawString(25*mm, left_y, comp["name"])
    left_y -= 5*mm
    c.drawString(25*mm, left_y, comp["address"])
    left_y -= 5*mm
    c.drawString(25*mm, left_y, f"IBAN: {comp['iban']}")

    right_y = y - 12*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(A4[0]-25*mm, right_y, "Alıcı")
    c.setFont("Helvetica", 9)
    right_y -= 5*mm
    cust = invoice.get("customer") or "Müşteri"
    c.drawRightString(A4[0]-25*mm, right_y, str(cust))

    # Items table
    items = invoice.get("items") or [
        {"name": invoice.get("description","Hizmet"), "qty":1, "price": invoice.get("total",0), "vat_rate": 0.18}
    ]
    data = [["Ürün/Hizmet", "Adet", "Birim Fiyat", "KDV %", "Tutar"]]
    subtotal = 0.0
    vat_total = 0.0
    for it in items:
        qty = float(it.get("qty",1))
        price = float(it.get("price",0))
        vat_rate = float(it.get("vat_rate", 0.18))
        line = qty*price
        subtotal += line
        vat_total += line*vat_rate
        data.append([it.get("name","Kalem"), f"{qty:g}", f"{price:,.2f}", f"{int(vat_rate*100)}", f"{line:,.2f}"])

    t = Table(data, colWidths=[80*mm, 20*mm, 30*mm, 20*mm, 30*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#F2F2F0")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("ALIGN", (1,1), (-1,-1), "RIGHT"),
        ("ALIGN", (0,1), (0,-1), "LEFT"),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#C9A54A")),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ("TOPPADDING", (0,1), (-1,-1), 4),
    ]))
    table_y = right_y - 15*mm
    w, h = t.wrapOn(c, A4[0]-50*mm, A4[1])
    t.drawOn(c, 25*mm, table_y - h)

    # Totals
    y_tot = table_y - h - 10*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(A4[0]-25*mm, y_tot, f"Ara Toplam: {subtotal:,.2f} TL")
    y_tot -= 6*mm
    c.drawRightString(A4[0]-25*mm, y_tot, f"KDV: {vat_total:,.2f} TL")
    y_tot -= 6*mm
    grand = subtotal + vat_total
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#7A1F1F"))
    c.drawRightString(A4[0]-25*mm, y_tot, f"Genel Toplam: {grand:,.2f} TL")
    c.setFillColor(colors.black)

    # QR code (payment link mock)
    pay_link = f"https://pay.fiscus.ai/invoice/{invoice.get('id','') or invoice.get('number','')}?amount={grand:.2f}"
    qr_bio = _qr_image(pay_link)
    c.drawImage(qr_bio, 25*mm, 20*mm, width=30*mm, height=30*mm, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica", 8)
    c.drawString(25*mm, 18*mm, "Ödeme için tarayın (mock)")

    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.4,0.4,0.4)
    c.drawRightString(A4[0]-25*mm, 15*mm, "Fiscus AI — Akıllı Muhasebe, Roma Disipliniyle.")
    c.setFillColorRGB(0,0,0)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
