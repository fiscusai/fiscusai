from app.dependencies import require_org

from fastapi import APIRouter, Depends, Query, Request, Response
from typing import List, Dict, Any, Optional
from app.security.deps import require_org, require_role
from app.utils.listing import apply_query_sort, paginate, set_cache_headers
from datetime import datetime, timezone

router = APIRouter(prefix="/v2/customers", tags=["v2-customers"])

_DATA: List[Dict[str, Any]] = [
    {"id":"C-100","organization_id":"ORG-ALPHA","name":"Aurea Ltd","email":"aurea@example.com","tax_id":"1111111111","updated_at":"2025-08-08T11:00:00Z"},
    {"id":"C-101","organization_id":"ORG-BETA","name":"Legera AŞ","email":"legera@example.com","tax_id":"2222222222","updated_at":"2025-08-07T12:00:00Z"},
]

def _last_updated(items: List[Dict[str, Any]], org=Depends(require_org())):
    ts = None
    for it in items:
        v = it.get("updated_at")
        try:
            dt = datetime.fromisoformat(v.replace("Z","+00:00"))
            if ts is None or dt > ts:
                ts = dt
        except Exception:
            continue
    return ts or datetime.now(timezone.utc)

@router.get("/")
def list_customers(
    request: Request,
    response: Response,
    org=Depends(require_org),
    role=Depends(require_role(["user","accountant","admin"])),
    q: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    page: int = Query(1),
    page_size: int = Query(20),
):
    items = [it for it in _DATA if it.get("organization_id") == org]
    items = apply_query_sort(items, q, sort)
    page_items, total = paginate(items, page, page_size)
    payload = {"items": page_items, "total": total, "page": page, "page_size": page_size}
    if set_cache_headers(request, response, payload, _last_updated(items)):
        return Response(status_code=304)
    return payload
