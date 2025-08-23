from fastapi import APIRouter, Response
from pathlib import Path
from datetime import datetime
import json
try:
    import pandas as pd
except Exception:
    pd = None

router = APIRouter(prefix="/exports/bi", tags=["exports"])
DATA = Path(__file__).resolve().parents[1] / "data" / "demo_invoices.json"

def _read():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return []

@router.get("/invoices.parquet")
def invoices_parquet(from_date: str = None, to_date: str = None):
    rows = _read()
    if from_date:
        rows = [r for r in rows if r.get("date") and r["date"] >= from_date]
    if to_date:
        rows = [r for r in rows if r.get("date") and r["date"] <= to_date]
    if pd is None:
        return rows
    df = pd.DataFrame(rows)
    buf = bytes()
    try:
        import io
        bio = io.BytesIO()
        df.to_parquet(bio, index=False)
        buf = bio.getvalue()
        return Response(content=buf, media_type="application/octet-stream", headers={
            "Content-Disposition": "attachment; filename=invoices.parquet"
        })
    except Exception:
        return rows
