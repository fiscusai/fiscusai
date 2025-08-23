from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class InvoiceIn(BaseModel):
    customer_id: Optional[int] = None
    number: str
    issue_date: date
    due_date: date
    amount: float
    currency: str = "TRY"
    status: str = "unpaid"
