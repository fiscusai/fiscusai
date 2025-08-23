from sqlmodel import SQLModel, Field
from typing import Optional
class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int; name: str; email: str | None = None; tax_no: str | None = None
