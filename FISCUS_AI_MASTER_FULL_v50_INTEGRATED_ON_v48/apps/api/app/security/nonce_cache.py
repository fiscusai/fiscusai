import time
from typing import Dict

class NonceCache:
    def __init__(self, ttl: int = 600):
        self.ttl = ttl
        self.store: Dict[str, float] = {}

    def seen(self, nonce: str) -> bool:
        now = time.time()
        # cleanup
        for k, v in list(self.store.items()):
            if v < now:
                del self.store[k]
        return nonce in self.store

    def mark(self, nonce: str):
        self.store[nonce] = time.time() + self.ttl
