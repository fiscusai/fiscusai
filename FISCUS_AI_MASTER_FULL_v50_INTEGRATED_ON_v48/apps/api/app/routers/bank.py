from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from pathlib import Path
import json, csv, io

router = APIRouter(prefix="/bank", tags=["bank"])

DATA = Path(__file__).resolve().parent.parent / "data" / "bank_transactions.json"
DATA.parent.mkdir(exist_ok=True, parents=True)

def _save(rows):
    DATA.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

@router.post("/import")
async def import_bank(file: UploadFile = File(...), x_token: str | None = Header(default=None)):
    # Simple token guard
    if not x_token or x_token != "dev-bank-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    content = await file.read()
    name = (file.filename or "").lower()
    rows = []
    try:
        if name.endswith(".json"):
            rows = json.loads(content.decode("utf-8"))
        elif name.endswith(".csv"):
            text = content.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            rows = list(reader)
        else:
            raise HTTPException(status_code=400, detail="Only CSV or JSON accepted")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parse error: {e}")

    # Normalize and simple summary
    norm = []
    total_in, total_out = 0.0, 0.0
    for r in rows:
        amount = float(r.get("amount") or r.get("tutar") or 0)
        kind = r.get("type") or r.get("tur") or ("in" if amount >= 0 else "out")
        desc = r.get("desc") or r.get("açıklama") or r.get("aciklama") or ""
        date = r.get("date") or r.get("tarih") or ""
        norm.append({"date": date, "type": kind, "amount": amount, "desc": desc})
        if amount >= 0: total_in += amount
        else: total_out += -amount
    _save(norm)
    return {"ok": True, "count": len(norm), "total_in": total_in, "total_out": total_out}
