from fastapi import Request, HTTPException
from typing import List

# Demo: extract user & roles from headers/local storage equivalent for API demo purposes.
# In production, bind to your auth/session.

def get_user_role(request: Request) -> str:
    # Expect 'X-User-Role' header for demo; fallback 'user'
    return request.headers.get("X-User-Role", "user")

def get_user_org(request: Request) -> str:
    return request.headers.get("X-Org", "ORG-ALPHA")

def require_any_role(roles: List[str]):
    async def guard(request: Request):
        role = get_user_role(request)
        if role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden: role required")
    return guard
