
from fastapi.responses import JSONResponse
from .listing import make_etag

def json_with_etag(payload, request):
    res = JSONResponse(payload)
    res.headers["X-ETag"] = make_etag(payload)
    return res
