from fastapi import APIRouter, Request
from pathlib import Path
import json, datetime

router = APIRouter(tags=["security"])

LOG = Path(__file__).resolve().parents[1] / "data" / "csp_reports.jsonl"
LOG.parent.mkdir(parents=True, exist_ok=True)

@router.post("/csp-report")
async def csp_report(req: Request):
    try:
        body = await req.json()
    except Exception:
        body = {"_raw": await req.body()}
    line = {"ts": datetime.datetime.utcnow().isoformat()+"Z", "report": body}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")
    return {"ok": True}
