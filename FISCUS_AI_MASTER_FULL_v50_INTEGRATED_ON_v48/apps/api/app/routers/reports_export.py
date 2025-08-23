from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from app.dependencies import require_role
from app.db import get_session
from sqlmodel import Session

router = APIRouter(prefix="/reports/export", tags=["reports"])

@router.get("/invoice-pdf")
async def invoice_pdf(number: str = "INV-0001", total: float = 0.0, vat: float = 0.0,
                      user=Depends(require_role(["admin","accountant","viewer"])),
                      s: Session = Depends(get_session)):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, h - 20*mm, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(20*mm, h - 40*mm, f"Invoice Number: {number}")
    c.drawString(20*mm, h - 50*mm, f"Total: {total:.2f}")
    c.drawString(20*mm, h - 60*mm, f"VAT: {vat:.2f}")
    c.drawString(20*mm, h - 70*mm, f"Grand Total: {total + vat:.2f}")

    c.showPage()
    c.save()
    buf.seek(0)

    headers = {"Content-Disposition": f'attachment; filename="{number}.pdf"'}
    return StreamingResponse(buf, media_type="application/pdf", headers=headers)
