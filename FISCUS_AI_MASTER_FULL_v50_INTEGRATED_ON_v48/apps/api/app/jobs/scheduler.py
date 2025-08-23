from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pathlib import Path
import json, datetime

DATA = Path(__file__).resolve().parents[1] / "data"
DATA.mkdir(parents=True, exist_ok=True)
HISTORY = DATA / "jobs_history.jsonl"
SCHEDULE = DATA / "jobs_schedule.json"

_sched = None

def _log(event, payload):
    line = json.dumps({"ts": datetime.datetime.utcnow().isoformat()+"Z", "event": event, "data": payload})
    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_scheduler():
    global _sched
    if _sched is None:
        _sched = BackgroundScheduler(timezone="UTC")
        _sched.start(paused=False)
        # restore persisted schedules
        if SCHEDULE.exists():
            try:
                cfg = json.loads(SCHEDULE.read_text(encoding="utf-8"))
                for job in cfg.get("cron", []):
                    add_cron(job["id"], job["cron"])
            except Exception:
                pass
    return _sched

def add_cron(job_id: str, cron: str):
    # cron format: "0 9 * * *" (min hour dom mon dow)
    sch = get_scheduler()
    # Remove existing
    if sch.get_job(job_id):
        sch.remove_job(job_id)
    minute, hour, day, month, dow = cron.split()
    trig = CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=dow)
    sch.add_job(lambda: _log("job.run", {"id": job_id}), trigger=trig, id=job_id, replace_existing=True)
    # persist
    data = {"cron": []}
    if SCHEDULE.exists():
        try: data = json.loads(SCHEDULE.read_text(encoding="utf-8"))
        except Exception: pass
    # update list
    data["cron"] = [j for j in data.get("cron", []) if j.get("id") != job_id] + [{"id": job_id, "cron": cron}]
    SCHEDULE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"ok": True, "id": job_id, "cron": cron}

def list_cron():
    if SCHEDULE.exists():
        try: return json.loads(SCHEDULE.read_text(encoding="utf-8")).get("cron", [])
        except Exception: return []
    return []

def history_tail(n: int = 100):
    if not HISTORY.exists():
        return []
    with HISTORY.open("r", encoding="utf-8") as f:
        lines = f.readlines()[-n:]
    return [json.loads(x) for x in lines if x.strip()]
