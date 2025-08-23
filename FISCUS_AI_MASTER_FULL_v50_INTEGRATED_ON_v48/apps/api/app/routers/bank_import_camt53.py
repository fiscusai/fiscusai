from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
import xml.etree.ElementTree as ET

router = APIRouter(prefix="/bank", tags=["bank"])

def parse_camt53(xml_text: str) -> List[Dict]:
    try:
        root = ET.fromstring(xml_text)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid XML: {e}")
    ns = {"ns":"urn:iso:std:iso:20022:tech:xsd:camt.053.001.02"}
    items = []
    for ntry in root.findall(".//ns:Ntry", ns):
        amt_el = ntry.find("./ns:Amt", ns)
        cdt_dbt = ntry.find("./ns:CdtDbtInd", ns)
        info = ntry.find(".//ns:AddtlNtryInf", ns)
        try:
            amt = float((amt_el.text or "0").replace(",", "."))
        except Exception:
            amt = 0.0
        sign = 1.0 if (cdt_dbt is not None and (cdt_dbt.text or "").strip().upper()=="CRDT") else -1.0
        items.append({
            "amount": sign * amt,
            "info": (info.text or "").strip() if info is not None else ""
        })
    return items

@router.post("/import/camt53")
async def import_camt53(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".xml", ".camt", ".camt53")):
        raise HTTPException(status_code=422, detail="Expecting .xml/.camt file")
    xml_text = (await file.read()).decode("utf-8", errors="ignore")
    items = parse_camt53(xml_text)
    return {"count": len(items), "items": items[:100]}
