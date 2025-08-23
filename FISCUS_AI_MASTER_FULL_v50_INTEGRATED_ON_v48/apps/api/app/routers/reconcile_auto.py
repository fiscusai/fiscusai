
from fastapi import APIRouter, Depends, Body, Request
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path

from app.security.deps import require_org, require_role
from app.services.reconcile_auto import auto_match

router = APIRouter(prefix="/reconcile/auto", tags=["reconcile"])

AUDIT = Path(__file__).resolve().parents[1] / "data" / "reconcile_matches.jsonl"
AUDIT.parent.mkdir(parents=True, exist_ok=True)

@router.post("/run")
def run_auto(payload: Dict[str, Any] = Body(...), org=Depends(require_org), role=Depends(require_role(["accountant","admin"]))):
    res = auto_match(payload.get("transactions",[]), payload.get("invoices",[]), payload.get("rules",{}))
    return res

@router.post("/apply")
def apply_matches(payload: Dict[str, Any] = Body(...), org=Depends(require_org), role=Depends(require_role(["accountant","admin"]))):
    matches = payload.get("matches", [])
    ts = datetime.utcnow().isoformat()
    lines = []
    for m in matches:
        m = dict(m)
        m.setdefault("org", org)
        m["ts"] = ts
        lines.append(json.dumps(m, ensure_ascii=False))
    if lines:
        with AUDIT.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    return {"ok": True, "saved": len(lines)}

@router.delete("/revert")
def revert(payload: Dict[str, Any] = Body(...), org=Depends(require_org), role=Depends(require_role(["accountant","admin"]))):
    tx_ids = set(payload.get("tx_ids", []))
    if not AUDIT.exists():
        return {"ok": True, "removed": 0}
    rows = [json.loads(l) for l in AUDIT.read_text(encoding="utf-8").splitlines() if l.strip()]
    keep = [r for r in rows if r.get("tx_id") not in tx_ids]
    AUDIT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in keep) + ("\n" if keep else ""), encoding="utf-8")
    return {"ok": True, "removed": len(rows)-len(keep)}
