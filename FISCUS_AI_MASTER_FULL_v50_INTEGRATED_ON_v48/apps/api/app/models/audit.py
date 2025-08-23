from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ts: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    actor: str = Field(default="system", nullable=False, index=True)
    role: str = Field(default="unknown", nullable=False, index=True)
    action: str = Field(nullable=False, index=True)
    target: str = Field(default="", nullable=False, index=True)
    meta: str = Field(default="", nullable=False)