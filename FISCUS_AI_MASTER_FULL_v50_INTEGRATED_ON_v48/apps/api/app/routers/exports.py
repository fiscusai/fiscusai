from fastapi import APIRouter, Response, HTTPException, Depends
from pathlib import Path
import json, io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from app.security import require_role

router = APIRouter(prefix="/exports", tags=["exports"])

BASE = Path(__file__).resolve().parent.parent / "data"
INV = BASE / "demo_invoices.json"

def _read_invoices():
    if INV.exists():
        return json.loads(INV.read_text(encoding="utf-8"))
    return []

@router.get("/invoice/{invoice_id}.pdf")
def export_invoice_pdf(invoice_id: str, user=Depends(require_role('admin','accountant','user'))):
    invoices = _read_invoices()
    inv = next((i for i in invoices if i.get("id")==invoice_id or i.get("number")==invoice_id), None)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # Header band
    c.setFillColorRGB(0.95,0.95,0.93)
    c.rect(0, height-80, width, 80, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30*mm, height-30, "FISCUS AI — E‑Fatura")
    c.setFont("Helvetica", 10)
    c.drawString(30*mm, height-45, "Akıllı Muhasebe, Roma Disipliniyle.")

    # Invoice data
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25*mm, height-90, f"Fatura No: {inv.get('number','-')}")
    c.setFont("Helvetica", 10)
    c.drawString(25*mm, height-105, f"Tarih: {inv.get('date','-')}")
    c.drawString(25*mm, height-120, f"Müşteri: {inv.get('customer','-')}")

    # Items (simplified single line)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(25*mm, height-150, "Kalemler")
    c.setFont("Helvetica", 10)
    total = float(inv.get("total",0) or 0)
    vat = float(inv.get("vat",0) or 0)
    c.drawString(25*mm, height-165, f"Toplam Tutar: {total:,.2f} TRY")
    c.drawString(25*mm, height-180, f"KDV: {vat:,.2f} TRY")
    c.line(25*mm, height-190, width-25*mm, height-190)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(25*mm, height-205, f"Genel Toplam: {total+vat:,.2f} TRY")

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.grey)
    c.drawString(25*mm, 15*mm, "Bu belge FISCUS AI tarafından otomatik oluşturulmuştur.")
    c.showPage()
    c.save()

    pdf = buf.getvalue()
    buf.close()
    headers = {"Content-Disposition": f"inline; filename=invoice_{invoice_id}.pdf"}
    return Response(content=pdf, media_type="application/pdf", headers=headers)
