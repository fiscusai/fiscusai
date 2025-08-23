from fastapi import APIRouter, Query
from app.services.s3_client import presign_post, presign_get

router = APIRouter(prefix="/s3", tags=["s3"])

@router.get("/presign-upload")
def presign_upload(filename: str = Query(...), content_type: str = Query("application/octet-stream")):
    key = filename
    return presign_post(key, content_type)

@router.get("/presign-get")
def presign_get_url(key: str, expires: int = 3600):
    url = presign_get(key, expires)
    return {"url": url}
