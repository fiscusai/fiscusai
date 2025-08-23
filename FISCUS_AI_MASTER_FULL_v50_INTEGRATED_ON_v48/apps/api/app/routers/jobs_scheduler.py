from fastapi import APIRouter, HTTPException
import os, json, datetime

router = APIRouter(prefix="/jobs", tags=["jobs"])

SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "cron_jobs.json")

def _load():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"schedules": []}

def _save(obj):
    os.makedirs(os.path.dirname(SCHEDULE_FILE), exist_ok=True)
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

@router.get("/schedules")
def list_schedules():
    return _load()

@router.post("/schedule/bi-email-daily")
def schedule_bi_email_daily(to: str, hour: int = 8, minute: int = 0):
    if not to:
        raise HTTPException(status_code=422, detail="to is required")
    obj = _load()
    job = {
        "id": f"bi-email-{hour:02d}{minute:02d}-{to}",
        "type": "daily",
        "job": "bi_email",
        "to": to,
        "hour": hour,
        "minute": minute,
        "created_at": datetime.datetime.utcnow().isoformat()+"Z"
    }
    obj["schedules"] = [j for j in obj["schedules"] if j["id"] != job["id"]] + [job]
    _save(obj)
    return {"ok": True, "job": job}
