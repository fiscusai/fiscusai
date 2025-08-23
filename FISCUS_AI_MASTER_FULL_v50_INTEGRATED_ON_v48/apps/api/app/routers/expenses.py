from fastapi import APIRouter, Depends
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from app.dependencies import require_org

router = APIRouter(prefix="/expenses", tags=["expenses"])

DATA = Path(__file__).resolve().parent.parent / "data" / "demo_expenses.json"

def _load() -> List[Dict[str, Any]]:
    if DATA.exists():
        try:
            return json.loads(DATA.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

@router.get("")
async def list_expenses(category: Optional[str] = None, org: str = Depends(require_org())):
    rows = _load()
    if rows and isinstance(rows[0], dict) and "org" in rows[0]:
        rows = [r for r in rows if r.get("org") == org]
    if category:
        rows = [r for r in rows if r.get("category") == category]
    total = sum(float(r.get("amount", 0)) for r in rows)
    return {"items": rows, "count": len(rows), "total": total}
