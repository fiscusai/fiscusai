from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str = Field(default="")
    role: str = Field(default="user", index=True)
    org: str = Field(default="default", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    # 2FA
    totp_secret: Optional[str] = Field(default=None)
    twofa_enabled: bool = Field(default=False, nullable=False)
