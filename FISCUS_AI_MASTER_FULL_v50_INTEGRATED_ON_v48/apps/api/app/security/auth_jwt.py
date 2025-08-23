from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import os, jwt

class AuthError(Exception):
    pass

ALGO = os.getenv("JWT_ALG", "HS256")
SECRET = os.getenv("JWT_SECRET", "change-me")
ACCESS_EXPIRES = int(os.getenv("JWT_EXPIRES", "3600"))
REFRESH_EXPIRES = int(os.getenv("JWT_REFRESH_EXPIRES", str(7*24*3600)))

def _now():
    return datetime.now(timezone.utc)

def create_token(payload: Dict[str, Any], refresh: bool=False) -> str:
    exp = _now() + timedelta(seconds=(REFRESH_EXPIRES if refresh else ACCESS_EXPIRES))
    data = dict(payload)
    data.update({"exp": exp, "iat": _now(), "typ": "refresh" if refresh else "access"})
    return jwt.encode(data, SECRET, algorithm=ALGO)

def verify_token(token: str, expect_typ: Optional[str]=None) -> Dict[str, Any]:
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        if expect_typ and data.get("typ") != expect_typ:
            raise AuthError("Invalid token type")
        return data
    except jwt.ExpiredSignatureError as e:
        raise AuthError("Token expired") from e
    except jwt.InvalidTokenError as e:
        raise AuthError("Invalid token") from e
