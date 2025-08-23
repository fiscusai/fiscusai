from fastapi import APIRouter
import os, json

router = APIRouter(prefix="/status", tags=["status"])

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
QUEUE_FILE = os.path.join(DATA_DIR, "queue_depth.json")
HISTORY_FILE = os.path.join(DATA_DIR, "jobs_history.jsonl")

@router.get("/queue-depth")
def queue_depth():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"queues": {"default": 0}}

@router.get("/last-jobs")
def last_jobs(n: int = 20):
    out = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines()[-n:]:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return {"items": out}
