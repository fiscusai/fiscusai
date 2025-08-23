from fastapi import APIRouter, HTTPException
from typing import List
from sqlmodel import select
from app.db.session import get_session, init_db
from app.db.models import Customer

router = APIRouter(prefix="/v2/customers", tags=["customers_v2"])

@router.get("/", response_model=List[Customer])
def list_customers():
    init_db()
    with get_session() as s:
        res = s.exec(select(Customer)).all()
        return res

@router.post("/", response_model=Customer)
def create_customer(c: Customer):
    init_db()
    with get_session() as s:
        s.add(c)
        s.commit()
        s.refresh(c)
        return c

@router.put("/{cid}", response_model=Customer)
def update_customer(cid: int, payload: Customer):
    init_db()
    with get_session() as s:
        obj = s.get(Customer, cid)
        if not obj:
            raise HTTPException(status_code=404, detail="Customer not found")
        for k, v in payload.dict(exclude_unset=True).items():
            setattr(obj, k, v)
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj

@router.delete("/{cid}")
def delete_customer(cid: int):
    init_db()
    with get_session() as s:
        obj = s.get(Customer, cid)
        if not obj:
            raise HTTPException(status_code=404, detail="Customer not found")
        s.delete(obj)
        s.commit()
        return {"ok": True}
