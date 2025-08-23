from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Optional
class Company(SQLModel, table=True):
    __tablename__ = "company"; __table_args__ = (UniqueConstraint("name"), )
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
class UserCompany(SQLModel, table=True):
    __tablename__ = "user_company"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int; company_id: int; role: str = "viewer"
