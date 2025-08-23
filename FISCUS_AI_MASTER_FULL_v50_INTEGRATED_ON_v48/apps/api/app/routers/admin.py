from fastapi import APIRouter, HTTPException, Depends
from typing import List
import os

from app.dependencies import require_role
# Redis is optional; if unavailable we degrade gracefully.
try:
    import redis  # type: ignore
except Exception:  # pragma: no cover
    redis = None  # type: ignore

from app.db import get_session
from sqlmodel import Session
from app.models.audit import AuditLog

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/uploads/recent")
async def recent(limit: int = 50, user=Depends(require_role(["admin"]))):
    limit = max(1, min(200, int(limit or 50)))
    items: List[str] = []
    if redis is None:
        # No Redis: return empty list (or we could read from DB if modeled)
        return {"recent": items, "source": "memory"}
    try:
        rds = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        keys = rds.lrange("uploads:recent", 0, limit - 1)
        items = [k.decode("utf-8") if isinstance(k, (bytes, bytearray)) else str(k) for k in keys]
    except Exception:
        # If redis misconfigured, avoid crashing the endpoint
        items = []
    return {"recent": items, "source": "redis"}

@router.post("/uploads/rescan")
async def rescan(key: str, user=Depends(require_role(["admin"])), s: Session = Depends(get_session)):
    """Mark a key for rescan; actual scanning handled by background worker in real deployment."""
    if not key:
        raise HTTPException(status_code=400, detail="key is required")
    # Record an audit log entry
    log = AuditLog(actor=user.get("email","admin"), role=user.get("role","admin"),
                   action="rescan", target=key, meta="{}")
    s.add(log)
    s.commit()
    return {"rescan": True, "key": key}
