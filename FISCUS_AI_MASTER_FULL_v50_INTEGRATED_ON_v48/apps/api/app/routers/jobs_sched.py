from fastapi import APIRouter, HTTPException
from typing import List
from app.jobs.scheduler import add_cron, list_cron, history_tail, get_scheduler

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/scheduled")
def get_scheduled():
    return {"cron": list_cron()}

@router.post("/schedule/cron")
def schedule_cron(id: str, cron: str):
    # e.g. cron = "0 9 * * *"
    return add_cron(id, cron)

@router.get("/history")
def get_history(n: int = 100):
    return {"history": history_tail(n)}
