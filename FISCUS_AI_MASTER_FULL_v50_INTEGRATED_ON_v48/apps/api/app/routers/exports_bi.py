
from fastapi import APIRouter, Response, Query
from pathlib import Path
import io, zipfile, json
from typing import Optional

router = APIRouter(prefix="/exports/bi", tags=["exports"])

DATA = Path(__file__).resolve().parents[1] / "data" / "demo_invoices.json"

def _filter(items, org_id=None, customer=None, start=None, end=None):
    out = []
    for it in items:
        if org_id and it.get("organization_id") != org_id: 
            continue
        if customer and (customer.lower() not in (it.get("customer","").lower())): 
            continue
        d = it.get("date")
        if start and d < start: 
            continue
        if end and d > end: 
            continue
        out.append(it)
    return out

@router.get("/invoices.zip")
def export_zip(
    org: Optional[str] = Query(None, alias="org"),
    customer: Optional[str] = Query(None),
    start: Optional[str] = Query(None, alias="from"),
    end: Optional[str] = Query(None, alias="to"),
):
    if DATA.exists():
        items = json.loads(DATA.read_text(encoding="utf-8"))
    else:
        items = []
    items = _filter(items, org, customer, start, end)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("invoices.json", json.dumps(items, indent=2, ensure_ascii=False))
        if items:
            headers = list(items[0].keys())
            csv_lines = [",".join(headers)]
            for it in items:
                csv_lines.append(",".join([json.dumps(it.get(h,'')) for h in headers]))
            z.writestr("invoices.csv", "\n".join(csv_lines))

    return Response(content=buf.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": "attachment; filename=invoices.zip"})
