from fastapi import APIRouter
from pathlib import Path
import json, statistics
from datetime import datetime
import math

router = APIRouter(prefix="/ai_adv", tags=["ai"])

BASE = Path(__file__).resolve().parent.parent / "data"
INV = BASE / "demo_invoices.json"
EXP = BASE / "demo_expenses.json"

def _read(p):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return []

@router.get("/anomalies")
def anomalies(z_threshold: float = 2.5):
    invoices = _read(INV)
    amts = [i.get("total",0.0) for i in invoices if isinstance(i.get("total",0.0), (int,float))]
    if len(amts) < 5:
        return {"anomalies": []}
    mean = statistics.mean(amts)
    stdev = statistics.pstdev(amts) or 1.0
    outliers = []
    seen_numbers = set()
    duplicates = []
    for i in invoices:
        val = i.get("total",0.0)
        z = (val - mean)/stdev
        if abs(z) >= z_threshold:
            outliers.append({"id": i.get("id"), "number": i.get("number"), "total": val, "z": z})
        # duplicate invoice numbers
        num = (i.get("number") or "").strip()
        if num in seen_numbers:
            duplicates.append({"id": i.get("id"), "number": num})
        else:
            seen_numbers.add(num)
    return {"outliers": outliers, "duplicates": duplicates, "mean": mean, "stdev": stdev}

@router.get("/cashflow_forecast")
def cashflow_forecast(months: int = 3):
    inv = _read(INV)
    exp = _read(EXP)
    # monthly buckets
    buckets = {}
    def monthkey(d):
        try:
            return datetime.fromisoformat(d).strftime("%Y-%m")
        except Exception:
            return "unknown"
    for i in inv:
        m = monthkey(i.get("date",""))
        buckets.setdefault(m, {"revenue":0.0, "cost":0.0})
        buckets[m]["revenue"] += i.get("total",0.0)
    for e in exp:
        m = monthkey(e.get("date",""))
        buckets.setdefault(m, {"revenue":0.0, "cost":0.0})
        buckets[m]["cost"] += e.get("amount",0.0)
    # order by month
    series = sorted([(k, v["revenue"]-v["cost"]) for k,v in buckets.items() if k!='unknown'])
    if not series:
        return {"history": [], "forecast": []}
    xs = list(range(len(series)))
    ys = [v for _, v in series]
    # simple linear regression y = a*x + b
    n = len(xs)
    sumx = sum(xs); sumy = sum(ys)
    sumxx = sum(x*x for x in xs); sumxy = sum(x*y for x,y in zip(xs,ys))
    denom = (n*sumxx - sumx*sumx) or 1.0
    a = (n*sumxy - sumx*sumy) / denom
    b = (sumy - a*sumx)/n
    hist = [{"month": m, "cashflow": v} for m, v in series]
    last_x = xs[-1] if xs else 0
    forecast = [{"month_index": last_x+i+1, "cashflow": a*(last_x+i+1)+b} for i in range(months)]
    return {"history": hist, "forecast": forecast, "model": {"a": a, "b": b}}
