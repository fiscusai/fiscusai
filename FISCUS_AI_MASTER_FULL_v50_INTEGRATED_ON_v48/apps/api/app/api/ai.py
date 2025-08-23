from fastapi import APIRouter, Depends, Header
from sqlmodel import Session, select
from typing import Optional
from ..core.db import get_session
from ..core.security import current_user, require_company
from ..models.invoice import Invoice
from ..models.expense import Expense
from ..utils.ai import summarize, anomaly, forecast_cash

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/summarize")
def ai_summarize(session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    invoices = [i.dict() for i in session.exec(select(Invoice).where(Invoice.company_id==company.id)).all()]
    expenses = [e.dict() for e in session.exec(select(Expense).where(Expense.company_id==company.id)).all()]
    return {"summary": summarize(invoices, expenses)}

@router.post("/anomaly")
def ai_anomaly(session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    expenses = [e.dict() for e in session.exec(select(Expense).where(Expense.company_id==company.id)).all()]
    return {"anomalies": anomaly(expenses)}

@router.post("/forecast")
def ai_forecast(session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    invoices = [i.dict() for i in session.exec(select(Invoice).where(Invoice.company_id==company.id)).all()]
    expenses = [e.dict() for e in session.exec(select(Expense).where(Expense.company_id==company.id)).all()]
    return {"forecast": forecast_cash(invoices, expenses)}
