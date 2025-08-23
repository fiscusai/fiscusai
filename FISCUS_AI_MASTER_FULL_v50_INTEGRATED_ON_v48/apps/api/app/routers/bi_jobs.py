from fastapi import APIRouter, Query
from app.jobs.bi_zip_report import run_bi_export_and_email

router = APIRouter(prefix="/bi", tags=["bi"])

@router.post("/export/email")
def bi_export_email(to: str = Query(...), from_date: str = Query(...), to_date: str = Query(...)):
    res = run_bi_export_and_email(to, from_date, to_date)
    return res
