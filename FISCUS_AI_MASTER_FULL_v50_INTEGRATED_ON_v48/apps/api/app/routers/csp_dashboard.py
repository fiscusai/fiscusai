from fastapi import APIRouter, Query
from pathlib import Path
import json

router = APIRouter(prefix="/csp", tags=["csp"])
LOG = Path(__file__).resolve().parents[2] / "data" / "csp_reports.jsonl"

@router.get("/reports")
def reports(limit: int = Query(100, ge=1, le=500)):
    if not LOG.exists():
        return []
    lines = LOG.read_text(encoding="utf-8").splitlines()[-limit:]
    return [json.loads(x) for x in lines if x.strip()]

@router.get("/stats")
def stats():
    if not LOG.exists():
        return {"by_directive": {}, "total": 0}
    from collections import Counter
    c = Counter()
    total = 0
    for line in LOG.read_text(encoding="utf-8").splitlines():
        try:
            obj = json.loads(line)
            d = obj.get("csp-report", {}).get("violated-directive", "unknown")
            c[d] += 1
            total += 1
        except Exception:
            continue
    return {"by_directive": dict(c.most_common()), "total": total}
