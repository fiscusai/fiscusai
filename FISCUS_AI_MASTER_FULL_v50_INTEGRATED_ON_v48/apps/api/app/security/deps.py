from fastapi import Depends, HTTPException, Request, status

def get_context(request: Request):
    return {"role": getattr(request.state, "role", None), "org": getattr(request.state, "org", None)}

def require_org(ctx = Depends(get_context)):
    if not ctx.get("org"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization header/claim required")
    return ctx["org"]

def require_role(*roles):
    def checker(ctx = Depends(get_context)):
        role = ctx.get("role")
        if not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Role required")
        if role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden for role: %s" % role)
        return role
    return checker
