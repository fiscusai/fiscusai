from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import os, uuid

router = APIRouter(prefix="/files", tags=["files"])

from app.dependencies import require_role
from app.db import get_session
from sqlmodel import Session
from app.models.audit import AuditLog

try:
    import boto3  # type: ignore
except Exception:
    boto3 = None  # type: ignore

def _guess_prefix(filename: str) -> str:
    fn = (filename or "").lower()
    if fn.endswith(".pdf"):
        return "invoices/"
    if any(fn.endswith(x) for x in [".png",".jpg",".jpeg",".webp",".gif"]):
        return "images/"
    return "uploads/"

@router.post("/presign")
async def presign(filename: str, user=Depends(require_role(["admin","user"]))):
    bucket = os.getenv("S3_BUCKET", "uploads")
    key = f"{_guess_prefix(filename)}{uuid.uuid4()}_{filename}"
    if boto3 is None:
        # No boto3: return a dummy form (client-side dev mode)
        return {"bucket": bucket, "key": key, "fields": {}, "url": "http://localhost:9000/fake"}
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT", None),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            region_name=os.getenv("S3_REGION", "us-east-1"),
        )
        post = s3.generate_presigned_post(
            Bucket=bucket,
            Key=key,
            Fields={"acl": "private"},
            Conditions=[["starts-with", "$key", ""]],
            ExpiresIn=3600,
        )
        return {"bucket": bucket, "key": key, **post}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notify")
async def notify_upload(key: str, user=Depends(require_role(["admin","user"])), s: Session = Depends(get_session)):
    if not key:
        raise HTTPException(status_code=400, detail="key is required")
    # Log the upload event
    log = AuditLog(actor=user.get("email","user"), role=user.get("role","user"),
                   action="upload", target=key, meta="{}")
    s.add(log)
    s.commit()
    return {"ok": True, "key": key}
