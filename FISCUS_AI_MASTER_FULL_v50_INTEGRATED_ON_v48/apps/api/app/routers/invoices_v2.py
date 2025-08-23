from fastapi import APIRouter, HTTPException
from typing import List
from sqlmodel import select
from app.db.session import get_session, init_db
from app.db.models import Invoice

router = APIRouter(prefix="/v2/invoices", tags=["invoices_v2"])

@router.get("/", response_model=List[Invoice])
def list_invoices():
    init_db()
    with get_session() as s:
        res = s.exec(select(Invoice)).all()
        return res

@router.post("/", response_model=Invoice)
def create_invoice(inv: Invoice):
    init_db()
    with get_session() as s:
        s.add(inv)
        s.commit()
        s.refresh(inv)
        return inv

@router.put("/{iid}", response_model=Invoice)
def update_invoice(iid: int, payload: Invoice):
    init_db()
    with get_session() as s:
        obj = s.get(Invoice, iid)
        if not obj:
            raise HTTPException(status_code=404, detail="Invoice not found")
        for k, v in payload.dict(exclude_unset=True).items():
            setattr(obj, k, v)
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj

@router.delete("/{iid}")
def delete_invoice(iid: int):
    init_db()
    with get_session() as s:
        obj = s.get(Invoice, iid)
        if not obj:
            raise HTTPException(status_code=404, detail="Invoice not found")
        s.delete(obj)
        s.commit()
        return {"ok": True}
