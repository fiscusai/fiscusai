from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST  # type: ignore
from starlette.requests import Request
from starlette.responses import Response
import time

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Latency", ["method", "path"])

async def metrics(_req: Request) -> Response:
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

class PrometheusMiddleware:
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        method = scope.get("method", "GET")
        path = scope.get("path", "/")
        start = time.time()

        status_holder = {"code": "0"}
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_holder["code"] = str(message["status"])
            await send(message)

        await self.app(scope, receive, send_wrapper)
        dur = time.time() - start
        REQUEST_LATENCY.labels(method, path).observe(dur)
        REQUEST_COUNT.labels(method, path, status_holder["code"]).inc()
AUDIT_EVENTS = Counter('audit_events_total', 'Audit events', ['action'])
