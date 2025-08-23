from fastapi import APIRouter, HTTPException
from typing import List, Dict
import uuid

router = APIRouter(prefix="/users", tags=["users"])

# In-memory demo user store
USERS: Dict[str, Dict] = {
    "1": {"id":"1","email":"admin@fiscus.ai","role":"admin"},
    "2": {"id":"2","email":"acc@fiscus.ai","role":"accountant"},
    "3": {"id":"3","email":"viewer@fiscus.ai","role":"user"},
}

@router.get("/", response_model=List[dict])
def list_users():
    return list(USERS.values())

@router.put("/{uid}/role")
def change_role(uid: str, payload: dict):
    role = payload.get("role")
    if role not in ("admin","accountant","user"):
        raise HTTPException(status_code=422, detail="Invalid role")
    if uid not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    USERS[uid]["role"] = role
    return {"ok": True, "user": USERS[uid]}
