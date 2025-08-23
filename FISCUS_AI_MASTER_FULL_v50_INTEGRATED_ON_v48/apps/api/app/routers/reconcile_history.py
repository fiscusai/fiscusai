
from fastapi import APIRouter, Response, Query
from typing import List, Dict, Any
from pathlib import Path
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

router = APIRouter(prefix="/reconcile/history", tags=["reconcile"])

AUDIT = Path(__file__).resolve().parents[1] / "data" / "reconcile_matches.jsonl"
AUDIT.parent.mkdir(parents=True, exist_ok=True)

def load() -> List[Dict[str,Any]]:
    if not AUDIT.exists(): return []
    out = []
    for l in AUDIT.read_text(encoding='utf-8').splitlines():
        try: out.append(json.loads(l))
        except: pass
    return out

@router.get("/")
def list_history(page: int = 1, page_size: int = 50):
    items = list(reversed(load()))
    total = len(items)
    s = max(0,(page-1)*page_size); e = s+page_size
    return {"items": items[s:e], "total": total, "page": page, "page_size": page_size}

@router.get("/export.csv")
def export_csv():
    items = load()
    headers = ["ts","org","tx_id","invoice_id","type","amount","invoice_amount","diff_amount"]
    lines = [",".join(headers)]
    for it in items:
        row = [str(it.get(h,"")) for h in headers]
        lines.append(",".join([json.dumps(x, ensure_ascii=False) for x in row]))
    return Response(content="\n".join(lines), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=reconcile_history.csv"})

@router.get("/export.pdf")
def export_pdf():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w,h = A4; y = h-40
    c.setFont("Helvetica-Bold", 12); c.drawString(40, y, "Reconcile History"); y -= 20
    c.setFont("Helvetica", 9)
    for it in load()[:800]:
        line = f"{it.get('ts','')} | {it.get('org','')} | {it.get('tx_id','')} -> {it.get('invoice_id','')} | {it.get('type','')} | {it.get('amount','')}"
        c.drawString(40, y, line[:120]); y -= 14
        if y < 40: c.showPage(); y = h-40; c.setFont("Helvetica", 9)
    c.showPage(); c.save()
    return Response(content=buf.getvalue(), media_type="application/pdf", headers={"Content-Disposition":"inline; filename=reconcile_history.pdf"})
