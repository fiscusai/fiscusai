from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
import io, datetime

def build_summary_report(title: str, stats: dict) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    # Cover
    c.setFillColorRGB(0.18, 0.18, 0.18)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(30*mm, h-50*mm, "FISCUS AI")
    c.setFont("Helvetica", 14)
    c.drawString(30*mm, h-60*mm, title)
    c.setFont("Helvetica", 10)
    c.drawString(30*mm, h-70*mm, datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))

    # Footer (signature placeholder)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(30*mm, 20*mm, "Bu rapor elektronik olarak oluşturulmuştur. Kurumsal imza gerekmez.")
    c.showPage()

    # Stats page
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, h-30*mm, "Özet İstatistikler")
    c.setFont("Helvetica", 12)
    y = h-45*mm
    for k, v in stats.items():
        c.drawString(25*mm, y, f"- {k}: {v}")
        y -= 10*mm
        if y < 30*mm:
            c.showPage()
            y = h-30*mm

    c.showPage()
    c.save()
    return buf.getvalue()
