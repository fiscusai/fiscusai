from fastapi import APIRouter, Response, HTTPException
from app.exports.invoice_pdf_adv import build_pdf

router = APIRouter(prefix="/exports", tags=["exports-adv2"])

@router.get("/invoice-adv/{invoice_id}.pdf")
def invoice_adv_pdf(invoice_id: str):
    try:
        data = build_pdf(invoice_id)
        return Response(content=data, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
