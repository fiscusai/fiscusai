from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
import io

router = APIRouter(prefix="/bank", tags=["bank"])

def parse_mt940(text: str) -> List[Dict]:
    # Minimalistic MT940 line parser (demo): parse :61: and :86:
    records = []
    cur = None
    for line in text.splitlines():
        if line.startswith(":61:"):
            # :61:YYMMDDC/AmtNTRFRef
            cur = {"raw61": line[4:].strip(), "extra": ""}
            records.append(cur)
            # crude amount extract
            amt = None
            try:
                # find 'D' or 'C', then amount until 'N'
                rest = cur["raw61"]
                sign = -1 if "D" in rest[:1] else 1
                rest = rest[1:] if rest[:1] in "DC" else rest
                amt_str = rest.split("N",1)[0]
                amt_str = amt_str.replace(",", ".")
                amt = float(amt_str)
                cur["amount"] = sign * amt
            except Exception:
                cur["amount"] = 0.0
        elif line.startswith(":86:") and cur:
            cur["extra"] += line[4:].strip()
    return records

@router.post("/import/mt940")
async def import_mt940(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".sta", ".mt940", ".txt")):
        raise HTTPException(status_code=422, detail="Expecting .sta/.mt940/.txt file")
    content = (await file.read()).decode("utf-8", errors="ignore")
    items = parse_mt940(content)
    return {"count": len(items), "items": items[:100]}
