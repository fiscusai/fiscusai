from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from sqlmodel import select
from app.dependencies import require_role
from app.db import get_session
from app.models.user import User

router = APIRouter(prefix='/admin/users', tags=['admin'])

@router.get('')
@require_role(['admin'])
def list_users():
    with get_session() as s:
        rows = s.exec(select(User).order_by(User.ts.desc())).all()
        return [dict(id=r.id, sub=r.sub, role=r.role, ts=r.ts.isoformat()) for r in rows]

@router.post('')
@require_role(['admin'])
def upsert_user(sub: str, role: str = 'uploader'):
    with get_session() as s:
        row = s.exec(select(User).where(User.sub == sub)).first()
        if row:
            row.role = role
        else:
            row = User(sub=sub, role=role)
            s.add(row)
        s.commit()
        return {'ok': True}

@router.delete('')
@require_role(['admin'])
def delete_user(sub: str):
    with get_session() as s:
        row = s.exec(select(User).where(User.sub == sub)).first()
        if not row:
            raise HTTPException(status_code=404, detail='not found')
        s.delete(row); s.commit()
        return {'ok': True}