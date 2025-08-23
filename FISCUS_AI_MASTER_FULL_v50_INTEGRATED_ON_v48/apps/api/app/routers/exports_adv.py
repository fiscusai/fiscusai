
from fastapi import APIRouter, HTTPException, Response
from pathlib import Path
import json
from app.exports.invoice_pdf import render_invoice_pdf

router = APIRouter(prefix="/exports", tags=["exports-adv"])

DATA = Path(__file__).resolve().parent.parent / "data" / "demo_invoices.json"

def _read():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return []

@router.get("/invoice/{invoice_id}.pdf")
def export_invoice_pdf(invoice_id: str):
    items = _read()
    inv = next((i for i in items if str(i.get("id")) == invoice_id or str(i.get("number")) == invoice_id), None)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    pdf_bytes = render_invoice_pdf(inv, company=None)
    return Response(content=pdf_bytes, media_type="application/pdf")
