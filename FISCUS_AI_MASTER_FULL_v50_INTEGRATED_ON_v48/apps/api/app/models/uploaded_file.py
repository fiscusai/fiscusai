from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class UploadedFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    owner_sub: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    status: str = Field(default="scanned")  # scanned|deleted|infected
    size: Optional[int] = Field(default=None)
    mime: Optional[str] = Field(default=None)