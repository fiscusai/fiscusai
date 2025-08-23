import os, hmac, hashlib, json
from typing import Any, Dict

def sign_payload(payload: Dict[str, Any]) -> str:
    secret = os.getenv("WEBHOOK_SECRET", "")
    body = json.dumps(payload, separators=(',',':'), ensure_ascii=False).encode('utf-8')
    if not secret:
        return ""
    sig = hmac.new(secret.encode('utf-8'), body, hashlib.sha256).hexdigest()
    return sig