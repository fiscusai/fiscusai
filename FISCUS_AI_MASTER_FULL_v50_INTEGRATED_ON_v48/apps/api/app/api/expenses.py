from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select
from typing import Optional, List
import csv, io
from ..core.db import get_session
from ..core.security import current_user, require_company
from ..models.expense import Expense
from ..schemas.expense import ExpenseIn

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.get("", response_model=List[Expense])
def list_expenses(session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    return session.exec(select(Expense).where(Expense.company_id==company.id)).all()

@router.post("", response_model=Expense)
def create_expense(payload: ExpenseIn, session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    e = Expense(company_id=company.id, **payload.dict())
    session.add(e); session.commit(); session.refresh(e)
    return e

@router.post("/import")
def import_expenses(authorization: str = Header(None), x_company_id: Optional[int] = Header(None), session: Session = Depends(get_session), file: UploadFile = File(...), amount_col: str = Form("amount"), title_col: str = Form("title"), date_col: str = Form("date"), category_col: str = Form("category")):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    content = file.file.read().decode("utf-8")
    rdr = csv.DictReader(io.StringIO(content))
    created = 0
    for row in rdr:
        try:
            e = Expense(company_id=company.id, title=row.get(title_col,"Gider"),
                        amount=float(row.get(amount_col, "0")), date=row.get(date_col, ""), category=row.get(category_col) or None)
            session.add(e); created += 1
        except Exception: continue
    session.commit(); return {"created": created}
