from app.dependencies import require_org
from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.security.deps import require_org, require_role
from app.utils.listing import apply_query_sort, paginate, set_cache_headers

router = APIRouter(prefix="/v2/invoices", tags=["v2-invoices"])

# Demo data (in-memory). Production: DB tablosu.
_DATA: List[Dict[str, Any]] = [
    {"id":"INV-1000","organization_id":"ORG-ALPHA","number":"INV-00001","total":1000,"vat":180,"updated_at":"2025-08-08T10:00:00Z"},
    {"id":"INV-1001","organization_id":"ORG-BETA","number":"INV-00018","total":2200,"vat":396,"updated_at":"2025-08-07T09:00:00Z"},
]

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _filter_by_org(items: List[Dict[str,Any]], org: str) -> List[Dict[str,Any]]:
    return [it for it in items if it.get("organization_id") == org]

@router.get("")
def list_invoices(
    q: Optional[str] = None,
    sort: Optional[str] = Query("-updated_at"),
    page: int = 1,
    size: int = 20,
    org: str = Depends(require_org),
    user_role=Depends(require_role("admin","accountant","viewer")),
):
    items = _filter_by_org(_DATA, org)
    if q:
        ql = q.lower()
        items = [it for it in items if ql in (it.get("number","").lower())]
    items = apply_query_sort(items, sort or "-updated_at")
    page_data, meta = paginate(items, page=page, size=size)
    return {"data": page_data, "meta": meta}

@router.post("")
def create_invoice(body: Dict[str,Any], org: str = Depends(require_org), user_role=Depends(require_role("admin","accountant"))):
    item = {
        "id": body.get("id") or f"INV-{len(_DATA)+1000}",
        "organization_id": org,
        "number": body.get("number") or f"INV-{len(_DATA)+1:05d}",
        "total": float(body.get("total", 0)),
        "vat": float(body.get("vat", 0)),
        "updated_at": _now_iso(),
    }
    _DATA.append(item)
    return item

@router.put("/{iid}")
def update_invoice(iid: str, body: Dict[str,Any], org: str = Depends(require_org), user_role=Depends(require_role("admin","accountant"))):
    for it in _DATA:
        if it["id"] == iid and it.get("organization_id") == org:
            it.update({k:v for k,v in body.items() if k in ("number","total","vat")})
            it["updated_at"] = _now_iso()
            return it
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Invoice not found or not in your organization")

@router.delete("/{iid}")
def delete_invoice(iid: str, org: str = Depends(require_org), user_role=Depends(require_role("admin"))):
    global _DATA
    before = len(_DATA)
    _DATA = [it for it in _DATA if not (it["id"] == iid and it.get("organization_id") == org)]
    if len(_DATA) == before:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Invoice not found or not in your organization")
    return {"ok": True}
