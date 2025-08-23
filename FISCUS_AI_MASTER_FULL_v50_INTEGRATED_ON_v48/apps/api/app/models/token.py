from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
class ResetToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int; token: str; expires_at: datetime
class InviteToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str; company_id: int; role: str = "viewer"; token: str; expires_at: datetime
