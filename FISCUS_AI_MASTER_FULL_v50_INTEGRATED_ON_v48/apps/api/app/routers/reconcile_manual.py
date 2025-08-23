from fastapi import APIRouter, HTTPException
from typing import Dict
from pathlib import Path
import json, uuid

router = APIRouter(prefix="/reconcile", tags=["reconcile"])
DATA = Path(__file__).resolve().parents[1] / "data" / "reconcile_matches.json"

def _load():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return {}

def _save(data):
    DATA.write_text(json.dumps(data, indent=2), encoding="utf-8")

@router.post("/manual")
def manual_match(payload: dict):
    data = _load()
    mid = str(uuid.uuid4())
    data[mid] = payload
    _save(data)
    return {"ok": True, "match_id": mid, "payload": payload}

@router.put("/manual/{match_id}")
def update_match(match_id: str, payload: dict):
    data = _load()
    if match_id not in data:
        raise HTTPException(status_code=404, detail="match not found")
    data[match_id].update(payload)
    _save(data)
    return {"ok": True, "match_id": match_id}

@router.delete("/manual/{match_id}")
def delete_match(match_id: str):
    data = _load()
    if match_id not in data:
        raise HTTPException(status_code=404, detail="match not found")
    data.pop(match_id)
    _save(data)
    return {"ok": True}
