from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from app.dependencies import require_org

router = APIRouter(prefix="/customers", tags=["customers"])

DATA = Path(__file__).resolve().parent.parent / "data" / "demo_customers.json"

def _load() -> List[Dict[str, Any]]:
    if DATA.exists():
        try:
            return json.loads(DATA.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

@router.get("")
async def list_customers(q: Optional[str] = None, org: str = Depends(require_org())):
    rows = _load()
    # demo data may not have org; if present, filter
    if rows and isinstance(rows[0], dict) and "org" in rows[0]:
        rows = [r for r in rows if r.get("org") == org]
    if q:
        ql = q.lower()
        rows = [r for r in rows if ql in (r.get("name","")+r.get("email","")).lower()]
    return {"items": rows, "count": len(rows)}
