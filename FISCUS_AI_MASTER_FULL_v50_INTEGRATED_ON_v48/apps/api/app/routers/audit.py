from fastapi import APIRouter, Query
from typing import List, Optional
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/audit", tags=["audit"])

AUDIT = Path(__file__).resolve().parents[1] / "data" / "audit.log"

def _parse_line(line: str):
    try:
        return json.loads(line)
    except Exception:
        return None

@router.get("")
def list_audit(
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    event: Optional[str] = Query(None, description="Comma-separated event names"),
    page: int = 1,
    page_size: int = 100
):
    items = []
    if AUDIT.exists():
        for line in AUDIT.read_text(encoding="utf-8").splitlines():
            obj = _parse_line(line)
            if not obj: continue
            ts = obj.get("ts")
            ev = obj.get("event")
            ok = True
            if from_date:
                ok = ok and ts >= f"{from_date}T00:00:00"
            if to_date:
                ok = ok and ts <= f"{to_date}T23:59:59"
            if event:
                allowed = [e.strip() for e in event.split(",") if e.strip()]
                ok = ok and ev in allowed
            if ok:
                items.append(obj)
    total = len(items)
    start = max((page-1)*page_size, 0)
    end = start + page_size
    return {"items": items[start:end], "total": total, "page": page, "page_size": page_size}
