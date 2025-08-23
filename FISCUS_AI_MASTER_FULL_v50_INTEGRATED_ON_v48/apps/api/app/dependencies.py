from fastapi import Header, HTTPException, Depends
from typing import Optional, List, Dict
from app.auth import verify_token as _verify_token

async def auth_bearer(authorization: Optional[str] = Header(None),
                      x_user_role: Optional[str] = Header(None, alias="X-User-Role"),
                      x_org: Optional[str] = Header(None, alias="X-Org"),
                      x_email: Optional[str] = Header(None, alias="X-Email")) -> Dict:
    # Accept Bearer JWT if provided; otherwise fall back to dev headers
    user: Dict = {}
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        sub = _verify_token(token)
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = {"sub": sub}
    else:
        # Dev mode: accept headers
        if not x_user_role and not x_org:
            raise HTTPException(status_code=401, detail="Missing auth (Bearer or X-User-Role/X-Org)")
        user = {"role": x_user_role or "viewer", "org": x_org or "default", "email": x_email or "dev@local"}
    return user

def require_role(required: List[str]):
    async def role_dep(user=Depends(auth_bearer)):
        role = (user or {}).get("role") or "viewer"
        if role not in required:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_dep

def require_org():
    async def org_dep(user=Depends(auth_bearer)):
        org = (user or {}).get("org")
        if not org:
            raise HTTPException(status_code=400, detail="Missing org")
        return user
    return org_dep
