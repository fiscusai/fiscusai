
from fastapi import APIRouter, UploadFile, File, Query, Depends
from typing import Any, Dict
import json
from app.security.deps import require_org, require_role
from app.services.reconcile_auto import auto_match

router = APIRouter(prefix="/bank/import", tags=["bank"])

@router.post("/mt940")
async def import_mt940(file: UploadFile = File(...), auto: bool = Query(False), org=Depends(require_org), role=Depends(require_role(["accountant","admin"]))):
    content = (await file.read()).decode("utf-8", errors="ignore")
    # demo parse
    txs = []
    for line in content.splitlines():
        if line.startswith(":61:"):
            amt = 0
            m = line.split("N")
            if len(m)>1:
                try: amt = float(re.sub(r"[^0-9.\-]","", m[-1]))
                except: amt = 0
            txs.append({"id": f"T{len(txs)+1}", "date": "2025-08-05", "amount": amt, "description": line})
    if auto:
        res = auto_match(txs, [], {"desc_rules":[], "tolerance_days":5, "amount_tolerance":1.0})
        return {"transactions": txs, "auto": res}
    return {"transactions": txs}
