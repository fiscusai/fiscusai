import time, os
from fastapi import APIRouter
start_time = time.time()

router = APIRouter(prefix="/status", tags=["status"])

@router.get("/uptime")
def uptime():
    return {"uptime_sec": int(time.time() - start_time)}

@router.get("/worker")
def worker_status():
    # Demo: check env flag set by worker or fallback
    return {"worker_alive": os.getenv("WORKER_HEARTBEAT","0") == "1"}
