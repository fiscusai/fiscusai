from app.security import require_role
from app.utils import paginate

from fastapi import Header
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import uuid

router = APIRouter(prefix="/invoices", tags=["invoices"])

class Invoice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    number: str
    customer: str
    date: date
    due_date: date
    currency: str = "TRY"
    subtotal: float
    tax: float = 0.0
    total: float
    status: str = "unpaid"

_DB: List[Invoice] = []

@router.get("", response_model=List[Invoice])
def list_invoices():
    return _DB

@router.post("", response_model=Invoice, status_code=201)
def create_invoice(inv: Invoice, user=Depends(require_role('admin','accountant'))):
    _DB.append(inv)
    return inv

@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: str):
    for inv in _DB:
        if inv.id == invoice_id:
            return inv
    raise HTTPException(404, "Invoice not found")

@router.put("/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: str, patch: Invoice, user=Depends(require_role('admin','accountant'))):
    for i, inv in enumerate(_DB):
        if inv.id == invoice_id:
            _DB[i] = patch
            return patch
    raise HTTPException(404, "Invoice not found")

@router.delete("/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: str, user=Depends(require_role('admin'))):
    global _DB
    before = len(_DB)
    _DB = [x for x in _DB if x.id != invoice_id]
    if len(_DB) == before:
        raise HTTPException(404, "Invoice not found")
    return None

def seed_demo(data: List[dict]):
    from datetime import datetime
    for row in data:
        # coerce dates
        for k in ["date", "due_date"]:
            if isinstance(row.get(k), str):
                row[k] = datetime.fromisoformat(row[k]).date()
        _DB.append(Invoice(**row))
