from fastapi import HTTPException, Request
from typing import Optional

def require_org(request: Request) -> str:
    org = getattr(request.state, "org", None)
    if not org:
        raise HTTPException(status_code=400, detail="Organization (org) missing. Provide via JWT claims or X-Org header.")
    return org

def require_role(request: Request, allowed: list[str]):
    role = getattr(request.state, "role", None)
    if role not in allowed:
        raise HTTPException(status_code=403, detail=f"Insufficient role: {role}. Required: {allowed}")
