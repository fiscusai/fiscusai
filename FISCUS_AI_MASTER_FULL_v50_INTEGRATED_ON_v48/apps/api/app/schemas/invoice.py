from pydantic import BaseModel
from datetime import date
class InvoiceIn(BaseModel):
    number: str; issue_date: date; due_date: date; customer_id: int
    subtotal: float; tax: float; total: float; status: str = "draft"
