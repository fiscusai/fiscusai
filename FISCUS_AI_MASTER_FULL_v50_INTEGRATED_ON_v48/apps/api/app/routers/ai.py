from fastapi import APIRouter
from pathlib import Path
import json
from statistics import mean, pstdev

router = APIRouter(prefix="/ai", tags=["ai"])

BASE = Path(__file__).resolve().parent.parent / "data"
INV = BASE / "demo_invoices.json"
EXP = BASE / "demo_expenses.json"

def _read(p):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return []

@router.get("/insights")
def insights():
    invoices = _read(INV)
    expenses = _read(EXP)
    revenue_values = [i.get("total", 0) for i in invoices if i.get("total") is not None]
    anomalies = []
    forecast = None

    if revenue_values:
        mu = mean(revenue_values)
        sd = pstdev(revenue_values) if len(revenue_values) > 1 else 0
        # flag > 2 sd
        for idx, val in enumerate(revenue_values):
            if sd and abs(val - mu) > 2 * sd:
                anomalies.append({"index": idx, "value": val, "reason": "outlier"})
        # naive forecast: last 3 avg
        tail = revenue_values[-3:] if len(revenue_values) >= 3 else revenue_values
        forecast = sum(tail) / len(tail)

    summary = {
        "revenue_mean": mu if revenue_values else 0,
        "revenue_std": sd if revenue_values and len(revenue_values) > 1 else 0,
        "expenses_total": sum(e.get("amount", 0) for e in expenses),
        "anomalies": anomalies,
        "forecast_next": forecast
    }
    suggestions = []
    if forecast is not None:
        suggestions.append(f"Gelecek dönem için kaba gelir tahmini: {round(forecast,2)}")
    if anomalies:
        suggestions.append("Gelirde olağan dışı sıçramalar var; ilgili faturaları gözden geçirin.")
    if summary["expenses_total"] > 0.6 * (summary['revenue_mean'] or 1):
        suggestions.append("Giderler yüksek; bulut hizmetleri ve pazarlama kalemlerini optimize edin.")
    return {"summary": summary, "suggestions": suggestions}
