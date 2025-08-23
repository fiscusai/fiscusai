from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime
class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int; number: str; issue_date: date; due_date: date; customer_id: int
    subtotal: float; tax: float; total: float; status: str = "draft"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
