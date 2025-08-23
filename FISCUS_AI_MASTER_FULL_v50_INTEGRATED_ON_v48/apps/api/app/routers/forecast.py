from fastapi import APIRouter
from pathlib import Path
import json
from datetime import datetime
import numpy as np

router = APIRouter(prefix="/ai", tags=["ai-forecast"])

INV = Path(__file__).resolve().parent.parent / "data" / "demo_invoices.json"
EXP = Path(__file__).resolve().parent.parent / "data" / "demo_expenses.json"

def _read(p):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return []

@router.get("/forecast")
def forecast(months: int = 3):
    invoices = _read(INV)
    # build monthly totals for last 12 months
    buckets = {}
    for i in invoices:
        d = i.get("date", "")
        try:
            k = datetime.fromisoformat(d).strftime("%Y-%m")
        except Exception:
            k = "unknown"
        buckets[k] = buckets.get(k, 0) + float(i.get("total", 0))
    months_sorted = sorted([k for k in buckets.keys() if k != "unknown"])
    y = np.array([buckets[m] for m in months_sorted], dtype=float)
    if len(y) < 2:
        # not enough data, return flat extrapolation
        baseline = float(y[-1]) if len(y) else 0.0
        return {"history": [{"month": m, "total": float(buckets[m])} for m in months_sorted],
                "forecast": [{"month": f"F+{i+1}", "total": baseline} for i in range(months)]}
    x = np.arange(len(y))
    # linear regression y = ax + b
    a, b = np.polyfit(x, y, 1)
    fc = []
    for i in range(1, months+1):
        xi = len(y) + i - 1
        yi = a * xi + b
        fc.append({"month": f"F+{i}", "total": float(max(0.0, yi))})
    return {
        "history": [{"month": m, "total": float(buckets[m])} for m in months_sorted],
        "forecast": fc
    }
