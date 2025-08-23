from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/status", tags=["status"])

@router.get("/version")
def version():
    p = Path(__file__).resolve().parents[3] / "VERSION"
    v = p.read_text(encoding="utf-8").strip() if p.exists() else "0.0.0"
    return {"version": v}
