
from fastapi import APIRouter
from typing import Dict
from datetime import datetime, timedelta

router = APIRouter(prefix="/security/nonce", tags=["security"])
_NONCES: Dict[str, datetime] = {}

@router.get("/list")
def list_nonces():
    now = datetime.utcnow()
    return [{"nonce":k, "expires_in": max(0, int((v-now).total_seconds()))} for k,v in _NONCES.items()]

@router.post("/remember/{nonce}")
def remember(nonce: str, ttl: int = 3600):
    _NONCES[nonce] = datetime.utcnow() + timedelta(seconds=ttl)
    return {"ok": True}

@router.post("/purge")
def purge():
    _NONCES.clear()
    return {"ok": True, "count": 0}
