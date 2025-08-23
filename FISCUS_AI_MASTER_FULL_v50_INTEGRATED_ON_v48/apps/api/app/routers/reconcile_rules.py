from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.utils.persist import load_rules, save_rules, audit

router = APIRouter(prefix="/reconcile", tags=["reconcile"])

@router.get("/rules")
def get_rules():
    return load_rules()

@router.post("/rules")
def set_rules(desc_rules: List[str], tolerance_days: int):
    if tolerance_days < 0 or tolerance_days > 60:
        raise HTTPException(status_code=422, detail="tolerance_days must be between 0-60")
    return save_rules(desc_rules, tolerance_days)

@router.get("/rules/preview")
def preview_rules(desc_rule: Optional[List[str]] = None, tolerance: int = 5):
    # This is a mock preview that just returns the rules & tolerance and mock match stats.
    rules = desc_rule or load_rules().get("desc_rules", [])
    return {
        "rules": rules,
        "tolerance_days": tolerance,
        "matched": 42,
        "unmatched": 7
    }

@router.post("/rules/apply")
def apply_rules(desc_rule: Optional[List[str]] = None, tolerance: int = 5):
    rules = desc_rule or load_rules().get("desc_rules", [])
    audit("reconcile.apply", {"rules": rules, "tolerance": tolerance})
    return {"ok": True, "applied": len(rules), "tolerance_days": tolerance}
