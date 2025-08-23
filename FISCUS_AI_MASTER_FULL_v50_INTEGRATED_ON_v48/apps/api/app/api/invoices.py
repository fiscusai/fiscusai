from fastapi import APIRouter, Depends, HTTPException, Header, Response
from sqlmodel import Session, select
from typing import Optional, List
from ..core.db import get_session
from ..core.security import current_user, require_company
from ..models.invoice import Invoice
from ..schemas.invoice import InvoiceIn
from ..utils.exporters import invoice_pdf, invoice_xlsx, invoice_ubl_xml

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.get("", response_model=List[Invoice])
def list_invoices(session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None), status: Optional[str] = None, q: Optional[str] = None):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    query = select(Invoice).where(Invoice.company_id==company.id)
    if status: query = query.where(Invoice.status==status)
    items = session.exec(query).all()
    if q: items = [i for i in items if q.lower() in i.number.lower()]
    return items

@router.post("", response_model=Invoice)
def create_invoice(payload: InvoiceIn, session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    if role == "viewer": raise HTTPException(403, "Viewer cannot create invoices")
    inv = Invoice(company_id=company.id, **payload.dict())
    session.add(inv); session.commit(); session.refresh(inv)
    return inv

@router.get("/{invoice_id}/export")
def export_invoice(invoice_id: int, format: str = "pdf", session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    inv = session.get(Invoice, invoice_id)
    if not inv or inv.company_id != company.id: raise HTTPException(404, "Invoice not found")
    data = inv.dict()
    if format == "pdf":
        content = invoice_pdf(data, company_name=f"Company #{company.id}")
        headers = {"Content-Disposition": f"attachment; filename=invoice_{inv.number}.pdf"}
        return Response(content, media_type="application/pdf", headers=headers)
    elif format == "xlsx":
        content = invoice_xlsx(data)
        headers = {"Content-Disposition": f"attachment; filename=invoice_{inv.number}.xlsx"}
        return Response(content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
    elif format == "xml":
        content = invoice_ubl_xml(data, company_name=f"Company #{company.id}")
        headers = {"Content-Disposition": f"attachment; filename=invoice_{inv.number}.xml"}
        return Response(content, media_type="application/xml", headers=headers)
    else:
        raise HTTPException(400, "format must be pdf|xlsx|xml")
