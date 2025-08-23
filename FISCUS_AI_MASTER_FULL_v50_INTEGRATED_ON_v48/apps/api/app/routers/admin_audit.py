from fastapi import APIRouter, Depends
from typing import Optional, List
from datetime import datetime
from sqlmodel import select
from sqlmodel import Session
from fastapi.responses import StreamingResponse
import csv
from io import StringIO

from app.dependencies import require_role
from app.db import get_session
from app.models.audit import AuditLog

router = APIRouter(prefix="/admin/audit", tags=["admin"])

@router.get("")
async def list_audit(
    q: Optional[str] = None,
    actor: Optional[str] = None,
    role: Optional[str] = None,
    action: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    limit: int = 200,
    s: Session = Depends(get_session),
    user=Depends(require_role(["admin"])),
):
    stmt = select(AuditLog)
    conds: List = []
    if q:
        # naive filter on action/target/meta
        like = f"%{q}%"
        from sqlmodel import or_
        conds.append(or_(AuditLog.action.like(like), AuditLog.target.like(like), AuditLog.meta.like(like)))
    if actor:
        conds.append(AuditLog.actor == actor)
    if role:
        conds.append(AuditLog.role == role)
    if action:
        conds.append(AuditLog.action == action)
    if since:
        conds.append(AuditLog.ts >= datetime.fromisoformat(since))
    if until:
        conds.append(AuditLog.ts <= datetime.fromisoformat(until))

    for c in conds:
        stmt = stmt.where(c)
    stmt = stmt.order_by(AuditLog.ts.desc()).limit(max(1, min(1000, limit)))
    rows = s.exec(stmt).all()
    return rows

@router.get("/export")
async def export_csv(
    q: Optional[str] = None,
    s: Session = Depends(get_session),
    user=Depends(require_role(["admin"])),
):
    # Reuse list filters for simplicity
    stmt = select(AuditLog).order_by(AuditLog.ts.desc()).limit(5000)
    rows = s.exec(stmt).all()

    def _gen():
        buf = StringIO()
        w = csv.writer(buf)
        w.writerow(["id","ts","actor","role","action","target","meta"])
        for r in rows:
            w.writerow([r.id, r.ts.isoformat(), r.actor, r.role, r.action, r.target, r.meta])
        buf.seek(0)
        yield buf.read()

    headers = {"Content-Disposition": 'attachment; filename="audit.csv"'}
    return StreamingResponse(_gen(), media_type="text/csv", headers=headers)
