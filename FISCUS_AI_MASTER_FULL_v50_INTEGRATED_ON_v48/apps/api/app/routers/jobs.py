from fastapi import APIRouter
from rq import Queue
import redis
from app.jobs.reports import generate_daily_report
import os

router = APIRouter(prefix="/jobs", tags=["jobs"])

def _q():
    r = redis.from_url(os.getenv("REDIS_URL","redis://localhost:6379/0"))
    return Queue('default', connection=r)

@router.post("/daily-report")
def enqueue_daily_report():
    job = _q().enqueue(generate_daily_report)
    return {"ok": True, "job_id": job.get_id()}
