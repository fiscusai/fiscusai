from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.s3_client import upload_bytes
import os

router = APIRouter(prefix="/s3", tags=["uploads-s3"])

@router.post("/upload")
async def s3_upload(file: UploadFile = File(...)):
    bucket = os.getenv("S3_BUCKET","fiscus-dev")
    content = await file.read()
    key = f"uploads/{file.filename}"
    try:
        info = upload_bytes(bucket, key, content, file.content_type or "application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True, **info}
