from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from typing import Optional

def get_signer(secret: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key=secret, salt="fiscus-email")

def sign(data: dict, secret: str) -> str:
    return get_signer(secret).dumps(data)

def verify(token: str, secret: str, max_age: int) -> Optional[dict]:
    try:
        return get_signer(secret).loads(token, max_age=max_age)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
