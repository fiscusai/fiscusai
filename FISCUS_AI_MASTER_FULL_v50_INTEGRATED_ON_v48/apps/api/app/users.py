from typing import Dict
from .auth_utils import hash_password, verify_password

# demo in-memory users {email: {password_hash, name}}
_USERS: Dict[str, dict] = {}

def create_user(email: str, password: str, name: str = ""):
    if email in _USERS:
        raise ValueError("User already exists")
    _USERS[email] = {"password_hash": hash_password(password), "name": name}
    return {"email": email, "name": name}

def authenticate(email: str, password: str):
    u = _USERS.get(email)
    if not u:
        return None
    if not verify_password(password, u["password_hash"]):
        return None
    return {"email": email, "name": u.get("name","")}

def get_user(email: str):
    if email in _USERS:
        return {"email": email, "name": _USERS[email].get("name","")}
    return None
