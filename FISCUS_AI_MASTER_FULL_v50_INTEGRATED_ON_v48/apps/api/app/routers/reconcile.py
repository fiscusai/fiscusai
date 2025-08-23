from fastapi import APIRouter, HTTPException, Header
from pathlib import Path
import json
from datetime import datetime, timedelta

router = APIRouter(prefix="/reconcile", tags=["reconcile"])

BASE = Path(__file__).resolve().parent.parent / "data"
INV = BASE / "demo_invoices.json"
BANK = BASE / "bank_import.json"

def _read(p):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return []

def parse_date(s, default=None):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return default

@router.get("/preview")
def preview(tolerance_days: int = 5):
    invoices = _read(INV)
    txs = _read(BANK)
    # Heuristic matching: same amount within date tolerance
    matches = []
    unmatched_invoices = []
    matched_invoice_ids = set()
    for inv in invoices:
        inv_date = parse_date(inv.get("date",""))
        inv_total = inv.get("total", 0.0)
        found = None
        for tx in txs:
            if tx.get("matched"):  # skip already marked matched
                continue
            if abs(tx.get("amount", 0.0) - inv_total) < 0.01:
                tx_date = parse_date(tx.get("date",""))
                if inv_date and tx_date and abs((tx_date - inv_date).days) <= tolerance_days:
                    found = tx
                    break
        if found:
            matches.append({"invoice_id": inv.get("id"), "invoice_total": inv_total, "tx_id": found.get("id"), "tx_date": found.get("date")})
            matched_invoice_ids.add(inv.get("id"))
            found["matched"] = True
        else:
            if not inv.get("paid", False):
                unmatched_invoices.append({"invoice_id": inv.get("id"), "invoice_total": inv_total})
    return {"matches": matches, "unmatched_invoices": unmatched_invoices, "total_txs": len(txs)}

@router.post("/apply")
def apply(tolerance_days: int = 5, x_token: str | None = Header(default=None)):
    if x_token != (Path(__file__).resolve().parent.parent / "data" / ".bank_token").read_text(encoding="utf-8").strip() if (Path(__file__).resolve().parent.parent / "data" / ".bank_token").exists() else "dev-bank-token":
        raise HTTPException(403, detail="invalid token")
    # mark matched invoices as paid
    base = Path(__file__).resolve().parent.parent / "data"
    inv_path = base / "demo_invoices.json"
    invoices = _read(inv_path)
    res = preview(tolerance_days=tolerance_days)
    matched_ids = {m["invoice_id"] for m in res["matches"]}
    changed = 0
    for inv in invoices:
        if inv.get("id") in matched_ids:
            inv["paid"] = True
            changed += 1
    inv_path.write_text(json.dumps(invoices, indent=2), encoding="utf-8")
    # write back bank file with matched flags
    bank_path = base / "bank_import.json"
    txs = _read(bank_path)
    bank_path.write_text(json.dumps(txs, indent=2), encoding="utf-8")
    return {"ok": True, "paid_updated": changed}
