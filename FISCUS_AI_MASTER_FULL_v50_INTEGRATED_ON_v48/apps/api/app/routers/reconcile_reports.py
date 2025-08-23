from fastapi import APIRouter, Response
import io, csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

router = APIRouter(prefix="/reconcile", tags=["reconcile"])

# Mock matched/unmatched lists
MATCHED = [
    {"match_id":"M-1","tx_id":"TX-101","invoice_no":"INV-1000","amount": 1250.0},
    {"match_id":"M-2","tx_id":"TX-102","invoice_no":"INV-1001","amount": 990.0},
]
UNMATCHED = [
    {"tx_id":"TX-201","desc":"Legera POS","amount": 425.25},
    {"tx_id":"TX-202","desc":"Aurea transfer","amount": 150.00},
]

@router.get("/matched")
def matched():
    return {"items": MATCHED, "total": len(MATCHED)}

@router.get("/unmatched")
def unmatched():
    return {"items": UNMATCHED, "total": len(UNMATCHED)}

@router.get("/matched.csv")
def matched_csv():
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["match_id","tx_id","invoice_no","amount"])
    w.writeheader()
    for r in MATCHED: w.writerow(r)
    return Response(content=buf.getvalue(), media_type="text/csv")

@router.get("/matched.pdf")
def matched_pdf():
    b = io.BytesIO()
    c = canvas.Canvas(b, pagesize=A4)
    w, h = A4
    y = h - 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Banka Mutabakat Raporu - Eşleşenler")
    y -= 30
    c.setFont("Helvetica", 10)
    for r in MATCHED:
        line = f"{r['match_id']}  {r['tx_id']}  {r['invoice_no']}  {r['amount']}"
        c.drawString(40, y, line)
        y -= 18
        if y < 60:
            c.showPage()
            y = h - 40
    c.showPage()
    c.save()
    return Response(content=b.getvalue(), media_type="application/pdf")
