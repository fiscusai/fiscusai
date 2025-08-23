from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from datetime import datetime
import json
from pathlib import Path
from sqlmodel import Session, select
from app.db.session import get_engine
from app.db.models import Flag

router = APIRouter(prefix="/flags", tags=["flags"])

FALLBACK = Path(__file__).resolve().parents[1] / "data" / "flags.json"

def _now(): return datetime.utcnow().isoformat() + "Z"

def _load_fallback():
    if FALLBACK.exists():
        return json.loads(FALLBACK.read_text(encoding="utf-8"))
    return {"FF_AI_PANEL": True, "FF_BILLING": True, "FF_RECON_RULES": True}

@router.get("/")
def list_flags() -> Dict[str, bool]:
    try:
        eng = get_engine()
        with Session(eng) as s:
            rows = s.exec(select(Flag)).all()
            if rows:
                return {r.name: r.value for r in rows}
    except Exception:
        pass
    # fallback
    return _load_fallback()

@router.post("/")
def save_flags(payload: Dict[str, bool]):
    saved = False
    try:
        eng = get_engine()
        with Session(eng) as s:
            for k, v in payload.items():
                row = s.exec(select(Flag).where(Flag.name==k)).first()
                if row:
                    row.value = bool(v)
                    row.updated_at = _now()
                else:
                    row = Flag(name=k, value=bool(v), scope="global", updated_at=_now())
                    s.add(row)
            s.commit()
            saved = True
    except Exception:
        # fall back to file
        FALLBACK.parent.mkdir(parents=True, exist_ok=True)
        FALLBACK.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        saved = True
    if not saved:
        raise HTTPException(status_code=500, detail="Could not save flags")
    return {"ok": True, "flags": payload}
