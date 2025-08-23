import time, hmac, hashlib
from typing import Optional
from fastapi import HTTPException
from .nonce_cache import NonceCache

class WebhookGuard:
    def __init__(self, secret: str, tolerance: int = 300, cache: Optional[NonceCache] = None):
        self.secret = secret.encode()
        self.tolerance = tolerance
        self.cache = cache or NonceCache()

    def verify(self, ts: int, body: bytes, signature_hex: str, nonce: Optional[str] = None):
        now = int(time.time())
        if abs(now - ts) > self.tolerance:
            raise HTTPException(status_code=400, detail="timestamp_skew")
        mac = hmac.new(self.secret, f"{ts}.".encode()+body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(mac, signature_hex):
            raise HTTPException(status_code=401, detail="bad_signature")
        if nonce:
            if self.cache.seen(nonce):
                raise HTTPException(status_code=409, detail="replay")
            self.cache.mark(nonce)

class Dummy:
    pass
