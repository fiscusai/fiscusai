from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from ..core.db import get_session
from ..core.security import current_user
from ..models.company import Company, UserCompany
from ..schemas.company import CompanyCreate

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("")
def list_companies(session: Session = Depends(get_session), authorization: str = Header(None)):
    user = current_user(session, authorization)
    ucs = session.exec(select(UserCompany).where(UserCompany.user_id==user.id)).all()
    ids = [uc.company_id for uc in ucs]
    return session.exec(select(Company).where(Company.id.in_(ids))).all()

@router.post("")
def create_company(payload: CompanyCreate, session: Session = Depends(get_session), authorization: str = Header(None)):
    user = current_user(session, authorization)
    c = Company(name=payload.name)
    session.add(c); session.commit(); session.refresh(c)
    session.add(UserCompany(user_id=user.id, company_id=c.id, role="admin")); session.commit()
    return c

@router.get("/{company_id}")
def get_company(company_id: int, session: Session = Depends(get_session), authorization: str = Header(None)):
    user = current_user(session, authorization)
    uc = session.exec(select(UserCompany).where(UserCompany.user_id==user.id, UserCompany.company_id==company_id)).first()
    if not uc: raise HTTPException(403, "No access")
    return session.get(Company, company_id)
