try:
    import redis  # type: ignore
except Exception:
    redis = None
import os
import time
from fastapi import HTTPException, Request
from typing import Callable, Dict, Tuple

# naive in-memory token bucket: key -> (tokens, last_ts)
_BUCKETS: Dict[str, Tuple[float, float]] = {}

def rate_limited(rate: float, burst: int = 10):
    interval = 1.0 / rate if rate>0 else 0.0
    capacity = float(burst)

    def decorator(handler: Callable):
        async def wrapper(request: Request, *args, **kwargs):
            key = request.client.host + ":" + request.url.path
            now = time.time()
            tokens, last = _BUCKETS.get(key, (capacity, now))
            # refill
            if interval>0:
                tokens = min(capacity, tokens + (now - last) / interval)
            allowed = tokens >= 1.0
            if allowed:
                tokens -= 1.0
                _BUCKETS[key] = (tokens, now)
                return await handler(request, *args, **kwargs)
            raise HTTPException(status_code=429, detail="Too many requests")
        return wrapper
    return decorator


def _get_rds():
    if not os.getenv("REDIS_RL"):
        return None
    url = os.getenv("REDIS_URL","redis://localhost:6379/0")
    if redis is None:
        return None
    try:
        return redis.from_url(url)
    except Exception:
        return None
