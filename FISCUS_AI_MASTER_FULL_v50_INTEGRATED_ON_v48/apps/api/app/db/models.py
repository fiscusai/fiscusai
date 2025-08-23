from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: Optional[str] = None
    name: str
    email: Optional[str] = None
    tax_id: Optional[str] = None
    organization_id: Optional[str] = None

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: str
    customer: str
    date: date
    total: float = 0
    vat: float = 0
    currency: str = "₺"
    organization_id: Optional[str] = None


from typing import Optional
from sqlmodel import SQLModel, Field

class Flag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    value: bool = False
    scope: str = "global"
    updated_at: str = ""


from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    role: str = Field(default="user")

class UserOrgRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    org_id: int = Field(foreign_key="organization.id")
    role: str = Field(default="user")  # admin/accountant/user
