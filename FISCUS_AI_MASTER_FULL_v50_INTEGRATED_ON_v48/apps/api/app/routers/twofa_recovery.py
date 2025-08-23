from fastapi import APIRouter
from pathlib import Path
import json, secrets

router = APIRouter(prefix="/2fa", tags=["auth"])

STORE = Path(__file__).resolve().parents[1] / "data" / "twofa.json"

def _load():
    if STORE.exists():
        return json.loads(STORE.read_text(encoding="utf-8"))
    return {"enabled": False, "recovery_codes": []}

def _save(obj):
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(obj, indent=2), encoding="utf-8")

@router.post("/recovery/generate")
def generate_recovery_codes(n: int = 5):
    obj = _load()
    codes = [secrets.token_hex(4) for _ in range(n)]
    obj["recovery_codes"] = codes
    _save(obj)
    return {"ok": True, "codes": codes}

@router.post("/recovery/use")
def use_recovery(code: str):
    obj = _load()
    codes = obj.get("recovery_codes", [])
    if code in codes:
        codes.remove(code)
        obj["recovery_codes"] = codes
        obj["enabled"] = True
        _save(obj)
        return {"ok": True, "verified": True}
    return {"ok": False, "verified": False}
