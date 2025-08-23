from fastapi import APIRouter, Depends, Header
from sqlmodel import Session, select
from typing import Optional, List
from ..core.db import get_session
from ..core.security import current_user, require_company
from ..models.customer import Customer
from ..schemas.customer import CustomerIn

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("", response_model=List[Customer])
def list_customers(session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    return session.exec(select(Customer).where(Customer.company_id==company.id)).all()

@router.post("", response_model=Customer)
def create_customer(payload: CustomerIn, session: Session = Depends(get_session), authorization: str = Header(None), x_company_id: Optional[int] = Header(None)):
    user = current_user(session, authorization)
    company, role = require_company(session, user, x_company_id)
    c = Customer(company_id=company.id, **payload.dict())
    session.add(c); session.commit(); session.refresh(c)
    return c
