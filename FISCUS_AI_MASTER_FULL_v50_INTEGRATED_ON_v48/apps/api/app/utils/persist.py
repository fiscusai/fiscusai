from pathlib import Path
import json, datetime

DATA = Path(__file__).resolve().parents[1] / "data"
RULES = DATA / "reconcile_rules.json"
AUDIT = DATA / "audit.log"

def load_rules():
    if RULES.exists():
        return json.loads(RULES.read_text(encoding="utf-8"))
    return {"desc_rules": [], "tolerance_days": 0}

def save_rules(desc_rules, tolerance_days):
    payload = {
        "desc_rules": desc_rules,
        "tolerance_days": tolerance_days,
        "updated_at": datetime.datetime.utcnow().isoformat()+"Z"
    }
    RULES.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    audit("rules.update", {"desc_rules": desc_rules, "tolerance_days": tolerance_days})
    return payload

def audit(event, data):
    line = json.dumps({
        "ts": datetime.datetime.utcnow().isoformat()+"Z",
        "event": event,
        "data": data
    })
    with AUDIT.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
