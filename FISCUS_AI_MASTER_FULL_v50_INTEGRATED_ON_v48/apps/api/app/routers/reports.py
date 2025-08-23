from fastapi import APIRouter, Depends
from pathlib import Path
from typing import List, Dict, Any
import json
from datetime import datetime

from app.dependencies import require_org

router = APIRouter(prefix="/reports", tags=["reports"])

BASE = Path(__file__).resolve().parent.parent / "data"
INV = BASE / "demo_invoices.json"
EXP = BASE / "demo_expenses.json"

def _read(p: Path) -> List[Dict[str, Any]]:
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

@router.get("/revenue-trend")
async def revenue_trend(org: str = Depends(require_org())):
    invoices = _read(INV)
    if invoices and "org" in invoices[0]:
        invoices = [i for i in invoices if i.get("org") == org]
    buckets = {}
    for i in invoices:
        d = i.get("date", "")
        try:
            month = datetime.fromisoformat(d).strftime("%Y-%m")
        except Exception:
            month = "unknown"
        buckets[month] = buckets.get(month, 0) + float(i.get("total", 0))
    data = [{"month": k, "total": v} for k, v in sorted(buckets.items())]
    return {"data": data}
