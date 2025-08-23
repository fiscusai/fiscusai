from fastapi import APIRouter, Response, HTTPException
from app.exports.invoice_pdf_v3 import build_invoice_pdf_v3

router = APIRouter(prefix="/exports", tags=["exports"])

# Mock fetchers for the demo (replace with DB calls)
def _get_invoice(invoice_id: str) -> dict:
    # In a real app, fetch invoice by id. Here we return a mock.
    return {
        "id": invoice_id,
        "number": invoice_id,
        "date": "2025-08-01",
        "customer": "Aurea Ltd.",
        "currency": "₺",
        "vat": 180.0,
        "discount": 0.0,
        "shipping": 0.0,
        "items": [
            {"desc":"Danışmanlık Hizmeti", "qty": 10, "unit":"saat", "price": 450.0},
            {"desc":"Raporlama", "qty": 1, "unit":"paket", "price": 750.0}
        ],
        "payment_link": "https://fiscus.ai/pay/mock?inv=" + invoice_id
    }

def _get_org() -> dict:
    return {
        "name": "FISCUS AI",
        "address": "Roma Cad. No:1, İstanbul",
        "vkn": "1234567890",
        "iban": "TR00 0000 0000 0000 0000 0000 00"
    }

@router.get("/invoice-v3/{invoice_id}.pdf")
def invoice_pdf_v3(invoice_id: str):
    inv = _get_invoice(invoice_id)
    org = _get_org()
    pdf = build_invoice_pdf_v3(inv, org)
    return Response(content=pdf, media_type="application/pdf", headers={
        "Content-Disposition": f'inline; filename="invoice-{invoice_id}.pdf"'
    })
