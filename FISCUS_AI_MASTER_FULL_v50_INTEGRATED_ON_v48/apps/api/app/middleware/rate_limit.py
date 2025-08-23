from fastapi import Request, Response
from time import time

class RateLimitMiddleware:
    def __init__(self, app, per_minute: int = 60):
        self.app = app
        self.per_minute = per_minute
        self.bucket = {}

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send); return
        req = Request(scope, receive=receive)
        ip = req.client.host if req.client else 'unknown'
        now = int(time()); window = now // 60; key = f"{ip}:{window}"
        self.bucket[key] = self.bucket.get(key, 0) + 1
        if self.bucket[key] > self.per_minute:
            resp = Response("Too Many Requests", status_code=429)
            await resp(scope, receive, send); return
        await self.app(scope, receive, send)

from fastapi import Request
class AuditMiddleware:
    def __init__(self, app, sink):
        self.app = app; self.sink = sink
    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send); return
        req = Request(scope, receive=receive)
        await self.sink(req.method, req.url.path, (req.client.host if req.client else 'unknown'))
        await self.app(scope, receive, send)
